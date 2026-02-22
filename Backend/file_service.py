from PyPDF2 import PdfReader
import pandas as pd
import io


def extract_text_from_pdf(file_bytes):
    pdf_stream = io.BytesIO(file_bytes)
    reader = PdfReader(pdf_stream)

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def extract_text_from_csv(file_bytes):
    df = pd.read_csv(io.BytesIO(file_bytes))
    return df.to_string()
