import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import math
import pandas as pd
from datetime import datetime
import datetime as dt
import event_store as ES

# ───────────────────────────────────────────────────────────────
# ⚠️  PASTE API KEY TOMTOM
# ───────────────────────────────────────────────────────────────
TOMTOM_API_KEY = "API PASTE SINI"

BANTARGEBANG = {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023}

# ───────────────────────────────────────────────────────────────
# INISIALISASI MASTER DATA (SAFETY NET ANTI-ERROR SAAT GANTI PAGE)
# ───────────────────────────────────────────────────────────────
if 'fleet_per_wilayah' not in st.session_state:
    st.session_state.fleet_per_wilayah = {}

WILAYAH_CONFIG_INIT = {
    "Jakarta Selatan": {"pool": "Pool Pesanggrahan (Jl. Deplu Raya)", "total": 56, "ready": 45, "cap": 8.0, "jam_operasi": "01.00 – 04.30 WIB", "rute_list": ["Standby", "Maintenance (Bengkel)", "Rute Harian", "Rute Event"]},
    "Jakarta Timur": {"pool": "Pool Pinang Ranti (Jl. Asem Nirbaya)", "total": 75, "ready": 60, "cap": 8.0, "jam_operasi": "23.00 – 02.00 WIB", "rute_list": ["Standby", "Maintenance (Bengkel)", "Rute Harian", "Rute Event"]},
    "Jakarta Utara": {"pool": "Pool Pluit (Jl. Pluit Raya)", "total": 50, "ready": 40, "cap": 8.0, "jam_operasi": "Malam – Subuh", "rute_list": ["Standby", "Maintenance (Bengkel)", "Rute Harian", "Rute Event"]},
    "Jakarta Barat": {"pool": "Pool Bambu Larangan (Kalideres)", "total": 62, "ready": 50, "cap": 8.0, "jam_operasi": "02.00 – 05.00 WIB", "rute_list": ["Standby", "Maintenance (Bengkel)", "Rute Harian", "Rute Event"]},
    "Jakarta Pusat": {"pool": "Pool Rawasari (Cempaka Putih)", "total": 40, "ready": 32, "cap": 8.0, "jam_operasi": "Sebelum 05.00 WIB", "rute_list": ["Standby", "Maintenance (Bengkel)", "Rute Harian", "Rute Event"]}
}

# Jika data belum ada, buat otomatis di background
for kota, cfg in WILAYAH_CONFIG_INIT.items():
    if kota not in st.session_state.fleet_per_wilayah or 'df_trucks' not in st.session_state.fleet_per_wilayah[kota]:
        truck_rows = []
        kode_wilayah = kota.split()[1][:3].upper()
        for i in range(1, cfg["total"] + 1):
            status = cfg["rute_list"][2] if i % 2 == 0 else cfg["rute_list"][0] if i <= cfg["ready"] else cfg["rute_list"][1]
            truck_rows.append({
                "No. Lambung": f"TRK-{kode_wilayah}-{i:02d}",
                "Status / Rute Penugasan": status,
                "Jam Operasi": cfg["jam_operasi"],
                "Kapasitas (Ton)": cfg["cap"],
                "BBM (%)": 100 if status == "Standby" else (0 if status == "Maintenance (Bengkel)" else 70)
            })
        st.session_state.fleet_per_wilayah[kota] = {
            'pool': cfg['pool'], 'total_trucks': cfg['total'], 'trucks_ready': cfg['ready'],
            'capacity_per_truck': cfg['cap'], 'fuel_tank_capacity': 100, 'avg_consumption': 0.2,
            'df_trucks': pd.DataFrame(truck_rows)
        }

# ───────────────────────────────────────────────────────────────
# DATA RUTE HARIAN MULTIPEL (Maksimal 3 Rute per Wilayah)
# ───────────────────────────────────────────────────────────────
RUTE_DATA = {
    "Jakarta Selatan": {
        "warna": "#e74c3c", "jam_operasi": "01.00 – 04.30 WIB", "jenis_truk": "Compactor + Dump Truck",
        "rute": {
            "Rute 1 (Blok S - JORR)": [
                {"nama": "Pool Pesanggrahan", "lat": -6.2677, "lng": 106.7714, "tipe": "🏁 Pool", "keterangan": "START"},
                {"nama": "TPS Blok S", "lat": -6.2432, "lng": 106.8003, "tipe": "🗑️ TPS", "keterangan": "STOP 1"},
                {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023, "tipe": "🚩 AKHIR", "keterangan": "END"}
            ],
            "Rute 2 (Jagakarsa - JORR)": [
                {"nama": "Pool Pesanggrahan", "lat": -6.2677, "lng": 106.7714, "tipe": "🏁 Pool", "keterangan": "START"},
                {"nama": "TPS Antam Jagakarsa", "lat": -6.3351, "lng": 106.8318, "tipe": "🗑️ TPS", "keterangan": "STOP 1"},
                {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023, "tipe": "🚩 AKHIR", "keterangan": "END"}
            ],
            "Rute 3 (Tebet - Pancoran)": [
                {"nama": "Pool Kalibata", "lat": -6.2730, "lng": 106.8313, "tipe": "🏁 Pool", "keterangan": "START"},
                {"nama": "Dipo Ciliwung", "lat": -6.2422, "lng": 106.8622, "tipe": "🗑️ TPS", "keterangan": "STOP 1"},
                {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023, "tipe": "🚩 AKHIR", "keterangan": "END"}
            ]
        }
    },
    "Jakarta Timur": {
        "warna": "#e67e22", "jam_operasi": "23.00 – 02.00 WIB", "jenis_truk": "Arm Roll",
        "rute": {
            "Rute 1 (Pulogadung)": [
                {"nama": "Pool Pinang Ranti", "lat": -6.2885, "lng": 106.8830, "tipe": "🏁 Pool", "keterangan": "START"},
                {"nama": "TPS Pulogadung", "lat": -6.1936, "lng": 106.9003, "tipe": "🗑️ TPS", "keterangan": "STOP 1"},
                {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023, "tipe": "🚩 AKHIR", "keterangan": "END"}
            ],
            "Rute 2 (Kramat Jati)": [
                {"nama": "Pool Pinang Ranti", "lat": -6.2885, "lng": 106.8830, "tipe": "🏁 Pool", "keterangan": "START"},
                {"nama": "TPS Pasar Induk", "lat": -6.2774, "lng": 106.8727, "tipe": "🗑️ TPS", "keterangan": "STOP 1"},
                {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023, "tipe": "🚩 AKHIR", "keterangan": "END"}
            ],
            "Rute 3 (Duren Sawit)": [
                {"nama": "Pool Pinang Ranti", "lat": -6.2885, "lng": 106.8830, "tipe": "🏁 Pool", "keterangan": "START"},
                {"nama": "TPS Duren Sawit", "lat": -6.2325, "lng": 106.9059, "tipe": "🗑️ TPS", "keterangan": "STOP 1"},
                {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023, "tipe": "🚩 AKHIR", "keterangan": "END"}
            ]
        }
    },
    "Jakarta Utara": {
        "warna": "#3498db", "jam_operasi": "Malam – Subuh", "jenis_truk": "Dump Truck",
        "rute": {
            "Rute 1 (Pademangan)": [
                {"nama": "Pool Pluit", "lat": -6.1202, "lng": 106.7950, "tipe": "🏁 Pool", "keterangan": "START"},
                {"nama": "TPS Pademangan", "lat": -6.1350, "lng": 106.8320, "tipe": "🗑️ TPS", "keterangan": "STOP 1"},
                {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023, "tipe": "🚩 AKHIR", "keterangan": "END"}
            ],
            "Rute 2 (Kelapa Gading)": [
                {"nama": "Pool Pluit", "lat": -6.1202, "lng": 106.7950, "tipe": "🏁 Pool", "keterangan": "START"},
                {"nama": "TPS Kelapa Gading", "lat": -6.1550, "lng": 106.9100, "tipe": "🗑️ TPS", "keterangan": "STOP 1"},
                {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023, "tipe": "🚩 AKHIR", "keterangan": "END"}
            ]
        }
    },
    "Jakarta Barat": {
        "warna": "#9b59b6", "jam_operasi": "02.00 – 05.00 WIB", "jenis_truk": "Compactor",
        "rute": {
            "Rute 1 (Kalideres)": [
                {"nama": "Pool Bambu Larangan", "lat": -6.1313, "lng": 106.7046, "tipe": "🏁 Pool", "keterangan": "START"},
                {"nama": "TPS Kalideres", "lat": -6.1308, "lng": 106.7070, "tipe": "🗑️ TPS", "keterangan": "STOP 1"},
                {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023, "tipe": "🚩 AKHIR", "keterangan": "END"}
            ],
            "Rute 2 (Grogol)": [
                {"nama": "Pool Bambu Larangan", "lat": -6.1313, "lng": 106.7046, "tipe": "🏁 Pool", "keterangan": "START"},
                {"nama": "TPS Grogol Petamburan", "lat": -6.1677, "lng": 106.7930, "tipe": "🗑️ TPS", "keterangan": "STOP 1"},
                {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023, "tipe": "🚩 AKHIR", "keterangan": "END"}
            ],
            "Rute 3 (Tambora)": [
                {"nama": "Pool Bambu Larangan", "lat": -6.1313, "lng": 106.7046, "tipe": "🏁 Pool", "keterangan": "START"},
                {"nama": "TPS Tambora", "lat": -6.1389, "lng": 106.8072, "tipe": "🗑️ TPS", "keterangan": "STOP 1"},
                {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023, "tipe": "🚩 AKHIR", "keterangan": "END"}
            ]
        }
    },
    "Jakarta Pusat": {
        "warna": "#27ae60", "jam_operasi": "Sebelum 05.00 WIB", "jenis_truk": "Compactor Hidrolik",
        "rute": {
            "Rute 1 (Kemayoran)": [
                {"nama": "Pool Rawasari", "lat": -6.1800, "lng": 106.8690, "tipe": "🏁 Pool", "keterangan": "START"},
                {"nama": "TPS Kemayoran", "lat": -6.1546, "lng": 106.8527, "tipe": "🗑️ TPS", "keterangan": "STOP 1"},
                {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023, "tipe": "🚩 AKHIR", "keterangan": "END"}
            ],
            "Rute 2 (Tanah Abang)": [
                {"nama": "Pool Rawasari", "lat": -6.1800, "lng": 106.8690, "tipe": "🏁 Pool", "keterangan": "START"},
                {"nama": "TPS Pasar Tanah Abang", "lat": -6.1871, "lng": 106.8207, "tipe": "🗑️ TPS", "keterangan": "STOP 1"},
                {"nama": "TPST Bantargebang", "lat": -6.3527, "lng": 107.0023, "tipe": "🚩 AKHIR", "keterangan": "END"}
            ]
        }
    }
}

# ───────────────────────────────────────────────────────────────
# HELPERS (OSRM & HAVERSINE & FMT WAKTU)
# ───────────────────────────────────────────────────────────────
def haversine(a, b):
    R = 6371.0
    la1, lo1 = math.radians(a[0]), math.radians(a[1])
    la2, lo2 = math.radians(b[0]), math.radians(b[1])
    dla, dlo = la2 - la1, lo2 - lo1
    h = math.sin(dla / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dlo / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def fmt_waktu(menit):
    return f"{int(menit // 60)} jam {int(menit % 60)} mnt" if menit >= 60 else f"{int(round(menit))} menit"

@st.cache_data(ttl=3600, show_spinner=False)
def osrm_route(points):
    coord = ";".join(f"{ln},{la}" for la, ln in points)
    url = f"https://router.project-osrm.org/route/v1/driving/{coord}?overview=full&geometries=geojson"
    try:
        r = requests.get(url, timeout=20)
        if r.status_code != 200: return None, f"HTTP {r.status_code}"
        d = r.json()
        if d.get("code") != "Ok" or not d.get("routes"): return None, d.get("code", "no route")
        route = d["routes"][0]
        coords = [[la, ln] for ln, la in route["geometry"]["coordinates"]]
        return {"coords": coords, "km": route["distance"] / 1000.0, "min": route["duration"] / 60.0}, None
    except Exception as e:
        return None, str(e)

# Sinkronisasi Data Pool Dinamis
def get_ready_trucks(kota, default_val):
    if 'fleet_per_wilayah' in st.session_state and kota in st.session_state.fleet_per_wilayah:
        return st.session_state.fleet_per_wilayah[kota].get('trucks_ready', default_val)
    return default_val

POOLS = [
    {"nama": "Pool Pinang Ranti (Jaktim)",   "lat": -6.2885, "lng": 106.8830, "truk_ready": get_ready_trucks("Jakarta Timur", 60), "warna": "#e67e22"},
    {"nama": "Pool Bambu Larangan (Jakbar)", "lat": -6.1313, "lng": 106.7046, "truk_ready": get_ready_trucks("Jakarta Barat", 50), "warna": "#9b59b6"},
    {"nama": "Pool Kalibata (Jaksel)",       "lat": -6.2730, "lng": 106.8313, "truk_ready": get_ready_trucks("Jakarta Selatan", 45), "warna": "#e74c3c"},
    {"nama": "Pool Pluit (Jakut)",           "lat": -6.1202, "lng": 106.7950, "truk_ready": get_ready_trucks("Jakarta Utara", 40), "warna": "#3498db"},
    {"nama": "Pool Rawasari (Jakpus)",       "lat": -6.1800, "lng": 106.8690, "truk_ready": get_ready_trucks("Jakarta Pusat", 32), "warna": "#27ae60"},
]

def alokasi_pool(event_ll, truk_dibutuhkan):
    urut = sorted(POOLS, key=lambda p: haversine(event_ll, (p["lat"], p["lng"])))
    alok, sisa = [], truk_dibutuhkan
    for p in urut:
        if sisa <= 0: break
        ambil = min(p["truk_ready"], sisa)
        if ambil <= 0: continue
        alok.append({"pool": p, "truk": ambil, "jarak": haversine(event_ll, (p["lat"], p["lng"]))})
        sisa -= ambil
    return alok, max(0, sisa)

# ───────────────────────────────────────────────────────────────
# UI DASHBOARD UTAMA
# ───────────────────────────────────────────────────────────────
api_key_valid = TOMTOM_API_KEY != "API PASTE SINI" and len(TOMTOM_API_KEY) > 10

st.header("🗺️ Peta Operasional Sampah DKI Jakarta")
tab_armada, tab_event = st.tabs(["🚛 Rute Armada & Live Dispatch", "🎪 Peta Event"])

# ═══════════════════════════════════════════════════════════════
# TAB 1 — RUTE ARMADA & LIVE DISPATCH
# ═══════════════════════════════════════════════════════════════
with tab_armada:
    with st.expander("⚙️ Pengaturan Peta Harian", expanded=False):
        cset1, cset2 = st.columns(2)
        with cset1:
            wilayah_pilih = st.multiselect("Tampilkan Wilayah:", list(RUTE_DATA.keys()), default=["Jakarta Selatan"])
            truk_animasi = st.toggle("🚛 Animasi Truk Berjalan", value=True)
            kecepatan = 5 
        with cset2:
            if truk_animasi and wilayah_pilih:
                wilayah_truk = st.multiselect("Truk jalan di wilayah:", wilayah_pilih, default=wilayah_pilih)
            else:
                wilayah_truk = []
            if api_key_valid:
                tampil_traffic = st.toggle("🚦 Traffic Realtime", value=True)
                traffic_opacity = st.slider("Opacity Traffic", 0.1, 1.0, 0.7, 0.1)
            else:
                tampil_traffic, traffic_opacity = False, 0.7

    # Render Map OSRM
    routes_payload = {}
    if wilayah_pilih:
        with st.spinner("🔄 Mengambil rute multi-titik (OSRM)..."):
            for w in wilayah_pilih:
                routes_payload[w] = []
                for nama_rute, urutan in RUTE_DATA[w]["rute"].items():
                    wp = [(t["lat"], t["lng"]) for t in urutan]
                    res, err = osrm_route(wp)
                    
                    if res:
                        coords = res["coords"]
                        pool = urutan[0]
                        akhir = urutan[-1]
                        pres, _ = osrm_route([(akhir["lat"], akhir["lng"]), (pool["lat"], pool["lng"])])
                        pulang_coords = pres["coords"] if pres else [[akhir["lat"], akhir["lng"]], [pool["lat"], pool["lng"]]]
                    else:
                        coords = wp
                        pulang_coords = [wp[-1], wp[0]]
                        
                    routes_payload[w].append({
                        "nama_rute": nama_rute, "color": RUTE_DATA[w]["warna"], "coords": coords, "returnCoords": pulang_coords,
                        "points": [{"lat": t["lat"], "lng": t["lng"], "tipe": t["tipe"], "nama": t["nama"], "ket": t["keterangan"]} for t in urutan],
                        # daftar No. Lambung truk yang ditugaskan ke rute ini dan sedang tidak maintenance
                        "assigned_trucks": []
                    })

    # Isi daftar `assigned_trucks` untuk setiap rute berdasarkan master data di session_state
    try:
        for w, arr in routes_payload.items():
            df_master = st.session_state.fleet_per_wilayah.get(w, {}).get('df_trucks') if 'fleet_per_wilayah' in st.session_state else None
            for r in arr:
                r['assigned_trucks'] = []
                if df_master is not None and 'Rute Penugasan Detail' in df_master.columns and 'Status / Rute Penugasan' in df_master.columns:
                    try:
                        sel = df_master[(df_master['Rute Penugasan Detail'] == r['nama_rute']) & (df_master['Status / Rute Penugasan'] != 'Maintenance (Bengkel)')]
                        r['assigned_trucks'] = list(sel['No. Lambung'].astype(str).values)
                    except Exception:
                        r['assigned_trucks'] = []
    except Exception:
        pass

    payload = {
        "routes": routes_payload, "depots": [],
        "anim": wilayah_truk if truk_animasi else [], "speed": kecepatan, "bantargebang": BANTARGEBANG,
        "tomtom": TOMTOM_API_KEY if (api_key_valid and tampil_traffic) else "", "trafficOpacity": traffic_opacity,
    }

    ARMADA_HTML = """
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
      #amap { height:540px; width:100%; border-radius:12px; }
      .truck-wrap{position:relative;width:40px;height:40px;}
      .truck-halo{position:absolute;left:50%;top:50%;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;opacity:.4;animation:pulse 1.4s ease-out infinite;}
      .truck-emoji{position:absolute;left:50%;top:50%;font-size:24px;transform:translate(-50%,-50%);filter:drop-shadow(0 2px 3px rgba(0,0,0,.55));}
      @keyframes pulse{0%{transform:scale(.7);opacity:.55}70%{transform:scale(1.7);opacity:0}100%{opacity:0}}
      .pt{width:22px;height:22px;border-radius:50%;background:#fff;border:2px solid #888;display:flex;align-items:center;justify-content:center;font-size:11px;box-shadow:0 1px 3px rgba(0,0,0,.3);}
      .bg-flag{font-size:30px;filter:drop-shadow(0 2px 4px rgba(0,0,0,.55));}
    </style>
    <div id="amap"></div>
    <script>
    const DATA = __PAYLOAD__;
    const map = L.map('amap').setView([-6.23,106.87],11);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{maxZoom:19}).addTo(map);
    if(DATA.tomtom){
      L.tileLayer('https://api.tomtom.com/traffic/map/4/tile/flow/relative0/{z}/{x}/{y}.png?key='+DATA.tomtom,{opacity:DATA.trafficOpacity}).addTo(map);
    }
    function pointIcon(e,c){return L.divIcon({className:'',html:'<div class="pt" style="border-color:'+c+'">'+e+'</div>',iconSize:[22,22],iconAnchor:[11,11]});}
    function truckIcon(c){return L.divIcon({className:'',iconSize:[40,40],iconAnchor:[20,20],html:'<div class="truck-wrap"><div class="truck-halo" style="background:'+c+'"></div><div class="truck-emoji">🚛</div></div>'});}
    const allLL=[];
    
    Object.entries(DATA.routes).forEach(function([nama_wilayah, array_rute]){
        array_rute.forEach(function(r){
            if(r.coords&&r.coords.length>=2){
                L.polyline(r.coords,{color:r.color,weight:4,opacity:.8}).addTo(map);
                r.coords.forEach(c=>allLL.push(c));
            }
            r.points.forEach(function(p){
                const e=p.tipe.split(' ')[0];
                L.marker([p.lat,p.lng],{icon:pointIcon(e,r.color)}).addTo(map).bindPopup('<b>'+p.nama+'</b><br><span style="color:'+r.color+'">'+r.nama_rute+'</span>');
                allLL.push([p.lat,p.lng]);
            });
        });
    });
    
    const bg=DATA.bantargebang;
    L.marker([bg.lat,bg.lng],{icon:L.divIcon({className:'',html:'<div class="bg-flag">🚩</div>',iconSize:[30,30],iconAnchor:[15,28]})}).addTo(map).bindPopup('<b>🚩 '+bg.nama+'</b>');
    if(allLL.length){map.fitBounds(allLL,{padding:[40,40]});}
    
    const SPEED=DATA.speed||5;
    function animateTruck(latlngs,color){
      const marker=L.marker(latlngs[0],{icon:truckIcon(color),zIndexOffset:1000}).addTo(map);
      const segs=[];let total=0;
      for(let i=0;i<latlngs.length-1;i++){const a=latlngs[i],b=latlngs[i+1];const d=Math.hypot(b[0]-a[0],b[1]-a[1]);segs.push(d);total+=d;}
      if(total===0)return;
      const dur=Math.max(4000,total*166667/SPEED);
      let s=null;
      function step(ts){
        if(!s)s=ts;const t=((ts-s)%dur)/dur;let dist=t*total,acc=0,idx=0;
        while(idx<segs.length&&acc+segs[idx]<dist){acc+=segs[idx];idx++;}
        if(idx>=segs.length)idx=segs.length-1;
        const a=latlngs[idx],b=latlngs[idx+1]||latlngs[idx];const st2=segs[idx]?(dist-acc)/segs[idx]:0;
        marker.setLatLng([a[0]+(b[0]-a[0])*st2,a[1]+(b[1]-a[1])*st2]);
        requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }
    
    DATA.anim.forEach(function(nama_wilayah){
        const arr=DATA.routes[nama_wilayah];
        if(arr){
            arr.forEach(function(r){
                if(r.coords&&r.coords.length>=2){
                    const pulang=(r.returnCoords&&r.returnCoords.length>=2)?r.returnCoords:[r.coords[r.coords.length-1],r.coords[0]];
                    // Tentukan berapa unit truk yang aktif pada rute ini (default 1)
                    const count = (r.assigned_trucks && r.assigned_trucks.length) ? r.assigned_trucks.length : 1;
                    for(let k=0;k<count;k++){
                        // offset kecil agar marker tidak tumpang tindih
                        const coords = r.coords.concat(pulang).map(function(c, idx){
                            const lat = c[0] + (k * 0.00009);
                            const lng = c[1] + (k * 0.00009);
                            return [lat, lng];
                        });
                        animateTruck(coords, r.color);
                    }
                }
            });
        }
    });
    </script>
    """
    
    if wilayah_pilih:
        components.html(ARMADA_HTML.replace("__PAYLOAD__", json.dumps(payload)), height=560, scrolling=False)
    else:
        st.info("Pilih minimal 1 wilayah di ⚙️ Pengaturan.")

    # ───────────────────────────────────────────────────────────────
    # LIVE DISPATCH ARMADA (FIXED: ANTI-GLITCH IN-PLACE UPDATE)
    # ───────────────────────────────────────────────────────────────
    st.divider()
    st.subheader("🎛️ Live Dispatch & Tracking Armada")
    st.markdown("Tugaskan rute spesifik untuk setiap unit truk. Data master otomatis terhubung dengan halaman **Manajemen Armada**.")
    
    dispatch_wilayah = st.selectbox("Pilih Wilayah Kendali:", wilayah_pilih if wilayah_pilih else list(RUTE_DATA.keys()))
    
    # Ambil referensi asli ke master data di memory
    df_truk_master = st.session_state.fleet_per_wilayah[dispatch_wilayah]['df_trucks']
    
    daftar_rute_spesifik = list(RUTE_DATA[dispatch_wilayah]["rute"].keys())
    pilihan_status = ["🟢 Standby di Pool", "🟡 Menuju TPS", "🟠 Menuju Bantargebang", "🔵 Bongkar Muatan", "✔️ Selesai & Kembali"]
    
    # Buat kolom default jika master data belum punya
    if "Rute Penugasan Detail" not in df_truk_master.columns:
        df_truk_master["Rute Penugasan Detail"] = daftar_rute_spesifik[0]
    if "Status Tracking" not in df_truk_master.columns:
        df_truk_master["Status Tracking"] = "🟢 Standby di Pool"
    if "Jam Operasi" not in df_truk_master.columns:
        df_truk_master["Jam Operasi"] = RUTE_DATA[dispatch_wilayah]["jam_operasi"]
        
    # Tampilkan hanya truk yang kondisinya bukan di bengkel
    mask_ready = df_truk_master["Status / Rute Penugasan"] != "Maintenance (Bengkel)"
    df_view = df_truk_master[mask_ready][["No. Lambung", "Rute Penugasan Detail", "Status Tracking", "Jam Operasi"]]
    
    st.caption(f"Menampilkan **{len(df_view)} unit siap jalan** dari total {len(df_truk_master)} aset di {dispatch_wilayah}.")
    
    # Render tabel interaktif
    df_terupdate = st.data_editor(
        df_view,
        column_config={
            "No. Lambung": st.column_config.TextColumn("No. Lambung", disabled=True),
            "Rute Penugasan Detail": st.column_config.SelectboxColumn("Lokasi Rute", options=daftar_rute_spesifik, required=True),
            "Status Tracking": st.column_config.SelectboxColumn("Posisi Saat Ini", options=pilihan_status, required=True),
            "Jam Operasi": st.column_config.TextColumn("Jam Shift (Bisa Diedit)", required=True)
        },
        use_container_width=True,
        hide_index=True,
        key=f"dispatch_editor_{dispatch_wilayah}"
    )
    
    # SIMPAN KE MASTER DATA SECARA AMAN (Tanpa merusak struktur tabel, anti-glitch)
    for idx in df_terupdate.index:
        df_truk_master.loc[idx, "Rute Penugasan Detail"] = df_terupdate.loc[idx, "Rute Penugasan Detail"]
        df_truk_master.loc[idx, "Status Tracking"] = df_terupdate.loc[idx, "Status Tracking"]
        df_truk_master.loc[idx, "Jam Operasi"] = df_terupdate.loc[idx, "Jam Operasi"]

    # Kalkulasi Ringkasan Cepat
    truk_otw = len(df_terupdate[df_terupdate["Status Tracking"].isin(["🟡 Menuju TPS", "🟠 Menuju Bantargebang", "🔵 Bongkar Muatan"])])
    truk_standby = len(df_terupdate[df_terupdate["Status Tracking"] == "🟢 Standby di Pool"])
    truk_selesai = len(df_terupdate[df_terupdate["Status Tracking"] == "✔️ Selesai & Kembali"])
    
    c1, c2, c3 = st.columns(3)
    c1.info(f"🚚 Sedang Bertugas (OTW): **{truk_otw} Unit**")
    c2.warning(f"🟢 Standby Menunggu: **{truk_standby} Unit**")
    c3.success(f"✅ Selesai Rute: **{truk_selesai} Unit**")


# ═══════════════════════════════════════════════════════════════
# TAB 2 — PETA EVENT 
# ═══════════════════════════════════════════════════════════════
with tab_event:
    st.caption("Pilih tanggal → lihat event terjadwal hari itu → generate rute & alokasi truk otomatis.")
    
    events_all = ES.load_events()
    tgl_tersedia = ES.all_dates()

    st.subheader("1️⃣ Pilih Tanggal Event")
    tc1, tc2 = st.columns([2, 3])
    default_tgl = dt.date.fromisoformat(tgl_tersedia[0]) if tgl_tersedia else dt.date.today()
    tgl = tc1.date_input("Tanggal", value=default_tgl, key="ev_tanggal")
    tgl_str = tgl.strftime("%Y-%m-%d")
    
    if tgl_tersedia:
        tc2.caption("Tanggal yang ada event: " + ", ".join(tgl_tersedia))

    events_hari = ES.events_by_date(tgl_str)

    if not events_hari:
        st.info("Tidak ada event terjadwal pada **" + tgl_str + "**. Tambah event dari halaman Event Simulator.")
    else:
        st.success("Ada **" + str(len(events_hari)) + " event** pada " + tgl_str + ":")

        opsi = {}
        for e in events_hari:
            key = e["jam"] + " — " + e["nama"] + " @ " + e.get("lokasi", "-") + " (" + format(e["pengunjung"], ",") + " org)"
            opsi[key] = e
        pilih = st.selectbox("Pilih event untuk di-track:", list(opsi.keys()))
        ev = opsi[pilih]

        st.subheader("2️⃣ Detail & Prediksi Event")
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Waktu", ev["tanggal"] + "  " + ev["jam"])
        d2.metric("Pengunjung", format(ev["pengunjung"], ","))
        d3.metric("Prediksi Sampah", "{:.1f} ton".format(ev["volume_ton"]))
        d4.metric("Truk Dibutuhkan", str(ev["truk"]) + " unit")
        
        if st.button("Generate Rute & Track Event", type="primary", use_container_width=True, key="track_event"):
            ev_ll = (ev["lat"], ev["lng"])
            alok, kurang = alokasi_pool(ev_ll, ev["truk"])
            routes = []
            for a in alok:
                p = a["pool"]
                res, _ = osrm_route([(p["lat"], p["lng"]), ev_ll])
                if res:
                    routes.append({"coords": res["coords"], "color": p["warna"], "km": res["km"], "min": res["min"]})
            resbg, _ = osrm_route([ev_ll, (BANTARGEBANG["lat"], BANTARGEBANG["lng"])])
            bg_leg = {"coords": resbg["coords"], "km": resbg["km"], "min": resbg["min"]} if resbg else None
            st.session_state.ev_track = {"ev": ev, "alok": alok, "kurang": kurang, "routes": routes, "bg_leg": bg_leg}

    if st.session_state.get("ev_track"):
        tr = st.session_state.ev_track
        ev = tr["ev"]
        st.subheader("3️⃣ Alokasi Armada & Rute Track")

        if tr["kurang"] > 0:
            st.error("Truk semua pool tidak cukup! Kekurangan **" + str(tr["kurang"]) + " unit** — perlu tambahan armada.")
        else:
            st.success("Kebutuhan **" + str(ev["truk"]) + " truk** terpenuhi dari **" + str(len(tr["alok"])) + " pool** terdekat.")

        if tr["routes"]:
            maxleg = max(tr["routes"], key=lambda r: r["km"])
            total_km = maxleg["km"] + (tr["bg_leg"]["km"] if tr["bg_leg"] else 0)
            total_min = maxleg["min"] + (tr["bg_leg"]["min"] if tr["bg_leg"] else 0)
            t1, t2, t3 = st.columns(3)
            t1.metric("Jarak Maks", "{:.1f} km".format(total_km))
            t2.metric("Waktu Maks", fmt_waktu(total_min))
            t3.metric("Pool", str(len(tr["alok"])))

        markers = [{"lat": ev["lat"], "lng": ev["lng"], "emoji": "🎪", "popup": "<b>" + ev["nama"] + "</b>"}]
        for a in tr["alok"]:
            p = a["pool"]
            markers.append({"lat": p["lat"], "lng": p["lng"], "emoji": "🅿️", "popup": "<b>" + p["nama"] + "</b>"})
        markers.append({"lat": BANTARGEBANG["lat"], "lng": BANTARGEBANG["lng"], "emoji": "🚩", "popup": "<b>TPST Bantargebang</b>"})

        ev_routes = [{"coords": r["coords"], "color": r["color"]} for r in tr["routes"]]
        if tr["bg_leg"]:
            ev_routes.append({"coords": tr["bg_leg"]["coords"], "color": "#374151"})
        ev_payload = {"routes": ev_routes, "markers": markers, "tomtom": TOMTOM_API_KEY if api_key_valid else ""}

        EVENT_HTML = """
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <div id="evmap" style="height:520px; border-radius:12px;"></div>
        <script>
        const D=__PAYLOAD__;
        const map=L.map('evmap').setView([-6.23,106.87],11);
        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{maxZoom:19}).addTo(map);
        const allLL=[];
        D.routes.forEach(function(r){if(r.coords&&r.coords.length>=2){L.polyline(r.coords,{color:r.color,weight:6,opacity:.9}).addTo(map);r.coords.forEach(c=>allLL.push(c));}});
        D.markers.forEach(function(m){L.marker([m.lat,m.lng],{icon:L.divIcon({html:'<div style="font-size:30px">'+m.emoji+'</div>',iconSize:[30,30],iconAnchor:[15,28]})}).addTo(map).bindPopup(m.popup);allLL.push([m.lat,m.lng]);});
        if(allLL.length)map.fitBounds(allLL,{padding:[50,50]});
        </script>
        """
        components.html(EVENT_HTML.replace("__PAYLOAD__", json.dumps(ev_payload)), height=540, scrolling=False)
        
        if st.button("Reset Track", key="reset_track"):
            st.session_state.pop("ev_track", None)
            st.rerun()