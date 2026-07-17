from typing import Any

from assistant.answer_engine import build_local_answer
from assistant.formatter import (
    format_heading,
    format_bullet_list,
    join_sections,
)


def select_primary_knowledge(
    knowledges: list[dict],
) -> dict:
    """
    Memilih knowledge utama dari hasil retrieval.

    Retriever sudah mengurutkan knowledge berdasarkan relevansi,
    sehingga item pertama dianggap sebagai knowledge utama.
    """

    if not isinstance(knowledges, list):
        return {}

    for knowledge in knowledges:
        if isinstance(knowledge, dict):
            return knowledge

    return {}


def build_sources_section(
    knowledges: list[dict],
) -> str:
    """
    Membuat daftar sumber knowledge.
    """

    sources = []

    for knowledge in knowledges:
        if not isinstance(knowledge, dict):
            continue

        title = str(
            knowledge.get("title", "")
        ).strip()

        if title and title not in sources:
            sources.append(title)

    if not sources:
        return ""

    return (
        f"{format_heading('Sumber Knowledge', level=3)}\n\n"
        f"{format_bullet_list(sources)}"
    )


def build_recommendation_section(
    recommendations: list[str],
    max_items: int = 4,
) -> str:
    """
    Membuat bagian rekomendasi operasional.
    """

    if not isinstance(recommendations, list):
        return ""

    cleaned_recommendations = [
        str(item).strip()
        for item in recommendations
        if str(item).strip()
    ]

    if not cleaned_recommendations:
        return ""

    return (
        f"{format_heading('Rekomendasi Operasional', level=3)}\n\n"
        f"{format_bullet_list(cleaned_recommendations, max_items)}"
    )


def build_risk_section(
    risks: list[str],
) -> str:
    """
    Membuat bagian kondisi operasional yang terdeteksi.
    """

    if not isinstance(risks, list):
        return ""

    risk_labels = {
        "increase": (
            "Terdapat indikasi peningkatan volume "
            "atau kebutuhan operasional."
        ),
        "shortage": (
            "Terdapat indikasi kekurangan armada "
            "atau kapasitas pengangkutan."
        ),
        "event": (
            "Terdapat potensi lonjakan sampah "
            "akibat event atau keramaian."
        ),
        "anomaly": (
            "Terdapat input atau hasil yang "
            "terindikasi anomali."
        ),
    }

    risk_descriptions = []

    for risk in risks:
        description = risk_labels.get(
            str(risk),
            str(risk).replace("_", " ").title(),
        )

        if description not in risk_descriptions:
            risk_descriptions.append(description)

    if not risk_descriptions:
        return ""

    return (
        f"{format_heading('Kondisi yang Terdeteksi', level=3)}\n\n"
        f"{format_bullet_list(risk_descriptions)}"
    )


def build_local_response(
    question: str,
    knowledges: list[dict],
    recommendations: list[str] | None = None,
    risks: list[str] | None = None,
    include_sources: bool = True,
) -> dict[str, Any]:
    """
    Menggabungkan Local Answer Engine dengan rekomendasi,
    risiko, dan sumber knowledge.

    Return:
        {
            "answer": str,
            "response_type": str,
            "faq_matched": bool,
            "sources": list[str]
        }
    """

    recommendations = recommendations or []
    risks = risks or []

    primary_knowledge = select_primary_knowledge(
        knowledges
    )

    if not primary_knowledge:
        return {
            "answer": (
                "Informasi yang relevan belum tersedia "
                "di Knowledge Base EcoRoute AI."
            ),
            "response_type": "general",
            "faq_matched": False,
            "sources": [],
        }

    local_result = build_local_answer(
        question=question,
        knowledge=primary_knowledge,
    )

    response_sections = [
        local_result.get("answer", ""),
        build_risk_section(risks),
        build_recommendation_section(
            recommendations
        ),
    ]

    if include_sources:
        response_sections.append(
            build_sources_section(knowledges)
        )

    final_answer = join_sections(
        response_sections
    )

    sources = []

    for knowledge in knowledges:
        if not isinstance(knowledge, dict):
            continue

        title = str(
            knowledge.get("title", "")
        ).strip()

        if title and title not in sources:
            sources.append(title)

    return {
        "answer": final_answer,
        "response_type": local_result.get(
            "response_type",
            "general",
        ),
        "faq_matched": local_result.get(
            "faq_matched",
            False,
        ),
        "sources": sources,
    }