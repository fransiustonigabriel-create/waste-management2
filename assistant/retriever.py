import re
from typing import Any

from assistant.intent import detect_intent
from assistant.knowledge_registry import KNOWLEDGE


STOPWORDS = {
    "apa",
    "itu",
    "yang",
    "dan",
    "atau",
    "dari",
    "ke",
    "di",
    "pada",
    "untuk",
    "dengan",
    "adalah",
    "bagaimana",
    "mengapa",
    "kenapa",
    "jelaskan",
    "tolong",
    "saya",
    "kami",
    "bisa",
    "dapat",
}


def normalize_text(text: Any) -> str:
    """
    Mengubah teks menjadi format standar untuk pencocokan.
    """

    if text is None:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9À-ÿ\s²]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def tokenize(text: str) -> set[str]:
    """
    Memecah teks menjadi token unik dan membuang stopword.
    """

    normalized = normalize_text(text)

    return {
        word
        for word in normalized.split()
        if len(word) >= 3 and word not in STOPWORDS
    }


def phrase_match(
    question: str,
    phrase: str,
) -> bool:
    """
    Memeriksa apakah sebuah frasa terdapat dalam pertanyaan.
    """

    normalized_question = normalize_text(question)
    normalized_phrase = normalize_text(phrase)

    if not normalized_phrase:
        return False

    return normalized_phrase in normalized_question


def token_overlap_score(
    question_tokens: set[str],
    text: str,
    weight: int,
) -> int:
    """
    Memberikan skor berdasarkan jumlah token yang cocok.
    """

    text_tokens = tokenize(text)
    overlap = question_tokens.intersection(text_tokens)

    return len(overlap) * weight


def score_list_field(
    question: str,
    question_tokens: set[str],
    values: list,
    phrase_weight: int,
    token_weight: int,
) -> int:
    """
    Menghitung skor untuk field berbentuk list.
    """

    score = 0

    for value in values:
        value_text = str(value)

        if phrase_match(question, value_text):
            score += phrase_weight

        score += token_overlap_score(
            question_tokens,
            value_text,
            token_weight,
        )

    return score


def score_dictionary_field(
    question: str,
    question_tokens: set[str],
    values: dict,
    key_phrase_weight: int,
    key_token_weight: int,
    value_token_weight: int,
) -> int:
    """
    Menghitung skor untuk field berbentuk dictionary.
    """

    score = 0

    for key, value in values.items():
        key_text = str(key)
        value_text = str(value)

        if phrase_match(question, key_text):
            score += key_phrase_weight

        score += token_overlap_score(
            question_tokens,
            key_text,
            key_token_weight,
        )

        score += token_overlap_score(
            question_tokens,
            value_text,
            value_token_weight,
        )

    return score


def calculate_score(
    question: str,
    knowledge: dict,
    knowledge_name: str,
    intent: str,
) -> tuple[int, list[str]]:
    """
    Menghitung skor relevansi satu knowledge.

    Return:
        score, alasan pencocokan
    """

    score = 0
    matches = []

    question_normalized = normalize_text(question)
    question_tokens = tokenize(question)

    title = knowledge.get("title", "")
    description = knowledge.get("description", "")
    keywords = knowledge.get("keywords", [])
    aliases = knowledge.get("aliases", [])
    examples = knowledge.get("examples", [])
    related_topics = knowledge.get("related_topics", [])
    faq = knowledge.get("faq", {})
    concepts = knowledge.get("concepts", {})
    terms = knowledge.get("terms", {})
    questions = knowledge.get("questions", {})

    # =====================================================
    # Intent
    # =====================================================

    if knowledge_name == intent:
        score += 40
        matches.append("intent")

    # =====================================================
    # Title
    # =====================================================

    if phrase_match(question_normalized, title):
        score += 30
        matches.append("title")

    title_token_score = token_overlap_score(
        question_tokens,
        title,
        8,
    )

    if title_token_score:
        score += title_token_score
        matches.append("title-token")

    # =====================================================
    # Keywords
    # =====================================================

    keyword_score = score_list_field(
        question,
        question_tokens,
        keywords,
        phrase_weight=18,
        token_weight=5,
    )

    if keyword_score:
        score += keyword_score
        matches.append("keywords")

    # =====================================================
    # Aliases
    # =====================================================

    alias_score = score_list_field(
        question,
        question_tokens,
        aliases,
        phrase_weight=22,
        token_weight=6,
    )

    if alias_score:
        score += alias_score
        matches.append("aliases")

    # =====================================================
    # Example Questions
    # =====================================================

    example_score = score_list_field(
        question,
        question_tokens,
        examples,
        phrase_weight=25,
        token_weight=4,
    )

    if example_score:
        score += example_score
        matches.append("examples")

    # =====================================================
    # FAQ
    # =====================================================

    if isinstance(faq, dict):
        faq_score = score_dictionary_field(
            question,
            question_tokens,
            faq,
            key_phrase_weight=35,
            key_token_weight=7,
            value_token_weight=2,
        )

        if faq_score:
            score += faq_score
            matches.append("faq")

    # =====================================================
    # General Questions
    # =====================================================

    if isinstance(questions, dict):
        question_score = score_dictionary_field(
            question,
            question_tokens,
            questions,
            key_phrase_weight=35,
            key_token_weight=7,
            value_token_weight=2,
        )

        if question_score:
            score += question_score
            matches.append("questions")

    # =====================================================
    # Concepts
    # =====================================================

    if isinstance(concepts, dict):
        concept_score = score_dictionary_field(
            question,
            question_tokens,
            concepts,
            key_phrase_weight=25,
            key_token_weight=6,
            value_token_weight=2,
        )

        if concept_score:
            score += concept_score
            matches.append("concepts")

    # =====================================================
    # Glossary Terms
    # =====================================================

    if isinstance(terms, dict):
        term_score = score_dictionary_field(
            question,
            question_tokens,
            terms,
            key_phrase_weight=30,
            key_token_weight=7,
            value_token_weight=2,
        )

        if term_score:
            score += term_score
            matches.append("terms")

    # =====================================================
    # Description
    # =====================================================

    description_score = token_overlap_score(
        question_tokens,
        description,
        2,
    )

    if description_score:
        score += description_score
        matches.append("description")

    # =====================================================
    # Related Topics
    # =====================================================

    topic_score = score_list_field(
        question,
        question_tokens,
        related_topics,
        phrase_weight=8,
        token_weight=2,
    )

    if topic_score:
        score += topic_score
        matches.append("related-topics")

    return score, matches


def retrieve(
    question: str,
    top_k: int = 3,
) -> dict:
    """
    Mengambil knowledge paling relevan.

    Return:
        {
            "intent": str,
            "knowledges": list[dict],
            "ranking": list[dict]
        }
    """

    clean_question = normalize_text(question)

    if not clean_question:
        return {
            "intent": "general",
            "knowledges": [],
            "ranking": [],
        }

    intent = detect_intent(clean_question)

    ranking = []

    for name, knowledge in KNOWLEDGE.items():
        score, matches = calculate_score(
            question=clean_question,
            knowledge=knowledge,
            knowledge_name=name,
            intent=intent,
        )

        ranking.append(
            {
                "name": name,
                "title": knowledge.get(
                    "title",
                    name,
                ),
                "score": score,
                "matches": matches,
                "knowledge": knowledge,
            }
        )

    ranking.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    selected_items = [
        item
        for item in ranking
        if item["score"] > 0
    ][:top_k]

    selected_knowledges = [
        item["knowledge"]
        for item in selected_items
    ]

    if not selected_knowledges:
        selected_knowledges = [
            {
                "title": "General",
                "description": (
                    "Informasi yang relevan belum tersedia "
                    "di Knowledge Base EcoRoute AI."
                ),
                "faq": {},
                "keywords": [],
                "aliases": [],
                "examples": [],
                "related_topics": [],
            }
        ]

    public_ranking = [
        {
            "name": item["name"],
            "title": item["title"],
            "score": item["score"],
            "matches": item["matches"],
        }
        for item in ranking[:top_k]
    ]

    return {
        "intent": intent,
        "knowledges": selected_knowledges,
        "ranking": public_ranking,
    }