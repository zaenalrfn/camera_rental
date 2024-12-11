class Kamera:
    def __init__(self, id_kamera, nama, stok, harga):
        self.id_kamera = id_kamera
        self.nama = nama
        self.stok = stok
        self.harga = harga

    def tampilkan_info(self):
        return f"ID: {self.id_kamera} | Nama: {self.nama} | Stok: {self.stok} | Harga: Rp{self.harga}/hari"


class SistemSewaKamera:
    def __init__(self):
        self.kamera_list = [
            Kamera(1, "Canon EOS 5D", 5, 200000),
            Kamera(2, "Sony Alpha A7 III", 3, 250000),
            Kamera(3, "Nikon Z6", 4, 220000),
        ]

    def lihat_kamera(self):
        print("\nDaftar Kamera:")
        for kamera in self.kamera_list:
            print(kamera.tampilkan_info())

    def stok_kamera(self):
        print("\nStok Kamera:")
        for kamera in self.kamera_list:
            print(f"{kamera.nama}: {kamera.stok} unit tersedia")

    def sewa_kamera(self):
        self.lihat_kamera()
        try:
            id_kamera = int(input("\nMasukkan ID Kamera yang ingin disewa: "))
            jumlah = int(input("Masukkan jumlah unit yang ingin disewa: "))
            hari = int(input("Berapa hari Anda ingin menyewa? "))
            kamera = next((k for k in self.kamera_list if k.id_kamera == id_kamera), None)

            if kamera and kamera.stok >= jumlah:
                total_harga = kamera.harga * jumlah * hari
                kamera.stok -= jumlah
                print(f"\nBerhasil menyewa {jumlah} unit {kamera.nama}.")
                print(f"Total harga sewa untuk {hari} hari: Rp{total_harga}")
            else:
                print("\nStok tidak mencukupi atau kamera tidak ditemukan!")
        except ValueError:
            print("\nInput tidak valid, coba lagi.")

    def jalankan(self):
        while True:
            print("\n=== Sistem Sewa Kamera ===")
            print("1. Lihat Kamera")
            print("2. Stok Kamera")
            print("3. Sewa Kamera")
            print("4. Keluar")
            try:
                pilihan = int(input("Pilih menu: "))
                if pilihan == 1:
                    self.lihat_kamera()
                elif pilihan == 2:
                    self.stok_kamera()
                elif pilihan == 3:
                    self.sewa_kamera()
                elif pilihan == 4:
                    print("Terima kasih telah menggunakan sistem kami!")
                    break
                else:
                    print("Pilihan tidak valid, coba lagi.")
            except ValueError:
                print("Input tidak valid, masukkan angka 1-4.")

if __name__ == "__main__":
    sistem = SistemSewaKamera()
    sistem.jalankan()
class Kamera:
    def _init_(self, id_kamera, nama, stok, harga):
        self.id_kamera = id_kamera
        self.nama = nama
        self.stok = stok
        self.harga = harga

    def tampilkan_info(self):
        return f"ID: {self.id_kamera} | Nama: {self.nama} | Stok: {self.stok} | Harga: Rp{self.harga}/hari"

class DSLR(Kamera):
    def _init_(self, id_kamera, nama, stok, harga, lensa):
        super()._init_(id_kamera, nama, stok, harga)
        self.lensa = lensa

    def tampilkan_info(self):
        return super().tampilkan_info() + f" | Lensa: {self.lensa}"

class Mirrorless(Kamera):
    def _init_(self, id_kamera, nama, stok, harga, berat):
        super()._init_(id_kamera, nama, stok, harga)
        self.berat = berat

    def tampilkan_info(self):
        return super().tampilkan_info() + f" | Berat: {self.berat} kg"

class SistemSewaKamera:
    def _init_(self):
        self.kamera_list = [
            DSLR(1, "Canon EOS 5D", 5, 200000, "24-70mm"),
            Mirrorless(2, "Sony Alpha A7 III", 3, 250000, 0.65),
            DSLR(3, "Nikon Z6", 4, 220000, "35mm"),
        ]

    def lihat_kamera(self):
        print("\nDaftar Kamera:")
        for kamera in self.kamera_list:
            print(kamera.tampilkan_info())

    def stok_kamera(self):
        print("\nStok Kamera:")
        for kamera in self.kamera_list:
            print(f"{kamera.nama}: {kamera.stok} unit tersedia")

    def sewa_kamera(self):
        self.lihat_kamera()
        try:
            id_kamera = int(input("\nMasukkan ID Kamera yang ingin disewa: "))
            jumlah = int(input("Masukkan jumlah unit yang ingin disewa: "))
            hari = int(input("Berapa hari Anda ingin menyewa? "))
            kamera = next((k for k in self.kamera_list if k.id_kamera == id_kamera), None)

            if kamera and kamera.stok >= jumlah:
                total_harga = kamera.harga * jumlah * hari
                kamera.stok -= jumlah
                print(f"\nBerhasil menyewa {jumlah} unit {kamera.nama}.")
                print(f"Total harga sewa untuk {hari} hari: Rp{total_harga}")
            else:
                print("\nStok tidak mencukupi atau kamera tidak ditemukan!")
        except ValueError:
            print("\nInput tidak valid, coba lagi.")

    def jalankan(self):
        while True:
            print("\n=== Sistem Sewa Kamera ===")
            print("1. Lihat Kamera")
            print("2. Stok Kamera")
            print("3. Sewa Kamera")
            print("4. Keluar")
            try:
                pilihan = int(input("Pilih menu: "))
                if pilihan == 1:
                    self.lihat_kamera()
                elif pilihan == 2:
                    self.stok_kamera()
                elif pilihan == 3:
                    self.sewa_kamera()
                elif pilihan == 4:
                    print("Terima kasih telah menggunakan sistem kami!")
                    break
                else:
                    print("Pilihan tidak valid, coba lagi.")
            except ValueError:
                print("Input tidak valid, masukkan angka 1-4.")

if __name__ == "__main__":
    sistem = SistemSewaKamera()
    sistem.jalankan()
