import json

path = 'servicePointGlobal.geojson'


def getStationDeatils(num):
    #todo: temp function , need to be written difrently
    with open(path, 'r') as stationsFile:
        stationsJson = json.load(stationsFile)

    stationsJson = stationsJson["features"]

    return stationsJson[num - 1]

def coordinatesAllSp():
    '''
    #TODO: make sure it work efficentyly
    :return:
    '''

    with open(path, 'r') as stationsFile:
        stationsJson = json.load(stationsFile)
    coordList=[]
    stationsJson = stationsJson["features"]
    for feature in stationsJson:
        coordList.append((feature['properties']['fid'],feature['geometry']['coordinates']))
    return coordList