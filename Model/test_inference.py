# File: Model/test_inference.py
from src.inference import predict_waste_volume

# SKENARIO A: Hari biasa di Jakarta Selatan (Kebayoran Baru), Cuaca Cerah, TIDAK ADA ACARA
hari_biasa = {
    'kota_adm': 'Jakarta Selatan',
    'zone': 'urban',
    'population_density': 14800,
    'day_of_week': 2, # Selasa
    'month': 5,
    'is_weekend': 0,
    'season': 'Kemarau',
    'weather': 'Cerah',
    'temperature_c': 32.0,
    'humidity_pct': 65.0,
    'rainfall_mm': 0.0,
    'has_event': 0,
    'event_visitors': 0
}

# SKENARIO B: Ada Konser Musik Besar Besok di lokasi yang sama, Cuaca Hujan
hari_konser = {
    'kota_adm': 'Jakarta Selatan',
    'zone': 'urban',
    'population_density': 14800,
    'day_of_week': 5, # Sabtu
    'month': 5,
    'is_weekend': 1,
    'season': 'Kemarau',
    'weather': 'Hujan',
    'temperature_c': 27.0,
    'humidity_pct': 85.0,
    'rainfall_mm': 15.5, # Hujan lebat membuat sampah basah & berat
    'has_event': 1,      # ADA EVENT!
    'event_visitors': 25000 # 25 Ribu Pengunjung
}

print("="*60)
print("PENGUJIAN SIMULASI PREDIKSI LONJAKAN SAMPAH")
print("="*60)

# Jalankan prediksi dengan model Ensemble terbaik kita
hasil_biasa = predict_waste_volume(hari_biasa, model_type='ensemble')
hasil_konser = predict_waste_volume(hari_konser, model_type='ensemble')

print(f"\n[Skenario A - Hari Biasa Normal]")
print(f"  -> Prediksi Volume Sampah: {hasil_biasa['predicted_volume_kg']} Kg ({hasil_biasa['predicted_volume_tons']} Ton)")
print(f"  -> Input Terdeteksi Anomali? {hasil_biasa['is_anomaly_input']}")

print(f"\n[Skenario B - ADA KONSER BESAR & HUJAN]")
print(f"  -> Prediksi Volume Sampah: {hasil_konser['predicted_volume_kg']} Kg ({hasil_konser['predicted_volume_tons']} Ton)")
print(f"  -> Input Terdeteksi Anomali? {hasil_konser['is_anomaly_input']}")

print("\n" + "="*60)
# Hitung berapa kali lipat lonjakannya
kenaikan = (hasil_konser['predicted_volume_kg'] / hasil_biasa['predicted_volume_kg'])
print(f"🚨 KESIMPULAN: Sistem mendeteksi LONJAKAN SAMPAH sebesar {kenaikan:.2f}x lipat pada hari konser!")
print("="*60)