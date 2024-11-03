# Panduan Penggunaan Proyek

Proyek ini adalah aplikasi dashboard berbasis Python untuk menganalisis data dari file CSV yang disediakan. Proyek ini menggunakan Streamlit untuk membuat antarmuka dashboard interaktif.

## Struktur Proyek

- **dashboard/**: Folder berisi file untuk menjalankan dashboard.
  - `dashboard.py`: File utama yang menjalankan aplikasi dashboard.
  - `func.py`: File berisi fungsi-fungsi pendukung untuk dashboard.
  - `requirements.txt`: File daftar pustaka yang dibutuhkan untuk menjalankan aplikasi.
- **data/**: Folder berisi data yang diperlukan oleh aplikasi.
  - `all_data.csv`: File utama berisi data yang akan dianalisis.
  - `geolocation.csv`: Data tambahan terkait geolokasi.

## Prasyarat

Proyek ini memerlukan Python versi 3.9 atau lebih baru. Untuk menjalankan aplikasi dengan benar, disarankan menggunakan *virtual environment* agar pustaka yang diinstal terisolasi.

## Cara Menggunakan

### 1. Siapkan Environment

1. Clone repository ini ke komputer lokal Anda menggunakan perintah berikut:
     
   ```bash
   git clone https://github.com/Fiqry-Wahyu-Diky/project-dicoding-data-analis.git
   
3. Install pustaka yang diperlukan:
   ```bash
   pip install streamlit
   pip install -r dashboard/requirements.txt

### 2. Menjalankan aplikasi
#### Online
Anda bisa menjalankan aplikasi melalui online dengan mengeklik link di bawah ini:

https://e-commerceanalysis.streamlit.app/


#### Offline
Untuk secara offline jalankan perintah berikut:
1. Masuk ke direktori lokal yang sudah diclone:
``` bash
cd project-dicoding-data-analis/dashboard
streamlit run dashboard.py
