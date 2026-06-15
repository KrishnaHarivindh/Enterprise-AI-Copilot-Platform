from app.services.search_service import generate_grounded_answer


class LLMService:
    def generate_answer(self, question: str, context_results: list[dict]) -> dict:
        return generate_grounded_answer(question, context_results)

    def summarize(self, text: str) -> str:
        clean = " ".join(text.split())
        return clean[:900] + ("..." if len(clean) > 900 else "")

    def generate_report(self, query: str, context_results: list[dict]) -> dict:
        text = " ".join(item["chunk_text"] for item in context_results)
        return {
            "executive_summary": self.summarize(text),
            "key_findings": [item["chunk_text"][:180] for item in context_results[:4]],
            "recommendations": ["Review cited source documents before action."],
            "risks": ["Generated content requires human review."],
            "sources": sorted({item["document"] for item in context_results}),
        }


def get_llm_service(provider: str = "local") -> LLMService:
    # Provider hook for OpenAI, Gemini, or Ollama without changing API routes.
    return LLMService()
