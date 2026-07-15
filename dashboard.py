import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import folium_static
from Model.src.inference import predict_waste_volume

st.header("Pemetaan Spasial & Temporal Timbulan Sampah")

# ==========================================
# 1. LOAD DATA & FITUR YANG DIBUTUHKAN MODEL
# ==========================================
FEATURE_COLS = ['kota_adm', 'zone', 'population_density', 'day_of_week', 'month',
                 'is_weekend', 'season', 'weather', 'temperature_c', 'humidity_pct',
                 'rainfall_mm', 'has_event', 'event_visitors']

try:
    # Memanggil dataset yang dipakai untuk melatih model (lihat Model/train_main.py)
    df_clean = pd.read_csv('Model/data/Data waste DKI Jakarta - Sheet1.csv')
except FileNotFoundError:
    st.error("⚠️ File Model atau Data tidak ditemukan. Pastikan Anda menjalankan ini dari folder utama (Waste Managment).")
    st.stop()


def prediksi_batch(df_sample, model_type='ensemble'):
    # predict_waste_volume hanya menerima satu baris input sekaligus,
    # jadi kita panggil untuk tiap baris sampel dan gabungkan hasilnya
    hasil_kg = [
        predict_waste_volume(row[FEATURE_COLS].to_dict(), model_type=model_type)['predicted_volume_kg']
        for _, row in df_sample.iterrows()
    ]
    return np.array(hasil_kg)

# ==========================================
# 2. PROSES PREDIKSI HARI INI
# ==========================================
# Untuk demonstrasi "Hari Ini", kita ambil 5 sampel acak dari data kita
# Di dunia nyata, ini diganti dengan data sensor/input harian terbaru
df_today = df_clean.sample(5, random_state=42).copy()

# >>> AI MELAKUKAN PREDIKSI <<<
prediksi_kg = prediksi_batch(df_today)

# ==========================================
# 3. KALKULASI KPI UNTUK DASHBOARD
# ==========================================
total_sampah_kg = prediksi_kg.sum()
total_sampah_ton = total_sampah_kg / 1000

# Kalkulasi Armada & Man-hours (Asumsi 1 Truk = 6 Ton, 1 Shift = 4 Jam)
kebutuhan_truk = int(np.ceil(total_sampah_ton / 6))
kebutuhan_jam_kerja = kebutuhan_truk * 4

# Menampilkan KPI di layar
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
col_kpi1.metric("Total Prediksi Sampah (Hari Ini)", f"{total_sampah_ton:.1f} Ton")
col_kpi2.metric("Estimasi Kebutuhan Armada", f"{kebutuhan_truk} Truk")
col_kpi3.metric("Kebutuhan Tenaga Lapangan", f"{kebutuhan_jam_kerja} Jam Kerja")

st.divider()

# ==========================================
# 4. PEMETAAN SPASIAL (MAP)
# ==========================================
col_map, col_chart = st.columns([1.5, 1])

with col_map:
    st.subheader("📍 Peta Spasial Area Sibuk (Prediksi AI)")
    
    # Koordinat pusat Jakarta
    m = folium.Map(location=[-6.200000, 106.816666], zoom_start=11)
    
    # Kamus koordinat wilayah untuk mengganti latitude/longitude yang dibuang
    koordinat_wilayah = {
        "Jakarta Pusat": [-6.18, 106.82],
        "Jakarta Selatan": [-6.26, 106.81],
        "Jakarta Barat": [-6.16, 106.74],
        "Jakarta Timur": [-6.22, 106.90],
        "Jakarta Utara": [-6.12, 106.89]
    }

    # Memetakan hasil tebakan AI ke dalam Peta
    for i, (idx, row) in enumerate(df_today.iterrows()):
        nama_kota = row['kota_adm']
        volume_prediksi_ton = prediksi_kg[i] / 1000
        lokasi = koordinat_wilayah.get(nama_kota, [-6.20, 106.81])
        
        # Tentukan warna peringatan
        color = "red" if volume_prediksi_ton > 300 else "orange" if volume_prediksi_ton > 150 else "green"
        
        folium.CircleMarker(
            location=lokasi,
            radius=volume_prediksi_ton / 15, # Ukuran lingkaran menyesuaikan volume sampah
            popup=f"<b>{nama_kota}</b><br>Prediksi: {volume_prediksi_ton:.1f} Ton",
            color=color, fill=True, fill_color=color
        ).add_to(m)
        
    folium_static(m, width=650, height=400)
    st.caption("🔴 > 300 Ton | 🟠 150-300 Ton | 🟢 < 150 Ton")
    
# ==========================================
# 5. TREN TEMPORAL (GRAFIK)
# ==========================================
with col_chart:
    st.subheader("📈 Tren Temporal (Simulasi 7 Hari)")
    
    # Menggunakan AI untuk menebak 7 hari ke depan (mengambil 7 sampel)
    df_week = df_clean.sample(7, random_state=99).copy()
    prediksi_mingguan = prediksi_batch(df_week) / 1000 # Jadikan Ton
    
    dates = pd.date_range(start=pd.Timestamp.today(), periods=7).strftime('%Y-%m-%d')
    df_trend = pd.DataFrame({"Tanggal": dates, "Estimasi Tonase": prediksi_mingguan})
    
    fig = px.line(df_trend, x="Tanggal", y="Estimasi Tonase", markers=True, 
                  labels={"Estimasi Tonase": "Volume Sampah (Ton)"})
    st.plotly_chart(fig, use_container_width=True)