from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document, EmbeddingStatus
from app.models.document_chunk import DocumentChunk
from app.models.user import User, UserRole
from app.services.chunk_service import chunk_text
from app.services.embedding_service import embed_query, embed_texts


def index_document_chunks(db: Session, document: Document) -> None:
    if not document.extracted_text:
        return

    chunks = chunk_text(document.extracted_text)
    embeddings = embed_texts(chunks)

    for index, (text, embedding) in enumerate(zip(chunks, embeddings)):
        db.add(
            DocumentChunk(
                document_id=document.id,
                chunk_text=text,
                embedding=embedding,
                chunk_index=index,
            )
        )

    document.chunk_count = len(chunks)
    document.embedding_status = EmbeddingStatus.READY
    db.commit()


def semantic_search(db: Session, user: User, query: str, limit: int = 5) -> list[dict]:
    query_embedding = embed_query(query)
    distance = DocumentChunk.embedding.cosine_distance(query_embedding)
    statement = (
        select(DocumentChunk, Document, distance.label("distance"))
        .join(Document, Document.id == DocumentChunk.document_id)
        .where(DocumentChunk.embedding.is_not(None))
        .order_by(distance)
        .limit(limit)
    )
    if user.role != UserRole.ADMIN:
        statement = statement.where(Document.owner_id == user.id)

    results = []
    for chunk, document, score_distance in db.execute(statement):
        results.append(
            {
                "document": document.original_filename,
                "document_id": str(document.id),
                "chunk_text": chunk.chunk_text,
                "score": round(1 - float(score_distance), 4),
            }
        )
    return results


def generate_grounded_answer(query: str, results: list[dict]) -> dict:
    if not results:
        return {"answer": "No relevant document context was found.", "sources": [], "citations": []}
    context = "\n\n".join(item["chunk_text"] for item in results[:3])
    answer = f"Based on the indexed documents, the most relevant context for '{query}' is: {context[:900]}"
    sources = sorted({item["document"] for item in results})
    return {"answer": answer, "sources": sources, "citations": results[:5]}
