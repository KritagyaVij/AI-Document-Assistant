def chunk_text(text, chunk_size=700, overlap=100):
    """
    Splits text into overlapping chunks.

    chunk_size → approx words per chunk (acts like tokens)
    overlap → repeated words between chunks to preserve context
    """

    words = text.split()
    chunks = []

    start = 0
    text_length = len(words)

    while start < text_length:
        end = start + chunk_size
        chunk_words = words[start:end]

        chunk = " ".join(chunk_words)
        chunks.append(chunk)

        # Move start forward but keep overlap
        start += chunk_size - overlap

    return chunks
