from flask import Flask
from markupsafe import escape
from flask import render_template

app = Flask(__name__)

# url_for('static', filename='style.css')


@app.route('/')
def map():
    return render_template('map.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)