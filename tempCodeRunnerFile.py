"""Logika Permutasi P(n, r) beserta tahapan perhitungannya."""

import math

from constants import MULT
from display import print_header, print_section, format_number, print_final_result
from factorial_utils import descending_terms, format_product, print_factorial_expansions


def calculate_permutation(n, r):
    """Hitung P(n, r) = n! / (n - r)! sambil menampilkan setiap tahapan."""
    diff = n - r
    numerator = math.factorial(n)
    denominator = math.factorial(diff)
    result = numerator // denominator

    print_header(f"PERMUTASI  P({n}, {r})")

    # [1] Teorema & rumus formal
    print_section(1, "TEOREMA & RUMUS FORMAL")
    print("    P(n, r) = n! / (n - r)!")
    print("    Makna : banyaknya susunan TERURUT r objek yang diambil")
    print("            dari n objek berbeda (urutan diperhatikan).")

    # [2] Substitusi nilai
    print_section(2, "SUBSTITUSI NILAI")
    print(f"    n = {n},  r = {r}")
    print(f"    n - r = {n} - {r} = {diff}")
    print(f"    P({n}, {r}) = {n}! / ({n} - {r})!")
    print(f"    {' ' * len(f'P({n}, {r})')} = {n}! / {diff}!")

    # [3] Penjabaran faktorial
    print_section(3, "PENJABARAN FAKTORIAL")
    print_factorial_expansions([n, diff])

    # [4] Penyederhanaan / pembagian
    print_section(4, "PENYEDERHANAAN / PEMBAGIAN")
    print(f"    Pembilang : {n}! = {format_number(numerator)}")
    print(f"    Penyebut  : {diff}! = {format_number(denominator)}")
    print()

    remaining = descending_terms(n, diff)  # suku sisa setelah eliminasi
    label = f"P({n}, {r})"
    pad = " " * len(label)
    if r == 0:
        print(f"    Karena r = 0, pembilang dan penyebut sama ({n}!),")
        print("    sehingga seluruh suku tereliminasi:")
        print(f"    {label} = {n}! / {n}! = 1")
    elif diff <= 1:
        print(f"    Penyebut {diff}! = 1, sehingga tidak ada suku yang")
        print("    perlu dieliminasi:")
        print(f"    {label} = {n}! / 1 = {format_number(result)}")
    else:
        print(f"    Ekspansi n! dapat ditulis memuat {diff}!, sehingga")
        print(f"    suku {diff}! pada pembilang & penyebut saling meniadakan:")
        print(f"    {label} = ({format_product(remaining)}{MULT}{diff}!) / {diff}!")
        print(f"    {pad} = {format_product(remaining)}")
        print(f"    {pad} = {format_number(result)}")
    print(f"\n    Verifikasi: {format_number(numerator)} / "
          f"{format_number(denominator)} = {format_number(result)}")

    # [5] Hasil akhir
    print_section(5, "HASIL AKHIR")
    print_final_result(label, result)
    return result