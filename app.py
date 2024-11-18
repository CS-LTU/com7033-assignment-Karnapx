#need to use mongodd, sql and html
from flask import Flask, render_template
from IPython.display import display, Javascript

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', fname= 'Home Page') 

@app.route('/aboutus')
def about():
    return render_template('about.html', fname = 'About Us')

@app.route('/registration')
def registration():
    return render_template('registration.html', fname='Register Here')

@app.route('/data')
def data():
    return render_template('data.html') #dont forge the fname
#Route to all pages have been inputted

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

def run_flask():
    display(Javascript('window.open("/proxy/5000/","_blank")'))
    app.run(host='0.0.0.0', port=5000)

