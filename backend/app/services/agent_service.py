from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.models.user import User
from app.services.document_service import get_accessible_document
from app.services.search_service import semantic_search


def summarize_document(db: Session, user: User, document_id) -> dict:
    document = get_accessible_document(db, document_id, user)
    chunks = list(
        db.scalars(
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document.id)
            .order_by(DocumentChunk.chunk_index)
            .limit(6)
        )
    )
    text = " ".join(chunk.chunk_text for chunk in chunks) or (document.extracted_text or "")
    summary = summarize_text(text)
    return {"summary": summary, "sources": [document.original_filename]}


def generate_report(db: Session, user: User, query: str) -> dict:
    results = semantic_search(db, user, query, limit=6)
    context = [item["chunk_text"] for item in results]
    joined = " ".join(context)
    sources = sorted({item["document"] for item in results})

    return {
        "executive_summary": summarize_text(joined),
        "key_findings": bulletize(joined, "finding", 4),
        "recommendations": [
            "Review the highest-scoring source documents before making policy or business decisions.",
            "Validate extracted findings with document owners where the source material is incomplete.",
        ],
        "risks": [
            "Answer quality depends on uploaded document coverage.",
            "Generated report is extractive and should be reviewed by a human.",
        ],
        "sources": sources,
    }


def create_meeting_notes(transcript: str) -> dict:
    lines = [line.strip("- ") for line in transcript.splitlines() if line.strip()]
    text = " ".join(lines)
    action_items = [line for line in lines if any(word in line.lower() for word in ["todo", "action", "assign", "follow"])]
    decisions = [line for line in lines if any(word in line.lower() for word in ["decided", "approved", "agreed"])]

    return {
        "summary": summarize_text(text),
        "action_items": action_items[:8] or ["Review transcript and assign explicit owners."],
        "decisions": decisions[:8] or ["No explicit decisions detected."],
        "follow_ups": action_items[:5] or ["Share meeting notes with stakeholders."],
    }


def summarize_text(text: str, max_chars: int = 900) -> str:
    clean = " ".join(text.split())
    if not clean:
        return "No extractable text was available."
    return clean[:max_chars] + ("..." if len(clean) > max_chars else "")


def bulletize(text: str, prefix: str, limit: int) -> list[str]:
    sentences = [sentence.strip() for sentence in text.replace("\n", " ").split(".") if sentence.strip()]
    return sentences[:limit] or [f"No {prefix}s found in the retrieved context."]
