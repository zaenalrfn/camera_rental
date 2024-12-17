import sqlite3
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime
import time

def init_db():
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    
    # Create kamera table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kamera (
        id INTEGER PRIMARY KEY,
        nama TEXT,
        stok INTEGER,
        harga INTEGER
    )
    """)

    # Create penyewa table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS penyewa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        nomor_telepon TEXT,
        kamera_id INTEGER,
        jumlah INTEGER,
        hari INTEGER,
        total_harga INTEGER,
        tanggal_sewa TEXT,
        tanggal_kembali TEXT,
        status TEXT,
        FOREIGN KEY(kamera_id) REFERENCES kamera(id)
    )
    """)



    cursor.execute("SELECT COUNT(*) FROM kamera")
    if cursor.fetchone()[0] == 0:
        kamera_data = [
            (1, "Canon EOS 5D", 5, 200000),
            (2, "Sony Alpha A7 III", 3, 250000),
            (3, "Nikon Z6", 4, 220000),
        ]
        cursor.executemany("INSERT INTO kamera (id, nama, stok, harga) VALUES (?, ?, ?, ?)", kamera_data)

    conn.commit()
    conn.close()

def lihat_kamera():
    conn = sqlite3.connect("sewa_kamera.db")
    kamera_df = pd.read_sql_query("SELECT * FROM kamera", conn)
    conn.close()
    return kamera_df

def edit_kamera(id_kamera, nama_baru, stok_baru, harga_baru):
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE kamera
    SET nama = ?, stok = ?, harga = ?
    WHERE id = ?
    """, (nama_baru, stok_baru, harga_baru, id_kamera))
    conn.commit()
    conn.close()

def hapus_kamera(id_kamera):
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM kamera WHERE id = ?", (id_kamera,))
    conn.commit()
    conn.close()

def lihat_penyewa():
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM penyewa")
    data = cursor.fetchall()
    penyewa_df = pd.DataFrame(data, columns=["id", "nama", "nomor_telepon", "kamera_id", "jumlah", "hari", "total_harga", "tanggal_kembali", "tanggal_sewa", "status"])
    conn.close()
    return penyewa_df

def sewa_kamera(nama, nomor_telepon, kamera_id, jumlah, hari, tanggal_sewa):
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM kamera WHERE id = ?", (kamera_id,))
    kamera = cursor.fetchone()
    
    if kamera and kamera[2] >= jumlah:
        total_harga = kamera[3] * jumlah * hari
        cursor.execute("UPDATE kamera SET stok = stok - ? WHERE id = ?", (jumlah, kamera_id))

        cursor.execute("""
        INSERT INTO penyewa (nama, nomor_telepon, kamera_id, jumlah, hari, total_harga, tanggal_sewa)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nama, nomor_telepon, kamera_id, jumlah, hari, total_harga, tanggal_sewa))
        
        conn.commit()
        conn.close()
        return True, total_harga
    
    conn.close()
    return False, 0


def hapus_penyewa(penyewa_id):
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM penyewa WHERE id = ?", (penyewa_id,))
    
    conn.commit()
    conn.close()

def edit_penyewa(penyewa_id, nama, nomor_telepon, jumlah, hari):
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE penyewa
    SET nama = ?, nomor_telepon = ?, jumlah = ?, hari = ?
    WHERE id = ?
    """, (nama, nomor_telepon, jumlah, hari, penyewa_id))
    conn.commit()
    conn.close()


from datetime import datetime, timedelta

def update_status(id_penyewa, status):
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    
    try:
        # Retrieve detailed rental information
        cursor.execute("""
            SELECT p.kamera_id, p.jumlah, p.tanggal_sewa, p.hari, p.total_harga, 
                   k.harga AS harga_kamera, p.status
            FROM penyewa p
            JOIN kamera k ON p.kamera_id = k.id
            WHERE p.id = ?
        """, (id_penyewa,))
        rental_info = cursor.fetchone()
        
        if rental_info:
            kamera_id, jumlah_dipinjam, tanggal_sewa, hari_sewa, total_harga, harga_kamera, current_status = rental_info
            
            # Calculate expected return date and current date
            tanggal_sewa = datetime.strptime(tanggal_sewa, "%Y-%m-%d")
            expected_return_date = tanggal_sewa + timedelta(days=hari_sewa)
            current_date = datetime.now()
            
            # Calculate denda (penalty)
            denda = 0
            if current_date > expected_return_date and status == "Selesai":
                days_overdue = (current_date - expected_return_date).days
                denda = days_overdue * harga_kamera  # Denda sebesar harga kamera per hari
                
                # Update total harga with denda
                total_harga_baru = total_harga + denda
                
                # Update penyewa table with new total harga and status
                cursor.execute("""
                    UPDATE penyewa 
                    SET status = ?, total_harga = ?, tanggal_kembali = ?
                    WHERE id = ?
                """, (status, total_harga_baru, current_date.strftime("%Y-%m-%d"), id_penyewa))
                
                # Optional: Add a notification or log about the denda
                print(f"Denda applied: {denda} for {days_overdue} days overdue")
            else:
                # Just update status if no denda
                cursor.execute("""
                    UPDATE penyewa 
                    SET status = ?, tanggal_kembali = ?
                    WHERE id = ?
                """, (status, current_date.strftime("%Y-%m-%d"), id_penyewa))
            
            # If status is 'Selesai', update camera stock
            if status == "Selesai":
                cursor.execute("""
                    UPDATE kamera 
                    SET stok = stok + ? 
                    WHERE id = ?
                """, (jumlah_dipinjam, kamera_id))
        
        # Commit the transaction
        conn.commit()
        
        return denda  # Return denda for potential UI notification
    
    except sqlite3.Error as e:
        # Rollback in case of any error
        conn.rollback()
        print(f"An error occurred: {e}")
        return 0
    
    finally:
        # Always close the connection
        conn.close()

def statistik_sewa_mingguan():
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            CASE
                WHEN strftime('%d', tanggal_sewa) BETWEEN '01' AND '07' THEN 'Minggu ke-1'
                WHEN strftime('%d', tanggal_sewa) BETWEEN '08' AND '14' THEN 'Minggu ke-2'
                WHEN strftime('%d', tanggal_sewa) BETWEEN '15' AND '21' THEN 'Minggu ke-3'
                WHEN strftime('%d', tanggal_sewa) >= '22' THEN 'Minggu ke-4'
            END AS minggu,
            SUM(jumlah) AS total_sewa
        FROM penyewa
        WHERE strftime('%Y-%m', date('now')) = strftime('%Y-%m', tanggal_sewa)
        GROUP BY minggu
        ORDER BY minggu
    """)
    
    result = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in result}

def tampilkan_statistik():
    data_mingguan = statistik_sewa_mingguan()
    data = pd.DataFrame({
        'Minggu': ['Minggu ke-1', 'Minggu ke-2', 'Minggu ke-3', 'Minggu ke-4'],
        'Total Sewa': [
            data_mingguan.get('Minggu ke-1', 0),
            data_mingguan.get('Minggu ke-2', 0),
            data_mingguan.get('Minggu ke-3', 0),
            data_mingguan.get('Minggu ke-4', 0)
        ]
    })
    st.bar_chart(data.set_index('Minggu'))


def statistik_sewa_bulan_ini():
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(jumlah) AS total_sewa_bulan_ini
        FROM penyewa
        WHERE strftime('%Y-%m', date('now')) = strftime('%Y-%m', tanggal_sewa)
    """)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[0] else 0

def tampilkan_statistik():
    total_sewa_bulan_ini = statistik_sewa_bulan_ini()
    data = pd.DataFrame({
        'Bulan': ['Bulan Ini'],
        'Total Sewa': [total_sewa_bulan_ini]
    })
    st.bar_chart(data.set_index('Bulan'))

def statistik_pendapatan_bulan_ini():
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(p.jumlah * k.harga) AS total_pendapatan_bulan_ini
        FROM penyewa p
        JOIN kamera k ON p.kamera_id = k.id
        WHERE strftime('%Y-%m', date('now')) = strftime('%Y-%m', p.tanggal_sewa)
    """)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[0] else 0

def tampilkan_statistik_pendapatan():
    total_pendapatan_bulan_ini = statistik_pendapatan_bulan_ini()
    data = pd.DataFrame({
        'Bulan': ['Bulan Ini'],
        'Total Pendapatan (Rp)': [total_pendapatan_bulan_ini]
    })
    st.bar_chart(data.set_index('Bulan'))

def add_css():
    st.markdown("""
    <style>
    .navbar {
        display: flex;
        justify-content: center;
        background-color: #333;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .navbar .nav-item {
        margin: 0 15px;
        padding: 10px 20px;
        background-color: #555;
        color: white;
        border-radius: 8px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
    }
    .navbar .nav-item:hover {
        background-color: #777;
    }
    </style>
    """, unsafe_allow_html=True)


def tentang():
    st.subheader("Tentang Aplikasi")
    html_content = """
    <style>
        .frosted-glass {
            background: rgba(255, 255, 255, 0.6); /* White with 60% opacity */
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px); /* Frosted glass effect */
            -webkit-backdrop-filter: blur(10px); /* Safari support */
        }
        .frosted-glass p, .frosted-glass a {
            color: #000; /* Ensure text is readable on the frosted background */
        }
        .version {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #007BFF; /* Blue color for the version text */
            margin-bottom: 20px;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
        }
        .marquee {
            position: fixed;
            bottom: 0;
            width: 100%;
            background: blue;
            padding: 10px;
            box-shadow: 0 -4px 8px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px); /* Frosted glass effect */
            -webkit-backdrop-filter: blur(10px); /* Safari support */
            font-size: 20px;
            text-align: center;
            overflow: hidden;
        }
        .marquee-content {
            display: inline-block;
            white-space: nowrap;
            animation: marquee 15s linear infinite;
            color: white;
        }
        @keyframes marquee {
            from { transform: translateX(100%); }
            to { transform: translateX(-100%); }
        }
    </style>
    <div class="frosted-glass">
        <div class="version">Versi Aplikasi: 1.0.0</div>
        <p>Aplikasi sederhana untuk memudahkan mengelola rental kamera.</p>
        <p><strong>Tim Pembuat:</strong> Kelompok 6</p>
        <p><strong>Source code :</strong></p>
        <a href="https://github.com/zaenalrfn/camera_rental" style="text-decoration: none;">
            <img src="https://img.shields.io/badge/GitHub-Profile-blue?logo=github" alt="GitHub">
        </a>
    </div>
    <div class="marquee">
        <div class="marquee-content">Universitas Teknologi Yogyakarta | Universitas Teknologi Yogyakarta | Universitas Teknologi Yogyakarta | </div>
    </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)

# ini Menu ya...
def main():
    add_css()  

    # Menu dengan sub-menu
    selected_menu = option_menu(
        menu_title="Sistem Sewa Kamera",
        options=["Kamera", "Sewa", "Statistik", "Tentang"],
        icons=["camera", "box", "bar-chart", "info-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    # Submenu berdasarkan pilihan menu
    if selected_menu == "Kamera":
        submenu_kamera = option_menu(
            menu_title="Kamera",
            options=["Lihat Kamera", "Tambah Kamera", "Edit Kamera", "Hapus Kamera"],
            icons=["eye", "plus-circle", "pen", "trash"],
            menu_icon="camera-retro",
            default_index=0,
            orientation="horizontal"
        )
        
              # Lihat Kamera
        if submenu_kamera == "Lihat Kamera":
            st.header("📷 Daftar Kamera")
            kamera_df = lihat_kamera()
            st.dataframe(kamera_df)

        # Tambah Kamera
        elif submenu_kamera == "Tambah Kamera":
            st.header("📥 Tambah Kamera")
            nama_kamera = st.text_input("Nama Kamera")
            stok = st.number_input("Stok Kamera", min_value=1, step=1)
            harga = st.number_input("Harga Sewa per Hari", min_value=1, step=1000)
            if st.button("Tambah Kamera"):
                conn = sqlite3.connect("sewa_kamera.db")
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO kamera (nama, stok, harga) VALUES (?, ?, ?)
                """, (nama_kamera, stok, harga))
                conn.commit()
                conn.close()
                st.balloons()
                st.success("Kamera berhasil ditambahkan!")
                st.toast('Sukses Menambahkan ...')

        # Edit Kamera
        elif submenu_kamera == "Edit Kamera":
            st.header("✏️ Edit Kamera")
            kamera_df = lihat_kamera()
            st.dataframe(kamera_df)

            # Memilih ID kamera untuk diedit
            id_kamera = st.selectbox("Pilih ID Kamera untuk Diedit", kamera_df['id'])
            nama_baru = st.text_input("Nama Baru Kamera")
            stok_baru = st.number_input("Stok Baru Kamera", min_value=1, step=1)
            harga_baru = st.number_input("Harga Baru Kamera", min_value=1, step=1000)

            if st.button("Simpan Perubahan"):
                edit_kamera(id_kamera, nama_baru, stok_baru, harga_baru)
                st.success("Data kamera berhasil diperbarui!")
                st.balloons()
                st.toast('Sukses Edit ...' ,icon="✅")

        # Hapus Kamera
        elif submenu_kamera == "Hapus Kamera":
            st.header("🗑️ Hapus Kamera")
            kamera_df = lihat_kamera()
            st.dataframe(kamera_df)

            # Memilih ID kamera untuk dihapus
            id_kamera = st.selectbox("Pilih ID Kamera untuk Dihapus", kamera_df['id'])
            if st.button("Hapus Kamera"):
                hapus_kamera(id_kamera)
                st.snow()
                st.warning(f"Kamera dengan ID {id_kamera} berhasil dihapus!")

    elif selected_menu == "Sewa":
        submenu_sewa = option_menu(
            menu_title="Sewa",
            options=["Sewa Kamera", "Lihat Penyewa", "Status", "Hapus"],
            icons=["clipboard", "eye", "clock", "trash"],
            menu_icon="hand-holding-box",
            default_index=0,
            orientation="horizontal"
        )
        
        if submenu_sewa == "Sewa Kamera":
            st.header("📥 Form Sewa Kamera")

            # Input data penyewa
            nama = st.text_input("Nama Penyewa")
            nomor_telepon = st.text_input("Nomor Telepon")

            # Menampilkan daftar kamera
            kamera_df = lihat_kamera()  # Mengambil daftar kamera
            kamera_dict = {row['nama']: row['id'] for index, row in kamera_df.iterrows()}
            kamera_pilihan = st.selectbox("Pilih Kamera", list(kamera_dict.keys()))

            # Input jumlah unit dan durasi sewa
            jumlah = st.number_input("Jumlah Unit", min_value=1, step=1)
            hari = st.number_input("Durasi Sewa (hari)", min_value=1, step=1)

            # Menambahkan input tanggal sewa
            tanggal_sewa = st.date_input("Tanggal Sewa", min_value=datetime.today().date())

            if st.button("Sewa"):
                kamera_id = kamera_dict[kamera_pilihan]

                # Memanggil fungsi sewa_kamera dengan parameter tambahan tanggal_sewa
                sukses, total_harga = sewa_kamera(nama, nomor_telepon, kamera_id, jumlah, hari, tanggal_sewa)

                if sukses:
                    st.success(f"Kamera berhasil disewa! Total harga: Rp{total_harga}")
                    st.toast('Berhasil sewa ...' , icon="✅")
                else:
                    st.error("Stok kamera tidak cukup", icon="🚨")
                    st.toast('Stok kosong ...' , icon="⚠️")
        elif submenu_sewa == "Lihat Penyewa":
            st.header("📊 Daftar Penyewa")
            penyewa_df = lihat_penyewa()
            st.dataframe(penyewa_df)
        elif submenu_sewa == "Status":
            st.header("📝 Edit Status Penyewa")

            # Menampilkan daftar penyewa
            penyewa_df = lihat_penyewa()
            penyewa_dict = {f"ID {row['id']} - {row['nama']}": row['id'] for index, row in penyewa_df.iterrows()}
            penyewa_pilihan = st.selectbox("Pilih Penyewa", list(penyewa_dict.keys()))

            # Mengambil ID penyewa yang dipilih
            penyewa_id = penyewa_dict[penyewa_pilihan]
            
            # Menampilkan status penyewa yang dipilih
            status = penyewa_df[penyewa_df['id'] == penyewa_id]['status'].values[0]
            
            # Validasi status, jika status tidak ada dalam daftar opsi, pilih default ("Diproses")
            valid_statuses = ["Diproses", "Selesai", "Dibatalkan"]
            if status not in valid_statuses:
                status = "Diproses"  

            new_status = st.selectbox("Pilih Status", valid_statuses, index=valid_statuses.index(status))

            # Tombol untuk memperbarui status
            if st.button("Update Status"):
                denda = update_status(penyewa_id, new_status)

                progress_text = "Sedang menyimpan. Tunggu."
                my_bar = st.progress(0, text=progress_text)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)

                time.sleep(1)
                my_bar.empty()

                with st.spinner('Tunggu sebentar...'):
                    time.sleep(4)

                st.toast('Selesai' , icon="✅")

                if denda > 0:
                    st.warning(f"Denda dikenakan: Rp {denda:,} karena keterlambatan pengembalian")

                st.success(f"Status penyewa dengan ID {penyewa_id} berhasil diperbarui menjadi {new_status}")

        elif submenu_sewa == "Hapus":
            st.header("❌ Hapus Penyewa")

            # Menampilkan daftar penyewa
            penyewa_df = lihat_penyewa()
            penyewa_dict = {f"ID {row['id']} - {row['nama']}": row['id'] for index, row in penyewa_df.iterrows()}
            penyewa_pilihan = st.selectbox("Pilih Penyewa yang Akan Dihapus", list(penyewa_dict.keys()))

            # Mengambil ID penyewa yang dipilih
            penyewa_id = penyewa_dict[penyewa_pilihan]

            # Konfirmasi hapus data penyewa
            if st.button("Hapus Penyewa"):
                hapus_penyewa(penyewa_id)
                st.success(f"Penyewa dengan ID {penyewa_id} telah dihapus.")
                with st.spinner('Tunggu sebentar...'):time.sleep(4)
                st.toast('Done ...' , icon="✅")


    elif selected_menu == "Statistik":
        st.header("📊 Statistik Bulan Ini")
        
        # Statistik Jumlah Sewa
        st.subheader("📈 Statistik Jumlah Sewa (Bulan Ini)")
        tampilkan_statistik() 
        total_sewa = statistik_sewa_mingguan()
        st.write(f"Jumlah sewa bulan ini: **{total_sewa} unit kamera**")
        
        # Statistik Pendapatan
        st.subheader("💰 Statistik Pendapatan (Bulan Ini)")
        tampilkan_statistik_pendapatan()  
        total_pendapatan = statistik_pendapatan_bulan_ini()
        st.write(f"Total pendapatan bulan ini: **Rp{total_pendapatan:,.0f}**")
    

    elif selected_menu == "Tentang":
        tentang()

if __name__ == "__main__":
    init_db()
    main()
