import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

def load_and_preprocess(data_path, test_size=0.2, random_state=42):
    print("Memuat dan membersihkan dataset...")
    df = pd.read_csv(data_path)
    
    # Membuang kolom yang tidak bisa dibaca mesin atau error
    df = df.drop(columns=['date', 'event_name', 'location'], errors='ignore')
    
    label_encoders = {}
    categorical_cols = ['zone', 'kota_adm', 'season', 'weather']
    
    # Transformasi Teks menjadi Angka
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = df[col].fillna('Unknown') 
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
        
    # Mendefinisikan Fitur (X) dan Target (y)
    feature_names = ['kota_adm', 'zone', 'population_density', 'day_of_week', 'month', 
                     'is_weekend', 'season', 'weather', 'temperature_c', 'humidity_pct', 
                     'rainfall_mm', 'has_event', 'event_visitors']
    
    X = df[feature_names]
    y = df['volume_kg']
    
    # Memisahkan data training dan testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # Mengembalikan data bersih dan nama fitur
    return X_train, X_test, y_train, y_test, feature_names, label_encoders