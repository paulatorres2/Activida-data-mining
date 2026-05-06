from flask import Flask, render_template
import Clustering


app = Flask(__name__)

@app.route('/hello')
def home():
    return 'Hello, World!'

@app.route('/')
def index():
    info = Clustering.RealizarClustering()
    return render_template('index.html', info=info)