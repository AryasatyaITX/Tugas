"""Utilitas faktorial: suku menurun, format perkalian, dan ekspansi."""

import math

from constants import MAX_TERMS_SHOWN, MULT
from display import format_number


def descending_terms(start, stop):
    """
    Kembalikan daftar bilangan menurun dari `start` hingga `stop + 1`.

    Contoh: descending_terms(5, 3) -> [5, 4]
    Ini adalah suku-suku yang tersisa dari start! / stop!.
    """
    return list(range(start, stop, -1))


def format_product(terms):
    """
    Ubah daftar suku menjadi string perkalian, misal "5 × 4 × 3".

    Jika jumlah suku terlalu banyak, ekspansi diringkas dengan "..."
    supaya terminal tetap rapi. Daftar kosong bernilai 1 (perkalian kosong).
    """
    if not terms:
        return "1"
    if len(terms) > MAX_TERMS_SHOWN:
        head = MULT.join(str(t) for t in terms[:6])
        tail = MULT.join(str(t) for t in terms[-3:])
        return f"{head}{MULT}...{MULT}{tail}"
    return MULT.join(str(t) for t in terms)


def expand_factorial(k):
    """
    Kembalikan string ekspansi faktorial k.

    Contoh: expand_factorial(5) -> "5! = 5 × 4 × 3 × 2 × 1 = 120"
    """
    if k == 0:
        return "0! = 1   (Catatan: menurut definisi, 0! = 1)"
    if k == 1:
        return "1! = 1"
    terms = descending_terms(k, 0)
    return f"{k}! = {format_product(terms)} = {format_number(math.factorial(k))}"


def print_factorial_expansions(values):
    """Cetak ekspansi tiap faktorial unik (urut dari terbesar)."""
    for k in sorted(set(values), reverse=True):
        print(f"    {expand_factorial(k)}")