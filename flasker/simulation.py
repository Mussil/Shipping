import datetime
import json

from flasker.SPutils import sp
from flasker.createPaths import createRandomPaths, createPaths
from flasker.createGraph import buildGraph
from flasker.createParcels import createRandomParcels
# from flasker.helpers import DatetimeEncoder
from flasker.helpers import convertStrToDate


def run():
    numDrivers = 20
    pathFile=1
    parcelFile=1

    numberOfSP = sp.numOfSP
    numParcels=15

    # routes=createPaths(numSP=numberOfSP,numDrivers=numDrivers)


    with open(f'paths/numDrivers{numDrivers}/pathsFile{pathFile}.json') as json_file:
        routes = json.load(json_file,object_hook=convertStrToDate)
        # print(routes)

    # parcels=createRandomParcels(numParcels=numParcels, maxSp=numberOfSP)
    with open(f'parcels/numParcels{numParcels}/parcelsFile{parcelFile}.json') as json_file:
        parcels = json.load(json_file,object_hook=convertStrToDate)
        # print(parcels)

    g=buildGraph(routes=routes,maxSp=numberOfSP,maxDrivers=numDrivers,stopTime=1,maxTimeMin=400,maxDistanceMeters=10000)
    g.addWeights(nameOfWeight='weightPriortyTimeDriverDistance',A='time',B='driver',C='distance',alph=0,beta=0)


    resultDict={}
    for parcel in parcels:
        source=parcel['source']
        target=parcel['target']
        time=parcel['startTime']
        path = g.getDetailsShortestPath(source, target, time,weight='weightPriortyTimeDriverDistance')
        resultDict[parcel['idParcel']]=path

    with open(f'results/parcels{numParcels}.{parcelFile}Paths{numDrivers}.{pathFile}.json','w') as json_file:
        json.dump(resultDict,json_file,indent=4)


if __name__=='__main__':
    run()