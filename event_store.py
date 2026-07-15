"""
Penyimpanan jadwal event — jembatan antara Event Simulator & Peta Event.
Event yang diprediksi di simulator disimpan ke sini, lalu dibaca di Peta Event
berdasarkan tanggal. Sudah ada dummy data biar langsung ada isinya.
"""
import os
import json
import math

# File JSON disimpan di folder yang sama dengan modul ini (biar konsisten)
STORE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "event_jadwal.json")

# Koordinat pusat tiap wilayah (dipakai kalau event dari simulator cuma punya wilayah)
WILAYAH_CENTROID = {
    "Jakarta Pusat":   (-6.1862, 106.8342),
    "Jakarta Selatan": (-6.2615, 106.8106),
    "Jakarta Timur":   (-6.2250, 106.9004),
    "Jakarta Barat":   (-6.1683, 106.7588),
    "Jakarta Utara":   (-6.1388, 106.8630),
}

KG_PER_ORANG = 0.4     # rata-rata timbulan sampah per pengunjung (kg) — bisa disesuaikan
KAPASITAS_TRUK = 8.0   # ton per truk


def prediksi_dari_pengunjung(pengunjung, faktor_cuaca=1.0):
    """Estimasi volume (ton) & kebutuhan truk dari jumlah pengunjung."""
    volume = pengunjung * KG_PER_ORANG * faktor_cuaca / 1000.0
    truk = math.ceil(volume / KAPASITAS_TRUK)
    return round(volume, 1), truk


# ── DUMMY DATA (event contoh biar langsung ada isinya) ──
DUMMY_EVENTS = [
    {"tanggal": "2026-07-14", "jam": "09:00", "nama": "Pekan Raya Jakarta",       "lokasi": "JIExpo Kemayoran", "lat": -6.1490, "lng": 106.8450, "pengunjung": 150000, "wilayah": "Jakarta Pusat", "sumber": "dummy"},
    {"tanggal": "2026-07-14", "jam": "18:00", "nama": "Konser Musik GBK",         "lokasi": "Stadion GBK",      "lat": -6.2185, "lng": 106.8022, "pengunjung": 80000,  "wilayah": "Jakarta Pusat", "sumber": "dummy"},
    {"tanggal": "2026-07-15", "jam": "10:00", "nama": "Jakarta Fair",             "lokasi": "JIExpo Kemayoran", "lat": -6.1490, "lng": 106.8450, "pengunjung": 120000, "wilayah": "Jakarta Pusat", "sumber": "dummy"},
    {"tanggal": "2026-07-16", "jam": "06:00", "nama": "Car Free Day Sudirman",    "lokasi": "Bundaran HI",      "lat": -6.1950, "lng": 106.8230, "pengunjung": 50000,  "wilayah": "Jakarta Pusat", "sumber": "dummy"},
    {"tanggal": "2026-07-20", "jam": "19:00", "nama": "Festival Kuliner Kota Tua","lokasi": "Kota Tua",         "lat": -6.1352, "lng": 106.8133, "pengunjung": 40000,  "wilayah": "Jakarta Barat", "sumber": "dummy"},
    {"tanggal": "2026-07-20", "jam": "16:00", "nama": "Bazar Ramadan Blok M",     "lokasi": "Blok M Square",    "lat": -6.2444, "lng": 106.7991, "pengunjung": 30000,  "wilayah": "Jakarta Selatan", "sumber": "dummy"},
]


def _lengkapi(ev):
    """Pastikan setiap event punya volume_ton & truk (dihitung kalau belum ada)."""
    if "volume_ton" not in ev or "truk" not in ev:
        vol, truk = prediksi_dari_pengunjung(ev.get("pengunjung", 0))
        ev.setdefault("volume_ton", vol)
        ev.setdefault("truk", truk)
    return ev


def load_events():
    """Baca semua event. Kalau file belum ada, seed pakai dummy lalu simpan."""
    if not os.path.exists(STORE_PATH):
        data = [_lengkapi(dict(e)) for e in DUMMY_EVENTS]
        try:
            with open(STORE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        return data
    try:
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            return [_lengkapi(e) for e in json.load(f)]
    except Exception:
        return [_lengkapi(dict(e)) for e in DUMMY_EVENTS]


def save_event(ev):
    """Tambah 1 event ke jadwal."""
    data = load_events()
    data.append(_lengkapi(ev))
    try:
        with open(STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def events_by_date(tanggal_str):
    """Ambil semua event pada tanggal tertentu (format 'YYYY-MM-DD')."""
    return [e for e in load_events() if e.get("tanggal") == tanggal_str]


def all_dates():
    """Daftar tanggal yang punya event (buat info)."""
    return sorted({e["tanggal"] for e in load_events()})