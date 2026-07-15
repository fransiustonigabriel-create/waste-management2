ARMADA = {

    "title": "Armada Management",

    "description": """
Armada Management adalah modul EcoRoute AI yang digunakan untuk mengelola
ketersediaan armada pengangkut sampah. Halaman ini membantu operator
menghitung jumlah armada yang tersedia, kapasitas angkut, serta estimasi
jumlah truk yang dibutuhkan berdasarkan hasil prediksi volume sampah.

Modul ini mendukung pengambilan keputusan operasional agar distribusi
armada menjadi lebih efisien dan mengurangi risiko kekurangan maupun
kelebihan kendaraan.
""",

    "keywords": [

        "armada",
        "truck",
        "truk",
        "kendaraan",
        "fleet",
        "pool",
        "ritase",
        "trip",
        "kapasitas",
        "kapasitas truk",
        "jumlah armada",
        "operasional",
        "driver",
        "angkutan sampah"

    ],

    "aliases": [

        "fleet management",
        "garbage truck",
        "waste truck",
        "mobil sampah",
        "kendaraan pengangkut",
        "kendaraan kebersihan"

    ],

    "examples": [

        "Apa itu armada?",

        "Bagaimana menghitung armada?",

        "Berapa truk yang dibutuhkan?",

        "Apa itu ritase?",

        "Apa itu trip?",

        "Apa itu pool?",

        "Bagaimana jika armada tidak cukup?",

        "Bagaimana menghitung kapasitas armada?"

    ],

    "objectives": [

        "Mengelola data armada pengangkut sampah.",

        "Menghitung kebutuhan armada berdasarkan volume sampah.",

        "Mengetahui kapasitas total armada yang tersedia.",

        "Membantu perencanaan operasional harian.",

        "Mendukung pengambilan keputusan distribusi armada."

    ],

    "features": [

        "Input jumlah armada tersedia.",

        "Input armada siap beroperasi.",

        "Input kapasitas truk.",

        "Perhitungan kebutuhan armada.",

        "Estimasi ritase (trip) yang diperlukan.",

        "Rekomendasi operasional armada."

    ],

    "workflow": [

        "Operator memasukkan jumlah armada.",

        "Operator menentukan kapasitas setiap truk.",

        "Sistem menerima hasil prediksi volume sampah.",

        "EcoRoute AI menghitung jumlah armada yang diperlukan.",

        "Sistem membandingkan kebutuhan armada dengan armada yang tersedia.",

        "Sistem menampilkan rekomendasi operasional."

    ],

    "concepts": {

        "armada":
            "Sekumpulan kendaraan pengangkut sampah yang digunakan dalam proses operasional.",

        "kapasitas":
            "Jumlah maksimum sampah yang dapat diangkut oleh satu kendaraan dalam satu perjalanan.",

        "ritase":
            "Jumlah perjalanan bolak-balik yang dilakukan satu kendaraan dalam satu hari.",

        "trip":
            "Satu kali perjalanan pengangkutan sampah dari TPS menuju TPST.",

        "pool":
            "Lokasi atau depo tempat armada disimpan sebelum beroperasi."

    },

    "calculation": {

        "required_trucks":
            """
Jumlah armada dihitung berdasarkan volume sampah yang diprediksi
dibagi kapasitas angkut setiap truk.
""",

        "formula":
            "Jumlah Armada = Volume Sampah ÷ Kapasitas Truk",

        "notes":
            "Jika hasil perhitungan bukan bilangan bulat maka jumlah armada dibulatkan ke atas."

    },

    "display_information": {

        "available_trucks":
            "Jumlah armada yang tersedia.",

        "ready_trucks":
            "Jumlah armada yang siap digunakan.",

        "required_trucks":
            "Estimasi jumlah armada yang dibutuhkan.",

        "truck_capacity":
            "Kapasitas angkut setiap armada.",

        "trip_estimation":
            "Estimasi jumlah ritase."

    },

    "recommendations": [

        "Tambahkan armada apabila kebutuhan melebihi armada siap operasi.",

        "Gunakan sistem ritase apabila jumlah armada terbatas.",

        "Prioritaskan armada menuju wilayah dengan volume sampah tertinggi.",

        "Lakukan pemeriksaan kendaraan sebelum operasi.",

        "Distribusikan armada berdasarkan hasil prediksi AI.",

        "Gunakan bantuan armada dari wilayah lain apabila diperlukan."

    ],

    "benefits": [

        "Mengoptimalkan distribusi armada.",

        "Mengurangi risiko kekurangan kendaraan.",

        "Mempermudah perencanaan operasional.",

        "Menghemat biaya operasional.",

        "Mendukung keputusan berbasis data."

    ],

    "faq": {

        "apa itu armada":
            "Armada adalah kumpulan kendaraan pengangkut sampah yang digunakan dalam proses pengelolaan sampah.",

        "apa fungsi armada":
            "Armada digunakan untuk mengangkut sampah dari TPS menuju TPST atau tempat pengolahan.",

        "bagaimana menghitung armada":
            "Jumlah armada dihitung dari volume sampah yang diprediksi dibagi kapasitas angkut setiap truk.",

        "apa itu ritase":
            "Ritase adalah jumlah perjalanan yang dilakukan kendaraan dalam satu hari.",

        "apa itu trip":
            "Trip adalah satu kali perjalanan pengangkutan sampah.",

        "apa itu pool":
            "Pool merupakan lokasi tempat armada diparkir sebelum beroperasi.",

        "apa itu kapasitas truk":
            "Kapasitas truk adalah jumlah maksimum sampah yang dapat diangkut dalam satu perjalanan.",

        "bagaimana jika armada kurang":
            "Sistem dapat menyarankan penambahan ritase atau bantuan armada dari wilayah lain.",

        "mengapa armada penting":
            "Karena armada menentukan kemampuan sistem dalam mengangkut seluruh volume sampah secara tepat waktu."

    },

    "related_topics": [

        "Dashboard",

        "Event Simulator",

        "Routing",

        "Machine Learning",

        "Waste Management"

    ]

}