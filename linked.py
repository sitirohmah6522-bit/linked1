import streamlit as st
from datetime import datetime
import pandas as pd
from io import BytesIO
import streamlit as st
from datetime import datetime

# LOGIN ADMIN
def login_admin():
    st.title("🔐 Login Admin SIGMALINK")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "12345":
            st.session_state["login"] = True
            st.success("Login berhasil!")
            st.rerun()
        else:
            st.error("Username atau password salah!")

if "login" not in st.session_state:
    st.session_state["login"] = False

if st.session_state["login"] == False:
    login_admin()
    st.stop()
    
with st.sidebar:
    st.write("👤 Login sebagai Admin")
    if st.button("Logout"):
        st.session_state["login"] = False
        st.rerun()

class BarangNode:
    def __init__(self, kode, nama, kategori, stok, harga):
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.stok = stok
        self.harga = harga
        self.next = None


class GudangLinkedList:
    def __init__(self):
        self.head = None
        self.riwayat = []

    def tambah_riwayat(self, aktivitas):
        waktu = datetime.now()
        self.riwayat.append({
            "Tanggal": waktu.strftime("%d-%m-%Y"),
            "Waktu": waktu.strftime("%H:%M:%S"),
            "Aktivitas": aktivitas
    })
    def tambah_barang(self, kode, nama, kategori, stok, harga):
        node_baru = BarangNode(kode, nama, kategori, stok, harga)

        if self.head is None:
            self.head = node_baru
        else:
            bantu = self.head
            while bantu.next is not None:
                bantu = bantu.next
            bantu.next = node_baru

        self.tambah_riwayat(f"Menambahkan barang {nama} sebanyak {stok}")

    def tampilkan_barang(self):
        data = []
        bantu = self.head

        while bantu is not None:
            data.append({
                "Kode Barang": bantu.kode,
                "Nama Barang": bantu.nama,
                "Kategori": bantu.kategori,
                "Stok": bantu.stok,
                "Harga": bantu.harga,
                "Total Nilai": bantu.stok * bantu.harga
            })
            bantu = bantu.next

        return data

    def cari_by_kode(self, kode):
        bantu = self.head
        while bantu is not None:
            if bantu.kode.lower() == kode.lower():
                return bantu
            bantu = bantu.next
        return None

    def cari_barang(self, kata_kunci):
        hasil = []
        bantu = self.head

        while bantu is not None:
            if bantu.kode.lower().startswith(kata_kunci.lower()) or bantu.nama.lower().startswith(kata_kunci.lower()):
                hasil.append(bantu)
            bantu = bantu.next

        return hasil

    def tambah_stok(self, kode, jumlah):
        barang = self.cari_by_kode(kode)
        if barang:
            barang.stok += jumlah
            self.tambah_riwayat(f"Stok {barang.nama} bertambah {jumlah}")
            return True
        return False

    def kurangi_stok(self, kode, jumlah):
        barang = self.cari_by_kode(kode)
        if barang:
            if barang.stok >= jumlah:
                barang.stok -= jumlah
                self.tambah_riwayat(f"Stok {barang.nama} berkurang {jumlah}")
                return "berhasil"
            return "stok_kurang"
        return "tidak_ditemukan"

    def edit_barang(self, kode, nama_baru, kategori_baru, stok_baru, harga_baru):
        barang = self.cari_by_kode(kode)
        if barang:
            barang.nama = nama_baru
            barang.kategori = kategori_baru
            barang.stok = stok_baru
            barang.harga = harga_baru
            self.tambah_riwayat(f"Data barang {kode} berhasil diedit")
            return True
        return False

    def hapus_barang(self, kode):
        bantu = self.head

        if bantu is not None and bantu.kode.lower() == kode.lower():
            self.tambah_riwayat(f"Barang {bantu.nama} dihapus")
            self.head = bantu.next
            return True

        sebelumnya = None
        while bantu is not None:
            if bantu.kode.lower() == kode.lower():
                self.tambah_riwayat(f"Barang {bantu.nama} dihapus")
                sebelumnya.next = bantu.next
                return True
            sebelumnya = bantu
            bantu = bantu.next

        return False

    def stok_menipis(self):
        data = []
        bantu = self.head

        while bantu is not None:
            if bantu.stok <= 5:
                data.append({
                    "Kode Barang": bantu.kode,
                    "Nama Barang": bantu.nama,
                    "Stok": bantu.stok
                })
            bantu = bantu.next

        return data

    def statistik_gudang(self):
        total_barang = 0
        total_stok = 0
        total_nilai = 0
        stok_terbanyak = None
        stok_tersedikit = None

        bantu = self.head

        while bantu is not None:
            total_barang += 1
            total_stok += bantu.stok
            total_nilai += bantu.stok * bantu.harga

            if stok_terbanyak is None or bantu.stok > stok_terbanyak.stok:
                stok_terbanyak = bantu

            if stok_tersedikit is None or bantu.stok < stok_tersedikit.stok:
                stok_tersedikit = bantu

            bantu = bantu.next

        return total_barang, total_stok, total_nilai, stok_terbanyak, stok_tersedikit


st.set_page_config(page_title="Sistem Gudang Retail", page_icon="📦")

st.title("📦 SIGMALINK ( Sistem Informasi Gudang Manajemen Aset )")
st.write("SIGMALINK merupakan sistem informasi gudang yang dirancang untuk membantu proses pengelolaan inventaris secara lebih cepat, akurat, dan terorganisir. Aplikasi ini memudahkan pengguna dalam memantau stok barang, mengelola data inventaris, serta mendokumentasikan aktivitas gudang secara efisien.")
st.write("✅ Menyediakan riwayat aktivitas yang terstruktur.")
st.write("✅ Meningkatkan efisiensi operasional gudang.")
st.write("✅ Menghemat waktu pengelolaan stok barang.")
st.write("✅ Mengurangi risiko kesalahan pencatatan.")
st.write("✅ Mempermudah pencarian data.")

if "gudang" not in st.session_state:
    st.session_state.gudang = GudangLinkedList()

kategori_list = ["Makanan", "Minuman", "Snack", "Sembako", "Peralatan", "Lainnya"]

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "➕ Tambah",
    "📋 Lihat",
    "🔍 Cari",
    "📥 Tambah Stok",
    "➖ Kurangi Stok",
    "✏️ Edit/Hapus",
    "⚠️ Stok Menipis",
    "📊 Statistik",
    "🕒 Riwayat"
])

with tab1:
    st.subheader("Tambah Data Barang")

    kode = st.text_input("Kode Barang")
    nama = st.text_input("Nama Barang")
    kategori = st.selectbox("Kategori Barang", kategori_list)
    stok = st.number_input("Stok Barang", min_value=0, step=1)
    harga = st.number_input("Harga Barang", min_value=0, step=500)

    if st.button("Tambah Barang"):
        if kode and nama:
            if st.session_state.gudang.cari_by_kode(kode):
                st.warning("Kode barang sudah ada.")
            else:
                st.session_state.gudang.tambah_barang(kode, nama, kategori, stok, harga)
                st.success("Barang berhasil ditambahkan!")
        else:
            st.warning("Kode dan nama barang harus diisi.")


with tab2:
    st.subheader("Data Barang Gudang")

    data = st.session_state.gudang.tampilkan_barang()

    if data:
        st.table(data)

        df = pd.DataFrame(data)

        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(
                writer,
                index=False,
                sheet_name="Data Gudang"
            )

        st.download_button(
            label="📥 Export Data Excel",
            data=output.getvalue(),
            file_name="SIGMALINK_Data_Gudang.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.info("Belum ada data barang.")

with tab3:
    st.subheader("Cari Cepat Barang")
    kata_kunci = st.text_input("Masukkan minimal 3 huruf kode atau nama")

    if len(kata_kunci) >= 3:
        hasil = st.session_state.gudang.cari_barang(kata_kunci)

        if hasil:
            data_hasil = []
            for barang in hasil:
                data_hasil.append({
                    "Kode Barang": barang.kode,
                    "Nama Barang": barang.nama,
                    "Kategori": barang.kategori,
                    "Stok": barang.stok,
                    "Harga": barang.harga,
                    "Total Nilai": barang.stok * barang.harga
                })
            st.success("Barang ditemukan!")
            st.table(data_hasil)
        else:
            st.error("Barang tidak ditemukan.")
    elif kata_kunci:
        st.warning("Masukkan minimal 3 huruf.")


with tab4:
    st.subheader("Tambah Stok Barang")

    kode_tambah = st.text_input("Kode Barang Tambah Stok")
    jumlah_tambah = st.number_input("Jumlah Stok Masuk", min_value=1, step=1)

    if st.button("Proses Tambah Stok"):
        berhasil = st.session_state.gudang.tambah_stok(kode_tambah, jumlah_tambah)

        if berhasil:
            st.success("Stok berhasil ditambahkan.")
        else:
            st.error("Barang tidak ditemukan.")


with tab5:
    st.subheader("Kurangi Stok Barang")

    kode_kurang = st.text_input("Kode Barang Kurangi Stok")
    jumlah_kurang = st.number_input("Jumlah Stok Keluar", min_value=1, step=1)

    if st.button("Proses Kurangi Stok"):
        hasil = st.session_state.gudang.kurangi_stok(kode_kurang, jumlah_kurang)

        if hasil == "berhasil":
            st.success("Stok berhasil dikurangi.")
        elif hasil == "stok_kurang":
            st.warning("Stok tidak mencukupi.")
        else:
            st.error("Barang tidak ditemukan.")


with tab6:
    st.subheader("Edit dan Hapus Barang")

    kode_edit = st.text_input("Masukkan Kode Barang yang Ingin Diedit / Dihapus")
    barang_edit = st.session_state.gudang.cari_by_kode(kode_edit)

    if barang_edit:
        nama_baru = st.text_input("Nama Baru", value=barang_edit.nama)
        kategori_baru = st.selectbox(
            "Kategori Baru",
            kategori_list,
            index=kategori_list.index(barang_edit.kategori)
        )
        stok_baru = st.number_input("Stok Baru", min_value=0, step=1, value=barang_edit.stok)
        harga_baru = st.number_input("Harga Baru", min_value=0, step=500, value=barang_edit.harga)

        if st.button("Simpan Perubahan"):
            berhasil = st.session_state.gudang.edit_barang(
                kode_edit, nama_baru, kategori_baru, stok_baru, harga_baru
            )

            if berhasil:
                st.success("Data barang berhasil diedit.")

        if st.button("Hapus Barang"):
            berhasil = st.session_state.gudang.hapus_barang(kode_edit)

            if berhasil:
                st.success("Barang berhasil dihapus.")
                st.rerun()

    elif kode_edit:
        st.error("Barang tidak ditemukan.")


with tab7:
    st.subheader("Notifikasi Stok Menipis")

    data_menipis = st.session_state.gudang.stok_menipis()

    if data_menipis:
        st.warning("Ada barang dengan stok menipis!")
        st.table(data_menipis)
    else:
        st.success("Tidak ada stok yang menipis.")


with tab8:
    st.subheader("Statistik Gudang")

    total_barang, total_stok, total_nilai, terbanyak, tersedikit = st.session_state.gudang.statistik_gudang()

    st.write("Total Jenis Barang:", total_barang)
    st.write("Total Seluruh Stok:", total_stok)
    st.write("Total Nilai Gudang: Rp", total_nilai)

    if terbanyak:
        st.write("Stok Terbanyak:", terbanyak.nama, "-", terbanyak.stok)

    if tersedikit:
        st.write("Stok Tersedikit:", tersedikit.nama, "-", tersedikit.stok)


with tab9:
    st.subheader("Riwayat Transaksi")

    if st.session_state.gudang.riwayat:
        st.table(st.session_state.gudang.riwayat)
    else:
        st.info("Belum ada riwayat transaksi.")


tab_laporan = st.tabs(["📅 Laporan Per Tanggal"])[0]

with tab_laporan:
    st.header("📅 Laporan Aktivitas Per Tanggal")

    tanggal_pilih = st.date_input("Pilih tanggal laporan")
    tanggal_format = tanggal_pilih.strftime("%d-%m-%Y")

    data_laporan = [
        r for r in st.session_state.gudang.riwayat
        if r["Tanggal"] == tanggal_format
    ]

    if data_laporan:
        st.success(f"Data laporan tanggal {tanggal_format}")
        st.table(data_laporan)
    else:
        st.warning(f"Tidak ada aktivitas pada tanggal {tanggal_format}")
    
