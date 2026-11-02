"""Validasi dan pembacaan input pengguna."""

from constants import MAX_N


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