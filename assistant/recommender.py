from typing import Any


RECOMMENDATION_RULES = {
    "dashboard": {
        "keywords": [
            "dashboard",
            "kpi",
            "grafik",
            "monitoring",
            "tren",
            "peta",
            "prediksi",
        ],
        "recommendations": [
            "Gunakan Dashboard untuk melihat wilayah dengan prediksi volume sampah tertinggi.",
            "Periksa KPI kebutuhan armada sebelum menentukan rencana operasional.",
            "Bandingkan grafik tren untuk melihat apakah peningkatan hanya terjadi satu hari atau berlanjut.",
        ],
    },

    "armada": {
        "keywords": [
            "armada",
            "truk",
            "kendaraan",
            "ritase",
            "trip",
            "kapasitas",
            "unit",
            "pool",
        ],
        "recommendations": [
            "Bandingkan jumlah armada yang dibutuhkan dengan armada yang siap beroperasi.",
            "Tambahkan ritase jika jumlah armada siap belum mencukupi kebutuhan pengangkutan.",
            "Prioritaskan armada untuk wilayah dengan prediksi volume sampah tertinggi.",
            "Pertimbangkan bantuan armada dari wilayah terdekat jika kapasitas wilayah tidak mencukupi.",
        ],
    },

    "simulator": {
        "keywords": [
            "simulator",
            "simulasi",
            "event",
            "acara",
            "pengunjung",
            "prediksi harian",
            "lonjakan",
        ],
        "recommendations": [
            "Gunakan Event Simulator sebelum pelaksanaan acara untuk memperkirakan lonjakan sampah.",
            "Bandingkan kondisi normal dan kondisi event sebelum menetapkan jumlah armada.",
            "Siapkan armada cadangan jika jumlah pengunjung diperkirakan tinggi.",
            "Lakukan pengangkutan lebih awal di sekitar lokasi event.",
        ],
    },

    "routing": {
        "keywords": [
            "routing",
            "rute",
            "jalur",
            "jarak",
            "waktu tempuh",
            "osrm",
            "pool",
            "tps",
            "tpst",
            "bantargebang",
        ],
        "recommendations": [
            "Gunakan pool armada yang paling dekat dengan lokasi pengumpulan.",
            "Pilih rute dengan jarak dan waktu tempuh yang paling efisien.",
            "Kurangi perjalanan kosong agar pemakaian bahan bakar lebih efisien.",
            "Gunakan alokasi multi-pool jika satu pool tidak memiliki armada yang cukup.",
        ],
    },

    "machine_learning": {
        "keywords": [
            "machine learning",
            "model",
            "xgboost",
            "random forest",
            "ensemble",
            "mae",
            "rmse",
            "r2",
            "akurasi",
            "prediksi",
            "anomali",
        ],
        "recommendations": [
            "Bandingkan MAE, RMSE, dan R² sebelum menentukan model terbaik.",
            "Periksa status anomali sebelum menggunakan hasil prediksi untuk keputusan operasional.",
            "Lakukan pelatihan ulang apabila pola data terbaru sudah berbeda dari data training.",
            "Gunakan hasil model sebagai pendukung keputusan, bukan satu-satunya dasar keputusan.",
        ],
    },

    "waste_management": {
        "keywords": [
            "sampah",
            "waste",
            "organik",
            "anorganik",
            "tps",
            "tpst",
            "3r",
            "reduce",
            "reuse",
            "recycle",
        ],
        "recommendations": [
            "Prioritaskan pemilahan sampah sejak dari sumbernya.",
            "Gunakan prinsip Reduce, Reuse, dan Recycle untuk mengurangi timbulan sampah.",
            "Pastikan pengangkutan dilakukan tepat waktu agar tidak terjadi penumpukan di TPS.",
            "Gunakan prediksi volume untuk menyusun jadwal pengangkutan yang lebih efisien.",
        ],
    },

    "general": {
        "keywords": [],
        "recommendations": [
            "Gunakan Dashboard untuk melihat kondisi operasional secara umum.",
            "Gunakan Event Simulator untuk melakukan prediksi sebelum kegiatan besar.",
            "Gunakan Armada Management untuk menghitung kebutuhan kendaraan.",
            "Gunakan Rute Armada untuk melihat jalur pengangkutan yang direkomendasikan.",
        ],
    },
}


RISK_RULES = {
    "increase": {
        "keywords": [
            "meningkat",
            "naik",
            "tinggi",
            "melonjak",
            "lonjakan",
            "bertambah",
            "kelebihan",
        ],
        "recommendations": [
            "Siapkan armada tambahan atau ritase kedua untuk mengantisipasi peningkatan volume.",
            "Prioritaskan wilayah dengan tingkat kenaikan tertinggi.",
        ],
    },

    "shortage": {
        "keywords": [
            "kurang",
            "kekurangan",
            "tidak cukup",
            "terbatas",
            "habis",
        ],
        "recommendations": [
            "Gunakan ritase tambahan jika armada yang tersedia masih dapat beroperasi.",
            "Minta bantuan armada dari pool atau wilayah terdekat.",
        ],
    },

    "event": {
        "keywords": [
            "event",
            "festival",
            "konser",
            "acara",
            "pengunjung",
        ],
        "recommendations": [
            "Tempatkan armada cadangan di sekitar lokasi event.",
            "Jadwalkan pengangkutan sebelum, selama, dan setelah acara.",
        ],
    },

    "anomaly": {
        "keywords": [
            "anomali",
            "tidak normal",
            "aneh",
            "berbeda",
            "outlier",
        ],
        "recommendations": [
            "Periksa kembali nilai input sebelum menggunakan hasil prediksi.",
            "Bandingkan input dengan rentang data historis.",
        ],
    },
}


def normalize_text(value: Any) -> str:
    """
    Mengubah input menjadi teks lowercase yang aman.
    """

    if value is None:
        return ""

    return str(value).lower().strip()


def detect_operational_risks(question: str) -> list[str]:
    """
    Mendeteksi kondisi atau risiko yang disebut dalam pertanyaan.
    """

    normalized_question = normalize_text(question)
    risks = []

    for risk_name, rule in RISK_RULES.items():
        if any(
            keyword in normalized_question
            for keyword in rule["keywords"]
        ):
            risks.append(risk_name)

    return risks


def build_recommendations(
    question: str,
    intent: str = "general",
    knowledges: list[dict] | None = None,
    max_recommendations: int = 4,
) -> dict:
    """
    Menghasilkan rekomendasi operasional berdasarkan intent,
    pertanyaan, dan knowledge yang ditemukan.

    Return:
        {
            "intent": str,
            "risks": list[str],
            "recommendations": list[str]
        }
    """

    normalized_question = normalize_text(question)
    knowledges = knowledges or []

    recommendations = []
    detected_intent = intent if intent in RECOMMENDATION_RULES else "general"

    # =====================================================
    # Recommendation by Intent
    # =====================================================

    intent_rule = RECOMMENDATION_RULES[detected_intent]

    recommendations.extend(
        intent_rule["recommendations"]
    )

    # =====================================================
    # Recommendation by Question Keywords
    # =====================================================

    for rule_name, rule in RECOMMENDATION_RULES.items():
        if rule_name == detected_intent:
            continue

        matched = any(
            keyword in normalized_question
            for keyword in rule["keywords"]
        )

        if matched:
            recommendations.extend(
                rule["recommendations"][:2]
            )

    # =====================================================
    # Recommendation from Retrieved Knowledge
    # =====================================================

    for knowledge in knowledges:
        if not isinstance(knowledge, dict):
            continue

        knowledge_recommendations = knowledge.get(
            "recommendations",
            [],
        )

        if isinstance(knowledge_recommendations, list):
            recommendations.extend(
                str(item)
                for item in knowledge_recommendations
            )

    # =====================================================
    # Risk-based Recommendations
    # =====================================================

    risks = detect_operational_risks(question)

    for risk in risks:
        recommendations.extend(
            RISK_RULES[risk]["recommendations"]
        )

    # =====================================================
    # Remove Duplicate Recommendations
    # =====================================================

    unique_recommendations = []

    for recommendation in recommendations:
        cleaned = recommendation.strip()

        if (
            cleaned
            and cleaned not in unique_recommendations
        ):
            unique_recommendations.append(cleaned)

    return {
        "intent": detected_intent,
        "risks": risks,
        "recommendations": unique_recommendations[
            :max_recommendations
        ],
    }


def recommendations_to_context(
    recommendation_result: dict,
) -> str:
    """
    Mengubah hasil rekomendasi menjadi teks untuk prompt LLM.
    """

    recommendations = recommendation_result.get(
        "recommendations",
        [],
    )

    risks = recommendation_result.get(
        "risks",
        [],
    )

    sections = []

    if risks:
        sections.append(
            "Risiko atau kondisi yang terdeteksi:\n- "
            + "\n- ".join(risks)
        )

    if recommendations:
        sections.append(
            "Rekomendasi operasional:\n- "
            + "\n- ".join(recommendations)
        )

    if not sections:
        return "Belum ada rekomendasi operasional khusus."

    return "\n\n".join(sections)