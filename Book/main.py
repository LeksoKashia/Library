from flask import Flask, redirect, url_for, render_template, request,session,flash,abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from datetime import timedelta
from logging import FileHandler,WARNING

import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
from random import randrange
import sqlite3
# page = 1
# while page < 2:
#     t12 = ()
#     tuple12 = ()
#     book_href_list = []
#     book_list = []
#
#     url = 'https://biblusi.ge/products?category=291&category_id=309&page=' + str(page)
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     sub_soup = soup.find('div', class_="row")
#     books = sub_soup.find_all('div', class_="mb-1_875rem col-sm-4 col-md-3 col-xl-2 col-6")
#
#     for each in books:
#         img_url = each.a.div.attrs.get('style').strip("background-image:url('")[:-3]
#         book = each.div.acronym.text
#         price = each.find('div', class_='text-primary font-weight-700').text
#         price = price.replace(' ', '').replace('\n', '')
#         book_url = each.a.get('href')
#         tuple1 = tuple12+(book,)
#         tuple2 = tuple1+(price,)
#         tuple3 = tuple2+(img_url,)
#         tuple4 = tuple3+('https://biblusi.ge'+book_url,)
#         book_list.append(tuple4)
#     page += 1
#
#
# conn = sqlite3.connect("Biblusi_books.sqlite")
# cursor = conn.cursor()
# cursor.execute('''CREATE TABLE  if not exists  Biblusi_books
#                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                       book VARCHAR(30),
#                       price INTEGER,
#                       img_url VARCHAR(300),
#                       book_url VARCHAR(40))''')
#
# cursor.executemany("INSERT INTO Biblusi_books (book,price,img_url,book_url) VALUES (?,?,?,?)", book_list)
#
# conn.commit()
# conn.close()


app = Flask(__name__)

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
app.logger.addHandler(file_handler)

app.config['SECRET_KEY'] = 'Key'
app.permanent_session_lifetime = timedelta(days=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Biblusi_books.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Biblusi_books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(300), nullable=False)
    book_url = db.Column(db.String(40), nullable=False)

    def __str__(self):
        return f'Book title:{self.book}; Price: {self.price}; I mg_url: {self.img_url}; Book_url{self.book_url}'


books = Biblusi_books.query.all()
tuple12 = ()
book_list = []
for i in books:
    tuple1 = tuple12+(i.book,)
    tuple2 = tuple1+(i.price,)
    tuple3 = tuple2+(i.img_url,)
    tuple4 = tuple3+(i.book_url, )
    book_list.append(tuple4)




@app.route('/')
@app.route('/home')
def home():
    book_list1 = book_list
    return render_template('index.html',book_list=book_list1)

@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
        session.permanent = True
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        age = request.form['age']
        phone = request.form['phone']
        session['email'] = email
        session['username'] = username
        session['password'] = password
        session['address'] = address
        session['age'] = age
        session['phone'] = phone
        return redirect(url_for('home'))

    return render_template('signin.html')



@app.route('/remove',methods=['POST','GET'])
def remove():
    if request.method == 'POST':
        booke = request.form['book']
        if booke == '':
            flash('შეიტანეთ სათაური','error')
        else:
            Biblusi_books.query.filter_by(book=booke).delete()
            db.session.commit()
            flash('წარმატებით წაიშალა წიგნი','info')

    return render_template('remove.html')


@app.route('/add',methods=['POST','GET'])
def add():
    if request.method == 'POST':
        id = request.form['id']
        b = request.form['book1']
        p = request.form['price']
        iu = request.form['img_url']
        bu = request.form['book_url']
        if id == '' or b == '' or p == '' or iu == '' or bu == '':
            flash('აუცილებელია ყველა ველის შეტანა','danger')
        elif not p.isdecimal():
            flash("რიცხვია საჭირო ფასის ველში",'warning')
        else:
            b1 = Biblusi_books(id=id,book=b, price=float(p), img_url=iu, book_url=bu)
            db.session.add(b1)
            db.session.commit()
            flash('წიგნი ატვირთულია','success')


    return render_template('add.html')



@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logout.html')
    else:
        abort(500)


@app.route('/books', methods=['GET', 'POST'])
def books():
    return render_template('books.html')


if __name__ == "__main__":
    app.run(debug=True)