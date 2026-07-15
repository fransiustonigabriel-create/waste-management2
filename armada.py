import streamlit as st
import pandas as pd
import datetime

st.header("🚛 Master Data & Manajemen Armada Truk")
st.markdown("Kelola total aset armada per wilayah, pantau status penugasan rute, dan jam operasional setiap unit.")

# Indikator Waktu Real-time
waktu_sekarang = datetime.datetime.now().strftime('%d %B %Y - %H:%M WIB')
st.caption(f"🕒 **Update Terakhir:** {waktu_sekarang}")

# ===============================================================
# 1. KONFIGURASI DAN INJEKSI DETAIL DATA TRUK PER WILAYAH
# ===============================================================
WILAYAH_CONFIG = {
    "Jakarta Selatan": {
        "pool": "Pool Pesanggrahan (Jl. Deplu Raya)", 
        "total": 50, "ready": 45, "cap": 8.0, "jam_operasi": "01.00 – 04.30 WIB",
        "rute_list": ["Standby", "Maintenance (Bengkel)", "Rute Harian", "Rute Event"]
    },
    "Jakarta Timur": {
        "pool": "Pool Pinang Ranti (Jl. Asem Nirbaya)", 
        "total": 75, "ready": 60, "cap": 8.0, "jam_operasi": "23.00 – 02.00 WIB",
        "rute_list": ["Standby", "Maintenance (Bengkel)", "Rute Harian", "Rute Event"]
    },
    "Jakarta Utara": {
        "pool": "Pool Pluit (Jl. Pluit Raya)", 
        "total": 50, "ready": 40, "cap": 8.0, "jam_operasi": "Malam – Subuh",
        "rute_list": ["Standby", "Maintenance (Bengkel)", "Rute Harian", "Rute Event"]
    },
    "Jakarta Barat": {
        "pool": "Pool Bambu Larangan (Kalideres)", 
        "total": 62, "ready": 50, "cap": 8.0, "jam_operasi": "02.00 – 05.00 WIB",
        "rute_list": ["Standby", "Maintenance (Bengkel)", "Rute Harian", "Rute Event"]
    },
    "Jakarta Pusat": {
        "pool": "Pool Rawasari (Cempaka Putih)", 
        "total": 40, "ready": 32, "cap": 8.0, "jam_operasi": "Sebelum 05.00 WIB",
        "rute_list": ["Standby", "Maintenance (Bengkel)", "Rute Harian", "Rute Event"]
    }
}

# Inisialisasi awal session state
if 'fleet_per_wilayah' not in st.session_state:
    st.session_state.fleet_per_wilayah = {}

for kota, cfg in WILAYAH_CONFIG.items():
    if kota not in st.session_state.fleet_per_wilayah or 'df_trucks' not in st.session_state.fleet_per_wilayah[kota]:
        truck_rows = []
        kode_wilayah = kota.split()[1][:3].upper()
        
        for i in range(1, cfg["total"] + 1):
            if i <= cfg["ready"]:
                status = cfg["rute_list"][2] if i % 2 == 0 else cfg["rute_list"][0]
            else:
                status = cfg["rute_list"][1]
                
            truck_rows.append({
                "No. Lambung": f"TRK-{kode_wilayah}-{i:02d}",
                "Status / Rute Penugasan": status,
                "Jam Operasi": cfg["jam_operasi"], # INFO JAM DITAMBAHKAN
                "Kapasitas (Ton)": cfg["cap"],
                "BBM (%)": 100 if status == "Standby" else (0 if status == "Maintenance (Bengkel)" else 70)
            })
            
        st.session_state.fleet_per_wilayah[kota] = {
            'pool': cfg['pool'],
            'total_trucks': cfg['total'],
            'trucks_ready': cfg['ready'],
            'capacity_per_truck': cfg['cap'],
            'fuel_tank_capacity': 100,
            'avg_consumption': 0.2,
            'df_trucks': pd.DataFrame(truck_rows)
        }

# ===============================================================
# 2. SELEKSI WILAYAH OPERASIONAL
# ===============================================================
st.markdown("### 📍 Pilih Wilayah Kendali Master Data")
wilayah_terpilih = st.selectbox("Kota Administrasi Operasional:", list(WILAYAH_CONFIG.keys()))

data_aktif = st.session_state.fleet_per_wilayah[wilayah_terpilih]
rute_opsi = WILAYAH_CONFIG[wilayah_terpilih]["rute_list"]
jam_default = WILAYAH_CONFIG[wilayah_terpilih]["jam_operasi"]

# ===============================================================
# 3. FORM INPUT MASTER DATA
# ===============================================================
st.markdown("---")
st.subheader(f"⚙️ Form Update Master Data: {wilayah_terpilih}")
with st.container():
    with st.form("master_fleet_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            input_total_truk = st.number_input("Total Aset Unit Truk di Wilayah", min_value=1, value=int(data_aktif['total_trucks']), help="Mengubah angka ini akan menambah/mengurangi baris manifest truk secara otomatis.")
            capacity_per_truck = st.number_input("Kapasitas Muatan per Unit (Ton)", min_value=1.0, value=data_aktif['capacity_per_truck'], format="%.1f")
            
        with col2:
            fuel_tank = st.number_input("Kapasitas Tangki BBM (Liter)", min_value=10, value=data_aktif.get('fuel_tank_capacity', 100))
            consumption = st.number_input("Konsumsi BBM Rata-rata (Liter/Km)", min_value=0.01, value=data_aktif.get('avg_consumption', 0.2), format="%.2f")
        
        submitted = st.form_submit_button("Simpan & Sinkronisasikan Master Data")
        
        if submitted:
            df_lama = data_aktif['df_trucks']
            jumlah_lama = len(df_lama)
            kode_wilayah = wilayah_terpilih.split()[1][:3].upper()
            
            # LOGIKA JIKA TRUK BERTAMBAH
            if input_total_truk > jumlah_lama:
                new_rows = []
                for i in range(jumlah_lama + 1, input_total_truk + 1):
                    new_rows.append({
                        "No. Lambung": f"TRK-{kode_wilayah}-{i:02d}",
                        "Status / Rute Penugasan": "Standby",
                        "Jam Operasi": jam_default, # Masukkan info jam untuk unit baru
                        "Kapasitas (Ton)": capacity_per_truck,
                        "BBM (%)": 100
                    })
                df_baru = pd.concat([df_lama, pd.DataFrame(new_rows)], ignore_index=True)
            
            # LOGIKA JIKA TRUK BERKURANG
            elif input_total_truk < jumlah_lama:
                df_baru = df_lama.head(input_total_truk).copy()
                df_baru["Kapasitas (Ton)"] = capacity_per_truck 
            
            else:
                df_baru = df_lama.copy()
                df_baru["Kapasitas (Ton)"] = capacity_per_truck
            
            bengkel_unit = len(df_baru[df_baru["Status / Rute Penugasan"] == "Maintenance (Bengkel)"])
            ready_unit = input_total_truk - int(bengkel_unit)
            
            st.session_state.fleet_per_wilayah[wilayah_terpilih] = {
                'pool': data_aktif['pool'],
                'total_trucks': input_total_truk,
                'trucks_ready': ready_unit,
                'capacity_per_truck': capacity_per_truck,
                'fuel_tank_capacity': fuel_tank,
                'avg_consumption': consumption,
                'df_trucks': df_baru
            }
            st.toast(f"Master data {wilayah_terpilih} berhasil direstrukturisasi menjadi {input_total_truk} unit!", icon="✅")
            st.rerun()

st.markdown("---")

# ===============================================================
# 4. INTERACTIVE DATA EDITOR (Manifest Unit)
# ===============================================================
st.subheader(f"📋 Manifest Detail Penugasan Unit: {wilayah_terpilih}")
st.caption("💡 *Info: Anda tetap bisa mengubah detail status harian/bensin masing-masing unit secara spesifik di tabel bawah ini.*")

# Siapkan kolom agar seragam dengan `map_route.py` (sinkronisasi nama kolom)
df_truk_sekarang = data_aktif['df_trucks']
if "Rute Penugasan Detail" not in df_truk_sekarang.columns:
    df_truk_sekarang["Rute Penugasan Detail"] = rute_opsi[0] if len(rute_opsi) > 0 else ""
if "Status Tracking" not in df_truk_sekarang.columns:
    df_truk_sekarang["Status Tracking"] = "🟢 Standby di Pool"
if "Jam Operasi" not in df_truk_sekarang.columns:
    df_truk_sekarang["Jam Operasi"] = jam_default

# Tampilkan kolom manifest agar sama dengan tampilan Dispatch di map_route,
# tetapi tetap menampilkan kolom master `Status / Rute Penugasan` untuk
# menentukan apakah unit berada di Maintenance atau Standby.
cols_to_show = ["No. Lambung", "Status / Rute Penugasan", "Rute Penugasan Detail", "Jam Operasi", "Kapasitas (Ton)"]
for c in cols_to_show:
    if c not in df_truk_sekarang.columns:
        df_truk_sekarang[c] = ""

df_truk_diedit = st.data_editor(
    df_truk_sekarang[cols_to_show],
    column_config={
        "No. Lambung": st.column_config.TextColumn("No. Lambung", disabled=True),
        "Status / Rute Penugasan": st.column_config.SelectboxColumn(
            "Status / Rute Penugasan",
            options=rute_opsi,
            required=True
        ),
        "Rute Penugasan Detail": st.column_config.SelectboxColumn("Lokasi Rute", options=list(df_truk_sekarang["Rute Penugasan Detail"].unique()) if df_truk_sekarang["Rute Penugasan Detail"].nunique()>0 else rute_opsi, required=True),
        "Jam Operasi": st.column_config.TextColumn("Waktu Shift", required=True),
        "Kapasitas (Ton)": st.column_config.NumberColumn("Kapasitas (Ton)", format="%.1f Ton", disabled=True),
    },
    hide_index=True,
    use_container_width=True,
    key=f"editor_{wilayah_terpilih}"
)

# Terapkan perubahan kembali ke DataFrame master (`df_truk_sekarang`) berdasarkan index
try:
    for idx in df_truk_diedit.index:
        for col in df_truk_diedit.columns:
            df_truk_sekarang.at[idx, col] = df_truk_diedit.at[idx, col]
except Exception:
    # fallback: jika index berubah, sinkronkan by No. Lambung
    try:
        for _, row in df_truk_diedit.reset_index(drop=True).iterrows():
            no = row["No. Lambung"]
            mask = df_truk_sekarang["No. Lambung"] == no
            for col in df_truk_diedit.columns:
                df_truk_sekarang.loc[mask, col] = row[col]
    except Exception:
        pass

# Hitung ulang metrik live pasca interaksi tabel editor (menggunakan master DF)
total_unit = len(df_truk_sekarang)
bengkel_hitung = int(len(df_truk_sekarang[df_truk_sekarang["Status / Rute Penugasan"] == "Maintenance (Bengkel)"]))
standby_hitung = int(len(df_truk_sekarang[df_truk_sekarang["Status / Rute Penugasan"] == "Standby"]))
ready_hitung = total_unit - bengkel_hitung
jalan_hitung = int(len(df_truk_sekarang[~df_truk_sekarang["Status / Rute Penugasan"].isin(["Standby", "Maintenance (Bengkel)"])]))

# Sinkronisasi balik ke state global
st.session_state.fleet_per_wilayah[wilayah_terpilih]['df_trucks'] = df_truk_sekarang
st.session_state.fleet_per_wilayah[wilayah_terpilih]['total_trucks'] = total_unit
st.session_state.fleet_per_wilayah[wilayah_terpilih]['trucks_ready'] = ready_hitung

# ===============================================================
# 5. METRIK MONITORING LIVE
# ===============================================================
total_kapasitas_ton = ready_hitung * data_aktif['capacity_per_truck']
jangkauan_km = data_aktif['fuel_tank_capacity'] / data_aktif['avg_consumption']
persentase_kesiapan = (ready_hitung / total_unit) * 100 if total_unit > 0 else 0

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total Kapasitas Angkut", f"{total_kapasitas_ton:.1f} Ton")
with m2:
    st.metric("Radius Operasional Truk", f"{jangkauan_km:.0f} Km")
with m3:
    st.metric("Tingkat Kesiapan (Readiness)", f"{persentase_kesiapan:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)
s1, s2, s3 = st.columns(3)
s1.metric("🟢 Truk Standby", f"{standby_hitung} Unit")
s2.metric("🔵 Truk Jalan Operasional", f"{jalan_hitung} Unit")
s3.metric("🔴 Truk Rusak (Bengkel)", f"{bengkel_hitung} Unit")

st.progress(persentase_kesiapan / 100 if persentase_kesiapan <= 100 else 1.0)