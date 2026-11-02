#!/usr/bin/env python3
"""
Kalkulator Permutasi & Kombinasi (Step-by-Step)
================================================

Program CLI interaktif untuk praktikum Matematika Diskrit.
Menghitung Permutasi P(n, r) dan Kombinasi C(n, r) sekaligus
menampilkan seluruh tahapan kalkulasi secara rinci.

Struktur modul:
    main.py            -> menu & main loop (file ini)
    constants.py       -> konstanta tampilan & batasan
    display.py         -> utilitas cetak terminal
    factorial_utils.py -> utilitas faktorial & format perkalian
    validation.py      -> validasi & pembacaan input
    permutation.py     -> logika P(n, r)
    combination.py     -> logika C(n, r)

Jalankan : python main.py
Hanya menggunakan Python Standard Library (Python 3.8+).
"""

from constants import LINE_WIDTH
from display import configure_console, print_header
from validation import read_n_and_r
from permutation import calculate_permutation
from combination import calculate_combination


def show_menu():
    """Tampilkan menu utama."""
    print_header("KALKULATOR PERMUTASI & KOMBINASI")
    print("  1. Hitung Permutasi (P)")
    print("  2. Hitung Kombinasi (C)")
    print("  3. Keluar")
    print("-" * LINE_WIDTH)


def main():
    """Main loop: tampilkan menu berulang hingga user memilih keluar."""
    configure_console()
    actions = {"1": calculate_permutation, "2": calculate_combination}

    try:
        while True:
            show_menu()
            choice = input("Pilih menu [1-3]: ").strip()

            if choice == "3":
                print("\nTerima kasih telah menggunakan program ini. Sampai jumpa!")
                break
            if choice not in actions:
                print(f"  [!] Pilihan '{choice}' tidak valid. "
                      "Masukkan angka 1, 2, atau 3.")
                continue

            n, r = read_n_and_r()
            actions[choice](n, r)
            input("\nTekan Enter untuk kembali ke menu utama...")
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram dihentikan oleh pengguna. Sampai jumpa!")


if __name__ == "__main__":
    main()