import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from src.preprocess import load_and_preprocess
from src.evaluate import calculate_metrics, print_metrics

"""Script pelatihan khusus untuk model Random Forest.
File ini fokus pada pelatihan model Random Forest untuk memprediksi target
berdasarkan fitur hasil preprocessing yang sudah disiapkan sebelumnya.
"""

def main():
    print("="*60)
    print(" ECO-ROUTE AI: TRAINING RANDOM FOREST MODEL")
    print("="*60)
    
    # Menentukan lokasi file data dan folder output model.
    data_path = "Model/data/Data waste DKI Jakarta - Sheet1.csv"
    models_dir = "Model/models_output"
    os.makedirs(models_dir, exist_ok=True)
    
    # 1. Preprocessing
    # Proses ini mempersiapkan data sebelum model dilatih, termasuk pembersihan data,
    # encoding fitur kategori, dan pembagian data menjadi latih serta uji.
    print("\n[STEP 1] PROSES ETL & PREPROCESSING")
    X_train, X_test, y_train, y_test, feature_names, encoders = load_and_preprocess(data_path)
    
    # Menyimpan hasil preprocessing supaya saat inferensi model dipakai nanti,
    # transformasi yang sama bisa diterapkan pada data baru.
    joblib.dump(encoders, f"{models_dir}/label_encoders.pkl")
    joblib.dump(feature_names, f"{models_dir}/feature_columns.pkl")
    
    # 2. Training Random Forest
    # Random Forest adalah kumpulan banyak decision tree yang bekerja bersama.
    # Model ini cocok untuk data tabular dan biasanya lebih stabil dibanding satu tree tunggal.
    print("\n[STEP 2] MELATIH RANDOM FOREST...")
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # 3. Evaluasi & Simpan
    # Setelah model dilatih, prediksi diuji menggunakan data uji untuk mengukur kualitasnya.
    # Hasil model lalu disimpan agar bisa dipakai kembali oleh aplikasi.
    rf_metrics = calculate_metrics(y_test, rf_model.predict(X_test))
    print_metrics(rf_metrics, "Random Forest")
    joblib.dump(rf_model, f"{models_dir}/random_forest.pkl")
    print("\n[OK] Random Forest berhasil dilatih dan disimpan!")

if __name__ == "__main__":
    main()