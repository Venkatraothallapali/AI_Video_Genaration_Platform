# 🎥 AI Video Semantic Search Engine

An end-to-end AI-powered video search application that allows users to search videos using natural language queries.  
The system uses Sentence Transformers + FAISS for semantic similarity and returns the most relevant videos based on meaning, not keywords.

---

## 🚀 Features

- Search videos using natural language (semantic search)
- Powered by Sentence Transformers (MiniLM)
- Ultra-fast similarity search using FAISS
- Video streaming & download support
- Full-stack app with FastAPI backend + HTML/JS frontend
- Excel-based metadata ingestion
- Real-time embedding and query matching

---

## 🧠 How It Works

User enters a query →  
It is converted to an embedding →  
FAISS finds closest vectors →  
Top matching videos are returned.

---

## 🛠 Tech Stack

### Backend
- Python
- FastAPI
- Sentence-Transformers
- FAISS
- NumPy, Pandas

### Frontend
- HTML
- CSS
- JavaScript

### ML Model
- all-MiniLM-L6-v2

---

## 📁 Project Structure

AI_Video_APP/
├── backened/
│   ├── app.py  
│   ├── generate_embeddings.py  
│   ├── Input_Vid_File.xlsx  
│   ├── Videos_Data/  
│
├── frontend/
│   ├── index.html  
│   ├── script.js  
│   └── style.css  
│
├── requirements.txt  
└── README.md  

---

## 📊 Excel Format

Input_Vid_File.xlsx must contain:

| video_file | Description |
|------------|-------------|
| video1.mp4 | A man walking in a park |
| video2.mp4 | A car driving on highway |

---

## ⚙ Installation & Run

### 1. Create virtual environment
python -m venv env  
env\Scripts\activate  

### 2. Install packages
pip install -r requirements.txt  

### 3. Run backend
uvicorn app:app --reload --port 8000  

### 4. Open in browser
http://127.0.0.1:8000  

---

## 🔍 Example Queries

- a person walking in park  
- dog playing with ball  
- car driving on highway  

---

## 📌 API Endpoints

POST /search  
GET /videos/{filename}  

---

## 🧪 Generate Embeddings

python generate_embeddings.py  

---

## 🎯 Use Cases

- Video platforms  
- Media search engines  
- E-learning systems  
- Surveillance systems  

---

## 👨‍💻 Author

Venkatrao Thallapalli  
AI/ML Engineer  

GitHub: https://github.com/Venkatraothallapali  
LinkedIn: https://linkedin.com/in/venkatraothallapalli  

---

## 🧠 Interview One-Liner

I built an AI-powered semantic video search engine using Sentence Transformers and FAISS that retrieves videos based on meaning rather than keywords, served through a FastAPI backend with a full frontend interface.
