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



tokenisasi =  st.Page("Preprocessing/tokenisasi.py", title="Tokenisasi", icon=":material/edit_square:")

tfidf_vsm = st.Page("Search/tfidf_vsm.py", title="TF-IDF & VSM", icon=":material/search:")
importData = st.Page("Preprocessing/import.py", title="Import Data", icon=":material/file_upload:")
Indexing = st.Page("Preprocessing/Indexing.py", title="Indexing", icon=":material/text_compare:")
pg = st.navigation(
    {
        "Preprocessing": [tokenisasi, Indexing],
        "Search": [tfidf_vsm],
        "Import Data": [importData]
    }
)
pg.run()

