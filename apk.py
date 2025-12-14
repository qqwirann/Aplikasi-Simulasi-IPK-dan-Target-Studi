import tkinter as tk
from tkinter import messagebox

# ===================== WARNA UI =====================
BG_MAIN = "#ECF0F1"
BG_CARD = "#FFFFFF"
COLOR_PRIMARY = "#2C3E50"
COLOR_BUTTON = "#2980B9"
COLOR_EXCELLENT = "#27AE60"   # Hijau
COLOR_GOOD = "#2980B9"        # Biru
COLOR_AVERAGE = "#F39C12"     # Oranye
COLOR_BAD = "#C0392B"         # Merah

# ===================== DATA =====================
mata_kuliah = []

# ===================== KONVERSI NILAI =====================
def konversi_nilai(nilai):
    if nilai >= 90:
        return "A", 4.00, "Lulus"
    elif nilai >= 85:
        return "A-", 3.70, "Lulus"
    elif nilai >= 80:
        return "B+", 3.30, "Lulus"
    elif nilai >= 75:
        return "B", 3.00, "Lulus"
    elif nilai >= 70:
        return "B-", 2.70, "Lulus"
    elif nilai >= 65:
        return "C+", 2.30, "Lulus"
    elif nilai >= 55:
        return "C", 2.00, "Lulus"
    elif nilai >= 50:
        return "D", 1.00, "Tidak Lulus"
    else:
        return "E", 0.00, "Tidak Lulus"

# ===================== INDIKATOR IPK =====================
def indikator_ipk(ipk):
    if ipk >= 3.70:
        return "Sangat Baik (Cumlaude)", COLOR_EXCELLENT
    elif ipk >= 3.30:
        return "Baik", COLOR_GOOD
    elif ipk >= 3.00:
        return "Cukup", COLOR_AVERAGE
    else:
        return "Perlu Perbaikan", COLOR_BAD

# ===================== FUNGSI TAMBAH MK =====================
def tambah_mk():
    try:
        nama = entry_mk.get()
        sks = int(entry_sks.get())
        nilai = float(entry_nilai.get())

        huruf, bobot, ket = konversi_nilai(nilai)

        mata_kuliah.append({
            "nama": nama,
            "sks": sks,
            "bobot": bobot
        })

        listbox.insert(
            tk.END,
            f"{nama} | SKS:{sks} | Nilai:{nilai} | {huruf} | {ket}"
        )

        entry_mk.delete(0, tk.END)
        entry_sks.delete(0, tk.END)
        entry_nilai.delete(0, tk.END)

    except:
        messagebox.showerror("Error", "Input tidak valid!")


# ===================== HITUNG IPK =====================
def hitung_ipk():
    if not mata_kuliah:
        return

    total_sks = sum(mk["sks"] for mk in mata_kuliah)
    total_bobot = sum(mk["sks"] * mk["bobot"] for mk in mata_kuliah)

    ipk = total_bobot / total_sks
    jumlah_mk = len(mata_kuliah)

    label_ipk.config(
        text=f"Total Mata Kuliah : {jumlah_mk}\n"
             f"Total SKS         : {total_sks}\n"
             f"IPK Saat Ini      : {ipk:.2f}"
    )

    status, warna = indikator_ipk(ipk)
    label_status.config(text=f"Status Akademik : {status}", fg=warna)

def hitung_target():
    if not mata_kuliah:
        messagebox.showwarning("Peringatan", "Masukkan mata kuliah terlebih dahulu.")
        return

    try:
        target = float(entry_target.get())
        sisa_sks = int(entry_sisa_sks.get())

        total_sks = sum(mk["sks"] for mk in mata_kuliah)
        total_bobot = sum(mk["sks"] * mk["bobot"] for mk in mata_kuliah)
        ipk_sekarang = total_bobot / total_sks

        if target <= ipk_sekarang:
            hasil = (
                f"Target IPK : {target}\n"
                f"Sisa SKS   : {sisa_sks}\n\n"
                "✅ Target sudah tercapai\n"
                "Pertahankan prestasi!"
            )
            warna = COLOR_EXCELLENT
        else:
            bobot_min = ((target * (total_sks + sisa_sks)) - total_bobot) / sisa_sks
            hasil = (
                f"Target IPK : {target}\n"
                f"Sisa SKS   : {sisa_sks}\n"
                f"Bobot Min  : {bobot_min:.2f}\n"
            )

            if bobot_min > 4:
                hasil += "⚠️ Target sangat berat"
                warna = COLOR_BAD
            elif bobot_min >= 3.7:
                hasil += "Strategi : Mayoritas A"
                warna = COLOR_EXCELLENT
            elif bobot_min >= 3.3:
                hasil += "Strategi : Minimal B+"
                warna = COLOR_GOOD
            else:
                hasil += "Strategi : Minimal B"
                warna = COLOR_AVERAGE

        # ================= WINDOW BARU =================
        win = tk.Toplevel(root)
        win.title("Hasil Simulasi Target IPK")
        win.geometry("400x300")
        win.resizable(False, False)

        tk.Label(
            win,
            text="HASIL SIMULASI TARGET IPK",
            font=("Helvetica", 14, "bold")
        ).pack(pady=10)

        tk.Label(
            win,
            text=hasil,
            font=("Helvetica", 12),
            fg=warna,
            justify="left"
        ).pack(padx=20, pady=10)

        tk.Button(
            win,
            text="Tutup",
            command=win.destroy
        ).pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ===================== GUI =====================
root = tk.Tk()
root.title("Simulasi IPK & Target Studi")
root.geometry("700x700")
root.configure(bg=BG_MAIN)

# ===== HEADER =====
header = tk.Frame(root, bg=COLOR_PRIMARY, height=60)
header.pack(fill="x")

tk.Label(
    header,
    text="SIMULASI IPK & TARGET STUDI",
    bg=COLOR_PRIMARY,
    fg="white",
    font=("Helvetica", 16, "bold")
).pack(pady=15)

# ===== INPUT MK =====
card_input = tk.LabelFrame(root, text="Input Mata Kuliah", bg=BG_CARD, padx=10, pady=10)
card_input.pack(padx=15, pady=10, fill="x")

tk.Label(card_input, text="Mata Kuliah", bg=BG_CARD).grid(row=0, column=0, sticky="w")
entry_mk = tk.Entry(card_input, width=30)
entry_mk.grid(row=0, column=1)

tk.Label(card_input, text="SKS", bg=BG_CARD).grid(row=1, column=0, sticky="w")
entry_sks = tk.Entry(card_input, width=10)
entry_sks.grid(row=1, column=1, sticky="w")

tk.Label(card_input, text="Nilai Angka", bg=BG_CARD).grid(row=2, column=0, sticky="w")
entry_nilai = tk.Entry(card_input, width=10)
entry_nilai.grid(row=2, column=1, sticky="w")

tk.Button(card_input, text="Tambah Mata Kuliah", bg=COLOR_BUTTON, fg="white",
          command=tambah_mk).grid(row=3, columnspan=2, pady=10)

# ===== LIST =====
listbox = tk.Listbox(root, width=90, height=8, font=("Consolas", 10))
listbox.pack(padx=15, pady=10)

# ===== IPK =====
card_ipk = tk.LabelFrame(root, text="Hasil IPK", bg=BG_CARD, padx=10, pady=10)
card_ipk.pack(padx=15, pady=10, fill="x")

tk.Button(card_ipk, text="Hitung IPK", bg=COLOR_BUTTON, fg="white",
          command=hitung_ipk).pack(pady=5)

label_ipk = tk.Label(card_ipk, bg=BG_CARD, font=("Helvetica", 11))
label_ipk.pack()

label_status = tk.Label(card_ipk, bg=BG_CARD, font=("Helvetica", 12, "bold"))
label_status.pack(pady=5)

# ===== TARGET =====
card_target = tk.LabelFrame(
    root,
    text="Simulasi Target IPK",
    bg="#D5F5E3",
    padx=10,
    pady=10
)
card_target.pack(padx=15, pady=10, fill="x")

tk.Label(card_target, text="Target IPK", bg="#D5F5E3").grid(row=0, column=0, sticky="w")
entry_target = tk.Entry(card_target, width=10)
entry_target.grid(row=0, column=1, sticky="w")

tk.Label(card_target, text="Sisa SKS", bg="#D5F5E3").grid(row=1, column=0, sticky="w")
entry_sisa_sks = tk.Entry(card_target, width=10)
entry_sisa_sks.grid(row=1, column=1, sticky="w")

tk.Button(
    card_target,
    text="Hitung Target",
    bg=COLOR_BUTTON,
    fg="white",
    command=hitung_target
).grid(row=2, column=0, columnspan=2, pady=10)

label_target = tk.Label(
    card_target,
    bg="#D5F5E3",
    font=("Helvetica", 11),
    justify="left",
    wraplength=500
)
label_target.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)

root.mainloop()