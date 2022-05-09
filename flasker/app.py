from flask import Flask, request, render_template, request
from flasker.SPutils import sp
from flasker.helpers import getFiles


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/menu1')
def start():
    return render_template('menu1.html')


@app.route('/map', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        return ('/map') 

    args = request.args.to_dict()
    print("----", args)
    drivers, results, parcels = getFiles(args['driversNum'], args['parcelsNum'], args['userChoice'])
    return render_template('map.html', stations=sp.stations, paths=drivers, results=results)


@app.route('/menu2', methods=['POST'])
def end():
    result = request.form.to_dict()
    print(result)
    return render_template('menu2.html',driver_num=result["drivers-amount"],parcels_num=result["parcels-amount"])
