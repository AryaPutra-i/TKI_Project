import streamlit as st
import pandas as pd
import string
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import os
from backend.indexing import indexing_proces
import io

st.title("Melakukan Indexing")
st.write("Melakukan indexing pada data yang sudah diproses untuk memudahkan pencarian informasi")

daftar_file = [file for file in os.listdir("file_hasil_upload") if file.endswith((".csv", ".txt", ".xlsx"))]
if len(daftar_file) > 0:
    file_terpilih = st.selectbox("Pilih file untuk diproses:", daftar_file)
    st.write(f"File yang dipilih: {file_terpilih}")
    if st.button("Baca File"):
        jalur_lengkap = os.path.join("file_hasil_upload", file_terpilih)

        with st.spinner("Membaca file..."):
            if file_terpilih.endswith(".csv"):
                data = pd.read_csv(jalur_lengkap)
            elif file_terpilih.endswith(".xlsx"):
                data = pd.read_excel(jalur_lengkap)
        st.success("File berhasil dibaca!")
        st.write("Tampilkan data:")
        st.dataframe(data)
        st.session_state['df_data'] = data
        st.session_state['file_terpilih'] = file_terpilih
else:
    st.warning("Tidak ada file yang diunggah. Silakan unggah file terlebih dahulu di halaman Import Data.")

if st.button("Lanjut ke indexing"):
    if st.session_state['df_data'] is not None:
        df_data = st.session_state['df_data']
        file_terpilih = st.session_state['file_terpilih']
        with st.spinner("Melakukan indexing..."):
            time.sleep(2)
            hasil_indexing = indexing_proces(df_data)
        st.success("Indexing selesai!")
        st.write("Hasil Indexing:")
        st.dataframe(hasil_indexing)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            hasil_indexing.to_excel(writer, index=False, sheet_name='Hasil Indexing')
        buffer.seek(0)

        filename = "indexing_hasil.xlsx"
        if 'file_terpilih' in st.session_state:
            nama_file_asli = os.path.splitext(st.session_state['file_terpilih'])[0]
            filename = f"{nama_file_asli}_indexing_hasil.xlsx"
        st.download_button(
            label="Download Hasil Indexing",
            data=buffer,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("Data belum tersedia. Silakan baca file terlebih dahulu.")
else:
    st.info("Klik tombol 'baca file' untuk memulai proses indexing setelah membaca file.")