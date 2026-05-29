import io
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
from backend.back_tokenisasi import bersihkan_teks

st.title("Tokenisasi")
st.write("Melakukan preprocessing data dengan tahapan tokenisasi, case folding, stopword removal, dan stemming")

if 'hasil_proses' not in st.session_state:
    st.session_state['hasil_proses'] = None

def prepare_sastrawi():
    time.sleep(2)
    factory_stemmer = StemmerFactory()
    stemmer = factory_stemmer.create_stemmer()
    factory_stopword = StopWordRemoverFactory()
    stopword_list = factory_stopword.get_stop_words()
    stopword_list.extend(['paling', 'berbahaya', 'di', 'tahun', 'yang', 'dan', 'atau'])
    return stemmer, stopword_list


with st.spinner("Mempersiapkan Sastrawi..."):
    stemmer, stopword_list = prepare_sastrawi()
    st.session_state['hasil_proses'] = stemmer, stopword_list
    
st.success("Sastrawi siap digunakan!")

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

if st.button("Lanjut ke Tokenisasi"):
    if st.session_state['hasil_proses'] is not None and 'df_data' in st.session_state:
        stemmer, stopword_list = st.session_state['hasil_proses']
        df_data = st.session_state['df_data']
        if 'Isi' not in df_data.columns:
            st.error("Kolom 'Isi' tidak ditemukan pada data.")
        else:
            with st.spinner("Memproses tokenisasi..."):
                df_data['hasil'] = df_data['Isi'].fillna('').astype(str).apply(
                    lambda x: bersihkan_teks(x, stemmer, stopword_list)
                )
            st.success("Tokenisasi selesai!")
            st.write("Hasil Tokenisasi:")
            st.dataframe(df_data[['hasil']])

            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df_data.to_excel(writer, index=False, sheet_name='Hasil Tokenisasi')
            buffer.seek(0)

            filename = "tokenisasi_hasil.xlsx"
            if 'file_terpilih' in st.session_state:
                base_name = os.path.splitext(st.session_state['file_terpilih'])[0]
                filename = f"tokenisasi_{base_name}.xlsx"
            st.download_button(
                label="Download Hasil Tokenisasi",
                data=buffer,
                file_name=filename,
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    else:
        st.error("Pastikan Sastrawi sudah siap dan data sudah dibaca sebelum melanjutkan ke tokenisasi.")
else:
    st.info("Silakan pilih file dan klik 'Baca File' untuk memulai proses tokenisasi.")

