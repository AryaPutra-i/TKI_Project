# Aplikasi Temu Kembali Informasi (TF-IDF & VSM)

Aplikasi berbasis web ini dibuat menggunakan **Streamlit** untuk melakukan proses Temu Kembali Informasi (*Information Retrieval*). Aplikasi ini menerapkan metode pemodelan **TF-IDF** (Term Frequency-Inverse Document Frequency) dan **Vector Space Model (VSM)** (menggunakan *Cosine Similarity*) untuk mencari dan mengurutkan dokumen yang relevan berdasarkan kueri pengguna.

Aplikasi ini dilengkapi dengan tahapan yang lengkap mulai dari persiapan data hingga pencarian:
- **Import Data**: Fasilitas untuk mengunggah dataset dokumen.
- **Tokenisasi (Preprocessing)**: Tahap pembersihan teks yang meliputi *case folding*, penghapusan tanda baca, *stopword removal*, dan *stemming* kata ke bentuk dasar (dioptimalkan menggunakan library Python **Sastrawi**).
- **Indexing**: Tahapan untuk membuat struktur data *Inverted Index* dari kumpulan dokumen yang telah diproses untuk mempercepat sistem pencarian.
- **Search (TF-IDF & VSM)**: Mesin pencarian yang menghitung bobot kueri dan menampilkan skor kemiripan (*similarity score*) ke masing-masing dokumen.

---

## Persyaratan (Prerequisites)
Pastikan Anda telah menginstal **Python** (disarankan versi 3.8 ke atas) di perangkat/komputer Anda.

## Instalasi Library Lingkungan

1. Buka Terminal, Command Prompt, atau PowerShell.
2. Arahkan direktori (gunakan perintah `cd`) ke folder proyek ini.
3. Instal semua dependensi dan *library* yang dibutuhkan dengan menjalankan perintah berikut:
   
   ```bash
   pip install streamlit pandas numpy Sastrawi scikit-learn xlsxwriter openpyxl
   ```
   
*(Catatan: `xlsxwriter` dan `openpyxl` dibutuhkan karena aplikasi banyak membaca dan mengekspor/mengunduh file dalam format Excel (.xlsx).)*

---

## Cara Penggunaan

### 1. Menjalankan Aplikasi Web
Buka terminal di direktori utama proyek, kemudian jalankan perintah:
```bash
streamlit run app.py
```
Browser default Anda akan terbuka secara otomatis dan menampilkan antarmuka web aplikasi.

### 2. Mengunggah Data (Import Data)
- Pada *sidebar* (bilah navigasi kiri), pilih menu **Import Data**.
- Unggah file dataset Anda yang berformat `.csv`, `.xlsx`, atau `.txt`.
- **Penting:** Pastikan dataset yang Anda unggah memiliki kolom bernama `Isi` yang memuat teks dokumen utama untuk diproses.

### 3. Memproses Teks (Tokenisasi)
- Beralih ke menu **Tokenisasi** di *sidebar*.
- Pilih file yang baru saja Anda unggah dari kotak pilihan (*selectbox*), lalu klik **Baca File**.
- Setelah data tertampil, klik **Lanjut ke Tokenisasi**. Proses ini mungkin membutuhkan waktu karena sistem memuat kamus *Sastrawi*.
- Anda dapat melihat hasil bersihan (token) dan mengunduhnya ke dalam format `.xlsx`.

### 4. Melakukan Indexing
- Beralih ke menu **Indexing**.
- Pilih file data yang ingin dibuat *Inverted Index*-nya (umumnya dataset yang sudah bersih/ditokenisasi).
- Klik **Baca File**, kemudian klik **Lanjut ke indexing**.
- Tabel *Inverted Index* beserta daftar *Posting List* akan dibuat secara otomatis.

### 5. Mencari Informasi (TF-IDF & VSM)
- Beralih ke menu **TF-IDF & VSM**.
- Masukkan kata kunci atau kalimat pertanyaan (*query*) yang ingin Anda cari pada kolom teks.
- Klik tombol **Cari**.
- Aplikasi akan menampilkan daftar dokumen hasil pencarian yang diurutkan dari skor relevansi (Cosine Similarity) tertinggi ke terendah, serta menampilkan visualisasi Matriks TF-IDF di bagian bawah halaman.