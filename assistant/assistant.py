from typing import Any

from assistant.retriever import retrieve
from assistant.recommender import (
    build_recommendations,
    recommendations_to_context,
)
from assistant.prompt import build_prompt
from assistant.llm import generate_response


class EcoRouteAssistant:
    """
    Orchestrator utama EcoRoute AI Assistant.
    """

    def ask(self, question: str) -> dict[str, Any]:
        """
        Memproses pertanyaan pengguna dan menghasilkan
        jawaban beserta rekomendasi operasional.
        """

        question = question.strip()

        if not question:
            return {
                "answer": (
                    "Silakan tuliskan pertanyaan "
                    "mengenai EcoRoute AI."
                ),
                "intent": "general",
                "sources": [],
                "recommendations": [],
                "risks": [],
            }

        try:
            retrieval_result = retrieve(question)

            knowledges = retrieval_result.get(
                "knowledges",
                [],
            )

            intent = retrieval_result.get(
                "intent",
                "general",
            )

            ranking = retrieval_result.get(
                "ranking",
                [],
            )

            knowledge_context = self._build_context(
                knowledges
            )

            recommendation_result = build_recommendations(
                question=question,
                intent=intent,
                knowledges=knowledges,
            )

            recommendation_context = recommendations_to_context(
                recommendation_result
            )

            combined_context = f"""
KNOWLEDGE BASE

{knowledge_context}

========================================

OPERATIONAL RECOMMENDATION

{recommendation_context}
"""

            prompt = build_prompt(
                user_question=question,
                retrieved_context=combined_context,
            )

            answer = generate_response(prompt)

            sources = [
                knowledge.get("title", "Unknown")
                for knowledge in knowledges
                if isinstance(knowledge, dict)
            ]

            return {
                "answer": answer,
                "intent": intent,
                "sources": sources,
                "recommendations": recommendation_result.get(
                    "recommendations",
                    [],
                ),
                "risks": recommendation_result.get(
                    "risks",
                    [],
                ),
                "ranking": ranking,
            }

        except Exception as error:
            return {
                "answer": (
                    "Maaf, EcoRoute AI Assistant mengalami "
                    "kesalahan saat memproses pertanyaan.\n\n"
                    f"Detail: `{error}`"
                ),
                "intent": "error",
                "sources": [],
                "recommendations": [],
                "risks": [],
                "ranking": [],
            }

    def _build_context(
        self,
        knowledges: list[dict],
    ) -> str:
        """
        Menyusun context dari knowledge hasil retrieval.
        """

        if not knowledges:
            return (
                "Tidak ditemukan knowledge lokal "
                "yang relevan."
            )

        context_sections = []

        for knowledge in knowledges:
            if not isinstance(knowledge, dict):
                continue

            title = knowledge.get(
                "title",
                "Untitled Knowledge",
            )

            description = knowledge.get(
                "description",
                "",
            )

            concepts = knowledge.get(
                "concepts",
                {},
            )

            faq = knowledge.get(
                "faq",
                {},
            )

            section = [
                f"## {title}",
                description.strip(),
            ]

            if isinstance(concepts, dict) and concepts:
                concept_lines = [
                    f"- {name}: {explanation}"
                    for name, explanation
                    in concepts.items()
                ]

                section.append(
                    "Concepts:\n"
                    + "\n".join(concept_lines)
                )

            if isinstance(faq, dict) and faq:
                faq_lines = [
                    f"- Q: {faq_question}\n"
                    f"  A: {faq_answer}"
                    for faq_question, faq_answer
                    in faq.items()
                ]

                section.append(
                    "FAQ:\n"
                    + "\n".join(faq_lines)
                )

            context_sections.append(
                "\n\n".join(
                    item
                    for item in section
                    if item
                )
            )

        return "\n\n---\n\n".join(
            context_sections
        )