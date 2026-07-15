# Eco-Route AI: Sistem Prediksi Timbulan Sampah & Manajemen Armada

![Header](https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png)

Eco-Route AI adalah sebuah aplikasi berbasis web yang dirancang untuk membantu dinas kebersihan atau manajer operasional dalam mengelola sampah di wilayah perkotaan, khususnya DKI Jakarta. Sistem ini menggunakan model Machine Learning untuk memprediksi volume timbulan sampah dan memberikan rekomendasi strategis untuk optimalisasi armada truk pengangkut.

Aplikasi ini dibangun menggunakan **Streamlit** untuk antarmuka yang interaktif dan ditenagai oleh model **Ensemble (XGBoost + Random Forest)** untuk akurasi prediksi yang tinggi.

---

## 🚀 Fitur Utama

*   **📊 Dashboard Interaktif**: Visualisasi KPI utama seperti total prediksi sampah, estimasi kebutuhan armada, dan pemetaan spasial area dengan volume sampah tinggi menggunakan peta Folium.
*   **🎛️ Simulator Skenario Proaktif**:
    *   **Prediksi Harian**: Memasukkan parameter rutin (cuaca, hari, kepadatan penduduk) untuk mendapatkan prediksi volume sampah harian.
    *   **Simulasi Event**: Mensimulasikan dampak acara besar (konser, festival) terhadap lonjakan volume sampah dengan memasukkan estimasi pengunjung.
*   **🚛 Manajemen Armada**: Mengonfigurasi inventaris armada (jumlah total, unit siap pakai, kapasitas) yang menjadi dasar kalkulasi rekomendasi operasional.
*   **🤖 Pelatihan Model Mandiri (MLOps)**: Fitur untuk melatih ulang model AI langsung dari antarmuka web jika ada pembaruan dataset, memastikan model tetap relevan.
*   **📈 Analisis Dampak**: Grafik perbandingan visual antara kondisi normal dan kondisi saat ada event, memberikan gambaran jelas mengenai skala lonjakan sampah.
*   **📋 Rekomendasi Aksi**: Memberikan saran operasional yang jelas, seperti jumlah truk yang dibutuhkan, potensi penambahan jadwal angkut (trip/ritase), dan strategi pengerahan armada.

---

## 🛠️ Teknologi yang Digunakan

- **Frontend**: Streamlit
- **Machine Learning**: Scikit-learn, XGBoost
- **Analisis Data**: Pandas, Numpy
- **Visualisasi Data**: Plotly, Folium
- **Deployment**: (Lokal)

---

## 📂 Struktur Proyek

```
Waste Managment/
├── Model/
│   ├── data/
│   │   └── Data waste DKI Jakarta - Sheet1.csv  # Dataset utama
│   ├── models_output/                           # Folder output untuk file .pkl
│   ├── src/
│   │   ├── preprocess.py                        # Script untuk pemrosesan data
│   │   ├── evaluate.py                          # Script untuk evaluasi model
│   │   └── inference.py                         # Script untuk melakukan prediksi
│   ├── train_main.py                            # Script utama untuk melatih model ensemble
│   ├── train_xgboost.py                         # Script untuk melatih XGBoost saja
│   └── train_random_forest.py                   # Script untuk melatih Random Forest saja
│
├── App.py                                       # File utama untuk menjalankan aplikasi Streamlit
├── dashboard.py                                 # Halaman dashboard
├── simulator.py                                 # Halaman simulasi
├── armada.py                                    # Halaman manajemen armada
├── summary.py                                   # Halaman ringkasan eksekutif
├── requirements.txt                             # Daftar pustaka Python yang dibutuhkan
└── README.md                                    # Anda sedang membacanya
```

---

## ⚙️ Instalasi dan Cara Menjalankan

Ikuti langkah-langkah berikut untuk menjalankan aplikasi ini di komputer lokal Anda.

### 1. Prasyarat

Pastikan Anda sudah menginstal **Python 3.8 atau versi lebih baru**.

### 2. Setup Lingkungan

a. **Clone Repositori (Jika ada di Git)**
   ```bash
   git clone <URL_REPOSITORI_ANDA>
   cd "Waste Managment"
   ```
   Jika tidak, cukup navigasikan ke folder `c:\Waste Managment` Anda.

b. **Buat dan Aktifkan Virtual Environment (Sangat Direkomendasikan)**
   ```bash
   # Buat environment
   python -m venv venv

   # Aktifkan di Windows
   .\venv\Scripts\activate

   # Aktifkan di macOS/Linux
   source venv/bin/activate
   ```

c. **Instal Semua Pustaka yang Dibutuhkan**
   Gunakan file `requirements.txt` yang sudah disediakan.
   ```bash
   pip install -r requirements.txt
   ```

### 3. Langkah Menjalankan Aplikasi

**PENTING**: Sebelum menjalankan aplikasi web, Anda harus melatih model terlebih dahulu agar file-file `.pkl` yang dibutuhkan tersedia.

a. **Langkah 1: Latih Model AI**
   Jalankan script `train_main.py` dari terminal. Script ini akan memproses data dan menyimpan semua model yang diperlukan ke dalam folder `Model/models_output/`.
   ```bash
   python "Model/train_main.py"
   ```

b. **Langkah 2: Jalankan Aplikasi Streamlit**
   Setelah model berhasil dilatih, jalankan aplikasi utama.
   ```bash
   streamlit run App.py
   ```
   Aplikasi akan otomatis terbuka di browser default Anda. Selamat! Anda sekarang bisa mulai menggunakan Eco-Route AI.