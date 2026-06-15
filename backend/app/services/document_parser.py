from pathlib import Path

import pandas as pd
from docx import Document as DocxDocument
from PyPDF2 import PdfReader


def extract_text(file_path: Path, file_type: str) -> str:
    extension = file_type.lower()
    if extension == "pdf":
        return extract_pdf_text(file_path)
    if extension == "docx":
        return extract_docx_text(file_path)
    if extension in {"txt", "md"}:
        return extract_plain_text(file_path)
    if extension == "csv":
        return extract_csv_text(file_path)
    raise ValueError(f"Unsupported file type: {file_type}")


def extract_pdf_text(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(page.strip() for page in pages if page.strip())


def extract_docx_text(file_path: Path) -> str:
    document = DocxDocument(str(file_path))
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs)


def extract_plain_text(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8", errors="ignore")


def extract_csv_text(file_path: Path) -> str:
    dataframe = pd.read_csv(file_path)
    return dataframe.to_csv(index=False)
