from flask import Flask
from flask import render_template
from flasker.SPutils import sp

app = Flask(__name__)

# @app.route('/')
# def map():
#     # print(sp.listOfFidCoords())
#     return render_template('map.html')

@app.route('/')
def map():
    path1 = [15, 14, 6, 7, 17, 8, 18, 19] #  TODO: send this temp path to client and represent it
    return render_template('map.html',stations=list(sp.getStationsDict().values()), path=path1)


# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)

