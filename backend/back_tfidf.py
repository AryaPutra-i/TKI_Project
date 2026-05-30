import pandas as pd
import string
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math
import numpy as np
from backend.back_tokenisasi import bersihkan_teks

stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

factory = StopWordRemoverFactory()
stopword_list = factory.get_stop_words()

stopword_list.extend(['paling', 'berbahaya', 'di', 'tahun', 'yang', 'dan', 'atau'])

df = pd.read_excel("file_hasil_upload/tokenisasi_raw_data.xlsx")
df_inverted_index = pd.read_excel("file_hasil_upload/indexing_hasil.xlsx")
df_inverted_index['Posting_list_dict'] = df_inverted_index['Posting_list (Dokumen:Frekuensi)'].apply(ast.literal_eval)
inverted_index_siap_pakai = dict(zip(df_inverted_index['Kata'], df_inverted_index['Posting_list_dict']))
print(inverted_index_siap_pakai)

total_dokumen = len(df)
bobot_tfidf_dokumen = {} 
    
for token, posting_list in inverted_index_siap_pakai.items():
    df_term = len(posting_list)
    idf = math.log10(total_dokumen / df_term) if df_term > 0 else 0

    for doc_id, tf_mentah in posting_list.items():
        if doc_id not in bobot_tfidf_dokumen:
            bobot_tfidf_dokumen[doc_id] = {}

        tf_log = 1 + math.log10(tf_mentah) if tf_mentah > 0 else 0
        bobot_tfidf_dokumen[doc_id][token] = tf_log * idf


def cari_dokumen(query):
    tokens_query = bersihkan_teks(query, stemmer, stopword_list)
    tf_query_mentah = {}
    for token in tokens_query:
        tf_query_mentah[token] = tf_query_mentah.get(token, 0) + 1
    bobot_tfidf_query = {}
    for token, tf_mentah in tf_query_mentah.items():
        df_term = len(inverted_index_siap_pakai[token])
        idf = math.log10(total_dokumen / df_term) if df_term > 0 else 0
        tf_log = 1 + math.log10(tf_mentah) if tf_mentah > 0 else 0
        bobot_tfidf_query[token] = tf_log * idf
    
    skor_cosine_dokumen = {}
    panjang_vector_query = math.sqrt(sum(bobot ** 2 for bobot in bobot_tfidf_query.values()))
    for doc_id in range(1, total_dokumen + 1):
        dot_product = 0.0
        panjang_vector_dokumen = 0.0

        kata_dokumen = bobot_tfidf_dokumen.get(doc_id, {})
        for token in bobot_tfidf_query:
            if token in kata_dokumen:
                dot_product += bobot_tfidf_query[token] * kata_dokumen[token]
        for token in kata_dokumen:
            panjang_vector_dokumen += kata_dokumen[token] ** 2
        panjang_vector_dokumen = math.sqrt(panjang_vector_dokumen)

        pembagi = panjang_vector_query * panjang_vector_dokumen
        if pembagi > 0:
            skor_cosine_dokumen[doc_id] = dot_product / pembagi
        else:
            skor_cosine_dokumen[doc_id] = 0.0
    
    df_hasil = pd.DataFrame({
        'Dokumen': df['Dokumen'],
        'Isi_teks': df['Isi'],
        'Similarity_score': df['Dokumen'].map(skor_cosine_dokumen)
    })

    df_hasil = df_hasil.sort_values(by='Similarity_score', ascending=False)
    return df_hasil

def buat_matriks_tfidf():
    daftar_kata_manual = sorted(list(inverted_index_siap_pakai.keys()))
    matriks_angka_manual = []
    for doc_id in range(1, total_dokumen + 1):
        baris_bobot = []
        kata_dokumen = bobot_tfidf_dokumen.get(doc_id, {})

        for kata in daftar_kata_manual:
            baris_bobot.append(kata_dokumen.get(kata, 0.0))
        matriks_angka_manual.append(baris_bobot)
    
    df_tfidf_baru = pd.DataFrame(matriks_angka_manual, columns=daftar_kata_manual)
    df_tfidf_baru.insert(0, 'ID_Dokumen', range(1, total_dokumen + 1))
    return df_tfidf_baru



            
    