from flask import Flask, request, render_template, redirect
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


@app.route('/UserInputs/<int:drivers>/<int:parcels>', methods=['POST'])
def ProcessUserinfo(drivers: int, parcels: int):
    print()
    print(drivers, parcels)
    print()
    
    # drivers, results, parcels = getDemoFiles()
    # return render_template('map.html', stations=sp.stations, paths=drivers, results=results)
    
    return('/')