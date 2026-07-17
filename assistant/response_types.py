from enum import Enum


class ResponseType(str, Enum):
    """
    Jenis respons yang dapat dibuat oleh Local Answer Engine.
    """

    DEFINITION = "definition"
    FEATURE = "feature"
    WORKFLOW = "workflow"
    CALCULATION = "calculation"
    RECOMMENDATION = "recommendation"
    FAQ = "faq"
    COMPARISON = "comparison"
    GENERAL = "general"


DEFINITION_KEYWORDS = {
    "apa itu",
    "pengertian",
    "definisi",
    "arti",
    "jelaskan",
    "maksud",
}


FEATURE_KEYWORDS = {
    "fitur",
    "fungsi",
    "kegunaan",
    "manfaat",
    "apa saja yang tersedia",
    "apa yang bisa dilakukan",
}


WORKFLOW_KEYWORDS = {
    "bagaimana cara kerja",
    "bagaimana proses",
    "alur",
    "workflow",
    "tahapan",
    "langkah",
    "proses",
}


CALCULATION_KEYWORDS = {
    "hitung",
    "menghitung",
    "perhitungan",
    "rumus",
    "formula",
    "berapa",
    "estimasi",
}


RECOMMENDATION_KEYWORDS = {
    "rekomendasi",
    "saran",
    "sebaiknya",
    "apa yang harus dilakukan",
    "apa yang perlu dilakukan",
    "solusi",
    "tindakan",
}


FAQ_KEYWORDS = {
    "apakah",
    "bisakah",
    "dapatkah",
    "bolehkah",
}


COMPARISON_KEYWORDS = {
    "perbedaan",
    "apa perbedaan",
    "beda",
    "bedanya",
    "bandingkan",
    "membandingkan",
    "dibanding",
    "dibandingkan",
    "lebih baik",
    "lebih bagus",
    "lebih efektif",
    "lebih akurat",
    "mana yang lebih baik",
    "mana yang terbaik",
    "versus",
    " vs ",
    "hubungan",
}