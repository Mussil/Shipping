import json

from flask import Flask
from markupsafe import escape
from flask import render_template

app = Flask(__name__)

# url_for('static', filename='style.css')

@app.route('/')
def map():
    with open("servicePointGlobal.geojson", "r") as file:
        data = json.load(file)
        
        return render_template('map.html', stations=data)

# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)

# from flasker.graphDraft import drive

# @app.route('/graph/')
# def hello():
#     drive()
#     return 'graph try'
