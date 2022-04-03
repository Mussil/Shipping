from datetime import datetime
import json
import os
import random
import statistics
from pprint import pprint

from flasker.SPutils import sp
from flasker.plots import avgFunc1, medianFunc1, compareWeightsMax, compareWeightsActual, durationFunc3, plotSucc, \
    plotDuration, plotDBSucc, plotDBduration, plotDBdistance, plotDBdiffCost, plotDBddiffCost

random.seed()

from flasker.createGraph import buildGraph
from flasker.helpers import convertStrToDate, convertDateToStr, minutesInDay

import concurrent.futures

costDistanceG = 0.001
costDriversG = 3
stopTimeG = 1
maxTimeMinG = minutesInDay
maxDistanceMetersG = 60000000
numRunsG = 50

folderNameG = 'allResults/results2days_Source_50IA_Dest_ALL'
routesFolderName = f'paths/2days_Source_50IA_Dest_ALL10000'


# driversRangeG = range(100, 501, 100)
# parcelsRangeG = range(100, 1001, 100)


driversRangeG = [300]
parcelsRangeG = [500]




def chooseParcels(numParcels):
    with open(f'parcels/uniformDistribution100000.json') as json_file:
        parcels = json.load(json_file, object_hook=convertStrToDate)

    sampleParcels = random.sample(parcels, numParcels)
    # change the ids
    for i, route in enumerate(sampleParcels):
        route['idParcel'] = i + 1

    return sampleParcels

def chooseRoutes(numDrivers):
    with open(f'{routesFolderName}.json') as json_file:
        routes = json.load(json_file, object_hook=convertStrToDate)

    sampleRoutes = random.sample(routes, numDrivers)
    # change the ids
    for i, route in enumerate(sampleRoutes):
        route['driver'] = i + 1

    return sampleRoutes



class Simulator():
    namesOfWeights = ['weightPriortyTimeDriverDistance', 'weightPriortyTimeDistanceDriver',
                           'weightPriortyDistanceDriverTime', 'weightPriortyDistanceTimeDriver',
                           'weightPriortyDriverDistanceTime', 'weightPriortyDriverTimeDistance']

    def __init__(self,routes,numberOfSP,numDrivers,stopTime,maxTimeMin,maxDistanceMeters,costDistance,costDrivers):
        self.g = buildGraph(routes=routes, maxSp=numberOfSP, maxDrivers=numDrivers, stopTime=stopTime, maxTimeMin=maxTimeMin,
                       maxDistanceMeters=maxDistanceMeters, costDistance=costDistance, costDrivers=costDrivers)

        # all the combination of priorities
        alph=0
        beta=0
        # self.namesOfWeights=['weightPriortyTimeDriverDistance','weightPriortyTimeDistanceDriver','weightPriortyDistanceDriverTime','weightPriortyDistanceTimeDriver','weightPriortyDriverDistanceTime','weightPriortyDriverTimeDistance']
        self.addWeight(nameOfWeight='weightPriortyTimeDriverDistance',A='time',B='driver',C='distance',alph=alph,beta=beta)
        self.addWeight(nameOfWeight='weightPriortyTimeDistanceDriver',A='time',B='distance',C='driver',alph=alph,beta=beta)
        self.addWeight(nameOfWeight='weightPriortyDistanceDriverTime',A='distance',B='time',C='driver',alph=alph,beta=beta)
        self.addWeight(nameOfWeight='weightPriortyDistanceTimeDriver',A='distance',B='driver',C='time',alph=alph,beta=beta)
        self.addWeight(nameOfWeight='weightPriortyDriverDistanceTime',A='driver',B='distance',C='time',alph=alph,beta=beta)
        self.addWeight(nameOfWeight='weightPriortyDriverTimeDistance',A='driver',B='time',C='distance',alph=alph,beta=beta)



    def addWeight(self,nameOfWeight,A,B,C,alph,beta):
        self.g.addWeights(nameOfWeight=nameOfWeight, A=A, B=B, C=C,alph=alph, beta=beta)

    def sendParcelsBySameWeight(self,parcels,nameOfWeight):
        resultDict = {}
        for parcel in parcels:
            source = parcel['source']
            target = parcel['target']
            time = parcel['startTime']
            dictOfParcel = self.g.getDetailsShortestPath(source, target, time, weight=nameOfWeight)
            resultDict[parcel['idParcel']] = dictOfParcel


        # actual cost at the end
        for parcel in resultDict.values():
            # print(g.payParcel(parcel['path'],parcel['totalDrivers']))
            parcel['payActual'] = self.g.payParcel(parcel['path'], parcel['totalDrivers'])

        self.g.clearForNewRound() #clear the parcels driver took for diffrent round

        return Result(resultDict)


    def sendParcelsByRandomWeight(self,parcels):
        resultDict = {}
        for parcel in parcels:
            nameOfWeight=random.choice(self.namesOfWeights)
            source = parcel['source']
            target = parcel['target']
            time = parcel['startTime']
            dictOfParcel = self.g.getDetailsShortestPath(source, target, time, weight=nameOfWeight)
            dictOfParcel['weightName']=nameOfWeight
            resultDict[parcel['idParcel']] = dictOfParcel

        # actual cost at the end
        for parcel in resultDict.values():
            # print(g.payParcel(parcel['path'],parcel['totalDrivers']))
            parcel['payActual'] = self.g.payParcel(parcel['path'], parcel['totalDrivers'])

        self.g.clearForNewRound() #clear the parcels driver took for diffrent round

        return Result(resultDict)


class Result():

    def __init__(self,result):
        self.result=result

    def getAmountOfSucc(self):
        succ=0
        for dict in self.result.values():
            if dict['totalDrivers'] > 0:
                succ += 1
        return succ
    def getListPayMax(self):
        payMax = []
        for dict in self.result.values():
            if dict['payMax'] > 0:
                payMax.append(dict['payMax'])
        return payMax
    def getListPayActual(self):
        payActual = []
        for dict in self.result.values():
            if dict['payActual'] > 0:
                payActual.append(dict['payActual'])
        return payActual
    def getListDuration(self):
        durations=[]
        for dict in self.result.values():
            if dict['totalDuration'] > 0:
                durations.append(dict['totalDuration'])
        return durations
    def getListDistance(self):
        distances=[]
        for dict in self.result.values():
            if dict['totalDistance'] > 0:
                distances.append(dict['totalDistance'])
        return distances


    def getResult(self):
        return self.result








def createPreDrivers(folderName):
    # create all pre drivers
    for i in range(numRunsG):
        for numDrivers in driversRangeG:
            drivers = chooseRoutes(numDrivers)
            # Check whether the specified path exists or not
            path = f'{folderName}/driversDB/{numDrivers}'
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)

            with open(f'{path}/{i}.json', 'w', encoding='utf-8') as f:
                json.dump(drivers, f, indent=4, default=convertDateToStr)

def createPreParcels(folderName):
    # create all pre parcels
    path = f'{folderName}/parcelsDB'
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    for numParcels in parcelsRangeG:
        parcels=chooseParcels(numParcels)
        with open(f'{path}/{numParcels}.json', 'w', encoding='utf-8') as f:
            json.dump(parcels, f, indent=4, default=convertDateToStr)


def iterate(i):
    costDistance = costDistanceG
    costDrivers = costDriversG
    stopTime = stopTimeG
    maxTimeMin = minutesInDay
    maxDistanceMeters = maxDistanceMetersG

    folderName = folderNameG
    driversRange = driversRangeG
    parcelsRange = parcelsRangeG

    for numDrivers in driversRange:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'iteration #{i} | #drivers {numDrivers} | Current Time = {current_time}')

        with open(f'{folderName}/driversDB/{numDrivers}/{i}.json') as json_file:
            drivers = json.load(json_file, object_hook=convertStrToDate)

        graphSimulator = Simulator(routes=drivers, numberOfSP=sp.numOfSP, numDrivers=numDrivers, stopTime=stopTime,
                                   maxTimeMin=maxTimeMin, maxDistanceMeters=maxDistanceMeters,
                                   costDistance=costDistance, costDrivers=costDrivers)

        for numParcels in parcelsRange:
            path = f'{folderName}/results/{numParcels}parcels/{numDrivers}drivers'
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)

            with open(f'{folderName}/../parcelsDB/{numParcels}.json') as json_file:
                parcels = json.load(json_file, object_hook=convertStrToDate)

            results = graphSimulator.sendParcelsByRandomWeight(parcels)
            with open(f'{path}/{i}.json', 'w', encoding='utf-8') as f:
                json.dump(results.getResult(), f, indent=4, default=convertDateToStr)

            letter = 'a'
            for nameOfWeight in graphSimulator.namesOfWeights:
                results = graphSimulator.sendParcelsBySameWeight(parcels, nameOfWeight)
                with open(f'{path}/{i}{letter}.json', 'w', encoding='utf-8') as f:
                    json.dump(results.getResult(), f, indent=4, default=convertDateToStr)
                letter = chr(ord(letter) + 1)  # the next letter in alphbet
    return i



# def iterateOneNumDrivers(i):
#     costDistance = costDistanceG
#     costDrivers = costDriversG
#     stopTime = stopTimeG
#     maxTimeMin = minutesInDay
#     maxDistanceMeters = maxDistanceMetersG
#
#     folderName = folderNameG
#
#     numDrivers =300
#     numParcels= 500
#
#
#     now = datetime.now()
#     current_time = now.strftime("%H:%M:%S")
#     print(f'iteration #{i} | #drivers {numDrivers} | Current Time = {current_time}')
#
#     with open(f'{folderName}/driversDB/{numDrivers}/{i}.json') as json_file:
#         drivers = json.load(json_file, object_hook=convertStrToDate)
#
#     graphSimulator = Simulator(routes=drivers, numberOfSP=sp.numOfSP, numDrivers=numDrivers, stopTime=stopTime,
#                                maxTimeMin=maxTimeMin, maxDistanceMeters=maxDistanceMeters,
#                                costDistance=costDistance, costDrivers=costDrivers)
#
#     path = f'{folderName}/results/{numParcels}parcels/{numDrivers}drivers'
#     isExist = os.path.exists(path)
#     if not isExist:
#         os.makedirs(path)
#
#     with open(f'{folderName}/../parcelsDB/{numParcels}.json') as json_file:
#         parcels = json.load(json_file, object_hook=convertStrToDate)
#
#     results = graphSimulator.sendParcelsByRandomWeight(parcels)
#     with open(f'{path}/{i}.json', 'w', encoding='utf-8') as f:
#         json.dump(results.getResult(), f, indent=4, default=convertDateToStr)
#
#     letter = 'a'
#     for nameOfWeight in graphSimulator.namesOfWeights:
#         results = graphSimulator.sendParcelsBySameWeight(parcels, nameOfWeight)
#         with open(f'{path}/{i}{letter}.json', 'w', encoding='utf-8') as f:
#             json.dump(results.getResult(), f, indent=4, default=convertDateToStr)
#         letter = chr(ord(letter) + 1)  # the next letter in alphbet
#     return i


def resultsFromPre():
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:

        numRuns = numRunsG
        runsRange=range(numRuns)
        for i in executor.map(iterate, runsRange):
            print(f"-----------Done iteration #{i}------------\n")




if __name__=='__main__':

    folderName=folderNameG

    createPreDrivers(folderName)
    resultsFromPre()
