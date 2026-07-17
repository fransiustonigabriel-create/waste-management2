from typing import Any

from assistant.formatter import (
    format_section,
    join_sections,
)
from assistant.response_types import (
    CALCULATION_KEYWORDS,
    COMPARISON_KEYWORDS,
    DEFINITION_KEYWORDS,
    FAQ_KEYWORDS,
    FEATURE_KEYWORDS,
    RECOMMENDATION_KEYWORDS,
    WORKFLOW_KEYWORDS,
    ResponseType,
)
from assistant.templates import get_template


def normalize_text(value: Any) -> str:
    """
    Mengubah input menjadi teks lowercase yang aman.
    """

    if value is None:
        return ""

    return str(value).lower().strip()


def contains_any_phrase(
    question: str,
    phrases: set[str],
) -> bool:
    """
    Memeriksa apakah salah satu frasa terdapat
    di dalam pertanyaan.
    """

    normalized_question = normalize_text(question)

    return any(
        phrase in normalized_question
        for phrase in phrases
    )


def classify_response_type(
    question: str,
) -> ResponseType:
    """
    Menentukan jenis jawaban berdasarkan pola pertanyaan.

    Urutan pemeriksaan dibuat berdasarkan prioritas agar
    pertanyaan perbandingan tidak salah diklasifikasikan
    sebagai general atau jenis lainnya.
    """

    normalized_question = normalize_text(question)

    if not normalized_question:
        return ResponseType.GENERAL

    # Perbandingan diperiksa lebih awal karena sering
    # mengandung kata umum seperti "lebih baik".
    if contains_any_phrase(
        normalized_question,
        COMPARISON_KEYWORDS,
    ):
        return ResponseType.COMPARISON

    if contains_any_phrase(
        normalized_question,
        CALCULATION_KEYWORDS,
    ):
        return ResponseType.CALCULATION

    if contains_any_phrase(
        normalized_question,
        RECOMMENDATION_KEYWORDS,
    ):
        return ResponseType.RECOMMENDATION

    if contains_any_phrase(
        normalized_question,
        WORKFLOW_KEYWORDS,
    ):
        return ResponseType.WORKFLOW

    if contains_any_phrase(
        normalized_question,
        FEATURE_KEYWORDS,
    ):
        return ResponseType.FEATURE

    if contains_any_phrase(
        normalized_question,
        DEFINITION_KEYWORDS,
    ):
        return ResponseType.DEFINITION

    if contains_any_phrase(
        normalized_question,
        FAQ_KEYWORDS,
    ):
        return ResponseType.FAQ

    return ResponseType.GENERAL


def search_faq(
    question: str,
    knowledge: dict,
    response_type: ResponseType | None = None,
) -> str | None:
    """
    Mencari FAQ yang benar-benar relevan.

    Untuk pertanyaan kompleks seperti perbandingan,
    rekomendasi, dan workflow, FAQ hanya dipakai jika
    tingkat kecocokannya sangat kuat.
    """

    normalized_question = normalize_text(question)

    faq = knowledge.get("faq", {})

    if not isinstance(faq, dict) or not faq:
        return None

    selected_type = (
        response_type
        or classify_response_type(normalized_question)
    )

    strict_types = {
        ResponseType.COMPARISON,
        ResponseType.RECOMMENDATION,
        ResponseType.WORKFLOW,
    }

    best_answer = None
    best_score = 0
    best_coverage = 0.0

    question_words = {
        word
        for word in normalized_question.split()
        if len(word) >= 3
    }

    for faq_question, faq_answer in faq.items():
        normalized_faq_question = normalize_text(
            faq_question
        )

        if not normalized_faq_question:
            continue

        # Exact phrase adalah kecocokan paling kuat.
        if normalized_faq_question in normalized_question:
            return str(faq_answer).strip()

        faq_words = {
            word
            for word in normalized_faq_question.split()
            if len(word) >= 3
        }

        if not faq_words:
            continue

        overlap = question_words.intersection(
            faq_words
        )

        score = len(overlap)

        coverage = (
            score / len(faq_words)
            if faq_words
            else 0.0
        )

        # Pertanyaan kompleks membutuhkan kecocokan sangat kuat.
        if selected_type in strict_types:
            if coverage < 0.80:
                continue

        # Pertanyaan biasa tetap membutuhkan kecocokan minimum.
        else:
            minimum_score = (
                1
                if len(faq_words) == 1
                else 2
            )

            if score < minimum_score:
                continue

        if (
            coverage > best_coverage
            or (
                coverage == best_coverage
                and score > best_score
            )
        ):
            best_coverage = coverage
            best_score = score
            best_answer = str(
                faq_answer
            ).strip()

    return best_answer


def prepare_section_value(
    section_name: str,
    knowledge: dict,
    question: str,
) -> Any:
    """
    Menyiapkan data untuk setiap section template.
    """

    if section_name == "faq_answer":
        return knowledge.get("faq", {})

    return knowledge.get(section_name)


def build_local_answer(
    question: str,
    knowledge: dict,
    response_type: ResponseType | None = None,
) -> dict:
    """
    Menyusun jawaban lokal berdasarkan knowledge dan template.

    Return:
        {
            "answer": str,
            "response_type": str,
            "faq_matched": bool
        }
    """

    if not isinstance(knowledge, dict):
        return {
            "answer": (
                "Knowledge yang diterima tidak memiliki "
                "format yang dapat diproses."
            ),
            "response_type": ResponseType.GENERAL.value,
            "faq_matched": False,
        }

    selected_type = (
        response_type
        or classify_response_type(question)
    )

    faq_answer = search_faq(
        question=question,
        knowledge=knowledge,
        response_type=selected_type,
    )

    if faq_answer:
        title = knowledge.get(
            "title",
            "EcoRoute AI",
        )

        answer = join_sections(
            [
                format_section(
                    "title",
                    title,
                ),
                format_section(
                    "faq_answer",
                    {
                        question: faq_answer
                    },
                    question=question,
                ),
            ]
        )

        return {
            "answer": answer,
            "response_type": selected_type.value,
            "faq_matched": True,
        }

    template = get_template(
        selected_type
    )

    sections = []
    max_items = template.get(
        "max_items",
        {},
    )

    for section_name in template.get(
        "sections",
        [],
    ):
        value = prepare_section_value(
            section_name=section_name,
            knowledge=knowledge,
            question=question,
        )

        formatted_section = format_section(
            section_name=section_name,
            value=value,
            max_items=max_items.get(
                section_name
            ),
            question=question,
        )

        if formatted_section:
            sections.append(
                formatted_section
            )

    answer = join_sections(
        sections
    )

    if not answer:
        answer = (
            "Informasi yang diminta belum tersedia "
            "di Knowledge Base EcoRoute AI."
        )

    return {
        "answer": answer,
        "response_type": selected_type.value,
        "faq_matched": False,
    }