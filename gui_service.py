"""
Lapisan penghubung antara GUI dan logika perhitungan.

Modul permutation.py & combination.py menampilkan tahapan lewat print().
Di sini output print() itu ditangkap menjadi string sehingga bisa
ditampilkan di widget teks GUI, tanpa mengubah logika aslinya.
Modul ini tidak bergantung pada tkinter, jadi mudah diuji terpisah.
"""

import contextlib
import io

from constants import MAX_N
from permutation import calculate_permutation
from combination import calculate_combination

KINDS = {
    "P": ("Permutasi", calculate_permutation),
    "C": ("Kombinasi", calculate_combination),
}


def parse_non_negative_int(text, name):
    """Ubah teks menjadi bilangan bulat non-negatif, atau lempar ValueError."""
    raw = text.strip()
    try:
        value = int(raw)
    except ValueError:
        try:
            float(raw)
        except ValueError:
            raise ValueError(
                f"'{raw}' bukan angka. Masukkan {name} berupa bilangan bulat.")
        raise ValueError(
            f"'{raw}' adalah bilangan desimal. {name} harus bilangan BULAT.")
    if value < 0:
        raise ValueError(f"{name} = {value} negatif. Syarat: {name} >= 0.")
    if value > MAX_N:
        raise ValueError(f"{name} terlalu besar. Batasi {name} <= {MAX_N}.")
    return value


def parse_n_and_r(n_text, r_text):
    """Validasi pasangan (n, r) dengan syarat 0 <= r <= n."""
    if not n_text.strip():
        raise ValueError("n belum diisi.")
    if not r_text.strip():
        raise ValueError("r belum diisi.")
    n = parse_non_negative_int(n_text, "n")
    r = parse_non_negative_int(r_text, "r")
    if r > n:
        raise ValueError(
            f"r = {r} melebihi n = {n}. Tidak bisa mengambil {r} objek "
            f"dari {n} objek. Syarat: r <= n.")
    return n, r


def run_calculation(kind, n_text, r_text):
    """
    Jalankan perhitungan dan kembalikan dict:
        {"ok": True,  "n", "r", "result", "label", "steps"}
        {"ok": False, "error": "<pesan>"}
    `kind` adalah "P" (permutasi) atau "C" (kombinasi).
    """
    try:
        n, r = parse_n_and_r(n_text, r_text)
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}

    _, func = KINDS[kind]
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(n, r)
    return {
        "ok": True,
        "n": n,
        "r": r,
        "result": result,
        "label": f"{kind}({n}, {r})",
        "steps": buffer.getvalue().strip("\n"),
    }