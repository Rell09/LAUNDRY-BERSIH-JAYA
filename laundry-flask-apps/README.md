# Kalkulator Rute Laundry — Dijkstra (Python + Flask)

Aplikasi web untuk menghitung rute terpendek dari laundry pusat ke titik
pelanggan menggunakan Algoritma Dijkstra, dibangun dengan Python (Flask).

## Struktur folder

```
laundry-flask-app/
├── app.py                 # Backend: logika Dijkstra + route Flask
├── requirements.txt       # Daftar dependensi Python
├── templates/
│   └── index.html         # Halaman utama (Jinja2 template)
└── static/
    ├── style.css           # Styling halaman
    └── app.js              # Logika frontend (fetch ke API)
```

## Cara menjalankan

1. **Install Flask** (cukup sekali saja):
   ```
   pip install -r requirements.txt
   ```

2. **Jalankan server:**
   ```
   python app.py
   ```

3. **Buka di browser:**
   ```
   http://127.0.0.1:5000
   ```

Tekan `Ctrl+C` di terminal untuk menghentikan server.

## Cara kerja singkat

- `app.py` menyimpan data graf (7 titik, 11 ruas) dan mengimplementasikan
  **Algoritma Dijkstra** menggunakan *priority queue* (`heapq`) dari
  pustaka standar Python.
- Saat pengguna memilih titik tujuan di halaman web, JavaScript
  (`static/app.js`) memanggil endpoint API `/hitung/<tujuan>`, yang
  dijalankan oleh Flask di server dan mengembalikan hasil dalam format JSON.
- Endpoint `/ringkasan` menghitung rute optimal untuk seluruh titik
  pelanggan sekaligus, ditampilkan sebagai tabel ringkasan.

## Endpoint API

| Endpoint | Metode | Keterangan |
|---|---|---|
| `/` | GET | Halaman utama (form pemilihan tujuan) |
| `/hitung/<tujuan>` | GET | Menghitung rute optimal ke satu titik (JSON) |
| `/ringkasan` | GET | Menghitung rute optimal ke semua titik (JSON) |

Contoh: `http://127.0.0.1:5000/hitung/G` akan mengembalikan:
```json
{
  "tujuan": "G",
  "rute": ["A", "B", "D", "G"],
  "jarak_km": 5.2,
  "biaya_jarak": 10400,
  "biaya_zona": 7000,
  "total_biaya": 17400
}
```

## Mengubah data

Untuk mengganti titik pelanggan, jarak, atau tarif — edit langsung bagian
`GRAPH`, `NODE_LABELS`, dan `BIAYA_PER_KM` di bagian atas file `app.py`.
