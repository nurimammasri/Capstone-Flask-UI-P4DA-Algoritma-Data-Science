from flask import Flask, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import base64

matplotlib.use('Agg')
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import matplotlib.colors as mcolors

app = Flask(__name__)

playstore = pd.read_csv("data/googleplaystore.csv")

playstore.drop_duplicates(subset="App", keep='first', inplace=True)

# bagian ini untuk menghapus row 10472 karena nilai data tersebut tidak tersimpan pada kolom yang benar
playstore.drop([10472], inplace=True)

playstore.Category = playstore.Category.astype("category")

playstore.Installs = playstore.Installs.apply(lambda x: x.replace(",", ""))
playstore.Installs = playstore.Installs.apply(lambda x: x.replace("+", ""))
playstore.Installs = playstore.Installs.astype("int64")

# Bagian ini untuk merapikan kolom Size, Anda tidak perlu mengubah apapun di bagian ini
playstore['Size'].replace('Varies with device', np.nan, inplace=True)
playstore.Size = (playstore.Size.replace(r'[kM]+$', '', regex=True).astype(float) *
                  playstore.Size.str.extract(r'[\d\.]+([kM]+)', expand=False)
                  .fillna(1)
                  .replace(['k', 'M'], [10**3, 10**6]).astype(int))
playstore['Size'].fillna(playstore.groupby('Category')[
                         'Size'].transform('mean'), inplace=True)

playstore["Price"] = playstore["Price"].apply(lambda x: x.replace("$", ""))
playstore["Price"] = playstore["Price"].astype("float64")

# Ubah tipe data Reviews, Size, Installs ke dalam tipe data integer
playstore[['Reviews', 'Size', 'Installs']] = playstore[[
    'Reviews', 'Size', 'Installs']].astype('int64')


@app.route("/")
# This fuction for rendering the table
def index():
    df2 = playstore.copy()

    # Statistik
    top_category = pd.crosstab(
        index=df2["Category"],
        columns="Jumlah"
    ).sort_values("Jumlah", ascending=False).reset_index()
    # Dictionary stats digunakan untuk menyimpan beberapa data yang digunakan untuk menampilkan nilai di value box dan tabel
    stats = {
        'most_categories': top_category.Category.iloc[0],
        'total': top_category.Jumlah.iloc[0],
        'rev_table': df2.groupby(["Category", "App"]).agg({
            "Reviews": "sum",
            "Rating": "mean"
        }).sort_values("Reviews", ascending=False).reset_index().head(10).to_html(classes=['table thead-light table-striped table-bordered table-hover table-sm'])
    }

    # Bar Plot
    cat_order = df2.groupby('Category').agg({
        'Category': 'count'
    }).rename({'Category': 'Total'}, axis=1).sort_values("Total", ascending=False).head()
    X = cat_order.index
    Y = cat_order.Total
    my_colors = ['r', 'g', 'b', 'k', 'y', 'm', 'c']
    # bagian ini digunakan untuk membuat kanvas/figure
    fig = plt.figure(figsize=(8, 3), dpi=300)
    fig.add_subplot()
    # bagian ini digunakan untuk membuat bar plot
    plt.barh(X, Y, color=my_colors)
    # bagian ini digunakan untuk menyimpan plot dalam format image.png
    plt.savefig('cat_order.png', bbox_inches="tight")

    # bagian ini digunakan untuk mengconvert matplotlib png ke base64 agar dapat ditampilkan ke template html
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    # variabel result akan dimasukkan ke dalam parameter di fungsi render_template() agar dapat ditampilkan di
    # halaman html
    result = str(figdata_png)[2:-1]

    # Scatter Plot
    X = df2["Reviews"].values  # axis x
    Y = df2["Rating"].values  # axis y
    # ukuran besar/kecilnya lingkaran scatter plot
    area = playstore["Installs"].values/10000000
    fig = plt.figure(figsize=(5, 5))
    fig.add_subplot()
    # isi nama method untuk scatter plot, variabel x, dan variabel y
    plt.scatter(x=X, y=Y, s=area, alpha=0.3)
    plt.xlabel('Reviews')
    plt.ylabel('Rating')
    plt.savefig('rev_rat.png', bbox_inches="tight")

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result2 = str(figdata_png)[2:-1]

    # Histogram Size Distribution
    X = (df2["Size"]/1000000).values
    fig = plt.figure(figsize=(5, 5))
    fig.add_subplot()
    plt.hist(X, bins=100, density=True,  alpha=0.75)
    plt.xlabel('Size')
    plt.ylabel('Frequency')
    plt.savefig('hist_size.png', bbox_inches="tight")

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result3 = str(figdata_png)[2:-1]

    # Buatlah sebuah plot yang menampilkan insight di dalam data
    pstore = playstore.copy()
    pstore[['Content Rating', 'Genres']] = pstore[[
        'Content Rating', 'Genres']].astype('category')
    paid_pstore = pstore[pstore['Type'] != 'Free'].copy()
    paid_pstore['Income'] = paid_pstore['Price']*paid_pstore['Installs']

    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    top_selling = paid_pstore.groupby(["Category"]).agg({
        "App": "count",
        "Installs": "sum",
        "Income": "sum"
    }).sort_values("Income", ascending=False).head(10)
    top_selling["Income_Label"] = top_selling["Income"].apply(
        lambda x: str(round(x/10**6, 2))+"M")

    top_selling.sort_values("Income", inplace=True)
    data = list((top_selling['Income']/10**6).values)

    my_norm = Normalize(vmin=0, vmax=max(data))

    cmap = mcolors.LinearSegmentedColormap.from_list(
        "my_map", ["red", "yellow", "green"])
    colors = cmap(my_norm(data))

    X = top_selling.index
    Y = top_selling['Income']
    fig, ax = plt.subplots(figsize=(7, 7))
    plt.title('Category Aplikasi Berbayar dengan Income Tertinggi')
    plt.xlabel('Income')
    plt.ylabel('Category')
    my_colors = ['r', 'g', 'b', 'k', 'y', 'm', 'c']
    g = ax.barh(X, Y, color=colors)
    _, xmax = plt.xlim()
    ax.set_xlim(0, xmax+(xmax/8))
    ax.bar_label(g, labels=top_selling['Income_Label'], padding=10)
    plt.tight_layout()
    plt.savefig('income_order.png', bbox_inches="tight")

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result4 = str(figdata_png)[2:-1]

    # Tambahkan hasil result plot pada fungsi render_template()
    return render_template('index.html', stats=stats, result=result, result2=result2, result3=result3, result4=result4)


if __name__ == "__main__":
    app.run(debug=True)
