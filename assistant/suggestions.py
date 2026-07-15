SUGGESTIONS = {

    "dashboard": [

        "Apa itu KPI?",
        "Bagaimana membaca Dashboard?",
        "Apa saja fitur Dashboard?"

    ],

    "armada": [

        "Bagaimana menghitung armada?",
        "Apa itu ritase?",
        "Bagaimana menghitung kapasitas truk?"

    ],

    "simulator": [

        "Apa itu Event Simulator?",
        "Bagaimana simulasi dilakukan?",
        "Bagaimana prediksi volume sampah?"

    ],

    "routing": [

        "Bagaimana rute ditentukan?",
        "Apa itu OSRM?",
        "Mengapa memilih rute tercepat?"

    ],

    "machine_learning": [

        "Apa itu XGBoost?",
        "Apa itu Random Forest?",
        "Mengapa memakai Ensemble?"

    ],

    "waste_management": [

        "Apa itu TPS?",
        "Apa itu TPST?",
        "Apa itu Reduce Reuse Recycle?"

    ],

    "general": [

        "Apa fungsi EcoRoute AI?",
        "Bagaimana cara menggunakan aplikasi?",
        "Apa saja fitur aplikasi?"

    ]

}


def get_suggestions(intent):

    return SUGGESTIONS.get(intent, SUGGESTIONS["general"])