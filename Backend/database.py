import sqlite3

DB_NAME = "chat_memory.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_message TEXT,
            ai_response TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_message(session_id, user_message, ai_response):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations (session_id, user_message, ai_response)
        VALUES (?, ?, ?)
    """, (session_id, user_message, ai_response))

    conn.commit()
    conn.close()

def get_last_messages(session_id, limit=2):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_message, ai_response
        FROM conversations
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (session_id, limit))

    rows = cursor.fetchall()
    conn.close()

    return rows[::-1]  # return in correct order
