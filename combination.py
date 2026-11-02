"""Logika Kombinasi C(n, r) beserta tahapan perhitungannya."""

import math

from constants import MULT
from display import print_header, print_section, format_number, print_final_result
from factorial_utils import descending_terms, format_product, print_factorial_expansions


def calculate_combination(n, r):
    """Hitung C(n, r) = n! / [r! × (n - r)!] sambil menampilkan tahapan."""
    diff = n - r
    numerator = math.factorial(n)
    fact_r = math.factorial(r)
    fact_diff = math.factorial(diff)
    denominator = fact_r * fact_diff
    result = numerator // denominator

    print_header(f"KOMBINASI  C({n}, {r})")

    # [1] Teorema & rumus formal
    print_section(1, "TEOREMA & RUMUS FORMAL")
    print("    C(n, r) = n! / [r! × (n - r)!]")
    print("    Makna : banyaknya cara memilih r objek dari n objek")
    print("            berbeda TANPA memperhatikan urutan.")

    # [2] Substitusi nilai
    label = f"C({n}, {r})"
    pad = " " * len(label)
    print_section(2, "SUBSTITUSI NILAI")
    print(f"    n = {n},  r = {r}")
    print(f"    n - r = {n} - {r} = {diff}")
    print(f"    {label} = {n}! / [{r}! × ({n} - {r})!]")
    print(f"    {pad} = {n}! / [{r}! × {diff}!]")

    # [3] Penjabaran faktorial
    print_section(3, "PENJABARAN FAKTORIAL")
    print_factorial_expansions([n, r, diff])

    # [4] Penyederhanaan / pembagian
    print_section(4, "PENYEDERHANAAN / PEMBAGIAN")
    print(f"    Pembilang : {n}! = {format_number(numerator)}")
    print(f"    Penyebut  : {r}! × {diff}! = {format_number(fact_r)} × "
          f"{format_number(fact_diff)} = {format_number(denominator)}")
    print()

    # Strategi: eliminasi faktorial TERBESAR di penyebut dengan n!
    big, small = max(r, diff), min(r, diff)
    big_name = "r!" if big == r else "(n - r)!"
    remaining = descending_terms(n, big)
    partial = math.prod(remaining)  # = n! / big!

    if big <= 1:
        print("    Semua faktorial di penyebut bernilai 1, sehingga tidak")
        print("    ada suku yang perlu dieliminasi:")
        print(f"    {label} = {format_number(numerator)} / "
              f"{format_number(denominator)} = {format_number(result)}")
    elif not remaining:
        # Terjadi saat r = 0 atau r = n: penyebut memuat n! itu sendiri
        print(f"    Penyebut memuat {n}! [= {big_name}] dan 0! = 1,")
        print("    sehingga seluruh suku tereliminasi:")
        print(f"    {label} = {n}! / (0!{MULT}{n}!) = 1 / 1 = 1")
    else:
        print(f"    Faktorial terbesar di penyebut adalah {big}! [= {big_name}].")
        print(f"    Tulis {n}! = {format_product(remaining)}{MULT}{big}!, "
              f"lalu eliminasi {big}!:")
        print(f"    {label} = ({format_product(remaining)}{MULT}{big}!)"
              f" / ({small}!{MULT}{big}!)")
        print(f"    {pad} = ({format_product(remaining)}) / {small}!")
        print(f"    {pad} = {format_number(partial)} / "
              f"{format_number(math.factorial(small))}")
        print(f"    {pad} = {format_number(result)}")
    print(f"\n    Verifikasi: {format_number(numerator)} / "
          f"{format_number(denominator)} = {format_number(result)}")
    print(f"    Hubungan  : C(n, r) = P(n, r) / r!  ->  "
          f"{format_number(numerator // fact_diff)} / {format_number(fact_r)}"
          f" = {format_number(result)}")

    # [5] Hasil akhir
    print_section(5, "HASIL AKHIR")
    print_final_result(label, result)
    return result