#!/usr/bin/env python3
"""
GUI Kalkulator Permutasi & Kombinasi (Step-by-Step)
===================================================

Antarmuka grafis berbasis tkinter (bawaan Python, tanpa instalasi tambahan).
Memakai logika yang sama dengan versi CLI (main.py).

Jalankan : python gui.py
"""

import tkinter as tk
from tkinter import ttk, font as tkfont

from display import format_number
from gui_service import KINDS, run_calculation

# Palet warna (selaras dengan tema slide: navy, teal, kuning)
NAVY = "#12233f"
TEAL = "#14958f"
GOLD = "#f4b53f"
BG = "#f2f7fb"
ERROR = "#c0392b"


class CalculatorApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)
        self.master = master
        self.kind = tk.StringVar(value="P")
        self.n_var = tk.StringVar()
        self.r_var = tk.StringVar()
        self.result_var = tk.StringVar(value="—")
        self.status_var = tk.StringVar()

        self._setup_style()
        self._build_header()
        self._build_inputs()
        self._build_result()
        self._build_output()
        self._update_formula()
        self.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # Tampilan
    # ------------------------------------------------------------------
    def _setup_style(self):
        self.master.configure(bg=BG)
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=NAVY)
        style.configure("TRadiobutton", background=BG, foreground=NAVY)
        style.configure("TLabelframe", background=BG)
        style.configure("TLabelframe.Label", background=BG,
                        foreground=NAVY, font=("TkDefaultFont", 10, "bold"))
        style.configure("Title.TLabel", font=("TkDefaultFont", 16, "bold"))
        style.configure("Formula.TLabel", foreground=TEAL,
                        font=("TkDefaultFont", 11, "italic"))
        style.configure("Result.TLabel", foreground=NAVY,
                        font=("TkDefaultFont", 20, "bold"))
        style.configure("Error.TLabel", foreground=ERROR)
        style.configure("Accent.TButton", background=TEAL, foreground="white",
                        font=("TkDefaultFont", 10, "bold"))
        style.map("Accent.TButton", background=[("active", NAVY)])

    def _build_header(self):
        ttk.Label(self, text="Kalkulator Permutasi & Kombinasi",
                  style="Title.TLabel").pack(anchor="w")
        ttk.Label(self, text="Matematika Diskrit • Perhitungan step-by-step").pack(
            anchor="w", pady=(0, 8))

    def _build_inputs(self):
        box = ttk.LabelFrame(self, text="Input", padding=10)
        box.pack(fill="x")

        # Pilihan jenis perhitungan
        row = ttk.Frame(box)
        row.pack(fill="x")
        for key, (name, _) in KINDS.items():
            ttk.Radiobutton(row, text=f"{name} ({key})", value=key,
                            variable=self.kind,
                            command=self._update_formula).pack(side="left", padx=(0, 16))

        self.formula_label = ttk.Label(box, style="Formula.TLabel")
        self.formula_label.pack(anchor="w", pady=(6, 8))

        # Isian n dan r
        grid = ttk.Frame(box)
        grid.pack(fill="x")
        ttk.Label(grid, text="n (total objek)").grid(row=0, column=0, sticky="w")
        ttk.Label(grid, text="r (jumlah diambil)").grid(row=0, column=1, sticky="w", padx=(12, 0))

        self.n_entry = ttk.Entry(grid, textvariable=self.n_var, width=14)
        self.n_entry.grid(row=1, column=0, sticky="w")
        self.r_entry = ttk.Entry(grid, textvariable=self.r_var, width=14)
        self.r_entry.grid(row=1, column=1, sticky="w", padx=(12, 0))

        ttk.Button(grid, text="Hitung", style="Accent.TButton",
                   command=self.calculate).grid(row=1, column=2, padx=(16, 0))
        ttk.Button(grid, text="Bersihkan",
                   command=self.clear).grid(row=1, column=3, padx=(6, 0))

        self.status_label = ttk.Label(box, textvariable=self.status_var,
                                      style="Error.TLabel", wraplength=640)
        self.status_label.pack(anchor="w", pady=(6, 0))

        # Enter = hitung
        self.master.bind("<Return>", lambda _e: self.calculate())
        self.n_entry.focus_set()

    def _build_result(self):
        box = ttk.LabelFrame(self, text="Hasil Akhir", padding=10)
        box.pack(fill="x", pady=(10, 0))
        ttk.Label(box, textvariable=self.result_var,
                  style="Result.TLabel").pack(side="left")
        ttk.Button(box, text="Salin hasil",
                   command=self.copy_result).pack(side="right")

    def _build_output(self):
        box = ttk.LabelFrame(self, text="Tahapan Perhitungan", padding=6)
        box.pack(fill="both", expand=True, pady=(10, 0))

        mono = self._pick_mono_font()
        self.text = tk.Text(box, width=78, height=24, wrap="none", font=mono,
                            bg="white", fg=NAVY, relief="flat", padx=8, pady=6)
        yscroll = ttk.Scrollbar(box, orient="vertical", command=self.text.yview)
        xscroll = ttk.Scrollbar(box, orient="horizontal", command=self.text.xview)
        self.text.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set,
                            state="disabled")

        self.text.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        box.rowconfigure(0, weight=1)
        box.columnconfigure(0, weight=1)

        self.text.tag_configure("header", foreground=TEAL, font=(mono[0], mono[1], "bold"))
        self.text.tag_configure("section", foreground=NAVY, font=(mono[0], mono[1], "bold"))

    @staticmethod
    def _pick_mono_font():
        families = set(tkfont.families())
        for name in ("Consolas", "Cascadia Mono", "DejaVu Sans Mono",
                     "Menlo", "Courier New"):
            if name in families:
                return (name, 10)
        return ("Courier", 10)

    # ------------------------------------------------------------------
    # Aksi
    # ------------------------------------------------------------------
    def _update_formula(self):
        if self.kind.get() == "P":
            text = "P(n, r) = n! / (n − r)!   — urutan diperhatikan"
        else:
            text = "C(n, r) = n! / [r! × (n − r)!]   — urutan tidak diperhatikan"
        self.formula_label.configure(text=text)

    def calculate(self):
        outcome = run_calculation(self.kind.get(), self.n_var.get(), self.r_var.get())
        if not outcome["ok"]:
            self.status_var.set(f"⚠ {outcome['error']}")
            return

        self.status_var.set("")
        self.result_var.set(f"{outcome['label']} = {format_number(outcome['result'])}")
        self._show_steps(outcome["steps"])

    def _show_steps(self, steps):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        for line in steps.splitlines():
            stripped = line.strip()
            if stripped.startswith(("PERMUTASI", "KOMBINASI")):
                tag = "header"
            elif line.startswith("["):
                tag = "section"
            else:
                tag = ""
            self.text.insert("end", line + "\n", tag)
        self.text.configure(state="disabled")
        self.text.yview_moveto(0)

    def clear(self):
        self.n_var.set("")
        self.r_var.set("")
        self.status_var.set("")
        self.result_var.set("—")
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")
        self.n_entry.focus_set()

    def copy_result(self):
        value = self.result_var.get()
        if value == "—":
            return
        self.master.clipboard_clear()
        self.master.clipboard_append(value)
        self.status_var.set("")


def main():
    root = tk.Tk()
    root.title("Kalkulator Permutasi & Kombinasi")
    root.minsize(700, 640)
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()