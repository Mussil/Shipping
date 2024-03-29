from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from flasker.SPutils import sp
from flasker.helpers import getFiles, convertSpeedToRatio


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
DRIVERS_DETAILS_DEFAULT = {"drivers-amount":300, "parcels-amount":600, "speed":1}


@app.route('/')
def homepage():
    session["drivers-details"] = DRIVERS_DETAILS_DEFAULT
    return render_template('homepage.html')

@app.route('/introduction')
def introduction():
    return render_template('introduction.html')

@app.route('/simulation-details')
def menu1():
    if session.get("drivers-details"):
        results = session.get('drivers-details')
        return render_template('menu1.html', driversNum=results["drivers-amount"], parcelsNum=results["parcels-amount"], speed=results["speed"]) 
    return render_template('menu1.html', driversNum=300, parcelsNum=600, speed=1) 


@app.route('/drivers-details', methods=['POST'])
def menu2():
    result = request.form.to_dict()
    session["drivers-details"] = result
    return render_template('menu2.html',driver_num=result["drivers-amount"],parcels_num=result["parcels-amount"],speed=result["speed"])

@app.route('/map', methods=['POST', 'GET'])
def map():
    if request.method == 'POST':
        return ('/map') 

    args = request.args.to_dict()

    drivers, results, parcels = getFiles(args['driversNum'], args['parcelsNum'], args['userChoice'])
    return render_template('map.html', stations=sp.stations, paths=drivers, results=results, speedRatio=convertSpeedToRatio(args['speed']))

@app.route('/end-simulation')
def end():
    return render_template('end.html')