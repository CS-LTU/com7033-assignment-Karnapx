import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
import re
from datetime import datetime
from threading import Thread
from IPython.display import display, Javascript

app = Flask(__name__)
app.secret_key = 'life_is_good'

users = []

#function to connect to the 2nd SQLITE database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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

def verify_users(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None


#ROUTE TO login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
       
        if verify_users(username, password):
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
            return render_template('/login')
    
    return render_template('/login')

#email validation 
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-z0-9]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def is_password_strong(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True

#rOUTE TO HOME PAGE
@app.route('/')
def home():
    return render_template('/home')

#ROUTE TO ABOUT PAGE
@app.route('/about')
def about():
    return render_template('/about')

#route to display  the registration form
@app.route('/register', methods=['GET', 'POST'])
def do_register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        if not is_valid_email(email):
            flash('Invalid email format. Please enter a valid one.')
            return render_template('/register')
        
        #validate password strength
        if not is_password_strong(password):
            flash('Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, and one number.')
            return render_template('register.html',
                                   first_name=first_name,
                                   last_name=last_name,
                                   email=email)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('''INSERT INTO users (first_name, last_name, email, password, created_at)
                     VALUES (?, ?, ?, ?, ?)''', 
                    (first_name, last_name, email, hashed_password, created_at))
            conn.commit()
            conn.close()
            return redirect(url_for('success', first_name=first_name))
        except sqlite3.IntegrityError:
            flash('Email already registered. Please use a different email.')
            return render_template('/register', first_name=first_name, last_name=last_name,
                           email=email)


#ROUTE FOR THE SUCCESS PAGE 
@app.route('/success/<first_name>')
def success(first_name):
    return f"User {first_name} registered successfully!"

#ROUTE TO DISPLAY REGISTERED USERS
@app.route('/users')
def list_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, first_name, last_name, email, created_at FROM users")
    users = c.fetchall()
    conn.close()
    return render_template('/users', users=users)

#route ti delete a user by ID
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('list_users'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False) 

def run_flask():
    display(Javascript('window.open("/proxy/5000/"."_blank")'))
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

Thread(target=run_flask).start()

