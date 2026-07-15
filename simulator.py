import streamlit as st
import datetime
import math
import subprocess
import pandas as pd
import plotly.express as px  # Ditambahkan untuk membuat diagram
from Model.src.inference import predict_waste_volume
import event_store as ES

st.header("🎛️ Proactive Scenario Simulator")
st.markdown("Pilih mode simulasi: Prediksi rutinitas harian kota atau mitigasi lonjakan akibat acara besar.")
st.markdown("---")

# ==========================================
# DATA ARMADA PER WILAYAH (BARU)
# Estimasi proporsional dari total ~1.200 truk DKI berdasarkan
# luas wilayah, kepadatan, & volume sampah harian.
# Angka bebas kamu ubah sesuai data asli.
# ==========================================
ARMADA_WILAYAH = {
    "Jakarta Selatan": {"pool": "Pool Pesanggrahan (Jl. Deplu Raya)",   "trucks_ready": 45, "total_trucks": 56, "capacity_per_truck": 8.0},
    "Jakarta Timur":   {"pool": "Pool Pinang Ranti (Jl. Asem Nirbaya)", "trucks_ready": 60, "total_trucks": 75, "capacity_per_truck": 8.0},
    "Jakarta Utara":   {"pool": "Pool Pluit (Jl. Pluit Raya)",          "trucks_ready": 40, "total_trucks": 50, "capacity_per_truck": 8.0},
    "Jakarta Barat":   {"pool": "Pool Bambu Larangan (Kalideres)",      "trucks_ready": 50, "total_trucks": 62, "capacity_per_truck": 8.0},
    "Jakarta Pusat":   {"pool": "Pool Rawasari (Cempaka Putih)",        "trucks_ready": 32, "total_trucks": 40, "capacity_per_truck": 8.0},
}

# Wilayah tetangga (untuk bantuan armada kalau kekurangan berat)
TETANGGA = {
    "Jakarta Selatan": ["Jakarta Pusat", "Jakarta Timur"],
    "Jakarta Timur":   ["Jakarta Pusat", "Jakarta Utara"],
    "Jakarta Utara":   ["Jakarta Pusat", "Jakarta Barat"],
    "Jakarta Barat":   ["Jakarta Pusat", "Jakarta Utara"],
    "Jakarta Pusat":   ["Jakarta Selatan", "Jakarta Timur", "Jakarta Barat", "Jakarta Utara"],
}


def get_armada_wilayah(kota):
    """Ambil data armada untuk wilayah terpilih.
    Kalau armada.py sudah menyetel data per-wilayah di session_state
    (key: 'fleet_per_wilayah'), itu yang dipakai biar tetap nyambung.
    """
    default = ARMADA_WILAYAH.get(kota, ARMADA_WILAYAH["Jakarta Selatan"])
    if "fleet_per_wilayah" in st.session_state and kota in st.session_state.fleet_per_wilayah:
        return st.session_state.fleet_per_wilayah[kota]
    return default


# ==========================================
# FITUR: MLOps & KONFIGURASI MODEL
# ==========================================
with st.expander("⚙️ Konfigurasi Model ML & Training", expanded=False):
    st.markdown("**Pilih Mesin Inferensi:**")
    model_option = st.selectbox(
        "Model yang digunakan untuk prediksi:", 
        ["Ensemble (Default - Paling Akurat)", "XGBoost", "Random Forest"],
        index=0
    )
    
    model_map = {
        "Ensemble (Default - Paling Akurat)": "ensemble",
        "XGBoost": "xgboost",
        "Random Forest": "random_forest"
    }
    selected_model = model_map[model_option]
    
    st.markdown("---")
    st.markdown("**Pemeliharaan Model:**")
    st.info(f"Sistem akan melatih ulang model **{model_option}** berdasarkan dataset terbaru.")
    
    if st.button(f"🔄 Latih Ulang {model_option}"):
        with st.spinner(f"Sedang memproses training untuk {model_option}... Mohon tunggu."):
            try:
                import sys
                if selected_model == "xgboost":
                    script_to_run = "Model/train_xgboost.py"
                elif selected_model == "random_forest":
                    script_to_run = "Model/train_random_forest.py"
                else:
                    script_to_run = "Model/train_main.py" 

                result = subprocess.run([sys.executable, script_to_run], capture_output=True, text=True)
                
                if result.returncode == 0:
                    st.success(f"✅ Pelatihan selesai! Model {model_option} berhasil diperbarui.")
                    with st.expander("Lihat Log Terminal"):
                        st.code(result.stdout)
                else:
                    st.error(f"❌ Gagal melatih model {model_option}.")
                    with st.expander("Lihat Error Log"):
                        st.code(result.stderr)
            except Exception as e:
                st.error(f"Terjadi kesalahan sistem: {e}")

st.markdown("---")

# ==========================================
# FUNGSI UNTUK MERENDER UI HASIL (DIPERBARUI)
# ==========================================
def tampilkan_hasil_ui(volume_ton, tanggal, is_anomaly, model_used, mode_simulasi, base_input):
    st.markdown(f"### 📊 Hasil Prediksi (Mesin: {model_used.upper()})")
    
    # 1 & 2: LOGIKA TAMPILAN KPI BERDASARKAN MODE (DAILY vs EVENT)
    if mode_simulasi == "daily":
        c1, c2, c3 = st.columns(3)
        weekly_total = volume_ton * 7
        monthly_total = volume_ton * 30
        with c1:
            st.metric("Prediksi Harian", f"{volume_ton:.2f} ton")
        with c2:
            st.metric("Prediksi Mingguan", f"{weekly_total:.2f} ton")
        with c3:
            st.metric("Prediksi Bulanan", f"{monthly_total:.2f} ton")
            
        # DIAGRAM BAR UNTUK 7 HARI KE DEPAN
        st.markdown("#### Rincian Prediksi 7 Hari Ke Depan")
        days, vols = [], []
        for i in range(7):
            next_date = tanggal + datetime.timedelta(days=i)
            curr_input = base_input.copy()
            curr_input['day_of_week'] = next_date.weekday()
            curr_input['month'] = next_date.month
            curr_input['is_weekend'] = 1 if next_date.weekday() >= 5 else 0
            
            res = predict_waste_volume(curr_input, model_type=model_used)
            days.append(next_date.strftime("%a<br>%d/%m"))
            vols.append(res['predicted_volume_tons'])
            
        df_chart = pd.DataFrame({"Hari": days, "Volume (ton)": vols})
        fig = px.bar(df_chart, x="Hari", y="Volume (ton)", text="Volume (ton)", color_discrete_sequence=["#4A90E2"])
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(yaxis_title="Volume (ton)", xaxis_title="Hari", margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    elif mode_simulasi == "event":
        # HANYA 1 KPI UNTUK EVENT
        st.metric("Estimasi Total Sampah Event", f"{volume_ton:.2f} ton")
        
        # DIAGRAM PERBANDINGAN NORMAL VS EVENT
        st.markdown("#### Analisis Dampak Event")
        normal_input = base_input.copy()
        normal_input['has_event'] = 0
        normal_input['event_visitors'] = 0
        res_normal = predict_waste_volume(normal_input, model_type=model_used)
        vol_normal = res_normal['predicted_volume_tons']
        
        df_evt = pd.DataFrame({
            "Skenario": ["Hari Normal (Tanpa Event)", "Hari Event (Lonjakan)"],
            "Volume (ton)": [vol_normal, volume_ton]
        })
        fig_evt = px.bar(df_evt, x="Skenario", y="Volume (ton)", color="Skenario", text="Volume (ton)", 
                         color_discrete_map={"Hari Normal (Tanpa Event)": "#A0AEC0", "Hari Event (Lonjakan)": "#E53E3E"})
        fig_evt.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_evt.update_layout(yaxis_title="Volume (ton)", margin=dict(t=20, b=20), showlegend=False)
        st.plotly_chart(fig_evt, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if is_anomaly:
        st.error("Status anomali: Outlier Detected - Input exceeds normal patterns!")
    else:
        st.info("Status anomali: Input is within normal training patterns")

    st.markdown("---")

    # ==========================================
    # 3. REKOMENDASI ARMADA (SEKARANG PER WILAYAH)
    # ==========================================
    st.markdown("### 🚛 Rekomendasi Armada")

    # Ambil wilayah dari input, lalu ambil data armada wilayah tsb
    kota = base_input.get('kota_adm', 'Jakarta Selatan')
    armada = get_armada_wilayah(kota)

    unit_ready         = armada['trucks_ready']
    total_unit         = armada['total_trucks']
    kapasitas_per_truk = armada['capacity_per_truck']
    pool_name          = armada.get('pool', '-')

    # Info wilayah yang sedang dihitung
    st.info(f"📍 **Wilayah:** {kota}  |  🏁 **Pool:** {pool_name}")

    # KPI armada wilayah
    ka1, ka2, ka3 = st.columns(3)
    ka1.metric("Truk Siap (Ready)", f"{unit_ready} unit")
    ka2.metric("Total Armada Wilayah", f"{total_unit} unit")
    ka3.metric("Kapasitas / Truk", f"{kapasitas_per_truk:.0f} ton")

    truk_diperlukan = math.ceil(volume_ton / kapasitas_per_truk)

    # Logika Detail Bolak-balik (DIPERTAHANKAN dari versi Adrian)
    if truk_diperlukan > unit_ready and unit_ready > 0:
        jumlah_trip = math.ceil(truk_diperlukan / unit_ready)
        
        # Menghitung secara spesifik berapa truk yang harus jalan lagi
        truk_bolak_balik = truk_diperlukan % unit_ready
        if truk_bolak_balik == 0:
            truk_bolak_balik = unit_ready # Jika habis dibagi, berarti semua truk bolak-balik
            
        pesan_armada = f"⚠️ Kekurangan armada di {kota}! Hanya tersedia {unit_ready} unit ready."
        rekomendasi_aksi = f"Disarankan melakukan **{jumlah_trip} kali pengangkutan (trip)**. Terdapat otomatis **{truk_bolak_balik} unit truk** yang harus beroperasi bolak-balik (ritase tambahan) untuk menutupi kekurangan."
        status_color = "warning"
        pesan_bawah = f"💡 Prediksi volume {volume_ton:.2f} ton memerlukan {truk_diperlukan} unit. Karena hanya {unit_ready} unit yang siap di {kota}, maka {truk_bolak_balik} truk perlu melakukan pengangkutan bertahap."
        
    elif unit_ready == 0:
        jumlah_trip = 0
        pesan_armada = f"❌ Tidak ada unit yang tersedia untuk operasi di {kota}!"
        rekomendasi_aksi = "Segera lakukan perbaikan armada di bengkel."
        status_color = "error"
        pesan_bawah = "Operasional tidak dapat dijalankan tanpa unit armada yang siap."
    else:
        jumlah_trip = 1
        pesan_armada = f"✅ Armada {kota} mencukupi ({unit_ready} unit ready tersedia)."
        rekomendasi_aksi = "Armada mencukupi untuk sekali angkut."
        status_color = "success"
        pesan_bawah = f"💡 Armada {kota} ({unit_ready} unit ready) cukup untuk mengangkut {volume_ton:.2f} ton dalam satu putaran."
    
    tanggal_format = tanggal.strftime('%d %B %Y')
    
    st.markdown(f"**Rekomendasi untuk tanggal {tanggal_format}:**")
    
    st.markdown(f"""
    * **Jumlah Truk Diperlukan:** {truk_diperlukan} unit
    * **Status Armada:** {pesan_armada}
    * **Strategi Operasional:** {rekomendasi_aksi}
    """)
    
    if status_color == "warning":
        st.warning(pesan_bawah)
    elif status_color == "success":
        st.success(pesan_bawah)
    else:
        st.error(pesan_bawah)

    # ==========================================
    # BANTUAN WILAYAH TETANGGA (BARU)
    # Muncul kalau kebutuhan truk melebihi TOTAL armada wilayah
    # (bukan cuma yang ready) — artinya beban berat, perlu bantuan.
    # ==========================================
    if truk_diperlukan > total_unit:
        kekurangan = truk_diperlukan - total_unit
        st.markdown("---")
        st.markdown("#### 🤝 Bantuan Armada Wilayah Tetangga")
        st.error(
            f"Beban di **{kota}** melebihi total armada wilayah ({total_unit} unit). "
            f"Kekurangan **{kekurangan} unit** — disarankan minta bantuan dari wilayah tetangga."
        )
        tetangga = TETANGGA.get(kota, [])
        if tetangga:
            cols_t = st.columns(len(tetangga))
            for i, wil in enumerate(tetangga):
                data_t = ARMADA_WILAYAH.get(wil, {})
                spare = max(0, data_t.get("total_trucks", 0) - data_t.get("trucks_ready", 0))
                cols_t[i].metric(
                    wil,
                    f"{data_t.get('trucks_ready', 0)} ready",
                    help=f"Cadangan yang bisa dipinjam: ±{spare} unit dari {data_t.get('pool', '-')}"
                )
            st.caption("⚠️ Redistribusi armada antar wilayah dikoordinasikan via Command Center DLH DKI (Cililitan).")


# ==========================================
# STRUKTUR TABS
# ==========================================
tab_daily, tab_event = st.tabs(["📅 Prediksi Harian Rutin", "🎪 Simulasi Lonjakan Event"])

# --- TAB 1: PREDIKSI HARIAN ---
with tab_daily:
    st.subheader("Parameter Harian Normal")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        kota_d = st.selectbox("Kota Administrasi", ["Jakarta Selatan", "Jakarta Barat", "Jakarta Pusat", "Jakarta Timur", "Jakarta Utara"], key="kota_d")
        zone_d = st.selectbox("Karakteristik Zona", ["urban", "komersial", "pemerintahan", "industri", "wisata"], key="zone_d")
        pop_density_d = st.slider("Kepadatan Penduduk", 5000, 50000, 15000, 1000, key="pop_d")
        
    with col2:
        date_d = st.date_input("Tanggal", datetime.date.today(), key="date_d")
        weather_d = st.selectbox("Cuaca", ["Cerah", "Berawan", "Hujan", "Hujan Lebat"], key="wea_d")
        temp_d = st.slider("Suhu Udara (°C)", 24.0, 36.0, 32.0, key="temp_d")
        
    with col3:
        hum_d = st.slider("Kelembaban (%)", 50.0, 100.0, 65.0, key="hum_d")
        rain_d = st.number_input("Curah Hujan (mm)", 0.0, 150.0, 0.0, key="rain_d")
        
    if st.button("🚀 Kalkulasi Harian", type="primary", use_container_width=True, key="btn_daily"):
        input_daily = {
            'kota_adm': kota_d, 'zone': zone_d, 'population_density': pop_density_d,
            'day_of_week': date_d.weekday(), 'month': date_d.month, 'is_weekend': 1 if date_d.weekday() >= 5 else 0,
            'season': "Kemarau" if date_d.month in [4,5,6,7,8,9] else "Berawan", 
            'weather': weather_d, 'temperature_c': temp_d,
            'humidity_pct': hum_d, 'rainfall_mm': rain_d,
            'has_event': 0, 'event_visitors': 0
        }
        hasil_d = predict_waste_volume(input_daily, model_type=selected_model)
        # Mengirimkan mode "daily" dan base input untuk diagram 7 hari
        tampilkan_hasil_ui(hasil_d['predicted_volume_tons'], date_d, hasil_d['is_anomaly_input'], selected_model, "daily", input_daily)

# --- TAB 2: PREDIKSI EVENT ---
with tab_event:
    st.subheader("Parameter Event Khusus")
    col1_e, col2_e, col3_e = st.columns(3)
    
    with col1_e:
        nama_event = st.text_input("Nama Event", "Pekan Raya Jakarta ")
        kota_e = st.selectbox("Lokasi Penyelenggaraan", ["Jakarta Barat", "Jakarta Pusat", "Jakarta Selatan", "Jakarta Timur", "Jakarta Utara"], key="kota_e")
        visitors_e = st.number_input("Estimasi Pengunjung", 1000, 500000, 100000, 1000, key="vis_e")
        
    with col2_e:
        zone_e = st.selectbox("Karakteristik Zona", ["wisata", "komersial", "urban", "pemerintahan", "industri"], key="zone_e")
        date_e = st.date_input("Tanggal Event", datetime.date.today(), key="date_e")
        weather_e = st.selectbox("Cuaca Saat Event", ["Cerah", "Berawan", "Hujan", "Hujan Lebat"], key="wea_e")
        
    with col3_e:
        jam_e = st.time_input("Jam Event", datetime.time(9, 0), key="jam_e")
        temp_e = st.slider("Suhu Udara (°C)", 24.0, 36.0, 32.0, key="temp_e")
        rain_e = st.number_input("Curah Hujan (mm)", 0.0, 150.0, 0.0, key="rain_e")

    if st.button(f"🚀 Prediksi Dampak {nama_event}", type="primary", use_container_width=True, key="btn_event"):
        input_event = {
            'kota_adm': kota_e, 'zone': zone_e, 'population_density': 15000,
            'day_of_week': date_e.weekday(), 'month': date_e.month, 'is_weekend': 1 if date_e.weekday() >= 5 else 0,
            'season': "Kemarau" if date_e.month in [4,5,6,7,8,9] else "Berawan",
            'weather': weather_e, 'temperature_c': temp_e,
            'humidity_pct': 65.0, 'rainfall_mm': rain_e,
            'has_event': 1, 'event_visitors': visitors_e
        }
        hasil_e = predict_waste_volume(input_event, model_type=selected_model)
        # Mengirimkan mode "event" dan base input untuk diagram perbandingan
        tampilkan_hasil_ui(hasil_e['predicted_volume_tons'], date_e, hasil_e['is_anomaly_input'], selected_model, "event", input_event)

        # Simpan hasil prediksi ke session biar bisa disimpan ke Jadwal Event
        vol_pred = hasil_e['predicted_volume_tons']
        st.session_state.event_prediksi = {
            "tanggal": date_e.strftime("%Y-%m-%d"),
            "jam": jam_e.strftime("%H:%M"),
            "nama": nama_event.strip(),
            "lokasi": nama_event.strip() + " (" + kota_e + ")",
            "lat": ES.WILAYAH_CENTROID.get(kota_e, (-6.2, 106.8))[0],
            "lng": ES.WILAYAH_CENTROID.get(kota_e, (-6.2, 106.8))[1],
            "pengunjung": int(visitors_e),
            "wilayah": kota_e,
            "volume_ton": round(float(vol_pred), 1),
            "truk": math.ceil(float(vol_pred) / 8.0),
            "sumber": "simulator",
        }

    # ── Simpan ke Jadwal Event (nyambung ke halaman Peta Event)
    if st.session_state.get("event_prediksi"):
        ep = st.session_state.event_prediksi
        st.divider()
        st.markdown("#### 📅 Simpan ke Jadwal Event")
        st.caption(f"Event **{ep['nama']}** — {ep['tanggal']} {ep['jam']} · {ep['wilayah']} · "
                   f"{ep['pengunjung']:,} pengunjung · prediksi {ep['volume_ton']} ton / {ep['truk']} truk")
        if st.button("💾 Simpan Event Ini ke Jadwal", key="save_event"):
            ok = ES.save_event(dict(ep))
            if ok:
                st.success(f"✅ Event '{ep['nama']}' tersimpan! Buka halaman **Rute Armada → tab Peta Event**, "
                           f"pilih tanggal **{ep['tanggal']}**, event-nya bakal muncul.")
                st.session_state.pop("event_prediksi", None)
            else:
                st.error("Gagal menyimpan event.")