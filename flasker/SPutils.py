import datetime
import json
from pprint import pprint

from mapbox import Directions
from helpers import access_token

class SP:
    def __init__(self, path):
        self.stations = self._json2DictSP(path)

    def _json2DictSP(self, path):
        with open(path, 'r') as stationsFile:
            jsonObj = json.load(stationsFile)

        jsonObj = jsonObj["features"]
        stations = {}
        for obj in jsonObj:
            fid=obj['properties']['fid']
            stations[fid] = obj['geometry']['coordinates']

        return stations

    def getStationCoords(self,fid):
        return self. stations[fid]

    def listOfFidCoords(self):
        return self.stations.items()






path = 'servicePointGlobal.geojson'
sp=SP(path)

if __name__=='__main__':
    pass

