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

st.title("Temu Kembali Informasi TF-IDF & VSM")
st.write("Melakukan pengujian TF-IDF dan VSM pada data yang sudah diproses")
query = st.text_input("Masukkan query:")