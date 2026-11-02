#!/usr/bin/env python3
"""
Kalkulator Permutasi & Kombinasi (Step-by-Step + Daftar Lengkap)
================================================================

Program CLI interaktif untuk praktikum Matematika Diskrit.
Menghitung Permutasi P(n, r) dan Kombinasi C(n, r), menampilkan
seluruh tahapan kalkulasi, DAN mendaftar SEMUA kemungkinan
susunan / kombinasi secara lengkap:

    1. Teorema & rumus formal
    2. Substitusi nilai
    3. Penjabaran (ekspansi) faktorial
    4. Proses penyederhanaan / pembagian
    5. Hasil akhir (jumlah cara)
    6. Daftar seluruh susunan / kombinasi + verifikasi jumlahnya

Hanya menggunakan Python Standard Library (Python 3.8+).
"""

import itertools
import math
import os
import string
import sys

# ----------------------------------------------------------------------
# Konstanta tampilan & batasan
# ----------------------------------------------------------------------
LINE_WIDTH = 64            # Lebar garis pemisah di terminal
MAX_TERMS_SHOWN = 10       # Ekspansi faktorial > 10 suku akan diringkas
MAX_N = 1000               # Batas atas n agar output tetap terbaca
LIST_WARN_LIMIT = 1000     # Minta konfirmasi jika daftar lebih dari ini
MULT = " × "               # Simbol perkalian


# ----------------------------------------------------------------------
# Utilitas tampilan
# ----------------------------------------------------------------------
def configure_console():
    """Pastikan karakter Unicode (×, ═, ∅) tidak membuat program crash."""
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass  # Versi Python lama / stream tidak mendukung reconfigure


def clear_screen():
    """Bersihkan layar terminal (mendukung Windows, Linux, dan macOS)."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title):
    """Cetak judul utama yang dibingkai garis ganda."""
    print("\n" + "=" * LINE_WIDTH)
    print(title.center(LINE_WIDTH))
    print("=" * LINE_WIDTH)


def print_section(number, label):
    """Cetak judul sub-tahapan perhitungan."""
    print(f"\n[{number}] {label}")
    print("-" * LINE_WIDTH)


def format_number(value):
    """Format integer dengan pemisah ribuan gaya Indonesia (titik)."""
    return f"{value:,}".replace(",", ".")


def print_final_result(expression, value):
    """Cetak hasil akhir dalam kotak agar tegas dan mudah dibaca."""
    text = f"{expression} = {format_number(value)}"
    width = len(text) + 4
    print("    ╔" + "═" * width + "╗")
    print("    ║  " + text + "  ║")
    print("    ╚" + "═" * width + "╝")


# ----------------------------------------------------------------------
# Utilitas faktorial
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# Validasi input
# ----------------------------------------------------------------------
def read_non_negative_int(prompt, name):
    """
    Minta input bilangan bulat non-negatif secara berulang hingga valid.

    Menangani: string/karakter aneh, bilangan desimal, bilangan negatif,
    dan nilai yang terlalu besar.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            # Bedakan pesan untuk bilangan desimal vs. teks sembarang
            try:
                float(raw)
                print(f"  [!] Error: '{raw}' adalah bilangan desimal. "
                      f"{name} harus bilangan BULAT (0, 1, 2, ...), karena "
                      "banyaknya objek tidak mungkin pecahan.")
            except ValueError:
                print(f"  [!] Error: '{raw}' bukan angka. "
                      f"Masukkan {name} berupa bilangan bulat, misal 5.")
            continue

        if value < 0:
            print(f"  [!] Error: {name} = {value} negatif. Faktorial hanya "
                  f"terdefinisi untuk bilangan bulat non-negatif ({name} >= 0).")
            continue
        if value > MAX_N:
            print(f"  [!] Error: {name} terlalu besar. Agar penjabaran tetap "
                  f"terbaca, batasi {name} <= {MAX_N}.")
            continue
        return value


def read_n_and_r():
    """
    Baca pasangan (n, r) dan pastikan memenuhi aturan 0 <= r <= n.

    Jika r > n, hanya r yang diminta ulang.
    """
    print("\nMasukkan nilai (bilangan bulat non-negatif):")
    n = read_non_negative_int("  n (total objek)        : ", "n")
    while True:
        r = read_non_negative_int("  r (jumlah objek diambil): ", "r")
        if r <= n:
            return n, r
        print(f"  [!] Error: r = {r} melebihi n = {n}. Kita tidak dapat "
              f"mengambil {r} objek dari himpunan yang hanya berisi {n} "
              "objek. Syarat: r <= n.")


def default_objects(n):
    """
    Buat label objek otomatis: A, B, C, ... (atau 1, 2, 3, ... jika n > 26).
    """
    if n <= len(string.ascii_uppercase):
        return list(string.ascii_uppercase[:n])
    return [str(i) for i in range(1, n + 1)]


def read_objects(n):
    """
    Minta user memasukkan n objek berbeda (dipisah koma).

    Tekan Enter tanpa isi untuk memakai label otomatis.
    Validasi: jumlah objek harus tepat n dan tidak boleh ada duplikat,
    karena teorema P dan C berlaku untuk objek yang BERBEDA.
    """
    auto = default_objects(n)
    preview = ", ".join(auto[:5]) + (", ..." if n > 5 else "")
    print(f"\nMasukkan {n} objek berbeda, pisahkan dengan koma.")
    print(f"  (Tekan Enter untuk otomatis: {preview or '-'})")
    while True:
        raw = input("  Objek: ").strip()
        if not raw:
            return auto
        objects = [item.strip() for item in raw.split(",") if item.strip()]
        if len(objects) != n:
            print(f"  [!] Error: Anda memasukkan {len(objects)} objek, "
                  f"padahal n = {n}. Masukkan tepat {n} objek.")
            continue
        if len(set(objects)) != len(objects):
            print("  [!] Error: Terdapat objek yang sama (duplikat). "
                  "Permutasi & kombinasi di sini mensyaratkan objek berbeda.")
            continue
        return objects


def confirm(prompt):
    """Kembalikan True jika user menjawab y/ya."""
    return input(prompt).strip().lower() in ("y", "ya", "yes")


# ----------------------------------------------------------------------
# Pendaftaran (enumerasi) seluruh kemungkinan
# ----------------------------------------------------------------------
def format_arrangement(items, ordered):
    """
    Format satu susunan.

    - Permutasi (urutan penting)    -> tupel terurut, misal (A, B)
    - Kombinasi (urutan tidak penting) -> himpunan,  misal {A, B}
    - r = 0 -> susunan kosong (∅)
    """
    if not items:
        return "()" if ordered else "{} = ∅"
    body = ", ".join(items)
    return f"({body})" if ordered else f"{{{body}}}"


def print_in_columns(entries):
    """Cetak daftar string bernomor dalam beberapa kolom agar ringkas."""
    numbered = [f"{i:>{len(str(len(entries)))}}. {e}"
                for i, e in enumerate(entries, start=1)]
    cell_width = max(len(cell) for cell in numbered) + 3
    columns = max(1, (LINE_WIDTH - 4) // cell_width)
    for start in range(0, len(numbered), columns):
        row = numbered[start:start + columns]
        print("    " + "".join(cell.ljust(cell_width) for cell in row).rstrip())


def list_all_arrangements(objects, r, expected, ordered):
    """
    Daftar SELURUH susunan (permutasi) atau kombinasi menggunakan
    itertools, lalu verifikasi jumlahnya terhadap hasil rumus.
    """
    kind = "susunan (permutasi)" if ordered else "kombinasi"
    print(f"    Himpunan objek S = {{{', '.join(objects)}}}")
    print(f"    Notasi: {'(..) = terurut, (A, B) ≠ (B, A)' if ordered else '{..} = tidak terurut, {A, B} = {B, A}'}")
    print()

    if expected > LIST_WARN_LIMIT:
        print(f"    [!] Terdapat {format_number(expected)} {kind}. "
              "Daftar akan sangat panjang.")
        if not confirm("    Tetap tampilkan semuanya? (y/n): "):
            print("    Daftar tidak ditampilkan.")
            return

    generator = (itertools.permutations(objects, r) if ordered
                 else itertools.combinations(objects, r))
    entries = [format_arrangement(items, ordered) for items in generator]
    print_in_columns(entries)

    status = "✓ SESUAI" if len(entries) == expected else "✗ TIDAK SESUAI"
    print(f"\n    Total {kind} terdaftar: {format_number(len(entries))} "
          f"→ {status} dengan hasil rumus ({format_number(expected)})")


def show_permutations_per_combination(objects, r):
    """
    Tunjukkan hubungan C dan P: tiap kombinasi dapat disusun r! cara.
    Hanya ditampilkan untuk kasus kecil agar tidak memenuhi layar.
    """
    combos = list(itertools.combinations(objects, r))
    if r < 2 or len(combos) > 10 or math.factorial(r) > 6:
        return
    print(f"\n    Hubungan dengan permutasi: tiap kombinasi dapat disusun "
          f"{r}! = {math.factorial(r)} cara.")
    for combo in combos:
        perms = ", ".join(format_arrangement(p, True)
                          for p in itertools.permutations(combo))
        print(f"      {format_arrangement(combo, False):<14} → {perms}")


# ----------------------------------------------------------------------
# Logika Permutasi
# ----------------------------------------------------------------------
def calculate_permutation(n, r, objects):
    """Hitung P(n, r) = n! / (n - r)!, tampilkan tahapan & seluruh susunan."""
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

    # [6] Daftar seluruh susunan
    print_section(6, "DAFTAR SELURUH SUSUNAN (PERMUTASI)")
    list_all_arrangements(objects, r, result, ordered=True)
    return result


# ----------------------------------------------------------------------
# Logika Kombinasi
# ----------------------------------------------------------------------
def calculate_combination(n, r, objects):
    """Hitung C(n, r) = n! / [r! × (n - r)!], tampilkan tahapan & daftar."""
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

    # [6] Daftar seluruh kombinasi
    print_section(6, "DAFTAR SELURUH KOMBINASI")
    list_all_arrangements(objects, r, result, ordered=False)
    show_permutations_per_combination(objects, r)
    return result


# ----------------------------------------------------------------------
# Menu & main loop
# ----------------------------------------------------------------------
def show_menu():
    """Tampilkan menu utama."""
    print_header("KALKULATOR PERMUTASI & KOMBINASI")
    print("  1. Hitung Permutasi (P)")
    print("  2. Hitung Kombinasi (C)")
    print("  3. Bersihkan Layar Terminal")
    print("  4. Keluar")
    print("-" * LINE_WIDTH)


def main():
    """Main loop: tampilkan menu berulang hingga user memilih keluar."""
    configure_console()
    clear_screen()

    try:
        while True:
            show_menu()
            choice = input("Pilih menu [1-4]: ").strip()

            if choice == "4":
                print("\nTerima kasih telah menggunakan program ini. Sampai jumpa!")
                break
            if choice == "3":
                clear_screen()
                continue
            if choice not in ("1", "2"):
                print(f"  [!] Pilihan '{choice}' tidak valid. "
                      "Masukkan angka 1, 2, 3, atau 4.")
                continue

            n, r = read_n_and_r()
            objects = read_objects(n)
            clear_screen()
            if choice == "1":
                calculate_permutation(n, r, objects)
            else:
                calculate_combination(n, r, objects)
            input("\nTekan Enter untuk kembali ke menu utama...")
            clear_screen()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram dihentikan oleh pengguna. Sampai jumpa!")


if __name__ == "__main__":
    main()