# File: Model/src/inference.py
import os
import joblib
import pandas as pd

def predict_waste_volume(input_data: dict, model_type='ensemble'):
    """
    Fungsi untuk memprediksi volume sampah berdasarkan input data baru.
    
    Args:
        input_data (dict): Data situasi hari yang ingin diprediksi
        model_type (str): Pilihan model ('xgboost', 'random_forest', 'ensemble')
    """
    models_dir = "Model/models_output"
    
    # 1. Load Model, Encoder, dan Struktur Kolom yang sudah disimpan
    encoders = joblib.load(f"{models_dir}/label_encoders.pkl")
    feature_names = joblib.load(f"{models_dir}/feature_columns.pkl")
    anomaly_detector = joblib.load(f"{models_dir}/anomaly_detector.pkl")
    
    # Pilih model sesuai keinginan
    if model_type == 'xgboost':
        model = joblib.load(f"{models_dir}/xgboost.pkl")
    elif model_type == 'random_forest':
        model = joblib.load(f"{models_dir}/random_forest.pkl")
    else:
        model = joblib.load(f"{models_dir}/ensemble_model.pkl")
        
    # 2. Ubah input dictionary menjadi Pandas DataFrame
    df_input = pd.DataFrame([input_data])
    
    # 3. Transformasi data teks input menggunakan Label Encoder lama
    categorical_cols = ['zone', 'kota_adm', 'season', 'weather']
    for col in categorical_cols:
        if col in df_input.columns:
            le = encoders[col]
            val = df_input[col].iloc[0]
            # Antisipasi jika ada teks baru yang tidak dikenali model
            if val not in le.classes_:
                df_input[col] = le.transform([le.classes_[0]])[0]
            else:
                df_input[col] = le.transform([val])[0]
                
    # Pastikan urutan kolom input sama persis dengan urutan saat training
    df_input = df_input[feature_names]
    
    # 4. Deteksi Anomaly (Apakah input masuk akal atau ngawur?)
    is_anomaly = anomaly_detector.predict(df_input)[0] == -1
    
    # 5. Eksekusi Prediksi
    predicted_val = model.predict(df_input)[0]
    
    # Hasil prediksi tidak boleh minus
    final_prediction = max(0.0, float(predicted_val))
    
    return {
        'predicted_volume_kg': round(final_prediction, 2),
        'predicted_volume_tons': round(final_prediction / 1000, 2),
        'is_anomaly_input': is_anomaly,
        'model_used': model_type
    }