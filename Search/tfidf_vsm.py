import streamlit as st
import pandas as pd
import numpy as np
import string
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.back_tfidf import cari_dokumen
from backend.back_tfidf import buat_matriks_tfidf as buat_tfidf_matriks



st.title("Temu Kembali Informasi TF-IDF & VSM")
st.write("Melakukan pengujian TF-IDF dan VSM pada data yang sudah diproses")
query = st.text_input("Masukkan query:")

if st.button("Cari"):
    if not query or query.strip() == "":
        st.warning("Silakan masukkan query sebelum menekan tombol Cari.")
    else:
        df_hasil = cari_dokumen(query)
        df_hasil.insert(0, 'No', range(1, len(df_hasil) + 1))
        st.subheader("Hasil Pencarian Dokumen")
        st.dataframe(df_hasil)

        df_matriks = buat_tfidf_matriks()
        st.subheader("Matriks TF-IDF Dokumen")
        st.dataframe(df_matriks)
