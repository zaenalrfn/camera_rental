from datetime import datetime, timedelta

class Kamera:
    def __init__(self, id_kamera, nama, stok, harga):
        self.id_kamera = id_kamera
        self.nama = nama
        self.stok = stok
        self.harga = harga

    def tampilkan_info(self):
        return f"ID: {self.id_kamera} | Nama: {self.nama} | Stok: {self.stok} | Harga: Rp{self.harga}/hari"

class DSLR(Kamera):
    def __init__(self, id_kamera, nama, stok, harga, lensa):
        super().__init__(id_kamera, nama, stok, harga)
        self.lensa = lensa

    def tampilkan_info(self):
        return super().tampilkan_info() + f" | Lensa: {self.lensa}"

class Mirrorless(Kamera):
    def __init__(self, id_kamera, nama, stok, harga, berat):
        super().__init__(id_kamera, nama, stok, harga)
        self.berat = berat

    def tampilkan_info(self):
        return super().tampilkan_info() + f" | Berat: {self.berat} kg"

class SistemSewaKamera:
    def __init__(self):
        self.kamera_list = [
            DSLR(1, "Canon EOS 5D", 5, 200000, "24-70mm"),
            Mirrorless(2, "Sony Alpha A7 III", 3, 250000, 0.65),
            DSLR(3, "Nikon Z6", 4, 220000, "35mm"),
        ]
        self.data_penyewa = []

    def lihat_kamera(self):
        print("\nDaftar Kamera:")
        for kamera in self.kamera_list:
            print(kamera.tampilkan_info())

    def sewa_kamera(self):
        self.lihat_kamera()
        try:
            # Input Penyewa
            nama_penyewa = input("\nMasukkan nama penyewa: ")
            nomor_telepon = input("Masukkan nomor telepon: ")

            # Pilih kamera dan jumlah unit
            id_kamera = int(input("Masukkan ID Kamera yang ingin disewa: "))
            jumlah = int(input("Masukkan jumlah unit yang ingin disewa: "))
            hari = int(input("Berapa hari Anda ingin menyewa? "))
            tanggal_sewa = input("Masukkan tanggal sewa (DD-MM-YYYY): ")
            tanggal_sewa = datetime.strptime(tanggal_sewa, "%d-%m-%Y")

            kamera = next((k for k in self.kamera_list if k.id_kamera == id_kamera), None)

            if kamera and kamera.stok >= jumlah:
                total_harga = kamera.harga * jumlah * hari
                kamera.stok -= jumlah
                self.data_penyewa.append(
                    {
                        "nama": nama_penyewa,
                        "nomor_telepon": nomor_telepon,
                        "kamera": kamera.nama,
                        "jumlah": jumlah,
                        "hari": hari,
                        "total_harga": total_harga,
                        "tanggal_sewa": tanggal_sewa,
                        "status_pengembalian": "Proses",  # Status awal adalah Proses
                    }
                )
                print(f"\nBerhasil menyewa {jumlah} unit {kamera.nama}.")
                print(f"Total harga sewa untuk {hari} hari: Rp{total_harga}")
            else:
                print("\nStok tidak mencukupi atau kamera tidak ditemukan!")
        except ValueError:
            print("\nInput tidak valid, coba lagi.")

    def edit_status_penyewa(self):
        try:
            nama_penyewa = input("Masukkan nama penyewa untuk mengedit status pengembalian: ")
            penyewa = next((p for p in self.data_penyewa if p["nama"] == nama_penyewa), None)

            if penyewa:
                print("Pilih status pengembalian:")
                print("1. Proses")
                print("2. Selesai")
                print("3. Dibatalkan")
                status_choice = int(input("Masukkan pilihan (1/2/3): "))

                if status_choice == 1:
                    penyewa["status_pengembalian"] = "Proses"
                elif status_choice == 2:
                    # Menghitung denda jika terlambat
                    tanggal_kembali = datetime.now()  # Waktu sekarang
                    tanggal_sewa = penyewa["tanggal_sewa"]
                    terlambat_hari = (tanggal_kembali - tanggal_sewa).days

                    if terlambat_hari > 0:
                        # Menghitung denda: denda dihitung per hari sesuai harga sewa per hari
                        kamera = next((k for k in self.kamera_list if k.nama == penyewa["kamera"]), None)
                        if kamera:
                            denda = kamera.harga * terlambat_hari  # Denda per hari sama dengan harga sewa kamera per hari
                            total_bayar = penyewa["total_harga"] + denda
                            penyewa["status_pengembalian"] = f"Selesai (Denda: Rp{denda}, Total: Rp{total_bayar})"
                            print(f"Total denda untuk {terlambat_hari} hari terlambat: Rp{denda}")
                            print(f"Total harga yang harus dibayar: Rp{total_bayar}")
                    else:
                        penyewa["status_pengembalian"] = f"Selesai (Total: Rp{penyewa['total_harga']})"
                        print(f"Total harga yang harus dibayar: Rp{penyewa['total_harga']}")

                    # Mengembalikan stok kamera
                    kamera = next((k for k in self.kamera_list if k.nama == penyewa["kamera"]), None)
                    if kamera:
                        kamera.stok += penyewa["jumlah"]  # Menambahkan stok sesuai jumlah yang disewa
                        print(f"Stok kamera {kamera.nama} telah dikembalikan. Stok sekarang: {kamera.stok}")
                
                elif status_choice == 3:
                    penyewa["status_pengembalian"] = "Dibatalkan"
                    print("Status pengembalian telah diubah menjadi Dibatalkan.")
                else:
                    print("Pilihan tidak valid!")
                    return

                print(f"Status pengembalian untuk {nama_penyewa} telah diperbarui menjadi {penyewa['status_pengembalian']}")
            else:
                print("Penyewa tidak ditemukan!")
        except ValueError:
            print("Input tidak valid.")


    def lihat_penyewa(self):
        print("\n=== Data Penyewa ===")
        if not self.data_penyewa:
            print("Belum ada data penyewa.")
        else:
            for idx, penyewa in enumerate(self.data_penyewa, start=1):
                status = penyewa['status_pengembalian']
                # Menampilkan status dan denda jika ada
                if "Denda" in status:  # Jika ada denda dalam status
                    print(f"{idx}. Nama: {penyewa['nama']} | Kamera: {penyewa['kamera']} | Jumlah: {penyewa['jumlah']} | Hari: {penyewa['hari']} | Total Harga: Rp{penyewa['total_harga']} | Tanggal Sewa: {penyewa['tanggal_sewa'].strftime('%d-%m-%Y')} | Status: {penyewa['status_pengembalian']}")
                else:
                    print(f"{idx}. Nama: {penyewa['nama']} | Kamera: {penyewa['kamera']} | Jumlah: {penyewa['jumlah']} | Hari: {penyewa['hari']} | Total Harga: Rp{penyewa['total_harga']} | Tanggal Sewa: {penyewa['tanggal_sewa'].strftime('%d-%m-%Y')} | Status: {penyewa['status_pengembalian']}")


    def menu_penyewa(self):
        while True:
            print("\n=== Menu Penyewa ===")
            print("1. Lihat Daftar Kamera")
            print("2. Sewa Kamera")
            print("3. Keluar")
            try:
                pilihan = int(input("Pilih menu: "))
                if pilihan == 1:
                    self.lihat_kamera()
                elif pilihan == 2:
                    self.sewa_kamera()
                elif pilihan == 3:
                    break
                else:
                    print("Pilihan tidak valid, coba lagi.")
            except ValueError:
                print("Input tidak valid.")

    def menu_pemilik(self):
        while True:
            print("\n=== Menu Pemilik ===")
            print("1. Kamera")
            print("2. Sewa")
            print("3. Keluar")
            try:
                pilihan = int(input("Pilih menu: "))
                if pilihan == 1:
                    self.menu_kamera()
                elif pilihan == 2:
                    self.menu_sewa()
                elif pilihan == 3:
                    break
                else:
                    print("Pilihan tidak valid, coba lagi.")
            except ValueError:
                print("Input tidak valid.")

    def menu_kamera(self):
        while True:
            print("\n=== Menu Kamera ===")
            print("1. Lihat Kamera")
            print("2. Tambah Kamera")
            print("3. Edit Kamera")
            print("4. Hapus Kamera")
            print("5. Kembali")
            try:
                pilihan = int(input("Pilih menu: "))
                if pilihan == 1:
                    self.lihat_kamera()
                elif pilihan == 2:
                    self.tambah_kamera()
                elif pilihan == 3:
                    self.edit_kamera()
                elif pilihan == 4:
                    self.hapus_kamera()
                elif pilihan == 5:
                    break
                else:
                    print("Pilihan tidak valid, coba lagi.")
            except ValueError:
                print("Input tidak valid.")

    def menu_sewa(self):
        while True:
            print("\n=== Menu Sewa ===")
            print("1. Sewa Kamera")
            print("2. Lihat Penyewa")
            print("3. Edit Status Penyewa")
            print("4. Kembali")
            try:
                pilihan = int(input("Pilih menu: "))
                if pilihan == 1:
                    self.sewa_kamera()
                elif pilihan == 2:
                    self.lihat_penyewa()
                elif pilihan == 3:
                    self.edit_status_penyewa()
                elif pilihan == 4:
                    break
                else:
                    print("Pilihan tidak valid, coba lagi.")
            except ValueError:
                print("Input tidak valid.")

    def jalankan(self):
        while True:
            print("Selamat datang di Sistem Sewa Kamera!")
            print("Pilih peran Anda:")
            print("1. Penyewa")
            print("2. Pemilik")
            try:
                peran = int(input("Masukkan peran Anda (1/2): "))
                if peran == 1:
                    self.menu_penyewa()
                elif peran == 2:
                    self.menu_pemilik()
                else:
                    print("Peran tidak valid.")
            except ValueError:
                print("Input tidak valid.")

def main():
    sistem = SistemSewaKamera()
    sistem.jalankan()

if __name__ == "__main__":
    main()
