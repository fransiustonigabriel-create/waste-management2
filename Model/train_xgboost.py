import os
import joblib
from xgboost import XGBRegressor
from src.preprocess import load_and_preprocess
from src.evaluate import calculate_metrics, print_metrics

"""Script pelatihan khusus untuk model XGBoost.
Tujuan file ini adalah mempersiapkan data, melatih model XGBoost,
dan menyimpan hasil model beserta metadata preprocessing untuk dipakai nanti.
"""

def main():
    print("="*60)
    print(" ECO-ROUTE AI: TRAINING XGBOOST MODEL")
    print("="*60)
    
    # Menentukan lokasi file data input dan folder output model.
    data_path = "Model/data/Data waste DKI Jakarta - Sheet1.csv"
    models_dir = "Model/models_output"
    os.makedirs(models_dir, exist_ok=True)
    
    # 1. Preprocessing
    # Memanggil fungsi preprocessing untuk membersihkan data, mengkodekan fitur kategori,
    # dan membagi data menjadi data latih dan data uji.
    print("\n[STEP 1] PROSES ETL & PREPROCESSING")
    X_train, X_test, y_train, y_test, feature_names, encoders = load_and_preprocess(data_path)
    
    # Menyimpan encoder dan daftar fitur agar saat prediksi nanti urutan kolom tetap sesuai.
    joblib.dump(encoders, f"{models_dir}/label_encoders.pkl")
    joblib.dump(feature_names, f"{models_dir}/feature_columns.pkl")
    
    # 2. Training XGBoost
    # XGBoost adalah model boosted tree yang kuat untuk data tabular.
    # Model ini dilatih menggunakan data latih untuk belajar pola dari fitur yang ada.
    print("\n[STEP 2] MELATIH XGBOOST...")
    xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    xgb_model.fit(X_train, y_train)
    
    # 3. Evaluasi & Simpan
    # Setelah dilatih, model dievaluasi menggunakan data uji untuk melihat seberapa akurat prediksinya.
    # Hasil model kemudian disimpan agar bisa dipakai oleh aplikasi/dashboard.
    xgb_metrics = calculate_metrics(y_test, xgb_model.predict(X_test))
    print_metrics(xgb_metrics, "XGBoost")
    joblib.dump(xgb_model, f"{models_dir}/xgboost.pkl")
    print("\n[OK] XGBoost berhasil dilatih dan disimpan!")

if __name__ == "__main__":
    main()