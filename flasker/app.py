from flask import Flask
from flask import render_template
from flasker.SPutils import sp


app = Flask(__name__)

# url_for('static', filename='style.css')



@app.route('/')
def showMap():

    path1=[[34.65680726524424, 31.811224410665826], [34.665119988538905, 31.813349063961557], [34.65880491825114, 31.80846539474827], [34.65267978180447, 31.79653581609056], [34.66408404847699, 31.778544880450557], [34.6529108074645, 31.796622836740987], [34.64018006846066, 31.790892537920627], [34.66449516914017, 31.811933625384977], [34.654529037201335, 31.812626772099204]]
    
    pathsFid=[
            37,
            36,
            38,
            42,
            16,
            39,
            19,
            22,
            24
        ]
    path1 = sp.listFidToCorrds(pathsFid)
    

    return render_template('map.html',stations=list(sp.getListOfCoords()), path=path1)



@app.route('/try')
def map2():
    return render_template('map2.html')

