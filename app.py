#this is the back end!
from flask import Flask, render_template, request, redirect, url_for
import sqlalchemy
import flask_sqlalchemy
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/aboutus')
def about():
    return render_template('about.html')

#route for the registration
@app.route('/register')
def register():
   return render_template ('register.html')

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


@app.route('/')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def do_register():
    username = request.form['username']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

    return redirect('users.html')

@app.route('/users')
def users():
    conn = sqlite3.connect('users.db')
    cursors = conn.cursor()
    cursors.execute("SELECT username, created_at FROM users")
    users = cursors.fetchall()
    conn.close()

    return render_template('users.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)


@app.route('/data')
def data():
    return render_template('data.html') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

def run_flask():
    display(Javascript('window.open("/proxy/5000/","_blank")'))
    app.run(host='0.0.0.0', port=5000)

run_flask
 