from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import faiss
import sqlite3
from sentence_transformers import SentenceTransformer
from file_service import extract_text_from_pdf, extract_text_from_csv
from gemini_service import get_gemini_response

app = FastAPI()

# -------------------------------
# Enable CORS (Frontend Access)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# LOAD EMBEDDING MODEL
# -------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

dimension = 384
index = faiss.IndexFlatL2(dimension)

document_chunks = []

# -------------------------------
# SQLITE MEMORY SETUP
# -------------------------------
conn = sqlite3.connect("chat_memory.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    session_id TEXT,
    user_message TEXT,
    ai_response TEXT
)
""")
conn.commit()

# -------------------------------
# TEXT CHUNKING (Day-5)
# -------------------------------
def chunk_text(text, chunk_size=850, overlap=150):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

# -------------------------------
# MEMORY FUNCTIONS (Day-10)
# -------------------------------
def save_chat(session_id, user_msg, ai_msg):
    cursor.execute(
        "INSERT INTO chat_history VALUES (?, ?, ?)",
        (session_id, user_msg, ai_msg)
    )
    conn.commit()

def get_last_messages(session_id, limit=2):
    cursor.execute("""
        SELECT user_message, ai_response
        FROM chat_history
        WHERE session_id=?
        ORDER BY ROWID DESC
        LIMIT ?
    """, (session_id, limit))
    return cursor.fetchall()[::-1]

# -------------------------------
# FOLLOW-UP DETECTION
# -------------------------------
def is_followup_instruction(message: str) -> bool:
    keywords = [
        "shorter", "summarize", "explain",
        "elaborate", "rephrase", "reduce",
        "expand", "clarify", "again", "make it"
    ]
    msg = message.lower()
    return any(word in msg for word in keywords)

# -------------------------------
# FILE UPLOAD ENDPOINT
# -------------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global document_chunks, index

    content = await file.read()

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    elif file.filename.endswith(".csv"):
        text = extract_text_from_csv(content)
    else:
        return {"error": "Unsupported file type"}

    document_chunks = chunk_text(text)

    embeddings = model.encode(document_chunks)
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))

    return {
        "message": "Document uploaded and indexed successfully",
        "total_chunks": len(document_chunks)
    }

# -------------------------------
# CHAT ENDPOINT (FINAL RAG)
# -------------------------------
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()

    user_message = data.get("message")
    session_id = data.get("session_id", "default")

    # -------- Input Validation --------
    if not user_message or user_message.strip() == "":
        return {"response": "Please enter a valid question."}

    if not document_chunks:
        return {"response": "No document indexed. Please upload a file first."}

    # -------- Follow-up Mode --------
    if is_followup_instruction(user_message):

        history = get_last_messages(session_id)

        context = "\n".join(
            [f"User: {h[0]}\nAssistant: {h[1]}" for h in history]
        )

        prompt = f"""
You are continuing an existing conversation.

Conversation so far:
{context}

User now says:
{user_message}

Respond appropriately using previous answer.
"""

        confidence = "Conversation-Based"

    # -------- Retrieval Mode (Semantic Search) --------
    else:
        query_embedding = model.encode([user_message]).astype("float32")

        distances, indices = index.search(query_embedding, k=5)

        retrieved_chunks = [document_chunks[i] for i in indices[0]]
        context = "\n\n".join(retrieved_chunks)

        avg_distance = float(np.mean(distances))

        if avg_distance < 0.5:
            confidence = "High"
        elif avg_distance < 1.2:
            confidence = "Medium"
        else:
            confidence = "Low"

        prompt = f"""
You are an AI assistant designed to answer questions ONLY from the provided document.

STRICT RULES:
- Use ONLY the given document context.
- Do NOT use outside knowledge.
- Do NOT guess.
- If the answer is not found, respond EXACTLY:
  "Not found in document."

Document Context:
{context}

User Question:
{user_message}
"""

    # -------- Call Gemini Safely --------
    try:
        response = get_gemini_response(prompt)
    except Exception as e:
        print("LLM Error:", e)
        return {"response": "Error generating response. Please try again."}

    save_chat(session_id, user_message, response)

    return {
        "response": response,
        "confidence": confidence
    }

# -------------------------------
# ROOT CHECK
# -------------------------------
@app.get("/")
def home():
    return {"message": "AI Document Chatbot Running Successfully"}
