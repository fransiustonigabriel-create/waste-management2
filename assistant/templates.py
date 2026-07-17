from typing import Final

from assistant.response_types import ResponseType


RESPONSE_TEMPLATES: Final[dict[ResponseType, dict]] = {

    ResponseType.DEFINITION: {
        "name": "Definition Template",
        "sections": [
            "title",
            "description",
            "concepts",
            "related_topics",
        ],
        "max_items": {
            "concepts": 4,
            "related_topics": 4,
        },
    },

    ResponseType.FEATURE: {
        "name": "Feature Template",
        "sections": [
            "title",
            "description",
            "features",
            "benefits",
            "related_topics",
        ],
        "max_items": {
            "features": 5,
            "benefits": 3,
            "related_topics": 4,
        },
    },

    ResponseType.WORKFLOW: {
        "name": "Workflow Template",
        "sections": [
            "title",
            "description",
            "workflow",
            "recommendations",
        ],
        "max_items": {
            "workflow": 7,
            "recommendations": 3,
        },
    },

    ResponseType.CALCULATION: {
        "name": "Calculation Template",
        "sections": [
            "title",
            "description",
            "calculation",
            "concepts",
            "recommendations",
        ],
        "max_items": {
            "concepts": 3,
            "recommendations": 3,
        },
    },

    ResponseType.RECOMMENDATION: {
        "name": "Recommendation Template",
        "sections": [
            "title",
            "description",
            "recommendations",
            "workflow",
        ],
        "max_items": {
            "recommendations": 5,
            "workflow": 4,
        },
    },

    ResponseType.FAQ: {
        "name": "FAQ Template",
        "sections": [
            "title",
            "faq_answer",
            "description",
            "related_topics",
        ],
        "max_items": {
            "related_topics": 4,
        },
    },

    ResponseType.COMPARISON: {
        "name": "Comparison Template",
        "sections": [
            "title",
            "description",
            "concepts",
            "features",
            "related_topics",
        ],
        "max_items": {
            "concepts": 5,
            "features": 4,
            "related_topics": 4,
        },
    },

    ResponseType.GENERAL: {
        "name": "General Template",
        "sections": [
            "title",
            "description",
            "objectives",
            "features",
            "recommendations",
            "related_topics",
        ],
        "max_items": {
            "objectives": 3,
            "features": 4,
            "recommendations": 3,
            "related_topics": 4,
        },
    },
}


SECTION_LABELS: Final[dict[str, str]] = {
    "title": "",
    "description": "",
    "objectives": "Tujuan",
    "features": "Fitur Utama",
    "workflow": "Cara Kerja",
    "concepts": "Konsep Penting",
    "calculation": "Perhitungan",
    "recommendations": "Rekomendasi",
    "benefits": "Manfaat",
    "limitations": "Keterbatasan",
    "related_topics": "Topik Terkait",
    "faq_answer": "Jawaban",
}


def get_template(response_type: ResponseType) -> dict:
    """
    Mengambil template berdasarkan jenis respons.
    """

    return RESPONSE_TEMPLATES.get(
        response_type,
        RESPONSE_TEMPLATES[ResponseType.GENERAL],
    )


def get_section_label(section_name: str) -> str:
    """
    Mengambil label tampilan sebuah section.
    """

    return SECTION_LABELS.get(
        section_name,
        section_name.replace("_", " ").title(),
    )