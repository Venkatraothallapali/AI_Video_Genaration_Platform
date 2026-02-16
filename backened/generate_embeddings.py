import os

os.environ['USE_TF'] = '0'
os.environ['TRANSFORMERS_NO_TF'] = '1'

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# ------------------ CONFIG ------------------
EXCEL_FILE = "Input_Vid_File.xlsx"
MODEL_NAME = "all-MiniLM-L6-v2"
EMBED_FILE = "prompt_embeddings.npy"

# ------------------ LOAD EXCEL ------------------
if not os.path.exists(EXCEL_FILE):
    raise FileNotFoundError(f"{EXCEL_FILE} not found!")

df = pd.read_excel(EXCEL_FILE)
if "Description" not in df.columns:
    raise ValueError("Excel must have a 'Description' column.")

# Clean description text
df["Description"] = df["Description"].astype(str).str.strip()

# ------------------ LOAD MODEL ------------------
model = SentenceTransformer(MODEL_NAME)
print("Generating embeddings for video descriptions...")

# ------------------ GENERATE EMBEDDINGS ------------------
embeddings = model.encode(df["Description"].tolist(), convert_to_numpy=True, show_progress_bar=True)

# Normalize for cosine similarity
embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

# ------------------ SAVE EMBEDDINGS ------------------
np.save(EMBED_FILE, embeddings)
print(f"Saved embeddings to {EMBED_FILE}")

