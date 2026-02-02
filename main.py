import json
import os
from datetime import datetime

DATA_FILE = "data.json"
TEMP_FILE = DATA_FILE + ".tmp"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                saldo = float(data.get("saldo", 0))
                transactions = data.get("transactions", [])
                return {"saldo": saldo, "transactions": transactions}
        except (json.JSONDecodeError, IOError, ValueError):
            return {"saldo": 0.0, "transactions": []}
    return {"saldo": 0.0, "transactions": []}


def save_data(saldo_value, transactions):
    try:
        tmp = TEMP_FILE
        with open(tmp, "w") as f:
            json.dump({"saldo": saldo_value, "transactions": transactions}, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, DATA_FILE)
    except IOError:
        print("Gagal menyimpan data ke file.")

# Inisialisasi dari file
_data = load_data()
saldo = _data["saldo"]
transactions = _data["transactions"]

def tambah_pemasukan():
    global saldo
    while True:
        try:
            jumlah = input("Masukkan jumlah pemasukan: ")
            if jumlah.strip() == "":
                print("Masukan tidak boleh kosong. Coba lagi.")
                continue
            jumlah = float(jumlah)
            if jumlah <= 0:
                print("Jumlah harus lebih besar dari 0. Coba lagi.")
                continue
            saldo += jumlah
            transaksi = {"type": "pemasukan", "amount": jumlah, "time": datetime.now().isoformat()}
            transactions.append(transaksi)
            save_data(saldo, transactions)
            print(f"Pemasukan sebesar {jumlah:.2f} berhasil ditambahkan.")
            break
        except ValueError:
            print("Input tidak valid. Masukkan angka, contoh: 10000")

def tambah_pengeluaran():
    global saldo
    while True:
        try:
            jumlah = input("Masukkan jumlah pengeluaran: ")
            if jumlah.strip() == "":
                print("Masukan tidak boleh kosong. Coba lagi.")
                continue
            jumlah = float(jumlah)
            if jumlah <= 0:
                print("Jumlah harus lebih besar dari 0. Coba lagi.")
                continue
            if jumlah > saldo:
                print(f"Saldo tidak cukup. Saldo saat ini: {saldo:.2f}")
                return
            saldo -= jumlah
            transaksi = {"type": "pengeluaran", "amount": jumlah, "time": datetime.now().isoformat()}
            transactions.append(transaksi)
            save_data(saldo, transactions)
            print(f"Pengeluaran sebesar {jumlah:.2f} berhasil dikurangi dari saldo.")
            break
        except ValueError:
            print("Input tidak valid. Masukkan angka, contoh: 10000")

def lihat_saldo():
    print("=== Saldo Saat Ini ===")
    print(f"Saldo: Rp {saldo:,.2f}")

def lihat_laporan():
    print("=== Laporan Rekap ===")
    total_pemasukan = sum(t["amount"] for t in transactions if t.get("type") == "pemasukan")
    total_pengeluaran = sum(t["amount"] for t in transactions if t.get("type") == "pengeluaran")
    print(f"Total pemasukan : Rp {total_pemasukan:,.2f}")
    print(f"Total pengeluaran: Rp {total_pengeluaran:,.2f}")
    print("")
    print("Riwayat transaksi (terbaru pertama):")
    # Tampilkan hingga 20 transaksi terakhir
    for t in reversed(transactions[-20:]):
        waktu = t.get("time", "")
        tipe = t.get("type", "")
        jumlah = t.get("amount", 0)
        tanda = "+" if tipe == "pemasukan" else "-"
        print(f"{waktu} | {tipe.capitalize():12} | {tanda} Rp {jumlah:,.2f}")

def menu():
    print("=== Aplikasi Pengelola Uang Saku ===")
    print("1. Tambah pemasukan")
    print("2. Tambah pengeluaran")
    print("3. Lihat saldo")
    print("4. Lihat laporan")
    print("5. Keluar")

while True:
    menu()
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_pemasukan()
    elif pilihan == "2":
        tambah_pengeluaran()
    elif pilihan == "3":
        lihat_saldo()
    elif pilihan == "4":
        lihat_laporan()
    elif pilihan == "5":
        print("Terima kasih!")
        break
    else:
        print("Pilihan tidak valid")