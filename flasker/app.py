from flask import Flask
from flask import render_template
from flasker.SPutils import sp

app = Flask(__name__)

# @app.route('/')
# def map():
#     # print(sp.listOfFidCoords())
#     return render_template('map.html')


@app.route('/')
def showMap():
    path1 = [[34.66298873986377, 31.77537251843408], [34.66385643448008, 31.775544673159242], [34.66385643448008, 31.775544673159242], [34.66408404847699, 31.778544880450557], [34.65998456814748, 31.80985125376073], [34.65991666060499, 31.810352776309365], [34.658266577330146, 31.8095198785306], [34.65680726524424, 31.811224410665826], [34.654529037201335, 31.812626772099204], [34.65551509672302, 31.81477667621152]] #  TODO: send this temp path to client and represent it
    pathsFid=[1, 2, 12, 6, 7, 8, 17, 18, 19]
    pathsFid=[15, 14, 6, 7, 17, 8, 18, 19]
    # pathsFid=[21, 20, 14, 15, 68, 29]
    path1=list(map(lambda x: sp.getStationCoords(x), pathsFid ))
    return render_template('map.html',stations=list(sp.getListOfCoords()), path=path1)



@app.route('/try')
def map2():
    return render_template('map2.html')


