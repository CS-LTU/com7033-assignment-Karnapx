#this is the back end!
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

users = []

# function to connect to the SQLite database and intialize the table
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor
    cursor.execute('''
    CREATE TABLE IF NOT EXSISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXR NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

#ROUTE TO HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')

#ROUTE TO ABOUT PAGE
@app.route('/aboutus')
def about():
    return render_template('about.html')

#ROUTE TO login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        users.append({'username': username, 'password': password}) #cai suggests verification for username and password logic here?
        return redirect(url_for('home'))
    return render_template('login.html')

#ROUTE TO REGISTERATION PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        hashed_passsword = generate_password_hash(password, method='pbkdf2:sha256')

    #INSERT THE NEW USER INTO THE DATABASE
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
          INSERT INTO users (first_name, last_name, email, password) 
          VALUES (?, ?, ?, ?)
    ''', (first_name, last_name, email, hashed_passsword))
    conn.commit()
    conn.close()

    return redirect('/users')
    return render_template('register.html')

#ROUTE TO DISPLAY REGISTERED USERS
@app.route('/users')
def users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, email, created_at FROM users")
    users = cursor.fetchall()
    conn.close()

    return render_template('users.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0',port=8080, debug=True) 
