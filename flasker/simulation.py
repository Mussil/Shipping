import datetime
import json
import os
import random
import statistics

from flasker.SPutils import sp
from flasker.createPaths import createRandomPaths, createPaths
from flasker.createGraph import buildGraph
from flasker.createParcels import createRandomParcels
# from flasker.helpers import DatetimeEncoder
from flasker.helpers import convertStrToDate


def run(routes,parcels,numDrivers,numParcels,numberOfSP,costDistance,costDrivers,stopTime,maxTimeMin,maxDistanceMeters,weight):


    # # routes=createPaths(numSP=numberOfSP,numDrivers=numDrivers)
    # with open(f'paths/numDrivers{numDrivers}/pathsFile{pathFile}.json') as json_file:
    #     routes = json.load(json_file,object_hook=convertStrToDate)
    #     # print(routes)
    #
    # # parcels=createRandomParcels(numParcels=numParcels, maxSp=numberOfSP)
    # with open(f'parcels/numParcels{numParcels}/parcelsFile{parcelFile}.json') as json_file:
    #     parcels = json.load(json_file,object_hook=convertStrToDate)
    #     # print(parcels)

    g=buildGraph(routes=routes,maxSp=numberOfSP,maxDrivers=numDrivers,stopTime=stopTime,maxTimeMin=maxTimeMin,maxDistanceMeters=maxDistanceMeters,costDistance=costDistance,costDrivers=costDrivers)
    g.addWeights(nameOfWeight=weight['nameOfWeight'],A=weight['A'],B=weight['B'],C=weight['C'],alph=weight['alph'],beta=weight['beta'])


    resultDict={}
    for parcel in parcels:
        source=parcel['source']
        target=parcel['target']
        time=parcel['startTime']
        dictOfParcel = g.getDetailsShortestPath(source, target, time,weight=weight['nameOfWeight'])
        resultDict[parcel['idParcel']]=dictOfParcel

    #no save for now
    # path=f'results/parcels{numParcels}paths{numDrivers}'
    # i=1
    # while os.path.exists(f'{path}_{i}.json'):
    #     i+=1
    # with open(f'{path}_{i}.json', 'w') as json_file:
    #     json.dump(resultDict, json_file, indent=4)

    #seprate files
    # with open(f'results/parcels{numParcels}.{parcelFile}Paths{numDrivers}.{pathFile}.json','w') as json_file:
    #     json.dump(resultDict,json_file,indent=4)




    # actual cost at the end
    for parcel in resultDict.values():
        # print(g.payParcel(parcel['path'],parcel['totalDrivers']))
        parcel['payActual']=g.payParcel(parcel['path'],parcel['totalDrivers'])

    # print('-----------------------------')
    # reward for drivers
    for driver in range(1,numDrivers):
        # print(g.rewardDriver(driver))
        pass


    # path=f'results/parcels{numParcels}paths{numDrivers}'
    # i=1
    # while os.path.exists(f'{path}_{i}.json'):
    #     i+=1
    # with open(f'{path}_{i}.json', 'w') as json_file:
    #     json.dump(resultDict, json_file, indent=4)

    return resultDict

def simulate(numDrivers,numParcels):
    with open(f'paths/uniformDistribution10000.json') as json_file:
        routes = json.load(json_file, object_hook=convertStrToDate)

    sampleRoutes = random.sample(routes, numDrivers)
    # change the ids
    for i, route in enumerate(sampleRoutes):
        route['driver'] = i + 1

    with open(f'parcels/uniformDistribution100000.json') as json_file:
        parcels = json.load(json_file, object_hook=convertStrToDate)

    sampleParcels = random.sample(parcels, numParcels)
    # change the ids
    for i, route in enumerate(sampleParcels):
        route['idParcel'] = i + 1

    # numParcels=1
    # parcelFile=1

    # numDrivers = 20
    # pathFile=1

    numberOfSP = sp.numOfSP

    costDistance = 0.001
    costDrivers = 3

    stopTime = 1
    maxTimeMin = 1440
    maxDistanceMeters = 60000000

    weight = {
        'nameOfWeight': 'weightPriortyTimeDriverDistance',
        'A': 'time',
        'B': 'driver',
        'C': 'distance',
        'alph': 0,
        'beta': 0
    }

    return run(routes=sampleRoutes,
        parcels=sampleParcels,
        numDrivers=numDrivers,
        numParcels=numParcels,
        numberOfSP=numberOfSP,
        costDistance=costDistance,
        costDrivers=costDrivers,
        stopTime=stopTime,
        maxTimeMin=maxTimeMin,
        maxDistanceMeters=maxDistanceMeters,
        weight=weight)


def amountOfSucc(resultDict):
    succ=0
    for dict in resultDict.values():
        if dict['totalDrivers']>0:
            succ+=1
    return succ

def results(numParcels):
    numDrivers=0
    step=100

    succsListAvg=[]
    succsListMedian=[]
    amountOfDrivers=[]
    while(numDrivers<=1000):
        numDrivers+=step
        resultsPerAmount=[]
        for i in range(10):
            resultDict=simulate(numParcels=numParcels,numDrivers=numDrivers)
            succ=amountOfSucc(resultDict)
            resultsPerAmount.append(succ/numParcels)

        succsListAvg.append(statistics.mean(resultsPerAmount))
        succsListMedian.append(statistics.median(resultsPerAmount))

        amountOfDrivers.append(numDrivers)

        print(succsListAvg)
        print(succsListMedian)
        print(amountOfDrivers)

    return succsListAvg,amountOfDrivers







def simulate6(numDrivers,numParcels):
    with open(f'paths/uniformDistribution10000.json') as json_file:
        routes = json.load(json_file, object_hook=convertStrToDate)

    sampleRoutes = random.sample(routes, numDrivers)
    # change the ids
    for i, route in enumerate(sampleRoutes):
        route['driver'] = i + 1

    with open(f'parcels/uniformDistribution100000.json') as json_file:
        parcels = json.load(json_file, object_hook=convertStrToDate)

    sampleParcels = random.sample(parcels, numParcels)
    # change the ids
    for i, route in enumerate(sampleParcels):
        route['idParcel'] = i + 1

    # numParcels=1
    # parcelFile=1

    # numDrivers = 20
    # pathFile=1

    numberOfSP = sp.numOfSP

    costDistance = 0.001
    costDrivers = 3

    stopTime = 1
    maxTimeMin = 1440
    maxDistanceMeters = 60000000

    # -----------------------------
    weight = {
        'nameOfWeight': 'weightPriortyTimeDriverDistance',
        'A': 'time',
        'B': 'driver',
        'C': 'distance',
        'alph': 0,
        'beta': 0
    }
    resultDict=run(routes=sampleRoutes,
        parcels=sampleParcels,
        numDrivers=numDrivers,
        numParcels=numParcels,
        numberOfSP=numberOfSP,
        costDistance=costDistance,
        costDrivers=costDrivers,
        stopTime=stopTime,
        maxTimeMin=maxTimeMin,
        maxDistanceMeters=maxDistanceMeters,
        weight=weight)
    path=f'results/parcels{numParcels}paths{numDrivers}'
    with open(f'{path}_TimeDriverDistance.json', 'w') as json_file:
        json.dump(resultDict, json_file, indent=4)

# -----------------------------
    weight = {
        'nameOfWeight': 'weightPriortyTimeDistanceDriver',
        'A': 'time',
        'B': 'distance',
        'C': 'driver',
        'alph': 0,
        'beta': 0
    }
    resultDict=run(routes=sampleRoutes,
        parcels=sampleParcels,
        numDrivers=numDrivers,
        numParcels=numParcels,
        numberOfSP=numberOfSP,
        costDistance=costDistance,
        costDrivers=costDrivers,
        stopTime=stopTime,
        maxTimeMin=maxTimeMin,
        maxDistanceMeters=maxDistanceMeters,
        weight=weight)
    path=f'results/parcels{numParcels}paths{numDrivers}'
    with open(f'{path}_TimeDistanceDriver.json', 'w') as json_file:
        json.dump(resultDict, json_file, indent=4)


# -----------------------------
    weight = {
        'nameOfWeight': 'weightPriortyDistanceDriverTime',
        'A': 'distance',
        'B': 'time',
        'C': 'driver',
        'alph': 0,
        'beta': 0
    }
    resultDict=run(routes=sampleRoutes,
        parcels=sampleParcels,
        numDrivers=numDrivers,
        numParcels=numParcels,
        numberOfSP=numberOfSP,
        costDistance=costDistance,
        costDrivers=costDrivers,
        stopTime=stopTime,
        maxTimeMin=maxTimeMin,
        maxDistanceMeters=maxDistanceMeters,
        weight=weight)
    path=f'results/parcels{numParcels}paths{numDrivers}'
    with open(f'{path}_DistanceDriverTime.json', 'w') as json_file:
        json.dump(resultDict, json_file, indent=4)
# -----------------------------
    weight = {
        'nameOfWeight': 'weightPriortyDistanceTimeDriver',
        'A': 'distance',
        'B': 'driver',
        'C': 'time',
        'alph': 0,
        'beta': 0
    }
    resultDict=run(routes=sampleRoutes,
        parcels=sampleParcels,
        numDrivers=numDrivers,
        numParcels=numParcels,
        numberOfSP=numberOfSP,
        costDistance=costDistance,
        costDrivers=costDrivers,
        stopTime=stopTime,
        maxTimeMin=maxTimeMin,
        maxDistanceMeters=maxDistanceMeters,
        weight=weight)
    path=f'results/parcels{numParcels}paths{numDrivers}'
    with open(f'{path}_DistanceTimeDriver.json', 'w') as json_file:
        json.dump(resultDict, json_file, indent=4)

# -----------------------------
    weight = {
        'nameOfWeight': 'weightPriortyDriverDistanceTime',
        'A': 'driver',
        'B': 'distance',
        'C': 'time',
        'alph': 0,
        'beta': 0
    }
    resultDict=run(routes=sampleRoutes,
        parcels=sampleParcels,
        numDrivers=numDrivers,
        numParcels=numParcels,
        numberOfSP=numberOfSP,
        costDistance=costDistance,
        costDrivers=costDrivers,
        stopTime=stopTime,
        maxTimeMin=maxTimeMin,
        maxDistanceMeters=maxDistanceMeters,
        weight=weight)
    path=f'results/parcels{numParcels}paths{numDrivers}'
    with open(f'{path}_DriverDistanceTime.json', 'w') as json_file:
        json.dump(resultDict, json_file, indent=4)
# -----------------------------
    weight = {
        'nameOfWeight': 'weightPriortyDriverTimeDistance',
        'A': 'driver',
        'B': 'time',
        'C': 'distance',
        'alph': 0,
        'beta': 0
    }
    resultDict=run(routes=sampleRoutes,
        parcels=sampleParcels,
        numDrivers=numDrivers,
        numParcels=numParcels,
        numberOfSP=numberOfSP,
        costDistance=costDistance,
        costDrivers=costDrivers,
        stopTime=stopTime,
        maxTimeMin=maxTimeMin,
        maxDistanceMeters=maxDistanceMeters,
        weight=weight)
    path=f'results/parcels{numParcels}paths{numDrivers}'
    with open(f'{path}_DriverTimeDistance.json', 'w') as json_file:
        json.dump(resultDict, json_file, indent=4)
if __name__=='__main__':
    # numDrivers=50
    numParcels=50
    # simulate(numDrivers,numParcels)


    # x,y=results(numParcels)

    resultDict = simulate6(numParcels=100, numDrivers=200)
