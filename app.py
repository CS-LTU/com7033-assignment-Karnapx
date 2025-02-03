#this is the back end!
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

#function to connect to the 2nd SQLITE database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS USERS (
        id INTERGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
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

@app.route('/register', methods=['GET', 'POST'])
def do_register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (first_name, last_name, email, password, created_at)
                     VALUES (?, ?, ?, ?)''', 
                  (first_name, last_name, email, hashed_password))
        conn.commit()
        conn.close()
    
    return redirect(url_for('success', first_name=first_name))
    return render_template('register.html')

#ROUTE FOR THE SUCCESS PAGE 
@app.route('/success/<first_name>')
def success(first_name):
    return f"User {first_name} registered successfully!"

#ROUTE TO DISPLAY REGISTERED USERS
@app.route('/users')
def list_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, first_name, last_name, email, created_at FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users)

#route ti delete a user by ID
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id))
    conn.commit
    conn.close
    return redirect(url_for('list_users'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0',port=5000, debug=True) 
