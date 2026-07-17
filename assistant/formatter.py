from typing import Any

from assistant.templates import get_section_label


def format_heading(text: str, level: int = 2) -> str:
    """
    Membuat heading Markdown.
    """

    clean_text = str(text).strip()

    if not clean_text:
        return ""

    level = max(1, min(level, 6))

    return f"{'#' * level} {clean_text}"


def format_paragraph(value: Any) -> str:
    """
    Mengubah nilai menjadi paragraf yang bersih.
    """

    if value is None:
        return ""

    clean_value = str(value).strip()

    return clean_value


def format_bullet_list(
    values: list[Any],
    max_items: int | None = None,
) -> str:
    """
    Mengubah list menjadi bullet Markdown.
    """

    if not isinstance(values, list):
        return ""

    selected_values = values

    if max_items is not None:
        selected_values = values[:max_items]

    cleaned_values = [
        str(item).strip()
        for item in selected_values
        if str(item).strip()
    ]

    if not cleaned_values:
        return ""

    return "\n".join(
        f"- {item}"
        for item in cleaned_values
    )


def format_numbered_list(
    values: list[Any],
    max_items: int | None = None,
) -> str:
    """
    Mengubah list menjadi numbered Markdown.
    """

    if not isinstance(values, list):
        return ""

    selected_values = values

    if max_items is not None:
        selected_values = values[:max_items]

    cleaned_values = [
        str(item).strip()
        for item in selected_values
        if str(item).strip()
    ]

    if not cleaned_values:
        return ""

    return "\n".join(
        f"{index}. {item}"
        for index, item in enumerate(
            cleaned_values,
            start=1,
        )
    )


def format_dictionary(
    values: dict[Any, Any],
    max_items: int | None = None,
) -> str:
    """
    Mengubah dictionary menjadi daftar istilah dan penjelasan.
    """

    if not isinstance(values, dict):
        return ""

    items = list(values.items())

    if max_items is not None:
        items = items[:max_items]

    formatted_items = []

    for key, value in items:
        clean_key = str(key).replace("_", " ").strip().title()
        clean_value = str(value).strip()

        if not clean_key or not clean_value:
            continue

        formatted_items.append(
            f"- **{clean_key}:** {clean_value}"
        )

    return "\n".join(formatted_items)


def format_calculation(
    calculation: dict[Any, Any],
) -> str:
    """
    Menampilkan bagian perhitungan secara khusus.
    """

    if not isinstance(calculation, dict):
        return ""

    formatted_parts = []

    formula = calculation.get("formula")

    if formula:
        formatted_parts.append(
            f"**Rumus:** `{str(formula).strip()}`"
        )

    explanation = (
        calculation.get("required_trucks")
        or calculation.get("description")
    )

    if explanation:
        formatted_parts.append(
            str(explanation).strip()
        )

    notes = calculation.get("notes")

    if notes:
        formatted_parts.append(
            f"**Catatan:** {str(notes).strip()}"
        )

    if not formatted_parts:
        return format_dictionary(calculation)

    return "\n\n".join(formatted_parts)


def format_faq_answer(
    question: str,
    faq: dict[Any, Any],
) -> str:
    """
    Mencari jawaban FAQ yang paling mendekati pertanyaan.
    """

    if not isinstance(faq, dict):
        return ""

    clean_question = str(question).lower().strip()

    if not clean_question:
        return ""

    best_answer = ""
    best_score = 0

    question_words = set(clean_question.split())

    for faq_question, faq_answer in faq.items():
        clean_faq_question = str(
            faq_question
        ).lower().strip()

        if clean_faq_question in clean_question:
            return str(faq_answer).strip()

        faq_words = set(clean_faq_question.split())

        score = len(
            question_words.intersection(faq_words)
        )

        if score > best_score:
            best_score = score
            best_answer = str(faq_answer).strip()

    return best_answer


def format_section(
    section_name: str,
    value: Any,
    max_items: int | None = None,
    question: str = "",
) -> str:
    """
    Memformat satu section berdasarkan jenis datanya.
    """

    if value is None:
        return ""

    if section_name == "title":
        return format_heading(
            str(value),
            level=2,
        )

    if section_name == "description":
        return format_paragraph(value)

    if section_name == "workflow":
        content = format_numbered_list(
            value,
            max_items,
        )

    elif section_name == "calculation":
        content = format_calculation(value)

    elif section_name == "faq_answer":
        content = format_faq_answer(
            question,
            value,
        )

    elif isinstance(value, list):
        content = format_bullet_list(
            value,
            max_items,
        )

    elif isinstance(value, dict):
        content = format_dictionary(
            value,
            max_items,
        )

    else:
        content = format_paragraph(value)

    if not content:
        return ""

    label = get_section_label(section_name)

    if not label:
        return content

    return (
        f"{format_heading(label, level=3)}\n\n"
        f"{content}"
    )


def join_sections(
    sections: list[str],
) -> str:
    """
    Menggabungkan beberapa section menjadi jawaban Markdown.
    """

    cleaned_sections = [
        section.strip()
        for section in sections
        if section and section.strip()
    ]

    return "\n\n".join(cleaned_sections)