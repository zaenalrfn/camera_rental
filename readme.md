<p align="center">
    <img src="https://github.com/user-attachments/assets/ec28e005-94d6-4e56-9eca-1707c529894f" alt="Foto Anda" style="width: 120px; height: auto;">
    <img src="https://github.com/user-attachments/assets/bee51b14-4232-4e81-b171-686d33b1ea01" alt="Foto Anda" style="width: 500px; height: auto;">
    <img src="https://github.com/user-attachments/assets/06078620-fa57-470b-9eac-f957da614b75" alt="Foto Anda" style="width: 120px; height: auto;">
</p>

# Sewa Kamera - Aplikasi Penyewaan Kamera

Sewa Kamera adalah aplikasi sederhana untuk mengelola penyewaan kamera. Pengguna dapat melihat daftar kamera yang tersedia, menambah, mengedit, dan menghapus kamera, serta melihat daftar penyewa yang telah melakukan peminjaman. Aplikasi ini menggunakan SQLite sebagai database dan Streamlit sebagai antarmuka pengguna.

## Fitur

- **Lihat Daftar Kamera**: Melihat daftar kamera yang tersedia untuk disewa.
- **Tambah Kamera**: Menambah data kamera baru ke dalam sistem.
- **Edit Kamera**: Mengubah data kamera yang sudah ada.
- **Hapus Kamera**: Menghapus kamera dari sistem.
- **Lihat Daftar Penyewa**: Menampilkan daftar penyewa yang telah melakukan penyewaan kamera.

## Teknologi yang Digunakan

- **Streamlit**: Untuk membangun antarmuka pengguna yang interaktif.
- **SQLite**: Database ringan untuk menyimpan data kamera dan penyewa.
- **Pandas**: Untuk memanipulasi dan menampilkan data dalam bentuk tabel.

## Instalasi

### 1. Clone Repository

Clone proyek ini ke komputer Anda dengan perintah berikut:

```bash
git clone https://github.com/zaenalrfn/camera_rental
cd repository-name
```

### 2. Membuat dan Mengaktifkan Virtual Environment

Untuk menghindari konflik dengan dependensi lain, buatlah virtual environment terlebih dahulu:

```bash
python -m venv venv
source venv/bin/activate  # Untuk Linux/macOS
venv\Scripts\activate     # Untuk Windows
```

### 3. Instalasi Dependensi

Instal dependensi yang dibutuhkan dengan pip:

```bash
pip install -r requirements.txt
```

### 4. Menjalankan Aplikasi

Setelah menginstal semua dependensi, Anda dapat menjalankan aplikasi dengan perintah:

```bash
streamlit run sewa_kamera_gui.py
```

Aplikasi akan berjalan di browser Anda pada `http://localhost:8501`.

## Struktur Proyek

```
sewa_kamera/
├── sewa_kamera_gui.py      # File utama aplikasi Streamlit 
├── sewa_kamera.db          # Database SQLite untuk menyimpan data kamera dan penyewa
├── requirements.txt        # Daftar dependensi yang dibutuhkan
├── rental_camera.py        # ini hanya di jalankan di terminal
└── README.md               # Dokumentasi proyek
```

# Tugas Pemrograman Berbasis Objek Praktik

### Dosen

- **Ledy Elsera Astrianty, S.Kom., M.Kom**

#### Kelompok 6

- **Zaenal Arifin**
- **Zidan Alfiyan Mubarok**
- **Novanda Rifqi Rajendra**



