#this is the back end!
from flask import Flask, render_template, request, redirect, url_for
import sqlite3 
import os

app = Flask(__name__)

#function to connect the sqlite database and initislize the table
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id iINTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP        
    )
    ''') 
conn.commit()
conn.close()

users = []

#route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for the about us page
@app.route('/aboutus')
def about():
    return render_template('about.html')

# Route for the User Registeration page, now including password encryption
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users.append({'username': username, 'password': password})
        return redirect(url_for('home'))
    return render_template('register.html', fname='Register Here')

#route to handle user registeration
@app.route('/register', methods=['POST'])
def do_register():
    username = request.form['username']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSTERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

    return redirect('/users')

#route for registered users
@app.route('/users')
def users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, created_at FROM users")
    users = cursor.fetchall()
    conn.close()

    return render_template('users.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=False)


# Route for the data page
@app.route('/data')
def data():
    return render_template('data.html') 

# Route to all pages have been inputted

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

def run_flask():
    display(Javascript('window.open("/proxy/5000/","_blank")'))
    app.run(host='0.0.0.0', port=5000)

run_flask


#check if this needs to be executed in terminal