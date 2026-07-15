import os
import sys
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, VotingRegressor, IsolationForest
from xgboost import XGBRegressor

"""Script pelatihan utama untuk membangun model ensemble.
Tujuan utamanya adalah mempersiapkan data, melatih beberapa model dasar,
membuat model gabungan (ensemble), melatih anomaly detector, lalu
menyimpan semua artefak model agar bisa dipakai oleh dashboard atau sistem inferensi.
"""

# Mengambil fungsi dari folder src
from src.preprocess import load_and_preprocess
from src.evaluate import calculate_metrics, print_metrics

def main():
    print("="*60)
    print(" ECO-ROUTE AI: PIPELINE PELATIHAN ENSEMBLE MODEL")
    print("="*60)
    
    # 1. Setup Direktori
    # Menentukan lokasi file data input dan folder tempat menyimpan model hasil pelatihan.
    # Folder output dibuat otomatis agar proses training bisa berjalan berulang tanpa error.
    data_path = "Model/data/Data waste DKI Jakarta - Sheet1.csv"
    models_dir = "Model/models_output"
    os.makedirs(models_dir, exist_ok=True)
    
    # 2. Data Preprocessing (Memanggil proses ETL dari file src/preprocess.py)
    # Langkah ini membersihkan data, mengubah fitur kategori menjadi angka, lalu membagi data
    # menjadi data latih dan data uji agar model bisa dievaluasi dengan objektif.
    print("\n[STEP 1] PROSES ETL & PREPROCESSING")
    X_train, X_test, y_train, y_test, feature_names, encoders = load_and_preprocess(data_path)
    
    # Menyimpan metadata hasil preprocessing agar saat inferensi nanti bisa dipakai lagi.
    # Encoder dibutuhkan untuk mengonversi fitur kategori yang sama, sedangkan feature_names
    # membantu memastikan urutan kolom tetap konsisten saat model dipakai.
    joblib.dump(encoders, f"{models_dir}/label_encoders.pkl")
    joblib.dump(feature_names, f"{models_dir}/feature_columns.pkl")
    
    # 3. Menyiapkan dan Melatih Base Models
    # Ensemble memerlukan model dasar yang kuat sebagai komponen pembangun.
    # Di sini Random Forest dan XGBoost dilatih terlebih dahulu agar hasil gabungannya lebih baik.
    print("\n[STEP 2 & 3] MELATIH RANDOM FOREST & XGBOOST SEBAGAI DASAR ENSEMBLE...")
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    
    # Melatih base models menggunakan data latih yang sama.
    rf_model.fit(X_train, y_train)
    xgb_model.fit(X_train, y_train)
    
    # Evaluasi base models untuk melihat performa masing-masing sebelum digabungkan.
    rf_metrics = calculate_metrics(y_test, rf_model.predict(X_test))
    xgb_metrics = calculate_metrics(y_test, xgb_model.predict(X_test))
    print_metrics(rf_metrics, "Random Forest Base")
    print_metrics(xgb_metrics, "XGBoost Base")

    # 4. Training Ensemble (Gabungan XGBoost + Random Forest)
    # VotingRegressor menggabungkan prediksi dari beberapa model sehingga hasil akhir
    # bisa lebih stabil dibanding satu model saja.
    print("\n[STEP 4] MELATIH VOTING ENSEMBLE (GABUNGAN)...")
    ensemble_model = VotingRegressor([('rf', rf_model), ('xgb', xgb_model)])
    ensemble_model.fit(X_train, y_train)
    
    # Mengevaluasi performa model gabungan agar bisa dibandingkan dengan model dasar.
    ens_metrics = calculate_metrics(y_test, ensemble_model.predict(X_test))
    print_metrics(ens_metrics, "Voting Ensemble Final")
    
    # 5. Training Anomaly Detector
    # IsolationForest digunakan untuk mendeteksi data yang tidak wajar atau outlier.
    # Model ini berguna untuk menemukan pola anomali yang mungkin tidak sesuai dengan data normal.
    print("\n[STEP 5] MELATIH ANOMALY DETECTOR...")
    detector = IsolationForest(contamination=0.03, random_state=42)
    detector.fit(X_train)
    print("  [OK] Model Anomaly Detector berhasil dilatih!")
    
    # 6. Simpan Semua Model
    # Semua model yang telah dilatih disimpan ke file .pkl agar bisa dipakai lagi nanti,
    # baik di dashboard, proses inferensi, maupun untuk keperluan evaluasi lanjutan.
    print("\n[STEP 6] MENYIMPAN SELURUH MODEL (.pkl) KE FOLDER 'models_output'...")
    joblib.dump(rf_model, f"{models_dir}/random_forest.pkl")
    joblib.dump(xgb_model, f"{models_dir}/xgboost.pkl")
    joblib.dump(ensemble_model, f"{models_dir}/ensemble_model.pkl")
    joblib.dump(detector, f"{models_dir}/anomaly_detector.pkl")
    
    print("\n" + "="*60)
    print(" PELATIHAN SELESAI! SEMUA MODEL SIAP DIPAKAI DI DASHBOARD.")
    print("="*60)

if __name__ == "__main__":
    main()