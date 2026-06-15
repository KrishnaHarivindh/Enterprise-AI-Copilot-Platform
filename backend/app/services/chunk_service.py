from app.core.config import settings


def chunk_text(text: str, chunk_size: int | None = None, overlap: int | None = None) -> list[str]:
    clean_text = " ".join(text.split())
    if not clean_text:
        return []

    size = chunk_size or settings.chunk_size
    step_back = overlap if overlap is not None else settings.chunk_overlap
    chunks: list[str] = []
    start = 0

    while start < len(clean_text):
        end = min(start + size, len(clean_text))
        chunks.append(clean_text[start:end])
        if end == len(clean_text):
            break
        start = max(end - step_back, start + 1)

    return chunks
