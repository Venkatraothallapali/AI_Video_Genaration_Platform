import os

os.environ['USE_TF'] = '0'
os.environ['TRANSFORMERS_NO_TF'] = '1'

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
import faiss

# ------------------ CONFIG ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
VIDEO_DIR = os.path.join(BASE_DIR, "Videos_Data")
EXCEL_FILE = os.path.join(BASE_DIR, "Input_Vid_File.xlsx")
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3  # number of similar videos to return

# ------------------ INIT APP ------------------
app = FastAPI(title="Video Semantic Search")

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists(FRONTEND_DIR):
    raise FileNotFoundError(f"Frontend directory '{FRONTEND_DIR}' not found!")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# ------------------ LOAD MODEL ------------------
model = SentenceTransformer(MODEL_NAME)
EMBED_DIM = model.get_sentence_embedding_dimension()

# ------------------ LOAD EXCEL ------------------
if not os.path.exists(EXCEL_FILE):
    raise FileNotFoundError(f"Excel file '{EXCEL_FILE}' not found!")

df = pd.read_excel(EXCEL_FILE)
if not {"video_file", "Description"}.issubset(df.columns):
    raise ValueError("Excel must have 'video_file' and 'Description' columns.")

# Validate files
df["video_file"] = df["video_file"].astype(str).str.strip()
df["Description"] = df["Description"].astype(str).str.strip()
missing = [f for f in df["video_file"] if not os.path.exists(os.path.join(VIDEO_DIR, f))]
if missing:
    raise FileNotFoundError(f"Missing video files: {missing}")

# ------------------ PRECOMPUTE PROMPT EMBEDDINGS ------------------
prompt_texts = df["Description"].tolist()
prompt_embeddings = model.encode(prompt_texts, convert_to_numpy=True, show_progress_bar=True)
prompt_embeddings = prompt_embeddings / np.linalg.norm(prompt_embeddings, axis=1, keepdims=True)

# Create FAISS index (cosine sim via inner product)
index = faiss.IndexFlatIP(EMBED_DIM)
index.add(prompt_embeddings)

print(f"Loaded {len(prompt_texts)} video prompts into FAISS index")

# ------------------ SCHEMAS ------------------
class QueryRequest(BaseModel):
    query: str
    top_k: int = TOP_K


class VideoResult(BaseModel):
    filename: str
    Description: str
    score: float


class QueryResponse(BaseModel):
    results: list[VideoResult]


# ------------------ ROUTES ------------------
@app.get("/")
def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.post("/search", response_model=QueryResponse)
def search_videos(req: QueryRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    q_emb = model.encode([query], convert_to_numpy=True)
    q_emb = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)

    D, I = index.search(q_emb, req.top_k)
    scores = D[0].tolist()
    indices = I[0].tolist()

    results = []
    for idx, score in zip(indices, scores):
        if idx == -1:
            continue
        filename = df.iloc[idx]["video_file"]
        Description = df.iloc[idx]["Description"]
        results.append(VideoResult(filename=filename, Description=Description, score=float(score)))

    return QueryResponse(results=results)


@app.get("/videos/{filename}")
def get_video(filename: str):
    path = os.path.join(VIDEO_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(path, media_type="video/mp4")


# ------------------ RUN ------------------
# Run using: uvicorn app:app --reload --port 8000

