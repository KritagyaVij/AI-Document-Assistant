# 📄 AI Document Assistant (RAG Chatbot)

An AI-powered chatbot that answers questions from uploaded documents using
**Retrieval-Augmented Generation (RAG)** with semantic search.

---

## 🚀 Features

* Upload PDF / CSV documents
* Ask natural language questions
* Semantic search using FAISS
* Answers grounded strictly in document content
* Conversation memory using SQLite
* Confidence estimation for answers
* Export chat as PDF
* Dark mode UI

---

## 🧠 How It Works (RAG Pipeline)

1. Document uploaded → text extracted
2. Text split into overlapping chunks
3. Chunks converted into embeddings (MiniLM model)
4. Stored in FAISS vector database
5. User question → converted to embedding
6. FAISS retrieves most relevant chunks
7. Gemini generates answer using retrieved context only

This prevents hallucination and ensures document-based answers.

---

## 🏗 Architecture

Frontend (React)
⬇
FastAPI Backend
⬇
Embedding Model (SentenceTransformers)
⬇
FAISS Vector Search
⬇
Gemini LLM (Answer Generation)
⬇
SQLite (Conversation Memory)

---

## 🛠 Tech Stack

| Layer      | Technology                               |
| ---------- | ---------------------------------------- |
| Frontend   | React (Vite)                             |
| Backend    | FastAPI                                  |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB  | FAISS                                    |
| LLM        | Google Gemini API                        |
| Database   | SQLite                                   |
| Styling    | CSS                                      |

---

## ⚙️ How to Run Locally

### 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd AI-Document-Chatbot
```

### 2️⃣ Start Backend

```bash
cd Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### 3️⃣ Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## 📊 Example Use Cases

* Research paper analysis
* Business report Q&A
* Study material assistant
* Knowledge base chatbot

---

## 🎥 Demo

(Attach your demo video link here)

---

## 📌 Future Improvements

* Multi-document indexing
* Cloud deployment
* Source citation highlighting
* User authentication

---

## 👨‍💻 Author

Your Name
Internship Project – AI Document Chatbot
