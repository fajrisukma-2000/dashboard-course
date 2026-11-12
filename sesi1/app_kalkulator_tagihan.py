import streamlit as st

st.set_page_config(page_title="Kalkulator Tagihan", page_icon="🧾")

st.title("🧾 Kalkulator Estimasi Tagihan Internet")
st.write("Pilih layanan dan durasi berlangganan untuk menghitung biaya.")

HARGA = {
    "DSL": 260_000,
    "Fiber": 420_000,
    "Mobile Broadband": 310_000,
    "Satelit": 550_000,
}

DISKON = {
    "Bulanan": 0.00,
    "Tahunan": 0.10,
    "Dua Tahun": 0.18,
}

# Inisialisasi penghitung klik.
if "jumlah_hitung" not in st.session_state:
    st.session_state.jumlah_hitung = 0

layanan = st.selectbox("Jenis layanan", list(HARGA))
kontrak = st.radio("Jenis kontrak", list(DISKON), horizontal=True)

bulan = st.number_input(
    "Durasi (bulan)",
    min_value=1,
    max_value=72,
    value=12,
    step=1,
)

promo = st.slider(
    "Diskon promosi tambahan (%)",
    min_value=0,
    max_value=20,
    value=0,
    step=1,
)

ppn = st.checkbox("Tambahkan PPN 11%", value=True)

if st.button("Hitung", type="primary"):
    st.session_state.jumlah_hitung += 1

    # Diskon promo diterapkan setelah diskon kontrak.
    setelah_diskon_kontrak = HARGA[layanan] * (1 - DISKON[kontrak])
    per_bulan = setelah_diskon_kontrak * (1 - promo / 100)

    subtotal = per_bulan * bulan
    pajak = subtotal * 0.11 if ppn else 0
    total = subtotal + pajak

    st.metric(
        "Biaya per bulan sebelum PPN",
        f"Rp{per_bulan:,.0f}".replace(",", "."),
    )
    st.metric(
        "Total estimasi",
        f"Rp{total:,.0f}".replace(",", "."),
    )

    st.caption(
        f"Diskon kontrak: {DISKON[kontrak]:.0%} | "
        f"Diskon promo tambahan: {promo}%"
    )
    st.caption("Estimasi bersifat ilustratif untuk latihan.")

st.write(
    f"Tombol Hitung sudah diklik "
    f"**{st.session_state.jumlah_hitung} kali** dalam sesi ini."
)

st.divider()

st.header("👤 Profil Peserta")

nama = st.text_input("Nama")
divisi = st.selectbox(
    "Divisi",
    ["IT", "Keuangan", "SDM", "Pemasaran", "Operasional"],
)
pengalaman = st.slider(
    "Tahun pengalaman",
    min_value=0,
    max_value=40,
    value=1,
    step=1,
)

if nama.strip():
    st.info(
        f"Nama: {nama.strip()}\n\n"
        f"Divisi: {divisi}\n\n"
        f"Pengalaman: {pengalaman} tahun"
    )
else:
    st.info("Masukkan nama untuk menampilkan ringkasan profil.")