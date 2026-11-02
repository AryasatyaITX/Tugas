"""Utilitas tampilan terminal (header, section, format angka, kotak hasil)."""

import sys

from constants import LINE_WIDTH


def configure_console():
    """Pastikan karakter Unicode (×, ═) tidak membuat program crash."""
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass  # Versi Python lama / stream tidak mendukung reconfigure


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