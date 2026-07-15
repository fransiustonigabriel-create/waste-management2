MACHINE_LEARNING = {

    "title": "Machine Learning",

    "description": """
Machine Learning merupakan inti dari EcoRoute AI yang digunakan untuk
memprediksi volume timbulan sampah berdasarkan pola pada data historis.

Sistem menggunakan model XGBoost, Random Forest, dan Ensemble Learning.
Hasil prediksi kemudian digunakan untuk mendukung simulasi, perhitungan
kebutuhan armada, analisis dashboard, dan rekomendasi operasional.

Selain prediksi, sistem juga menggunakan anomaly detection untuk
mengidentifikasi input yang berbeda dari pola data training.
""",

    "keywords": [

        "machine learning",
        "ai",
        "artificial intelligence",
        "kecerdasan buatan",
        "model",
        "algoritma",
        "prediksi",
        "prediction",
        "xgboost",
        "random forest",
        "ensemble",
        "training",
        "retraining",
        "inference",
        "preprocessing",
        "encoding",
        "feature",
        "feature importance",
        "anomaly detection",
        "akurasi",
        "mae",
        "rmse",
        "r2",
        "evaluasi model"

    ],

    "aliases": [

        "model prediksi",
        "predictive model",
        "ml model",
        "algoritma prediksi",
        "ensemble learning",
        "model ai",
        "sistem prediksi"

    ],

    "examples": [

        "Model apa yang digunakan?",

        "Apa itu XGBoost?",

        "Apa itu Random Forest?",

        "Mengapa menggunakan Ensemble?",

        "Bagaimana model melakukan prediksi?",

        "Apa arti MAE?",

        "Apa arti RMSE?",

        "Apa arti R²?",

        "Apa itu anomaly detection?",

        "Bagaimana cara melatih ulang model?"

    ],

    "objectives": [

        "Memprediksi volume sampah.",

        "Meningkatkan akurasi estimasi.",

        "Membantu perencanaan armada.",

        "Mendukung simulasi harian dan event.",

        "Mendeteksi input yang tidak wajar.",

        "Mendukung pengambilan keputusan berbasis data."

    ],

    "models": {

        "xgboost":
            """
XGBoost adalah algoritma Gradient Boosting yang membangun model secara
bertahap. Setiap model baru berusaha memperbaiki kesalahan model sebelumnya.
XGBoost memiliki performa tinggi untuk data tabular dan mampu menangani
hubungan non-linear.
""",

        "random_forest":
            """
Random Forest adalah algoritma yang menggabungkan banyak Decision Tree.
Setiap tree menghasilkan prediksi, lalu hasil akhirnya diperoleh dari
gabungan seluruh tree. Model ini relatif stabil dan dapat memberikan
informasi feature importance.
""",

        "ensemble":
            """
Ensemble Learning menggabungkan hasil prediksi dari XGBoost dan Random
Forest. Tujuannya adalah memperoleh hasil yang lebih stabil dan mengurangi
kelemahan apabila hanya menggunakan satu model.
""",

        "anomaly_detector":
            """
Anomaly Detector digunakan untuk memeriksa apakah input pengguna masih
berada dalam pola data training. Jika input terlalu berbeda dari pola normal,
sistem memberikan status anomali.
"""

    },

    "input_features": [

        "Kota Administrasi",

        "Zona Wilayah",

        "Kepadatan Penduduk",

        "Hari dalam Minggu",

        "Bulan",

        "Status Akhir Pekan",

        "Musim",

        "Cuaca",

        "Suhu Udara",

        "Kelembapan",

        "Curah Hujan",

        "Status Event",

        "Jumlah Pengunjung Event"

    ],

    "target": {

        "name":
            "Volume Sampah",

        "unit":
            "Kilogram dan ton",

        "description":
            "Nilai yang diprediksi model berdasarkan fitur input."

    },

    "prediction_pipeline": [

        "Input data diterima dari pengguna.",

        "Input divalidasi.",

        "Data kategori diubah menjadi nilai numerik menggunakan encoder.",

        "Urutan fitur disesuaikan dengan urutan saat training.",

        "Anomaly detector memeriksa kewajaran input.",

        "Model menghasilkan prediksi volume sampah.",

        "Hasil negatif dicegah dengan batas minimum nol.",

        "Hasil dikonversi menjadi kilogram dan ton.",

        "Prediksi dikirim ke antarmuka aplikasi."

    ],

    "training_pipeline": [

        "Dataset dimuat.",

        "Data dibersihkan.",

        "Fitur dan target dipisahkan.",

        "Data kategori dikodekan.",

        "Data dibagi menjadi training dan testing.",

        "Model XGBoost dilatih.",

        "Model Random Forest dilatih.",

        "Model Ensemble dibentuk.",

        "Model dievaluasi.",

        "Encoder, struktur kolom, dan model disimpan."

    ],

    "evaluation_metrics": {

        "mae":
            """
Mean Absolute Error adalah rata-rata selisih absolut antara prediksi dan
nilai aktual. Semakin kecil MAE, semakin kecil rata-rata kesalahan model.
""",

        "rmse":
            """
Root Mean Squared Error memberikan penalti lebih besar pada kesalahan yang
besar. Semakin kecil RMSE, semakin baik performa model.
""",

        "r2":
            """
R² Score menunjukkan kemampuan model menjelaskan variasi target.
Nilai yang mendekati 1 menunjukkan performa yang lebih baik.
""",

        "feature_importance":
            """
Feature Importance menunjukkan seberapa besar kontribusi suatu fitur
terhadap hasil prediksi model.
"""

    },

    "display_information": {

        "model_used":
            "Model yang digunakan untuk menghasilkan prediksi.",

        "predicted_volume":
            "Estimasi volume sampah dari model.",

        "anomaly_status":
            "Informasi apakah input termasuk normal atau anomali.",

        "evaluation_score":
            "Nilai evaluasi model seperti MAE, RMSE, dan R².",

        "feature_importance":
            "Fitur yang paling berpengaruh terhadap prediksi."

    },

    "advantages": [

        "Cocok untuk data tabular.",

        "Mampu menangani hubungan non-linear.",

        "Dapat membandingkan beberapa model.",

        "Ensemble menghasilkan prediksi lebih stabil.",

        "Dapat digunakan untuk prediksi harian dan event.",

        "Model dapat dilatih ulang jika dataset diperbarui."

    ],

    "limitations": [

        "Akurasi bergantung pada kualitas dataset.",

        "Model dapat mengalami penurunan performa jika pola data berubah.",

        "Input yang sangat berbeda dari data training dapat menghasilkan prediksi kurang andal.",

        "Prediksi tetap memiliki tingkat kesalahan.",

        "Model perlu dievaluasi dan dilatih ulang secara berkala.",

        "Hasil model tidak menggantikan keputusan operator lapangan."

    ],

    "recommendations": [

        "Gunakan data terbaru untuk proses training.",

        "Evaluasi model setelah dataset diperbarui.",

        "Bandingkan MAE, RMSE, dan R² sebelum memilih model.",

        "Gunakan Ensemble jika membutuhkan prediksi yang lebih stabil.",

        "Periksa status anomali sebelum memakai hasil prediksi.",

        "Gunakan hasil prediksi sebagai pendukung keputusan."

    ],

    "faq": {

        "apa itu machine learning":
            "Machine Learning adalah teknologi yang mempelajari pola dari data untuk menghasilkan prediksi.",

        "model apa yang digunakan":
            "EcoRoute AI menggunakan XGBoost, Random Forest, dan Ensemble Learning.",

        "apa itu xgboost":
            "XGBoost adalah algoritma Gradient Boosting yang memiliki performa tinggi pada data tabular.",

        "apa itu random forest":
            "Random Forest adalah algoritma yang menggabungkan banyak Decision Tree.",

        "apa itu ensemble":
            "Ensemble adalah teknik menggabungkan beberapa model agar hasil prediksi lebih stabil.",

        "mengapa menggunakan dua model":
            "Karena gabungan model dapat mengurangi kelemahan dari masing-masing model.",

        "bagaimana model melakukan prediksi":
            "Input dikodekan, disusun sesuai fitur training, lalu diberikan kepada model untuk menghasilkan prediksi.",

        "apa itu preprocessing":
            "Preprocessing adalah proses membersihkan dan menyiapkan data sebelum digunakan model.",

        "apa itu encoding":
            "Encoding adalah proses mengubah data kategori menjadi nilai numerik.",

        "apa itu feature importance":
            "Feature Importance menunjukkan fitur yang paling berpengaruh terhadap hasil prediksi.",

        "apa itu mae":
            "MAE adalah rata-rata kesalahan absolut antara prediksi dan nilai aktual.",

        "apa itu rmse":
            "RMSE adalah ukuran kesalahan yang memberi penalti lebih besar pada error besar.",

        "apa itu r2":
            "R² menunjukkan seberapa baik model menjelaskan variasi target.",

        "apa itu anomaly detection":
            "Anomaly Detection digunakan untuk mendeteksi input yang berbeda dari pola data normal.",

        "apakah model dapat dilatih ulang":
            "Ya, model dapat dilatih ulang menggunakan dataset terbaru.",

        "apakah hasil prediksi selalu benar":
            "Tidak. Hasil prediksi adalah estimasi dan tetap memiliki tingkat kesalahan.",

        "mengapa model perlu dilatih ulang":
            "Karena pola data dapat berubah sehingga model perlu diperbarui agar tetap relevan."

    },

    "related_topics": [

        "Dashboard",

        "Simulator",

        "Armada",

        "Routing",

        "Waste Management"

    ]

}