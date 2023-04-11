# Google Play Store Analytics

### **Nama : Nur Imam Masri**
### **Vulcan Scholarship Algoritma Academy**

<img src="https://raw.githubusercontent.com/nurimammasri/Capstone-Flask-UI-P4DA-Algoritma-Data-Science/main/full_capstone.jpeg">

## Introduction
Projek ini dikembangkan sebagai salah satu capstone project dari Algoritma Academy Data Analytics Specialization. Deliverables yang diharapkan adalah Anda dapat membangun sebuah aplikasi web sederhana (dashboard) menggunakan framework Flask. Capstone ini akan fokus pada tampilan user interface Flask. 

## Data Summary
Data yang digunakan pada capstone project ini adalah data hasil scraping dari Google Playstore App. Data Google Playstore App terdiri dari beberapa variabe dengan rincian sebagai berikut:
- `App` : Nama aplikasi                
- `Category` : Kategori aplikasi
- `Rating` : Rating keseluruhan yang diberikan oleh user aplikasi(ketika di scrap)
- `Reviews` : Jumlah review yang diberikan oleh user aplikasi(ketika di scrap)
- `Size` : Ukuran aplikasi(ketika di scrap)           
- `Installs` : Jumlah user yang menginstall/mendownload aplikasi(Ketika di scrap)     
- `Type` : Tipe aplikasi (berbayar/gratis)       
- `Price` : Harga aplikasi (ketika di scrap)        
- `Content Rating` : Kelompok usia aplikasi ini ditargetkan - Children / Mature 21+ / Adult   
- `Genres` : Genre aplikasi.        
- `Last Updated` : Tanggal kapan aplikasi terakhir diperbarui di Play Store (ketika discrap) 
- `Current Ver` : Versi aplikasi saat ini tersedia di Play Store (ketika discrap)   
- `Android Ver` : Minimum versi Android yang diperlukan (ketika discrap) 

## Dependencies
- Flask
- Matplotlib
- Pandas
- Numpy

## Rubrics
Pada capstone ini, Anda diharapkan untuk dapat membangun sebuah aplikasi Flask yang fokus pada tampilan user interface. Langkah pertama yang harus Anda lakukan adalah silahkan download atau clone repositori ini. File pada repositori ini merupakan sebuah skeleton untuk membuat sebuah dashboard aplikasi Flask. Pada bagian [`app.py`](https://github.com/nurimammasri/Capstone-Flask-UI-P4DA-Algoritma-Data-Science/blob/main/app.py) dan [`templates/index.html`](https://github.com/nurimammasri/Capstone-Flask-UI-P4DA-Algoritma-Data-Science/blob/main/templates/index.html) ada beberapa bagian yang rumpang dan harus Anda lengkapi. Untuk Notes template nya bisa di cek pada [`flask-ui-skeleton-template.ipynb`](https://github.com/nurimammasri/Capstone-Flask-UI-P4DA-Algoritma-Data-Science/blob/main/flask-ui-skeleton-template.ipynb). Beberapa bagian yang harus diperhatikan adalah sebagai berikut:

### 1. Setting Repository Github dan Environment (2 poin)
- Repository 

a. Membuat repository baru di Github

b. Clone repository tersebut ke local dengan git clone
- Environment 

a. Created virtual environment called "capstone-flask"

Hal pertama yang harus dilakukan adalah melakukan pengaturan environment conda. Untuk menyiapkan conda environment dan kernel, silahkan gunakan command berikut:
```
conda create -n <ENV_NAME> python=3.10
conda activate <ENV_NAME>

conda install ipykernel
python -m ipykernel install --user --name <ENV_NAME>
```

b. Install packages: pandas, flask, matplotlib, dan numpy

Seluruh dependecies telah di-export ke dalam file requirements.txt. Oleh karena itu untuk melakukan install packages, Anda dapat menggunakan perintah berikut:
```
pip install -r requirements.txt --user
```

### 2. Data Preproses and Exploratory Data Analysis (2 poin)
Pada tahap praproses ini, Anda diminta untuk melengkapi praproses data seperti menghapus data yang duplikat, mengubah tipe data dan memodifikasi nilai data. Pada file [`app.py`](https://github.com/nurimammasri/Capstone-Flask-UI-P4DA-Algoritma-Data-Science/blob/main/app.py) Anda diminta untuk melengkapi data yang rumpang tanpa mengubah alur praproses yang telah ada.
Berikut ini contoh bagian yang harus Anda lengkapi saat praproses data:
```
playstore._________(subset ="_____", keep = '_____', inplace=True) 
playstore.drop([10472], inplace=True)
# Buang tanda koma(,) dan tambah(+) kemudian ubah tipe data menjadi integer
playstore.Category = playstore.Category.astype('category')
playstore.Installs = ________.apply(lambda x: x.replace(______))
playstore.Installs = ________.apply(lambda x: x.replace(______))
```
### 3. Data Wrangling (4 poin)
- Pada tahap ini Anda diminta untuk melakukan grouping dan agregasi data. Data wrangling digunakan untuk menyiapkan data yang tepat sesuai analisis yang diminta. Pada capstone ini terdapat objek dictionary dengan nama `stats` dan Anda diminta untuk melengkapi bagian yang rumpang agar menghasilkan data/nilai yang sesuai. Sebagai gambaran pada objek `stats` terdapat variabel `rev_tablel` dimana Anda harus melakukan grouping dan agregasi data yang digunakan untuk membuat data table seperti di bawah ini:
<img src="https://raw.githubusercontent.com/fafilia/capstone-UIFlask/master/table_rev.PNG" width=400>

### 4. Data Visualization (4 poin)
- Membuat atau menduplikasi bar plot yang menggambarkan top 5 Category pada Google Playstore
- Membuat atau menduplikasi scatter plot yang menggambarkan sebaran aplikasi jika dilihat berdasarkan Review, Rating, dan jumlah aplikasi yang terinstall.
- Membuat atau menduplikasi histogram plot untuk melihat distribusi ukuran aplikasi 
- Membuat 1 plot tambahan bebas yang dapat merepresentasikan insight di dalam data

*Notes : Anda dapat melihat contoh plot lain yang hraus dibuat/diduplikat pada repositori ini. Silahkan clone/download repositori ini. 

### 5. Build Flask App (4 poin)
Mengacu pada poin ke empat Data Visualization di atas, selain membuat plot baru Anda harus mendemonstrasikan bagaimana cara merender plot tersebut pada aplikasi Flask dan menampilkannya pada templates / halaman html. Yang perlu Anda perhatikan adalah pada bagian [`app.py`](https://github.com/nurimammasri/Capstone-Flask-UI-P4DA-Algoritma-Data-Science/blob/main/app.py):
```
render_templates(__________)
```
dan pada `templates/index.html` Anda perlu memanggil source plot.png tempat Anda menyimpan gambar plot tersebut.
```
<img src="________________________" height="450" width=500>
```

### 6. Run Flask App
1. `Clone repository` tersebut ke local dengan git clone - Environment
2. Bka `app.py` dan select interpreter sesuai kernel `<ENV>` yang telah dibuat
3. Buka terminal (cmd/anaconda prompt) dan activate env `conda activate <ENV>`
4. Masuk ke folder project dan jalankan `python app.py` pada terminal, maka akan men-generate link server untuk membuka website
5. klik pada link `Running on http://127.0.0.1:5000/` atau link yang ada pada device anda
6. Done :)