# document_store.py

# This will store uploaded document text in memory (FREE alternative to databases)

DOCUMENT_TEXT = ""


def save_document(text: str):
    global DOCUMENT_TEXT
    DOCUMENT_TEXT = text


def get_document():
    return DOCUMENT_TEXT
