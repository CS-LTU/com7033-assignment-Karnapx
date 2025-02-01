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
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
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
def do_register():
   username = request.form['username']
   conn = sqlite3.connect('users.db')
   cursor = conn.cursor()
   cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
   conn.commit()
   conn.close()

   return redirect('/users')

#ROUTE TO DISPLAY REGISTERED USERS
@app.route('/users')
def list_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, created_at FROM users")
    users = cursor.fetchall()
    conn.close()

    return render_template('users.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0',port=5000, debug=True) 
