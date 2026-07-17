from typing import Any

from assistant.retriever import retrieve
from assistant.recommender import build_recommendations
from assistant.response_builder import build_local_response
from assistant.knowledge_sufficiency import (
    evaluate_knowledge_sufficiency,
)
from assistant.prompt import build_prompt
from assistant.llm import generate_response


class EcoRouteAssistant:
    """
    Orchestrator utama EcoRoute AI Assistant.

    Alur utama:
    1. Menerima pertanyaan pengguna.
    2. Mengambil knowledge paling relevan.
    3. Menghasilkan rekomendasi operasional.
    4. Menyusun jawaban lokal.
    5. Mengevaluasi kecukupan knowledge lokal.
    6. Menggunakan LLM hanya sebagai fallback.
    """

    def ask(self, question: str) -> dict[str, Any]:
        """
        Memproses satu pertanyaan pengguna.
        """

        clean_question = str(question).strip()

        if not clean_question:
            return {
                "answer": (
                    "Silakan tuliskan pertanyaan mengenai "
                    "EcoRoute AI."
                ),
                "intent": "general",
                "response_type": "general",
                "faq_matched": False,
                "sources": [],
                "recommendations": [],
                "risks": [],
                "ranking": [],
                "answer_mode": "local",
                "confidence": 0,
                "sufficiency_reasons": [],
            }

        try:
            # =====================================================
            # Knowledge Retrieval
            # =====================================================

            retrieval_result = retrieve(clean_question)

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

            # =====================================================
            # Recommendation Engine
            # =====================================================

            recommendation_result = build_recommendations(
                question=clean_question,
                intent=intent,
                knowledges=knowledges,
            )

            recommendations = recommendation_result.get(
                "recommendations",
                [],
            )

            risks = recommendation_result.get(
                "risks",
                [],
            )

            # =====================================================
            # Local Answer Engine
            # =====================================================

            local_result = build_local_response(
                question=clean_question,
                knowledges=knowledges,
                recommendations=recommendations,
                risks=risks,
                include_sources=False,
            )

            # =====================================================
            # Knowledge Sufficiency
            # =====================================================

            sufficiency_result = evaluate_knowledge_sufficiency(
                question=clean_question,
                ranking=ranking,
                local_result=local_result,
            )

            decision = sufficiency_result.get(
                "decision",
                "local",
            )

            confidence = sufficiency_result.get(
                "confidence",
                0,
            )

            sufficiency_reasons = sufficiency_result.get(
                "reasons",
                [],
            )

            # =====================================================
            # Out-of-Domain Response
            # =====================================================

            if decision == "out_of_domain":
                return {
                    "answer": (
                        "Maaf, EcoRoute AI Assistant hanya "
                        "membahas topik yang berkaitan dengan "
                        "EcoRoute AI, pengelolaan sampah, armada, "
                        "routing, dashboard, simulator, dan "
                        "Machine Learning."
                    ),
                    "intent": "out_of_domain",
                    "response_type": "general",
                    "faq_matched": False,
                    "sources": [],
                    "recommendations": [],
                    "risks": [],
                    "ranking": ranking,
                    "answer_mode": "out_of_domain",
                    "confidence": 0,
                    "sufficiency_reasons": sufficiency_reasons,
                }

            # =====================================================
            # Local Response
            # =====================================================

            if decision == "local":
                return {
                    "answer": local_result.get(
                        "answer",
                        (
                            "Informasi yang diminta belum tersedia "
                            "di Knowledge Base EcoRoute AI."
                        ),
                    ),
                    "intent": intent,
                    "response_type": local_result.get(
                        "response_type",
                        "general",
                    ),
                    "faq_matched": local_result.get(
                        "faq_matched",
                        False,
                    ),
                    "sources": local_result.get(
                        "sources",
                        [],
                    ),
                    "recommendations": recommendations,
                    "risks": risks,
                    "ranking": ranking,
                    "answer_mode": "local",
                    "confidence": confidence,
                    "sufficiency_reasons": sufficiency_reasons,
                }

            # =====================================================
            # LLM Fallback
            # =====================================================

            llm_prompt = self._build_llm_prompt(
                question=clean_question,
                response_type=local_result.get(
                    "response_type",
                    "general",
                ),
                knowledges=knowledges,
                recommendations=recommendations,
                risks=risks,
                local_answer=local_result.get(
                    "answer",
                    "",
                ),
            )

            llm_answer = generate_response(
                llm_prompt
            )

            return {
                "answer": llm_answer,
                "intent": intent,
                "response_type": local_result.get(
                    "response_type",
                    "general",
                ),
                "faq_matched": local_result.get(
                    "faq_matched",
                    False,
                ),
                "sources": local_result.get(
                    "sources",
                    [],
                ),
                "recommendations": recommendations,
                "risks": risks,
                "ranking": ranking,
                "answer_mode": "llm_fallback",
                "confidence": confidence,
                "sufficiency_reasons": sufficiency_reasons,
            }

        except Exception as error:
            return {
                "answer": (
                    "Maaf, EcoRoute AI Assistant mengalami "
                    "kesalahan saat memproses pertanyaan.\n\n"
                    f"**Detail:** `{error}`"
                ),
                "intent": "error",
                "response_type": "general",
                "faq_matched": False,
                "sources": [],
                "recommendations": [],
                "risks": [],
                "ranking": [],
                "answer_mode": "error",
                "confidence": 0,
                "sufficiency_reasons": [],
            }

    def _build_llm_prompt(
        self,
        question: str,
        response_type: str,
        knowledges: list[dict],
        recommendations: list[str],
        risks: list[str],
        local_answer: str,
    ) -> str:
        """
        Menyusun prompt fallback lengkap untuk Groq.

        Groq hanya melakukan sintesis berdasarkan:
        - knowledge hasil retrieval,
        - jawaban lokal sementara,
        - risiko,
        - rekomendasi operasional,
        - sumber knowledge.
        """

        # =====================================================
        # Knowledge Context
        # =====================================================

        knowledge_sections = []
        source_names = []

        for knowledge in knowledges:
            if not isinstance(knowledge, dict):
                continue

            title = str(
                knowledge.get(
                    "title",
                    "Knowledge EcoRoute AI",
                )
            ).strip()

            description = str(
                knowledge.get(
                    "description",
                    "",
                )
            ).strip()

            concepts = knowledge.get(
                "concepts",
                {},
            )

            faq = knowledge.get(
                "faq",
                {},
            )

            features = knowledge.get(
                "features",
                [],
            )

            workflow = knowledge.get(
                "workflow",
                [],
            )

            metrics = knowledge.get(
                "metrics",
                {},
            )

            model_comparison = knowledge.get(
                "model_comparison",
                {},
            )

            section_parts = []

            if title:
                section_parts.append(
                    f"## {title}"
                )

                if title not in source_names:
                    source_names.append(
                        title
                    )

            if description:
                section_parts.append(
                    description
                )

            if isinstance(concepts, dict) and concepts:
                concept_lines = [
                    f"- {name}: {explanation}"
                    for name, explanation
                    in concepts.items()
                ]

                section_parts.append(
                    "### Konsep\n"
                    + "\n".join(concept_lines)
                )

            if isinstance(features, list) and features:
                feature_lines = [
                    f"- {feature}"
                    for feature in features
                ]

                section_parts.append(
                    "### Fitur\n"
                    + "\n".join(feature_lines)
                )

            if isinstance(workflow, list) and workflow:
                workflow_lines = [
                    f"{index}. {step}"
                    for index, step in enumerate(
                        workflow,
                        start=1,
                    )
                ]

                section_parts.append(
                    "### Alur Kerja\n"
                    + "\n".join(workflow_lines)
                )

            if isinstance(metrics, dict) and metrics:
                metric_lines = [
                    f"- {name}: {value}"
                    for name, value
                    in metrics.items()
                ]

                section_parts.append(
                    "### Metrik\n"
                    + "\n".join(metric_lines)
                )

            if (
                isinstance(model_comparison, dict)
                and model_comparison
            ):
                comparison_lines = [
                    f"- {name}: {value}"
                    for name, value
                    in model_comparison.items()
                ]

                section_parts.append(
                    "### Perbandingan Model\n"
                    + "\n".join(comparison_lines)
                )

            if isinstance(faq, dict) and faq:
                faq_lines = [
                    (
                        f"- Pertanyaan: {faq_question}\n"
                        f"  Jawaban: {faq_answer}"
                    )
                    for faq_question, faq_answer
                    in faq.items()
                ]

                section_parts.append(
                    "### FAQ\n"
                    + "\n".join(faq_lines)
                )

            if section_parts:
                knowledge_sections.append(
                    "\n\n".join(section_parts)
                )

        knowledge_context = (
            "\n\n---\n\n".join(
                knowledge_sections
            )
            if knowledge_sections
            else (
                "Knowledge lokal yang relevan belum "
                "tersedia."
            )
        )

        # =====================================================
        # Recommendation Context
        # =====================================================

        recommendation_context = (
            "\n".join(
                f"- {recommendation}"
                for recommendation in recommendations
            )
            if recommendations
            else "Tidak ada rekomendasi operasional khusus."
        )

        # =====================================================
        # Risk Context
        # =====================================================

        risk_context = (
            "\n".join(
                f"- {risk}"
                for risk in risks
            )
            if risks
            else "Tidak ada kondisi khusus yang terdeteksi."
        )

        # =====================================================
        # Source Context
        # =====================================================

        source_context = (
            "\n".join(
                f"- {source}"
                for source in source_names
            )
            if source_names
            else "Sumber knowledge belum tersedia."
        )

        # =====================================================
        # Final Prompt
        # =====================================================

        return build_prompt(
            user_question=question,
            response_type=response_type,
            local_answer=(
                local_answer.strip()
                if local_answer
                else (
                    "Jawaban lokal sementara belum "
                    "tersedia."
                )
            ),
            retrieved_context=knowledge_context,
            recommendations=recommendation_context,
            risks=risk_context,
            sources=source_context,
        )