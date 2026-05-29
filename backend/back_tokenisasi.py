import pandas as pd
import string
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def bersihkan_teks(teks, stemmer, stopword_list):
    # A. Case Folding
    teks_lower = teks.lower()

    # B & C. Menghapus tanda baca (kecuali strip)
    tanda_baca_dihapus = string.punctuation.replace('-', '')
    tabel_translasi = str.maketrans('', '', tanda_baca_dihapus)
    teks_tanpa_baca = teks_lower.translate(tabel_translasi)

    # D. Tokenisasi
    tokens = teks_tanpa_baca.split()

    # E. Cleaning & Seleksi Angka/Kata Penitng
    tokens_hasil_seleksi = []
    for token in tokens:
        # Aturan 1: Jika berupa angka murni (misal: '2022', '2024', '1', '5')
        if token.isdigit():
            # Hanya pertahankan jika itu Angka Tahun (panjangnya tepat 4 digit)
            if len(token) == 4:
                tokens_hasil_seleksi.append(token)
            # Angka murni lain yang tidak penting (angka halaman, urutan tunggal) otomatis dibuang
            else:
                continue

        # Aturan 2: Jika kata mengandung kombinasi huruf & angka (misal: 'dosis-1', 'np-afp-3')
        elif any(char.isdigit() for char in token):
            tokens_hasil_seleksi.append(token) # Dipertahankan karena ini istilah penting

        # Aturan 3: Jika kata biasa (tidak mengandung angka murni)
        else:
            tokens_hasil_seleksi.append(token)

    # F. Stopword & Stemming
    tokens_tanpa_stopword = [token for token in tokens_hasil_seleksi if token not in stopword_list]
    tokens_final = [stemmer.stem(token) for token in tokens_tanpa_stopword]

    return tokens_final