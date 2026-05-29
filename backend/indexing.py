import pandas as pd
import string
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def parse_list(teks):
  try:
    return ast.literal_eval(teks)
  except(ValueError, SyntaxError):
    return str(teks).split()
  
def indexing_proces(data):
    data['tokens'] = data['hasil'].apply(parse_list)
    forward_index = {}
    inverse_index = {}
    for index, baris in data.iterrows():
       doc_id = baris['Dokumen']
       tokens = baris['tokens'] 
       forward_index[doc_id] = tokens

       for token in tokens:
          if token not in inverse_index:
             inverse_index[token]={}
          if doc_id not in inverse_index[token]:
             inverse_index[token][doc_id]=1
          else:
             inverse_index[token][doc_id]+=1
    
    data_laporan = []
    for kata, posting_list in inverse_index.items():
       data_laporan.append({
          'Kata': kata,
          'Posting_list (Dokumen:Frekuensi)': str(posting_list),
          'total_dokumen': len(posting_list)
       })
    df_laporan = pd.DataFrame(data_laporan)
    df_laporan = df_laporan.sort_values(by='total_dokumen', ascending=False).reset_index(drop=True)
    return df_laporan



