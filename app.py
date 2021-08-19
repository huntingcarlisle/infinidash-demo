import os
from io import BytesIO 
from flask import Flask, render_template, send_file, make_response
from flask.helpers import send_file
from . import charts

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/random_chart')
def random_chart():
    return charts.serve_chart()

if __name__ == '__main__':
    app.run()    