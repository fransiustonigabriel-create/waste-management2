from typing import Any


# =========================================================
# Configuration
# =========================================================

# Skor minimum knowledge agar dianggap relevan.
MIN_TOP_SCORE = 35

# Selisih minimum antara knowledge pertama dan kedua.
MIN_SCORE_GAP = 5

# Panjang minimum jawaban lokal agar dianggap layak.
MIN_LOCAL_ANSWER_LENGTH = 40

# Confidence maksimum ketika jawaban lokal belum cukup
# dan sistem harus menggunakan LLM fallback.
MAX_LLM_FALLBACK_CONFIDENCE = 69


COMPLEX_QUESTION_PATTERNS = {
    "mengapa",
    "kenapa",
    "analisis",
    "analisa",
    "bandingkan",
    "perbandingan",
    "dibanding",
    "dibandingkan",
    "hubungan",
    "dampak",
    "penyebab",
    "jelaskan hubungan",
    "lebih baik",
    "lebih efektif",
    "lebih akurat",
    "strategi",
}


OUT_OF_DOMAIN_PATTERNS = {
    "buatkan puisi",
    "resep makanan",
    "sejarah romawi",
    "presiden indonesia",
    "ramalan",
    "cerita lucu",
    "film terbaru",
    "sepak bola",
}


RESPONSE_TYPES_REQUIRING_SYNTHESIS = {
    "comparison",
}


# =========================================================
# Text Helpers
# =========================================================

def normalize_text(value: Any) -> str:
    """
    Mengubah input menjadi teks lowercase yang aman.
    """

    if value is None:
        return ""

    return str(value).lower().strip()


def is_complex_question(question: str) -> bool:
    """
    Menentukan apakah pertanyaan membutuhkan sintesis,
    analisis, atau penggabungan beberapa informasi.
    """

    clean_question = normalize_text(question)

    return any(
        pattern in clean_question
        for pattern in COMPLEX_QUESTION_PATTERNS
    )


def is_out_of_domain(question: str) -> bool:
    """
    Memeriksa apakah pertanyaan jelas berada di luar
    domain EcoRoute AI dan pengelolaan sampah.
    """

    clean_question = normalize_text(question)

    return any(
        pattern in clean_question
        for pattern in OUT_OF_DOMAIN_PATTERNS
    )


# =========================================================
# Ranking Helpers
# =========================================================

def get_top_score(ranking: list[dict]) -> int:
    """
    Mengambil skor knowledge tertinggi.
    """

    if not isinstance(ranking, list) or not ranking:
        return 0

    first_item = ranking[0]

    if not isinstance(first_item, dict):
        return 0

    try:
        return max(
            int(first_item.get("score", 0)),
            0,
        )

    except (TypeError, ValueError):
        return 0


def get_score_gap(ranking: list[dict]) -> int:
    """
    Menghitung selisih skor knowledge pertama dan kedua.
    """

    if not isinstance(ranking, list) or not ranking:
        return 0

    top_score = get_top_score(ranking)

    if len(ranking) < 2:
        return top_score

    second_item = ranking[1]

    if not isinstance(second_item, dict):
        return top_score

    try:
        second_score = max(
            int(second_item.get("score", 0)),
            0,
        )

    except (TypeError, ValueError):
        second_score = 0

    return max(
        top_score - second_score,
        0,
    )


# =========================================================
# Local Answer Validation
# =========================================================

def has_valid_local_answer(local_result: dict) -> bool:
    """
    Memeriksa apakah Local Answer Engine menghasilkan
    jawaban yang layak ditampilkan.
    """

    if not isinstance(local_result, dict):
        return False

    answer = str(
        local_result.get("answer", "")
    ).strip()

    unavailable_phrases = {
        "informasi yang diminta belum tersedia",
        "knowledge yang diterima tidak memiliki format",
        "informasi yang relevan belum tersedia",
        "jawaban belum tersedia",
    }

    if any(
        phrase in answer.lower()
        for phrase in unavailable_phrases
    ):
        return False

    return len(answer) >= MIN_LOCAL_ANSWER_LENGTH


# =========================================================
# Confidence Calculation
# =========================================================

def calculate_local_confidence(
    top_score: int,
    score_gap: int,
    valid_local_answer: bool,
    faq_matched: bool,
    complex_question: bool,
    requires_synthesis: bool,
) -> int:
    """
    Menghitung tingkat keyakinan terhadap kemampuan knowledge
    lokal dalam menjawab pertanyaan.

    Confidence ini bukan confidence LLM dan bukan ukuran
    kebenaran mutlak jawaban.
    """

    retrieval_component = (
        min(top_score, 100) * 0.50
    )

    ranking_gap_component = (
        min(score_gap * 5, 100) * 0.15
    )

    answer_component = (
        20
        if valid_local_answer
        else 0
    )

    faq_component = (
        15
        if faq_matched
        else 0
    )

    confidence = (
        retrieval_component
        + ranking_gap_component
        + answer_component
        + faq_component
    )

    # Pertanyaan kompleks mengurangi keyakinan bahwa jawaban
    # lokal saja sudah cukup.
    if complex_question:
        confidence -= 15

    # Pertanyaan yang membutuhkan sintesis mendapatkan
    # penalti tambahan.
    if requires_synthesis:
        confidence -= 15

    return int(
        max(
            0,
            min(confidence, 100),
        )
    )


# =========================================================
# Main Sufficiency Evaluation
# =========================================================

def evaluate_knowledge_sufficiency(
    question: str,
    ranking: list[dict],
    local_result: dict,
) -> dict:
    """
    Menentukan apakah jawaban lokal sudah cukup atau perlu
    bantuan LLM sebagai fallback.

    Return:
        {
            "is_sufficient": bool,
            "decision": "local" | "llm" | "out_of_domain",
            "confidence": int,
            "reasons": list[str],
            "top_score": int,
            "score_gap": int,
            "confidence_scope": str
        }
    """

    # =====================================================
    # Out-of-Domain Check
    # =====================================================

    if is_out_of_domain(question):
        return {
            "is_sufficient": False,
            "decision": "out_of_domain",
            "confidence": 0,
            "reasons": [
                (
                    "Pertanyaan berada di luar topik "
                    "yang didukung EcoRoute AI."
                ),
            ],
            "top_score": 0,
            "score_gap": 0,
            "confidence_scope": "local_knowledge",
        }

    # =====================================================
    # Extract Signals
    # =====================================================

    top_score = get_top_score(ranking)
    score_gap = get_score_gap(ranking)

    faq_matched = bool(
        local_result.get(
            "faq_matched",
            False,
        )
    )

    valid_local_answer = has_valid_local_answer(
        local_result
    )

    complex_question = is_complex_question(
        question
    )

    response_type = str(
        local_result.get(
            "response_type",
            "general",
        )
    ).lower()

    requires_synthesis = (
        response_type
        in RESPONSE_TYPES_REQUIRING_SYNTHESIS
    )

    confidence = calculate_local_confidence(
        top_score=top_score,
        score_gap=score_gap,
        valid_local_answer=valid_local_answer,
        faq_matched=faq_matched,
        complex_question=complex_question,
        requires_synthesis=requires_synthesis,
    )

    # =====================================================
    # Strong FAQ Match
    # =====================================================

    if (
        faq_matched
        and valid_local_answer
        and not requires_synthesis
        and not complex_question
    ):
        confidence = max(
            confidence,
            85,
        )

        return {
            "is_sufficient": True,
            "decision": "local",
            "confidence": min(
                confidence,
                100,
            ),
            "reasons": [
                (
                    "Jawaban yang sesuai ditemukan "
                    "di FAQ Knowledge Base."
                ),
                (
                    "Informasi lokal sudah cukup untuk "
                    "menjawab pertanyaan."
                ),
            ],
            "top_score": top_score,
            "score_gap": score_gap,
            "confidence_scope": "local_knowledge",
        }

    # =====================================================
    # Build User-Friendly Reasons
    # =====================================================

    reasons = []

    if top_score >= MIN_TOP_SCORE:
        reasons.append(
            "Informasi yang relevan berhasil ditemukan."
        )
    else:
        reasons.append(
            (
                "Knowledge Base belum menemukan informasi "
                "dengan tingkat relevansi yang cukup tinggi."
            )
        )

    if valid_local_answer:
        reasons.append(
            "Jawaban lokal sementara berhasil disusun."
        )
    else:
        reasons.append(
            (
                "Informasi lokal belum cukup untuk "
                "membentuk jawaban yang lengkap."
            )
        )

    if score_gap >= MIN_SCORE_GAP:
        reasons.append(
            (
                "Sumber utama memiliki relevansi lebih kuat "
                "dibandingkan sumber lainnya."
            )
        )
    else:
        reasons.append(
            (
                "Beberapa sumber memiliki tingkat relevansi "
                "yang hampir sama."
            )
        )

    if complex_question:
        reasons.append(
            (
                "Pertanyaan memerlukan analisis atau "
                "penggabungan beberapa informasi."
            )
        )

    if requires_synthesis:
        reasons.append(
            (
                "Pertanyaan perbandingan memerlukan sintesis "
                "dari lebih dari satu informasi."
            )
        )

    # =====================================================
    # Decision
    # =====================================================

    local_is_enough = (
        top_score >= MIN_TOP_SCORE
        and valid_local_answer
        and not complex_question
        and not requires_synthesis
    )

    if local_is_enough:
        decision = "local"

        confidence = max(
            confidence,
            70,
        )

    else:
        decision = "llm"

        # Confidence menunjukkan keyakinan terhadap jawaban
        # lokal. Karena masih memerlukan LLM, nilainya tidak
        # boleh tampil terlalu tinggi.
        confidence = min(
            confidence,
            MAX_LLM_FALLBACK_CONFIDENCE,
        )

        reasons.append(
            (
                "Sistem memilih bantuan LLM untuk "
                "menyusun jawaban yang lebih lengkap."
            )
        )

    return {
        "is_sufficient": local_is_enough,
        "decision": decision,
        "confidence": confidence,
        "reasons": reasons,
        "top_score": top_score,
        "score_gap": score_gap,
        "confidence_scope": "local_knowledge",
    }