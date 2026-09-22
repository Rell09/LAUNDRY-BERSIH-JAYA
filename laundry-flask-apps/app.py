"""
Kalkulator Rute Laundry - Dijkstra
==================================
Aplikasi web sederhana untuk menghitung rute terpendek dari titik pusat
laundry ke titik-titik pelanggan menggunakan Algoritma Dijkstra, sekaligus
menghitung estimasi biaya (biaya jarak + biaya tambahan jemput-antar).

Cara menjalankan:
    pip install flask
    python app.py
Lalu buka http://127.0.0.1:5000 di browser.
"""

import heapq
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# ---------------------------------------------------------------------------
# 1. DATA GRAF
# ---------------------------------------------------------------------------
# Graf tak berarah dan berbobot. Bobot = jarak tempuh dalam kilometer,
# diperoleh dari hasil observasi (mis. Google Maps).
GRAPH = {
    "A": {"B": 1.2, "C": 2.0},
    "B": {"A": 1.2, "D": 1.5, "E": 2.3},
    "C": {"A": 2.0, "E": 1.8, "F": 3.0},
    "D": {"B": 1.5, "E": 1.0, "G": 2.5},
    "E": {"B": 2.3, "C": 1.8, "D": 1.0, "F": 1.4, "G": 1.9},
    "F": {"C": 3.0, "E": 1.4, "G": 1.2},
    "G": {"D": 2.5, "E": 1.9, "F": 1.2},
}

NODE_LABELS = {
    "A": "Laundry Bersih Jaya (pusat)",
    "B": "Pelanggan 1 - Perum Melati",
    "C": "Pelanggan 2 - Jl. Mawar",
    "D": "Pelanggan 3 - Perum Anggrek",
    "E": "Pelanggan 4 - Jl. Kenanga",
    "F": "Pelanggan 5 - Perum Dahlia",
    "G": "Pelanggan 6 - Jl. Cempaka",
}

BIAYA_PER_KM = 2000  # rupiah


# ---------------------------------------------------------------------------
# 2. ALGORITMA DIJKSTRA
# ---------------------------------------------------------------------------
def dijkstra(graph: dict, start: str):
    """
    Mengembalikan (dist, prev) dari titik `start` ke semua titik lain
    menggunakan Algoritma Dijkstra dengan priority queue (min-heap).
    """
    dist = {node: float("inf") for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0

    visited = set()
    heap = [(0, start)]  # (jarak, node)

    while heap:
        current_dist, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        for v, weight in graph[u].items():
            if v in visited:
                continue
            alt = current_dist + weight
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(heap, (alt, v))

    return dist, prev


def build_path(prev: dict, start: str, target: str):
    """Menelusuri kembali (backtrack) rute dari start ke target."""
    path = [target]
    node = target
    while node != start:
        node = prev[node]
        if node is None:
            return []  # tidak ada rute
        path.append(node)
    path.reverse()
    return path


# ---------------------------------------------------------------------------
# 3. PERHITUNGAN BIAYA
# ---------------------------------------------------------------------------
def hitung_biaya_zona(jarak_km: float):
    """Biaya tambahan jemput-antar berdasarkan zona jarak dari pusat."""
    if jarak_km <= 1.5:
        return 3000, "0 - 1,5 km"
    elif jarak_km <= 3:
        return 5000, "1,5 - 3 km"
    else:
        return 7000, "> 3 km"


def hitung_rute(target: str):
    """Menghitung rute optimal, jarak, dan rincian biaya ke satu titik tujuan."""
    dist, prev = dijkstra(GRAPH, "A")
    path = build_path(prev, "A", target)
    jarak = round(dist[target], 2)
    biaya_jarak = round(jarak * BIAYA_PER_KM)
    biaya_zona, label_zona = hitung_biaya_zona(jarak)
    total = biaya_jarak + biaya_zona

    return {
        "tujuan": target,
        "nama_tujuan": NODE_LABELS[target],
        "rute": path,
        "jarak_km": jarak,
        "biaya_jarak": biaya_jarak,
        "biaya_zona": biaya_zona,
        "label_zona": label_zona,
        "total_biaya": total,
    }


# ---------------------------------------------------------------------------
# 4. ROUTES (endpoint web)
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Halaman utama, menampilkan form pemilihan tujuan."""
    tujuan_list = [(k, v) for k, v in NODE_LABELS.items() if k != "A"]
    return render_template("index.html", tujuan_list=tujuan_list)


@app.route("/hitung/<target>")
def hitung(target: str):
    """API endpoint: hitung rute optimal ke satu titik tujuan (format JSON)."""
    target = target.upper()
    if target not in GRAPH or target == "A":
        return jsonify({"error": "Titik tujuan tidak valid"}), 400
    return jsonify(hitung_rute(target))


@app.route("/ringkasan")
def ringkasan():
    """API endpoint: hitung rute optimal untuk SEMUA titik pelanggan sekaligus."""
    hasil = [hitung_rute(t) for t in GRAPH if t != "A"]
    return jsonify(hasil)


if __name__ == "__main__":
    app.run(debug=True)
