# 🎥 AI Video Semantic Search Engine

An end-to-end AI-powered video search application that allows users to search videos using natural language queries.  
The system uses Sentence Transformers + FAISS for semantic similarity and returns the most relevant videos based on meaning, not keywords.

---

##  Features

- Search videos using natural language (semantic search)
- Powered by Sentence Transformers (MiniLM)
- Ultra-fast similarity search using FAISS
- Video streaming & download support
- Full-stack app with FastAPI backend + HTML/JS frontend
- Excel-based metadata ingestion
- Real-time embedding and query matching

---

## How It Works

User enters a query →  
It is converted to an embedding →  
FAISS finds closest vectors →  
Top matching videos are returned.

---

## Tech Stack

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



##  Excel Format

Input_Vid_File.xlsx must contain:

| video_file | Description |
|------------|-------------|
| video1.mp4 | A man walking in a park |
| video2.mp4 | A car driving on highway |

---


##  Example Queries

- a person walking in park  
- dog playing with ball  
- car driving on highway  

---



##  Use Cases

- Video platforms  
- Media search engines  
- E-learning systems  
- Surveillance systems  

---

##  Author

Venkatrao Thallapalli  
AI/ML Engineer  

GitHub: https://github.com/Venkatraothallapali  
LinkedIn: https://linkedin.com/in/venkatraothallapalli  

---


