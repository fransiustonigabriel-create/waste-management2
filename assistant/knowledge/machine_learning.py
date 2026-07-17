MACHINE_LEARNING = {

    # =====================================================
    # Basic Information
    # =====================================================

    "title": "Machine Learning",

    "description": """
Machine Learning merupakan inti dari EcoRoute AI yang digunakan
untuk memprediksi volume timbulan sampah berdasarkan pola pada
data historis.

EcoRoute AI membandingkan Linear Regression, Random Forest,
dan XGBoost. Berdasarkan hasil evaluasi proyek, XGBoost menjadi
model dengan performa terbaik karena menghasilkan nilai MAE dan
RMSE paling rendah serta nilai R² paling tinggi.

Hasil prediksi digunakan untuk mendukung simulasi, perhitungan
kebutuhan armada, analisis dashboard, dan rekomendasi operasional.

Sistem juga memiliki anomaly detection untuk mengidentifikasi
input yang berbeda dari pola data training.
""".strip(),

    # =====================================================
    # Retrieval Fields
    # =====================================================

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
        "linear regression",
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
        "r²",
        "evaluasi model",
        "perbandingan model",
        "model terbaik",
        "performa model",
    ],

    "aliases": [
        "model prediksi",
        "predictive model",
        "ml model",
        "algoritma prediksi",
        "ensemble learning",
        "model ai",
        "sistem prediksi",
        "model volume sampah",
        "model terbaik",
    ],

    "examples": [
        "Model apa yang digunakan?",
        "Apa itu XGBoost?",
        "Apa itu Random Forest?",
        "Apa itu Linear Regression?",
        "Mengapa XGBoost lebih baik dibanding Random Forest?",
        "Model mana yang memiliki performa terbaik?",
        "Bagaimana perbandingan hasil model?",
        "Mengapa XGBoost dipilih sebagai model utama?",
        "Bagaimana model melakukan prediksi?",
        "Apa arti MAE?",
        "Apa arti RMSE?",
        "Apa arti R²?",
        "Apa itu anomaly detection?",
        "Bagaimana cara melatih ulang model?",
    ],

    # =====================================================
    # Fields Used by Local Answer and Prompt Builder
    # =====================================================

    "concepts": {

        "Linear Regression": (
            "Linear Regression adalah model dasar yang mempelajari "
            "hubungan linear antara fitur input dan volume sampah. "
            "Model ini mudah dijelaskan, tetapi kurang optimal untuk "
            "pola data yang kompleks dan non-linear."
        ),

        "Random Forest": (
            "Random Forest menggabungkan banyak Decision Tree. "
            "Setiap tree menghasilkan prediksi dan hasil akhirnya "
            "diperoleh dari gabungan seluruh tree. Model ini relatif "
            "stabil serta dapat memberikan feature importance."
        ),

        "XGBoost": (
            "XGBoost adalah algoritma Gradient Boosting yang membangun "
            "model secara bertahap. Setiap model baru berusaha "
            "memperbaiki kesalahan model sebelumnya. XGBoost memiliki "
            "performa tinggi pada data tabular dan mampu menangani "
            "hubungan non-linear."
        ),

        "Ensemble Learning": (
            "Ensemble Learning menggabungkan hasil beberapa model untuk "
            "memperoleh prediksi yang lebih stabil dan mengurangi "
            "kelemahan apabila hanya menggunakan satu model."
        ),

        "MAE": (
            "Mean Absolute Error adalah rata-rata selisih absolut "
            "antara hasil prediksi dan nilai aktual. Semakin kecil "
            "MAE, semakin kecil rata-rata kesalahan model."
        ),

        "RMSE": (
            "Root Mean Squared Error memberikan penalti lebih besar "
            "pada kesalahan prediksi yang besar. Semakin kecil RMSE, "
            "semakin baik performa model."
        ),

        "R²": (
            "R² menunjukkan kemampuan model dalam menjelaskan variasi "
            "target. Nilai yang semakin mendekati 1 menunjukkan "
            "performa yang semakin baik."
        ),

        "Feature Importance": (
            "Feature Importance menunjukkan seberapa besar kontribusi "
            "suatu fitur terhadap hasil prediksi model."
        ),

        "Anomaly Detection": (
            "Anomaly Detection digunakan untuk memeriksa apakah input "
            "pengguna masih berada dalam pola data training. Input yang "
            "sangat berbeda dapat ditandai sebagai anomali."
        ),
    },

    "features": [
        "Prediksi volume timbulan sampah.",
        "Perbandingan performa beberapa model Machine Learning.",
        "Evaluasi menggunakan MAE, RMSE, dan R².",
        "Deteksi input yang berbeda dari pola data training.",
        "Feature importance untuk mengetahui fitur berpengaruh.",
        "Dukungan prediksi harian dan simulasi event.",
        "Integrasi hasil prediksi dengan dashboard dan armada.",
    ],

    "workflow": [
        "Dataset dimuat dan diperiksa.",
        "Data dibersihkan dan disiapkan.",
        "Fitur dan target volume sampah dipisahkan.",
        "Data kategori diubah menjadi fitur numerik.",
        "Data dibagi menjadi training set dan testing set.",
        "Linear Regression dilatih sebagai model pembanding dasar.",
        "Random Forest dilatih dan dievaluasi.",
        "XGBoost dilatih dan dievaluasi.",
        "Performa model dibandingkan menggunakan MAE, RMSE, dan R².",
        "Model dengan performa terbaik dipilih.",
        "Model, encoder, scaler, dan struktur fitur disimpan.",
        "Model digunakan untuk melakukan inference pada aplikasi.",
    ],

    # =====================================================
    # Actual Project Metrics
    # =====================================================

    "metrics": {
        "Makna MAE": (
            "Semakin kecil nilainya, semakin kecil rata-rata "
            "kesalahan absolut prediksi."
        ),

        "Makna RMSE": (
            "Semakin kecil nilainya, semakin rendah kesalahan "
            "prediksi, terutama pada error yang besar."
        ),

        "Makna R²": (
            "Semakin tinggi dan semakin mendekati 1, semakin baik "
            "model menjelaskan variasi volume sampah."
        ),

        "Model dengan MAE terendah": (
            "XGBoost dengan MAE 41,763.92."
        ),

        "Model dengan RMSE terendah": (
            "XGBoost dengan RMSE 68,916.86."
        ),

        "Model dengan R² tertinggi": (
            "XGBoost dengan R² 0.9354."
        ),

        "Model utama EcoRoute AI": (
            "XGBoost dipilih sebagai model utama berdasarkan "
            "hasil evaluasi pada testing set."
        ),
    },

    "model_comparison": {
        "Linear Regression": (
            "MAE 68,154.18; RMSE 108,482.94; R² 0.8399. "
            "Model ini menjadi baseline dan memiliki performa "
            "paling rendah dari tiga model yang dibandingkan."
        ),

        "Random Forest": (
            "MAE 49,622.52; RMSE 86,852.82; R² 0.8974. "
            "Performanya lebih baik dibanding Linear Regression, "
            "tetapi masih berada di bawah XGBoost."
        ),

        "XGBoost": (
            "MAE 41,763.92; RMSE 68,916.86; R² 0.9354. "
            "Model ini memiliki MAE dan RMSE paling rendah serta "
            "R² paling tinggi sehingga dipilih sebagai model terbaik."
        ),

        "Kesimpulan": (
            "XGBoost merupakan model terbaik pada evaluasi proyek "
            "EcoRoute AI. Dibanding Random Forest, XGBoost menurunkan "
            "MAE sekitar 7,858.60, menurunkan RMSE sekitar 17,935.96, "
            "dan meningkatkan R² sekitar 0.0380."
        ),
    },

    # =====================================================
    # Original Rich Knowledge
    # =====================================================

    "objectives": [
        "Memprediksi volume sampah.",
        "Meningkatkan akurasi estimasi.",
        "Membantu perencanaan armada.",
        "Mendukung simulasi harian dan event.",
        "Mendeteksi input yang tidak wajar.",
        "Mendukung pengambilan keputusan berbasis data.",
    ],

    "models": {

        "linear_regression": """
Linear Regression digunakan sebagai baseline untuk membandingkan
performa model yang lebih kompleks. Model ini menghasilkan MAE
68,154.18, RMSE 108,482.94, dan R² 0.8399.
""".strip(),

        "random_forest": """
Random Forest menggabungkan banyak Decision Tree dan relatif stabil
untuk data tabular. Model ini menghasilkan MAE 49,622.52,
RMSE 86,852.82, dan R² 0.8974.
""".strip(),

        "xgboost": """
XGBoost menggunakan pendekatan Gradient Boosting untuk memperbaiki
kesalahan model secara bertahap. Model ini menghasilkan MAE
41,763.92, RMSE 68,916.86, dan R² 0.9354. Berdasarkan ketiga metrik
tersebut, XGBoost menjadi model terbaik pada proyek EcoRoute AI.
""".strip(),

        "ensemble": """
Ensemble Learning dapat menggabungkan hasil prediksi dari XGBoost
dan Random Forest untuk memperoleh hasil yang lebih stabil.
""".strip(),

        "anomaly_detector": """
Anomaly Detector memeriksa apakah input pengguna masih berada dalam
pola data training. Jika input terlalu berbeda dari pola normal,
sistem memberikan status anomali.
""".strip(),
    },

    "input_features": [
        "Kota Administrasi",
        "Zona Wilayah",
        "Latitude",
        "Longitude",
        "Kepadatan Penduduk",
        "Hari dalam Minggu",
        "Hari dalam Bulan",
        "Bulan",
        "Tahun",
        "Status Akhir Pekan",
        "Musim",
        "Cuaca",
        "Suhu Udara",
        "Kelembapan",
        "Curah Hujan",
        "Status Event",
        "Jumlah Pengunjung Event",
    ],

    "target": {
        "name": "Volume Sampah",
        "unit": "Kilogram",
        "description": (
            "Volume timbulan sampah yang diprediksi berdasarkan "
            "fitur input."
        ),
    },

    "prediction_pipeline": [
        "Input data diterima dari pengguna.",
        "Input divalidasi.",
        "Data kategori diubah menjadi nilai numerik.",
        "Urutan fitur disesuaikan dengan struktur saat training.",
        "Anomaly detector memeriksa kewajaran input.",
        "Model menghasilkan prediksi volume sampah.",
        "Hasil negatif dibatasi menjadi minimum nol.",
        "Hasil ditampilkan dalam kilogram atau ton.",
        "Prediksi diteruskan ke modul aplikasi terkait.",
    ],

    "training_pipeline": [
        "Dataset dimuat.",
        "Data dibersihkan.",
        "Fitur dan target dipisahkan.",
        "Data kategori dikodekan.",
        "Data dibagi menjadi training dan testing.",
        "Linear Regression dilatih sebagai baseline.",
        "Random Forest dilatih.",
        "XGBoost dilatih.",
        "Model dievaluasi menggunakan MAE, RMSE, dan R².",
        "Model terbaik dipilih.",
        "Encoder, scaler, struktur kolom, dan model disimpan.",
    ],

    "evaluation_metrics": {

        "mae": (
            "Mean Absolute Error adalah rata-rata selisih absolut "
            "antara prediksi dan nilai aktual."
        ),

        "rmse": (
            "Root Mean Squared Error memberikan penalti lebih besar "
            "pada kesalahan yang besar."
        ),

        "r2": (
            "R² menunjukkan kemampuan model dalam menjelaskan "
            "variasi target."
        ),

        "feature_importance": (
            "Feature Importance menunjukkan kontribusi suatu fitur "
            "terhadap hasil prediksi."
        ),
    },

    "feature_importance": {
        "population_density": (
            "Fitur paling dominan pada Random Forest dengan nilai "
            "importance sekitar 0.635374."
        ),
        "season_Kemarau": (
            "Salah satu fitur penting dengan nilai importance "
            "sekitar 0.117511 pada Random Forest."
        ),
        "event_visitors": (
            "Jumlah pengunjung event ikut berkontribusi terhadap "
            "prediksi volume sampah."
        ),
    },

    "advantages": [
        "Cocok untuk data tabular.",
        "Mampu menangani hubungan non-linear.",
        "Dapat membandingkan beberapa model.",
        "XGBoost memberikan performa evaluasi terbaik.",
        "Random Forest dapat memberikan feature importance.",
        "Dapat digunakan untuk prediksi harian dan event.",
        "Model dapat dilatih ulang jika dataset diperbarui.",
    ],

    "limitations": [
        "Akurasi bergantung pada kualitas dataset.",
        "Model dapat mengalami penurunan performa jika pola data berubah.",
        "Input yang sangat berbeda dari data training dapat kurang andal.",
        "Prediksi tetap memiliki tingkat kesalahan.",
        "Model perlu dievaluasi dan dilatih ulang secara berkala.",
        "Hasil model tidak menggantikan keputusan operator lapangan.",
    ],

    "recommendations": [
        "Gunakan data terbaru untuk proses training.",
        "Evaluasi model setelah dataset diperbarui.",
        "Bandingkan MAE, RMSE, dan R² sebelum memilih model.",
        "Gunakan XGBoost sebagai model utama berdasarkan evaluasi saat ini.",
        "Gunakan Ensemble jika membutuhkan prediksi yang lebih stabil.",
        "Periksa status anomali sebelum menggunakan hasil prediksi.",
        "Gunakan hasil prediksi sebagai pendukung keputusan.",
    ],

    # =====================================================
    # FAQ
    # =====================================================

    "faq": {

        "apa itu machine learning": (
            "Machine Learning adalah teknologi yang mempelajari "
            "pola dari data untuk menghasilkan prediksi."
        ),

        "model apa yang digunakan": (
            "EcoRoute AI membandingkan Linear Regression, "
            "Random Forest, dan XGBoost. Sistem juga mendukung "
            "Ensemble Learning."
        ),

        "apa itu linear regression": (
            "Linear Regression adalah model baseline yang mempelajari "
            "hubungan linear antara fitur dan target."
        ),

        "apa itu xgboost": (
            "XGBoost adalah algoritma Gradient Boosting yang memiliki "
            "performa tinggi pada data tabular."
        ),

        "apa itu random forest": (
            "Random Forest adalah algoritma yang menggabungkan "
            "banyak Decision Tree."
        ),

        "apa itu ensemble": (
            "Ensemble adalah teknik menggabungkan beberapa model "
            "agar hasil prediksi lebih stabil."
        ),

        "model mana yang terbaik": (
            "XGBoost menjadi model terbaik dengan MAE 41,763.92, "
            "RMSE 68,916.86, dan R² 0.9354."
        ),

        "mengapa xgboost lebih baik dibanding random forest": (
            "Pada evaluasi EcoRoute AI, XGBoost memiliki MAE dan "
            "RMSE lebih rendah serta R² lebih tinggi dibanding "
            "Random Forest."
        ),

        "mengapa xgboost dipilih": (
            "XGBoost dipilih karena memiliki MAE 41,763.92, "
            "RMSE 68,916.86, dan R² 0.9354, yang merupakan hasil "
            "terbaik dibanding model lain."
        ),

        "bagaimana model melakukan prediksi": (
            "Input dikodekan, disusun sesuai fitur training, lalu "
            "diberikan kepada model untuk menghasilkan prediksi."
        ),

        "apa itu preprocessing": (
            "Preprocessing adalah proses membersihkan dan menyiapkan "
            "data sebelum digunakan oleh model."
        ),

        "apa itu encoding": (
            "Encoding adalah proses mengubah data kategori menjadi "
            "nilai numerik."
        ),

        "apa itu feature importance": (
            "Feature Importance menunjukkan fitur yang paling "
            "berpengaruh terhadap hasil prediksi."
        ),

        "apa itu mae": (
            "MAE adalah rata-rata kesalahan absolut antara prediksi "
            "dan nilai aktual."
        ),

        "apa itu rmse": (
            "RMSE adalah ukuran kesalahan yang memberi penalti lebih "
            "besar pada error besar."
        ),

        "apa itu r2": (
            "R² menunjukkan seberapa baik model menjelaskan "
            "variasi target."
        ),

        "apa itu anomaly detection": (
            "Anomaly Detection digunakan untuk mendeteksi input "
            "yang berbeda dari pola data normal."
        ),

        "apakah model dapat dilatih ulang": (
            "Ya, model dapat dilatih ulang menggunakan dataset terbaru."
        ),

        "apakah hasil prediksi selalu benar": (
            "Tidak. Hasil prediksi adalah estimasi dan tetap memiliki "
            "tingkat kesalahan."
        ),

        "mengapa model perlu dilatih ulang": (
            "Pola data dapat berubah sehingga model perlu diperbarui "
            "agar tetap relevan."
        ),
    },

    "related_topics": [
        "Dashboard",
        "Simulator",
        "Armada",
        "Routing",
        "Waste Management",
    ],
}