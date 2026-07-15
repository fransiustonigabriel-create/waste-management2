"""
Intent Detection untuk EcoRoute AI Assistant
"""


INTENTS = {

    "dashboard": [

        "dashboard",
        "kpi",
        "grafik",
        "chart",
        "monitoring",
        "ringkasan",
        "overview",
        "prediksi hari ini"

    ],

    "armada": [

        "armada",
        "truk",
        "kendaraan",
        "kapasitas",
        "ritase",
        "trip",
        "pool"

    ],

    "simulator": [

        "simulator",
        "prediksi",
        "event",
        "simulasi",
        "pengunjung",
        "volume"

    ],

    "routing": [

        "rute",
        "routing",
        "osrm",
        "jalan",
        "bantargebang",
        "jalur"

    ],

    "machine_learning": [

        "xgboost",
        "random forest",
        "ensemble",
        "machine learning",
        "model",
        "training",
        "akurasi"

    ],

    "waste_management": [

        "sampah",
        "tps",
        "tpst",
        "3r",
        "reduce",
        "reuse",
        "recycle"

    ],

    "faq": [

        "cara",
        "bagaimana",
        "kenapa",
        "mengapa",
        "help",
        "bantuan"

    ]

}


def detect_intent(question: str):

    question = question.lower()

    for intent, keywords in INTENTS.items():

        for keyword in keywords:

            if keyword in question:

                return intent

    return "general"