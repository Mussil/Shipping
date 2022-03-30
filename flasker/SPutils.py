import datetime
import json
from pprint import pprint

from mapbox import Directions
# from flasker.helpers import access_token

class SP:
    def __init__(self, path):
        self.stations = self._json2DictSP(path)
        self.numOfSP=len(self.stations)

        self.industrial_areaSP = [7, 8, 9, 10, 13, 17, 18, 19, 20, 21, 22, 23, 24, 27]

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
        return self.stations[fid]

    def getListOfFidCoords(self):
        return self.stations.items()

    def getListOfCoords(self):
        return self.stations.values()

    def getDictFidCoords(self):
        return self.stations

    def listFidToCorrds(self,listFid):
        listCoords = list(map(lambda x: sp.getStationCoords(x), listFid))
        return listCoords

    def getIndustrial_areaSP(self):
        return self.industrial_areaSP


path = 'servicePointGlobal.geojson'
sp=SP(path)

if __name__=='__main__':
    pass




