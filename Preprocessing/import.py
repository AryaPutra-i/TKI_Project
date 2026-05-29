import streamlit as st
import pandas as pd
import os

st.title("Import Data")
st.write("Import data dari file yang diunggah")

folder_tujuan = "file_hasil_upload"
if not os.path.exists(folder_tujuan):
    os.makedirs(folder_tujuan)

def file_terunggah():
    st.toast("File berhasil diunggah!")

file_unggah = st.file_uploader(
    label="Pilih atau tarik file ke sini",
    type=["csv", "txt", "xlsx"],
    accept_multiple_files=False,
    key="uploader_data",
    help="hanya menerima file dengan format csv, txt, atau xlsx",
    on_change=file_terunggah
)

if file_unggah:
    st.write(f"File yang diunggah: {file_unggah.name}")
    # Simpan file ke folder tujuan
    jalur_simpan = os.path.join(folder_tujuan, file_unggah.name)
    with open(jalur_simpan, "wb") as f:
        f.write(file_unggah.getbuffer())
    st.success(f"File berhasil disimpan di {jalur_simpan}")
    st.info(f"Silakan cek folder **{folder_tujuan}** di sebelah kiri layar VS Code Anda.")