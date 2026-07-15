ROUTING = {

    "title": "Armada Routing",

    "description": """
Armada Routing merupakan modul EcoRoute AI yang digunakan untuk
menentukan jalur terbaik armada pengangkut sampah.

Modul ini memanfaatkan OpenStreetMap, Nominatim, dan OSRM untuk
menghitung rute, jarak, estimasi waktu tempuh, serta membantu
pengalokasian armada dari pool terdekat menuju lokasi pengumpulan
maupun lokasi event.

Routing membantu meningkatkan efisiensi perjalanan armada serta
mengurangi waktu dan biaya operasional.
""",

    "keywords": [

        "routing",
        "route",
        "rute",
        "jalur",
        "map",
        "peta",
        "osrm",
        "openstreetmap",
        "nominatim",
        "pool",
        "tps",
        "tpst",
        "spa",
        "bantargebang",
        "event",
        "lokasi",
        "jarak",
        "waktu tempuh"

    ],

    "aliases": [

        "route optimization",
        "optimasi rute",
        "jalur armada",
        "jalur truk",
        "truck routing",
        "vehicle routing"

    ],

    "examples": [

        "Bagaimana rute armada dihitung?",

        "Apa itu OSRM?",

        "Apa itu Nominatim?",

        "Mengapa memilih pool terdekat?",

        "Bagaimana menghitung jarak?",

        "Bagaimana menghitung waktu tempuh?",

        "Apa tujuan akhir armada?",

        "Bagaimana alokasi multi-pool bekerja?"

    ],

    "objectives": [

        "Menentukan rute paling efisien.",

        "Mengurangi waktu tempuh.",

        "Mengurangi jarak perjalanan.",

        "Mendukung distribusi armada.",

        "Memvisualisasikan perjalanan armada."

    ],

    "features": [

        "Peta rute armada.",

        "Perhitungan jarak.",

        "Estimasi waktu tempuh.",

        "Pencarian lokasi event.",

        "Alokasi multi-pool.",

        "Visualisasi jalur armada.",

        "Animasi perjalanan armada."

    ],

    "workflow": [

        "Pengguna memilih lokasi tujuan.",

        "Sistem mencari koordinat menggunakan Nominatim.",

        "Pool terdekat dipilih.",

        "OSRM menghitung rute terbaik.",

        "Jarak dan waktu dihitung.",

        "Peta dan jalur divisualisasikan."

    ],

    "route_process": [

        "Pool Armada",

        "TPS",

        "SPA",

        "TPST Bantargebang",

        "Kembali ke Pool"

    ],

    "concepts": {

        "routing":
            "Proses menentukan jalur perjalanan armada.",

        "pool":
            "Lokasi keberangkatan armada.",

        "tps":
            "Tempat Penampungan Sementara.",

        "spa":
            "Stasiun Peralihan Antara.",

        "tpst":
            "Tempat Pengolahan Sampah Terpadu.",

        "osrm":
            "Open Source Routing Machine untuk menghitung jalur kendaraan.",

        "nominatim":
            "Layanan pencarian alamat berbasis OpenStreetMap.",

        "multi_pool":
            "Distribusi armada dari lebih dari satu pool."

    },

    "display_information": {

        "route":
            "Rute perjalanan armada.",

        "distance":
            "Total jarak perjalanan.",

        "travel_time":
            "Estimasi waktu tempuh.",

        "selected_pool":
            "Pool yang dipilih.",

        "destination":
            "Lokasi tujuan.",

        "allocated_trucks":
            "Jumlah armada yang dialokasikan."

    },

    "recommendations": [

        "Gunakan pool terdekat.",

        "Kurangi perjalanan kosong.",

        "Gunakan multi-pool jika armada tidak mencukupi.",

        "Prioritaskan rute dengan waktu tempuh paling singkat.",

        "Lakukan evaluasi rute secara berkala."

    ],

    "benefits": [

        "Mengurangi biaya operasional.",

        "Mengurangi konsumsi bahan bakar.",

        "Meningkatkan efisiensi armada.",

        "Mengurangi waktu tempuh.",

        "Mempermudah monitoring perjalanan."

    ],

    "limitations": [

        "Routing bergantung pada koneksi internet.",

        "OSRM menggunakan data OpenStreetMap.",

        "Estimasi waktu tidak selalu sama dengan kondisi lalu lintas sebenarnya.",

        "Kualitas rute bergantung pada data peta."

    ],

    "faq": {

        "apa itu routing":
            "Routing merupakan proses menentukan jalur terbaik armada.",

        "apa fungsi routing":
            "Routing membantu armada mencapai tujuan secara efisien.",

        "apa itu osrm":
            "OSRM merupakan Open Source Routing Machine untuk menghitung rute kendaraan.",

        "apa itu nominatim":
            "Nominatim digunakan untuk mencari alamat dan koordinat lokasi.",

        "apa itu pool":
            "Pool merupakan lokasi keberangkatan armada.",

        "apa itu multi pool":
            "Multi Pool adalah penggunaan lebih dari satu pool untuk memenuhi kebutuhan armada.",

        "bagaimana rute dihitung":
            "Rute dihitung menggunakan jaringan jalan OpenStreetMap melalui OSRM.",

        "mengapa routing penting":
            "Routing membantu mengurangi jarak, waktu, dan biaya operasional.",

        "apa tujuan akhir armada":
            "Tujuan akhir armada adalah TPST atau fasilitas pengolahan sampah.",

        "bagaimana menghitung waktu tempuh":
            "Waktu tempuh dihitung berdasarkan panjang rute dan kecepatan rata-rata dari layanan routing."

    },

    "related_topics": [

        "Dashboard",

        "Armada",

        "Simulator",

        "Machine Learning",

        "Waste Management"

    ]

}