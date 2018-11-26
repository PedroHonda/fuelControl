from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('indexTemplate.html')

@app.route('/<carName>')
def carTable(carName):
    return render_template('carTemplate.html', APIipAddressPort="127.0.0.1:8080", carName=carName, OWNipAddressPort="127.0.0.1:8000")