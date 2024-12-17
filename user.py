import sqlite3
import streamlit as st

def get_kamera_data():
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama, stok, harga FROM kamera")
    data = cursor.fetchall()
    conn.close()
    return data

def update_stok(kamera_id, jumlah):
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE kamera SET stok = stok - ? WHERE id = ?", (jumlah, kamera_id))
    conn.commit()
    conn.close()


def insert_penyewa(nama, nomor_telepon, kamera_id, jumlah, hari, total_harga, tanggal_sewa):
    conn = sqlite3.connect("sewa_kamera.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO penyewa (nama, nomor_telepon, kamera_id, jumlah, hari, total_harga, tanggal_sewa, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nama, nomor_telepon, kamera_id, jumlah, hari, total_harga, tanggal_sewa, "Pending"))
    conn.commit()
    conn.close()

def main():
    st.set_page_config(page_title="ZNZ Rental Camera Luxury")
    st.title("ZNZ Luxury Camera Rental")
    st.write("Berikut adalah daftar kamera yang tersedia untuk disewa:")

    kamera_data = get_kamera_data()

    # Gambar kamera (dummy links)
    # Data kamera dengan link gambar (Anda bisa mengganti link ini dengan gambar yang sesuai)
    kamera_images = {
        2: "https://www.bhphotovideo.com/images/images1000x1000/sony_ilce7k_b_a7_mirrorless_digital_camera_1008113.jpg",
        3: "https://www.shutterbug.com/images/styles/600_wide/public/Nikon%20Z6%20Product1.jpg",
        1: "https://th.bing.com/th/id/OIP.2ewPvAlmOFp9wmJjHt3lVwHaHa?rs=1&pid=ImgDetMain",
        4: "https://th.bing.com/th/id/OIP.QgpEqeFFHBHRgdwEOf8YcAAAAA?rs=1&pid=ImgDetMain",
        5: "https://th.bing.com/th/id/OIP.0epAq7v64RLV3DmygsHj6QHaHa?rs=1&pid=ImgDetMain",
        6: "https://th.bing.com/th/id/OIP.CKS5k7Gk9WTH2C7jESYX-wHaHa?rs=1&pid=ImgDetMain",
        7: "https://www.fotohits.de/fileadmin/kameratests/fotohits/leica_vlux5/leica_vlux5_slant.jpg",
        8: "https://img1.kakaku.k-img.com/Images/news_icv/640/2020031/20200312165839_650_.jpg",
        9: "https://images-fe.ssl-images-amazon.com/images/I/517YRMK6ATL.jpg"
    }

    for kamera in kamera_data:
        kamera_id, nama, stok, harga = kamera

        # Container untuk setiap item kamera
        with st.container():
            col1, col2 = st.columns([1, 2], gap="large")

            with col1:
                st.image(kamera_images.get(kamera_id, 'https://via.placeholder.com/150'), width=250, caption=nama)

            with col2:
                st.subheader(nama)
                st.write(f"**Harga Sewa:** Rp{harga:,} per hari")
                st.write(f"**Stok Tersedia:** {stok} unit")

                # Tombol Pesan
                if st.button("Pesan", key=f"pesan_{kamera_id}"):
                    st.session_state[f"show_form_{kamera_id}"] = True

                # Status stok
                if stok == 0:
                    st.write("**Status:** Tidak Tersedia")

            # Menampilkan form pemesanan di bawah item
            if st.session_state.get(f"show_form_{kamera_id}", False):
                with st.form(f"form_pesan_{kamera_id}"):
                    st.write(f"**Form Pemesanan untuk {nama}**")
                    nama_penyewa = st.text_input("Nama Anda")
                    nomor_telepon = st.text_input("Nomor Telepon")
                    jumlah = st.number_input("Jumlah Unit", min_value=1, max_value=stok, value=1)
                    hari = st.number_input("Jumlah Hari", min_value=1, value=1)
                    tanggal_sewa = st.date_input("Tanggal Sewa")

                    # Total harga
                    total_harga = jumlah * hari * harga
                    st.write(f"**Total Harga: Rp{total_harga:,}**")

                    # Tombol Submit
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        if jumlah > stok:
                            st.error("Jumlah unit melebihi stok yang tersedia!")
                        else:
                            insert_penyewa(nama_penyewa, nomor_telepon, kamera_id, jumlah, hari, total_harga, str(tanggal_sewa))
                            update_stok(kamera_id, jumlah)
                            st.success(f"Berhasil memesan {nama} untuk {hari} hari!")
                            st.session_state[f"show_form_{kamera_id}"] = False

            # Garis pemisah antar item
            st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()