from flask import Flask, request, redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barangku.db'
db = SQLAlchemy(app)
# membuat tabel database


class Databarang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_barang = db.Column(db.String(200), nullable=False)
    jumlah_barang = db.Column(db.Integer, nullable=False)
    harga_barang = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id


@app.route('/')
def home():
    return render_template("blog/home.html")

    # delet data


@app.route('/delete/<int:id>')
def delete(id):
    deleteedata = Databarang.query.get_or_404(id)

    try:
        db.session.delete(deleteedata)
        db.session.commit()
        return redirect('/blog')
    except:
        return " Gagal menghapus  Data ....!!"


# update data


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    updatedata = Databarang.query.get_or_404(id)
    if request.method == "POST":
        updatedata.nama_barang = request.form['namabarang']
        updatedata.jumlah_barang = request.form['jumlahbarang']
        updatedata.harga_barang = request.form['hargabarang']
        try:
            db.session.commit()
            return redirect('/blog')
        except:
            return " Gagal mengupdate  Data ....!!"
    else:
        return render_template("blog/update.html", updatedata=updatedata)

# input data


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == "POST":

        barang_nama = request.form['namabarang']
        barang_jumla = request.form['jumlahbarang']
        barang_harga = request.form['hargabarang']
        hasil = Databarang(nama_barang=barang_nama,
                           jumlah_barang=barang_jumla, harga_barang=barang_harga)
        try:
            db.session.add(hasil)
            db.session.commit()
            return redirect('/blog')
        except:
            return " Gagal memasukan Data ....!!"
    else:
        outputnya = Databarang.query.order_by(Databarang.date_created)
        return render_template("blog/blog.html", outputnya=outputnya)


if __name__ == "__main__":
    app.run(debug=True)
