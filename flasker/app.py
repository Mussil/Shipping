from flask import Flask, request, render_template, redirect, url_for
from flasker.SPutils import sp
from flasker.helpers import getDemoFiles


app = Flask(__name__)


@app.route('/')
def showMapForAll():

    drivers, results, parcels = getDemoFiles()

    return render_template('map.html', stations=sp.stations, paths=drivers, results=results)


@app.route('/try')
def start():
    return render_template('userInputs.html')


@app.route('/map',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
        result = request.form.to_dict()
        print(result, result['Name'], '-----')

        drivers, results, parcels = getDemoFiles()
        return render_template('map.html', stations=sp.stations, paths=drivers, results=results)
