#this is the back end!
from flask import Flask, render_template, request, redirect, url_for
import sqlalchemy
import flask_sqlalchemy
import sqlite3
import os

app = Flask(__name__)

#route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for the about us page
@app.route('/aboutus')
def about():
    return render_template('about.html')

@app.route('/register')
def register():
   return render_template ('register.html')


# Route for the data page
@app.route('/data')
def data():
    return render_template('data.html') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

def run_flask():
    display(Javascript('window.open("/proxy/5000/","_blank")'))
    app.run(host='0.0.0.0', port=5000)

run_flask


#check if this needs to be executed in terminal