SIMULATOR = {

    "title": "Event Simulator",

    "description": """
Event Simulator adalah modul EcoRoute AI yang digunakan untuk melakukan
simulasi prediksi volume sampah berdasarkan kondisi harian maupun event.

Modul ini membantu pengguna memperkirakan jumlah sampah yang akan dihasilkan
pada suatu wilayah, membandingkan kondisi normal dengan kondisi event, serta
menghitung kebutuhan armada berdasarkan hasil prediksi.

Prediksi dilakukan menggunakan model Machine Learning yang telah dilatih
menggunakan data historis pengelolaan sampah DKI Jakarta.
""",

    "keywords": [

        "simulator",
        "event simulator",
        "simulasi",
        "prediksi",
        "forecast",
        "event",
        "acara",
        "pengunjung",
        "volume sampah",
        "estimasi",
        "skenario",
        "daily prediction",
        "event prediction",
        "what if",
        "analisis dampak"

    ],

    "aliases": [

        "scenario simulator",
        "simulasi acara",
        "prediksi event",
        "prediksi harian",
        "event prediction",
        "daily prediction",
        "what-if simulation",
        "simulasi skenario"

    ],

    "examples": [

        "Apa itu Event Simulator?",

        "Bagaimana simulasi event dilakukan?",

        "Apa saja input simulator?",

        "Apa output simulator?",

        "Bagaimana jika jumlah pengunjung bertambah?",

        "Bagaimana model memprediksi volume sampah?",

        "Apa perbedaan prediksi harian dan prediksi event?",

        "Bagaimana menghitung kebutuhan armada dari hasil simulasi?"

    ],

    "objectives": [

        "Memprediksi volume sampah harian.",

        "Mensimulasikan dampak event terhadap volume sampah.",

        "Menghitung estimasi kebutuhan armada.",

        "Membandingkan kondisi normal dan kondisi event.",

        "Memberikan rekomendasi operasional.",

        "Membantu pengambilan keputusan sebelum hari operasional."

    ],

    "features": [

        "Prediksi Harian Rutin.",

        "Simulasi Lonjakan Event.",

        "Pemilihan model Machine Learning.",

        "Grafik prediksi tujuh hari.",

        "Perbandingan kondisi normal dan kondisi event.",

        "Rekomendasi armada per wilayah.",

        "Deteksi input anomali.",

        "Pelatihan ulang model."

    ],

    "input_parameters": {

        "kota_adm":
            "Wilayah administrasi yang akan diprediksi.",

        "zone":
            "Karakteristik zona seperti urban, komersial, wisata, atau pemerintahan.",

        "population_density":
            "Kepadatan penduduk pada wilayah tersebut.",

        "date":
            "Tanggal prediksi atau tanggal pelaksanaan event.",

        "day_of_week":
            "Indeks hari dalam satu minggu.",

        "month":
            "Bulan pelaksanaan prediksi.",

        "is_weekend":
            "Penanda apakah tanggal termasuk akhir pekan.",

        "season":
            "Musim yang digunakan sebagai fitur model.",

        "weather":
            "Kondisi cuaca pada saat prediksi.",

        "temperature_c":
            "Suhu udara dalam derajat Celsius.",

        "humidity_pct":
            "Persentase kelembapan udara.",

        "rainfall_mm":
            "Curah hujan dalam milimeter.",

        "has_event":
            "Penanda apakah terdapat event khusus.",

        "event_visitors":
            "Estimasi jumlah pengunjung event."

    },

    "outputs": {

        "predicted_volume_kg":
            "Estimasi volume sampah dalam kilogram.",

        "predicted_volume_tons":
            "Estimasi volume sampah dalam ton.",

        "required_trucks":
            "Estimasi jumlah armada yang dibutuhkan.",

        "weekly_chart":
            "Visualisasi prediksi tujuh hari untuk mode harian.",

        "event_comparison":
            "Perbandingan antara kondisi normal dan kondisi event.",

        "anomaly_status":
            "Status apakah input berada di luar pola data normal.",

        "recommendation":
            "Saran operasional berdasarkan hasil prediksi."

    },

    "workflow": [

        "Pengguna memilih mode Prediksi Harian atau Simulasi Event.",

        "Pengguna mengisi parameter yang dibutuhkan.",

        "Sistem melakukan validasi input.",

        "Data kategori dikodekan menggunakan encoder model.",

        "Model Machine Learning menghasilkan prediksi.",

        "Hasil prediksi dikonversi ke kilogram dan ton.",

        "Sistem menghitung kebutuhan armada.",

        "Grafik dan rekomendasi operasional ditampilkan."

    ],

    "prediction_process": [

        "Input Data",

        "Data Validation",

        "Feature Encoding",

        "Feature Ordering",

        "Anomaly Detection",

        "Model Prediction",

        "Post Processing",

        "Visualization",

        "Operational Recommendation"

    ],

    "simulation_modes": {

        "daily":
            """
Mode Prediksi Harian digunakan untuk memperkirakan volume sampah pada
kondisi rutin tanpa event khusus. Hasil dapat ditampilkan dalam bentuk
prediksi harian, mingguan, dan bulanan.
""",

        "event":
            """
Mode Simulasi Event digunakan untuk memperkirakan lonjakan volume sampah
akibat adanya acara dengan jumlah pengunjung tertentu.
"""
    },

    "display_information": {

        "daily_prediction":
            "Prediksi volume sampah harian.",

        "weekly_prediction":
            "Akumulasi atau rincian prediksi selama tujuh hari.",

        "monthly_prediction":
            "Estimasi akumulasi volume sampah bulanan.",

        "normal_event_comparison":
            "Perbandingan volume hari normal dan hari event.",

        "anomaly_indicator":
            "Indikator apakah input dianggap tidak wajar oleh model.",

        "fleet_recommendation":
            "Jumlah armada dan ritase yang direkomendasikan."

    },

    "recommendations": [

        "Tambahkan armada jika hasil prediksi meningkat.",

        "Siapkan armada cadangan saat event besar.",

        "Lakukan pengangkutan lebih awal pada wilayah dengan volume tinggi.",

        "Gunakan ritase tambahan jika armada siap tidak mencukupi.",

        "Minta bantuan wilayah tetangga jika kapasitas total wilayah tidak cukup.",

        "Bandingkan hasil kondisi normal dan event sebelum menentukan strategi.",

        "Gunakan hasil prediksi sebagai pendukung keputusan, bukan satu-satunya dasar keputusan."

    ],

    "benefits": [

        "Membantu mengantisipasi lonjakan volume sampah.",

        "Mempermudah perencanaan armada.",

        "Membantu membandingkan beberapa skenario.",

        "Mengurangi risiko kekurangan kendaraan.",

        "Mendukung keputusan operasional berbasis data.",

        "Mempermudah komunikasi hasil prediksi melalui grafik."

    ],

    "limitations": [

        "Hasil prediksi tetap memiliki tingkat kesalahan.",

        "Akurasi bergantung pada kualitas data training.",

        "Input yang sangat berbeda dari pola data dapat ditandai sebagai anomali.",

        "Prediksi tidak menggantikan keputusan operator lapangan.",

        "Model perlu dilatih ulang jika pola data berubah secara signifikan."

    ],

    "faq": {

        "apa itu simulator":
            "Simulator digunakan untuk memperkirakan volume sampah berdasarkan skenario tertentu.",

        "apa itu event simulator":
            "Event Simulator menghitung dampak suatu event terhadap kenaikan volume sampah.",

        "apa fungsi simulator":
            "Simulator membantu perencanaan operasional sebelum hari pelaksanaan.",

        "apa yang diprediksi":
            "Simulator memprediksi volume sampah, kebutuhan armada, dan status anomali input.",

        "bagaimana prediksi dilakukan":
            "Input diproses, dikodekan, lalu diberikan kepada model Machine Learning.",

        "mengapa perlu simulasi":
            "Simulasi membantu mengantisipasi lonjakan sampah sebelum benar-benar terjadi.",

        "apa output simulator":
            "Output berupa volume sampah, kebutuhan armada, grafik, status anomali, dan rekomendasi.",

        "apa perbedaan daily dan event":
            "Mode daily digunakan untuk kondisi rutin, sedangkan mode event memperhitungkan dampak jumlah pengunjung.",

        "bagaimana menghitung kebutuhan armada":
            "Kebutuhan armada dihitung dari prediksi volume sampah dibagi kapasitas per truk.",

        "apa itu anomaly detection":
            "Anomaly detection digunakan untuk menandai input yang berbeda dari pola data training.",

        "apakah model bisa dilatih ulang":
            "Ya, simulator menyediakan fitur pelatihan ulang model melalui antarmuka aplikasi.",

        "apakah hasil prediksi selalu benar":
            "Tidak. Hasil prediksi adalah estimasi dan tetap memiliki tingkat kesalahan."

    },

    "related_topics": [

        "Machine Learning",

        "Dashboard",

        "Armada",

        "Routing",

        "Waste Management"

    ]

}