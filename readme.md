  

---

<p align="center">
    <img src="https://github.com/user-attachments/assets/ec28e005-94d6-4e56-9eca-1707c529894f" alt="Foto Anda" style="width: 120px; height: auto;">
    <img src="https://github.com/user-attachments/assets/bee51b14-4232-4e81-b171-686d33b1ea01" alt="Foto Anda" style="width: 500px; height: auto;">
    <img src="https://github.com/user-attachments/assets/06078620-fa57-470b-9eac-f957da614b75" alt="Foto Anda" style="width: 120px; height: auto;">
</p>


###
<div align="center">

# 📸 **Sewa Kamera** - Aplikasi Penyewaan Kamera 🎥

</div>

---

### 🌟 **Apa yang Disediakan?**
Aplikasi ini adalah **Sistem Sewa Kamera** berbasis web yang dibangun menggunakan **Streamlit**. Aplikasi ini menyediakan berbagai fitur menarik untuk memudahkan pengelolaan penyewaan kamera. Berikut fitur-fiturnya:

---

#### 🛠️ **1. Manajemen Kamera**
- **🔍 Lihat Kamera**: Menampilkan daftar kamera yang tersedia dalam bentuk tabel.
- **➕ Tambah Kamera**: Menambahkan kamera baru ke sistem dengan informasi nama, stok, dan harga sewa.
- **✏️ Edit Kamera**: Mengubah data kamera yang sudah ada.
- **🗑️ Hapus Kamera**: Menghapus kamera berdasarkan ID.

#### 🤝 **2. Manajemen Penyewaan Kamera**
- **📋 Sewa Kamera**: 
  - Form pencatatan data penyewaan, validasi stok, dan perhitungan otomatis total biaya.
- **📄 Lihat Penyewa**: Menampilkan daftar penyewa dan detail transaksi.
- **⚙️ Status Penyewa**: Update status penyewaan (Diproses, Selesai, Dibatalkan).
- **🗑️ Hapus Penyewa**: Menghapus data penyewa berdasarkan ID.

#### 📊 **3. Statistik**
- **📈 Grafik Statistik**: Statistik jumlah penyewaan dan total pendapatan.
- **📅 Statistik Bulanan**: Jumlah kamera disewa dan pendapatan bulan ini.

#### ℹ️ **4. Tentang**
- Informasi pembaruan aplikasi, kontak, dan pembuat.

---

### 🌟 **Fitur Tambahan**
- **🎉 Animasi Interaktif**: Efek **toast**, **progress bar**, hingga **balloon** untuk pengalaman yang menyenangkan!
- **✅ Validasi Otomatis**: Input valid dengan pengecekan stok kamera.
- **📱 Antarmuka Responsif**: Antarmuka sederhana, responsif, dan intuitif menggunakan Streamlit.

---

## 🛠️ **Teknologi yang Digunakan**

  <div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" height="40" alt="vscode logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="40" alt="python logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/streamlit/streamlit-original.svg" height="40" alt="Streamlit logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pandas/pandas-original-wordmark.svg" height="40" alt="pandas logo"  />
  <img width="12" />
  <img src="https://skillicons.dev/icons?i=tailwind" height="40" alt="tailwindcss logo"  />
  <img width="12" />
  <img src="https://skillicons.dev/icons?i=sqlite" height="40" alt="sqlite logo"  />
  <img width="12" />
  <img src="https://cdn.simpleicons.org/nginx/009639" height="40" alt="nginx logo"  />
</div>

[🔗 Demo Aplikasi](https://znz-rental-yogyakarta.streamlit.app/)

---

## 🚀 **Instalasi**

### 1. Clone Repository
```bash
git clone https://github.com/zaenalrfn/camera_rental
cd camera_rental
```

### 2. Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Aplikasi
```bash
streamlit run sewa_kamera_gui.py
```

Aplikasi akan berjalan di browser: **`http://localhost:8501`**

---

## 📂 **Struktur Proyek**
```
sewa_kamera/
├── sewa_kamera_gui.py      # Aplikasi utama
├── sewa_kamera.py      # Versi Terminal
├── sewa_kamera.db          # Database SQLite
├── requirements.txt        # Dependensi
└── README.md               # Dokumentasi
```

<div align="center">
  <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2pra2pmbW13cGdsdW82andybTYwZ2FrNDN3MjBjOWlpbXJkYzV2OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/Po8MIT5ohzx3a/giphy.gif" height="200" alt="stats graph"  />
  <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3YwczVpZmk1M2kzc3huczN5YXR1YXowaXA4Y2F6bGZmMzdxdW9vZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/Vf3ZKdillTMOOaOho0/giphy.gif" height="150" alt="stats graph"  />
  <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGlsbG9reHV2azR1Z3dpdHVka3g2bHlhNWJpenFoaGZtYnpoZnc4YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/O0ffU8oLcfiC73k1tP/giphy.gif" height="200" alt="stats graph"  />
    <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2pra2pmbW13cGdsdW82andybTYwZ2FrNDN3MjBjOWlpbXJkYzV2OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/Po8MIT5ohzx3a/giphy.gif" height="200" alt="stats graph"  />

</div>

## 🎓 **Tugas Pemrograman Berbasis Objek Praktik**

### 👩‍🏫 Dosen
- **Ledy Elsera Astrianty, S.Kom., M.Kom**

#### 👥 Kelompok 6
- **Zaenal Arifin**  
- **Zidan Alfiyan Mubarok**  
- **Novanda Rifqi Rajendra**

--- 
