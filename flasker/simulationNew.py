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


def chooseParcels(numParcels):
    with open(f'parcels/uniformDistribution100000.json') as json_file:
        parcels = json.load(json_file, object_hook=convertStrToDate)

    sampleParcels = random.sample(parcels, numParcels)
    # change the ids
    for i, route in enumerate(sampleParcels):
        route['idParcel'] = i + 1

    return sampleParcels

def chooseRoutes(numDrivers):
    with open(f'paths/uniformDistribution10000.json') as json_file:
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




def buildDBsameParcels(numParcels,folderName):
    prePath=f'{folderName}/{numParcels}parcels'

    # parcels=chooseParcels(numParcels)
    # same parcels as before:
    with open(f'results2days/300parcels/parcelsFile.json') as json_file:
        parcels = json.load(json_file, object_hook=convertStrToDate)
    with open(f'{prePath}/parcelsFile.json', 'w', encoding='utf-8') as f:
        json.dump(parcels, f, indent=4,default=convertDateToStr)


    driversRange=range(100,601,100)


    for i in range(100):

        for numDrivers in driversRange:
            drivers = chooseRoutes(numDrivers)
            graphSimulator = Simulator(routes=drivers, numberOfSP=sp.numOfSP, numDrivers=numDrivers, stopTime=stopTime,
                                       maxTimeMin=maxTimeMin, maxDistanceMeters=maxDistanceMeters,
                                       costDistance=costDistance, costDrivers=costDrivers)

            # Check whether the specified path exists or not
            path=f'{prePath}/resultsNonUniform/{numDrivers}'
            isExist = os.path.exists(path)
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)


            results = graphSimulator.sendParcelsByRandomWeight(parcels)
            with open(f'{path}/{i}.json', 'w', encoding='utf-8') as f:
                json.dump(results.getResult(), f, indent=4,default=convertDateToStr)

            letter='a'
            for nameOfWeight in graphSimulator.namesOfWeights:
                results = graphSimulator.sendParcelsBySameWeight(parcels,nameOfWeight)
                with open(f'{path}/{i}{letter}.json', 'w', encoding='utf-8') as f:
                    json.dump(results.getResult(), f, indent=4,default=convertDateToStr)
                letter = chr(ord(letter) + 1) #the next letter in alphbet


            #save the drivers details
            # Check whether the specified path exists or not
            path=f'{prePath}/driversDB/{numDrivers}'
            isExist = os.path.exists(path)
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)

            with open(f'{path}/{i}.json', 'w', encoding='utf-8') as f:
                json.dump(drivers, f, indent=4, default=convertDateToStr)




# def buildDBpostCreationWithWeights():
#     '''
#     this function comes after the buildDB function that create all the graphs for 300 parcels,
#     this function add the weight and save it also for the same data
#     :return:
#     '''
#     with open(f'resultsNonUniform/db300parcels/parcelsFile.json') as json_file:
#         parcels = json.load(json_file, object_hook=convertStrToDate)
#
#
#     driversRange=range(100,501,100)
#
#
#     for i in range(100):
#
#         for numDrivers in driversRange:
#             path=f'resultsNonUniform/db300parcels/driversDB/{numDrivers}'
#             with open(f'{path}/{i}.json') as json_file:
#                 drivers = json.load(json_file, object_hook=convertStrToDate)
#
#             graphSimulator = Simulator(routes=drivers, numberOfSP=sp.numOfSP, numDrivers=numDrivers, stopTime=stopTime,
#                                        maxTimeMin=maxTimeMin, maxDistanceMeters=maxDistanceMeters,
#                                        costDistance=costDistance, costDrivers=costDrivers)
#
#             # Check whether the specified path exists or not
#             path=f'resultsNonUniform/db300parcels/{numDrivers}'
#             isExist = os.path.exists(path)
#             if not isExist:
#                 # Create a new directory because it does not exist
#                 os.makedirs(path)
#
#
#             letter='a'
#             for nameOfWeight in graphSimulator.namesOfWeights:
#                 resultsNonUniform = graphSimulator.sendParcelsBySameWeight(parcels,nameOfWeight)
#                 with open(f'{path}/{i}{letter}.json', 'w', encoding='utf-8') as f:
#                     json.dump(resultsNonUniform.getResult(), f, indent=4)
#                 letter = chr(ord(letter) + 1) #the next letter in alphbet




def DBpsucc(numParcels,folderName):
    driversRange=range(100,601,100)
    dictResults={name : [] for name in driversRange}
    prePath=f'{folderName}/{numParcels}parcels'

    def DBsuccOneIndex(index):
        for numDrivers in driversRange:
            with open(f'{prePath}/resultsNonUniform/{numDrivers}/{index}.json') as json_file:
                results = json.load(json_file)
            results = Result(results)
            succ = results.getAmountOfSucc()
            dictResults[numDrivers].append(succ / numParcels)
        return dictResults

    for i in range(100):
        DBsuccOneIndex(index=str(i))

    plotDBSucc(numParcels,dictResults)


def DBpduration(numParcels,folderName):
    prePath=f'{folderName}/{numParcels}parcels'

    driversRange=range(100,601,100)
    dictResultsAllWeight={weightName: {numDrivers : [] for numDrivers in driversRange}for weightName in Simulator.namesOfWeights}
    dictResultsAllWeight['random']={numDrivers : [] for numDrivers in driversRange}
    # dictResults={numDrivers : [] for numDrivers in driversRange}

    def DBdurationOneIndex(index):
        for numDrivers in driversRange:
            dictResults = dictResultsAllWeight['random']
            with open(f'{prePath}/resultsNonUniform/{numDrivers}/{index}.json') as json_file:
                results = json.load(json_file)
            results = Result(results)
            listDuration = results.getListDuration()
            dictResults[numDrivers].append(statistics.mean(listDuration))

            letter='a'
            for weightName in Simulator.namesOfWeights:
                dictResults=dictResultsAllWeight[weightName]
                with open(f'{prePath}/resultsNonUniform/{numDrivers}/{index}{letter}.json') as json_file:
                    results = json.load(json_file)
                results = Result(results)
                listDuration = results.getListDuration()
                dictResults[numDrivers].append(statistics.mean(listDuration))
                letter = chr(ord(letter) + 1)  # the next letter in alphbet



        return dictResults

    for i in range(100):
        DBdurationOneIndex(index=str(i))

    plotDBduration(numParcels,dictResultsAllWeight)


def DBpdistance(numParcels,folderName):
    prePath=f'{folderName}/{numParcels}parcels'

    driversRange=range(100,601,100)
    dictResultsAllWeight={weightName: {numDrivers : [] for numDrivers in driversRange}for weightName in Simulator.namesOfWeights}
    dictResultsAllWeight['random']={numDrivers : [] for numDrivers in driversRange}
    # dictResults={numDrivers : [] for numDrivers in driversRange}

    def DBdistanceOneIndex(index):
        for numDrivers in driversRange:
            dictResults = dictResultsAllWeight['random']
            with open(f'{prePath}/resultsNonUniform/{numDrivers}/{index}.json') as json_file:
                results = json.load(json_file)
            results = Result(results)
            listDistance = results.getListDistance()
            dictResults[numDrivers].append(statistics.mean(listDistance))

            letter='a'
            for weightName in Simulator.namesOfWeights:
                dictResults=dictResultsAllWeight[weightName]
                with open(f'{prePath}/resultsNonUniform/{numDrivers}/{index}{letter}.json') as json_file:
                    results = json.load(json_file)
                results = Result(results)
                listDistance = results.getListDistance()
                dictResults[numDrivers].append(statistics.mean(listDistance))
                letter = chr(ord(letter) + 1)  # the next letter in alphbet



        return dictResults

    for i in range(100):
        DBdistanceOneIndex(index=str(i))

    plotDBdistance(numParcels,dictResultsAllWeight)

def DBpdiffCost(numParcels):
    prePath=f'{folderName}/{numParcels}parcels'
    driversRange=range(100,601,100)
    dictResultsAllWeight={weightName: {numDrivers : [] for numDrivers in driversRange}for weightName in Simulator.namesOfWeights}
    dictResultsAllWeight['random']={numDrivers : [] for numDrivers in driversRange}

    def DBdiffCostOneIndex(index):
        for numDrivers in driversRange:
            dictResults = dictResultsAllWeight['random']
            with open(f'{prePath}/resultsNonUniform/{numDrivers}/{index}.json') as json_file:
                results = json.load(json_file)
            results = Result(results)
            listPayMax = results.getListPayMax()
            listPayActual = results.getListPayActual()
            diff = [1-(b_i / a_i) for a_i, b_i in zip(listPayMax, listPayActual)]
            dictResults[numDrivers].append(statistics.mean(diff))

            letter='a'
            for weightName in Simulator.namesOfWeights:
                dictResults=dictResultsAllWeight[weightName]
                with open(f'{prePath}/resultsNonUniform/{numDrivers}/{index}{letter}.json') as json_file:
                    results = json.load(json_file)
                results = Result(results)
                listPayMax = results.getListPayMax()
                listPayActual = results.getListPayActual()
                diff = [1 - (b_i / a_i) for a_i, b_i in zip(listPayMax, listPayActual)]
                dictResults[numDrivers].append(statistics.mean(diff))

                letter = chr(ord(letter) + 1)  # the next letter in alphbet



        return dictResults

    for i in range(100):
        DBdiffCostOneIndex(index=str(i))

    plotDBdiffCost(numParcels,dictResultsAllWeight)




def buildDBsameDrivers(numDrivers,folderName):
    prePath=f'{folderName}/{numDrivers}drivers'
    drivers = chooseRoutes(numDrivers)
    with open(f'{prePath}/driversFile.json', 'w', encoding='utf-8') as f:
        json.dump(drivers, f, indent=4,default=convertDateToStr)
    graphSimulator = Simulator(routes=drivers, numberOfSP=sp.numOfSP, numDrivers=numDrivers, stopTime=stopTime,
                               maxTimeMin=maxTimeMin, maxDistanceMeters=maxDistanceMeters,
                               costDistance=costDistance, costDrivers=costDrivers)

    parcelsRange=range(50,501,50)

    for i in range(100):

        for numParcels in parcelsRange:

            parcels = chooseParcels(numParcels)

            # Check whether the specified path exists or not
            path=f'{prePath}/resultsNonUniform/{numParcels}'
            isExist = os.path.exists(path)
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)

            results = graphSimulator.sendParcelsByRandomWeight(parcels)
            with open(f'{path}/{i}.json', 'w', encoding='utf-8') as f:
                json.dump(results.getResult(), f, indent=4,default=convertDateToStr)

            letter='a'
            for nameOfWeight in graphSimulator.namesOfWeights:
                results = graphSimulator.sendParcelsBySameWeight(parcels,nameOfWeight)
                with open(f'{path}/{i}{letter}.json', 'w', encoding='utf-8') as f:
                    json.dump(results.getResult(), f, indent=4,default=convertDateToStr)
                letter = chr(ord(letter) + 1) #the next letter in alphbet


            # save the parcels details
            # Check whether the specified path exists or not
            path = f'{prePath}/parcelsDB/{numParcels}'
            isExist = os.path.exists(path)
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)

            with open(f'{path}/{i}.json', 'w', encoding='utf-8') as f:
                json.dump(drivers, f, indent=4, default=convertDateToStr)


def DBddiffCost(numDrivers,folderName):
    prePath=f'{folderName}/{numDrivers}drivers'
    parcelsRange=range(50,501,50)
    dictResultsAllWeight={weightName: {numDrivers : [] for numDrivers in parcelsRange}for weightName in Simulator.namesOfWeights}
    dictResultsAllWeight['random']={numDrivers : [] for numDrivers in parcelsRange}

    def DBdiffCostOneIndex(index):
        for numParcels in parcelsRange:
            dictResults = dictResultsAllWeight['random']
            with open(f'{prePath}/resultsNonUniform/{numParcels}/{index}.json') as json_file:
                results = json.load(json_file)
            results = Result(results)
            listPayMax = results.getListPayMax()
            listPayActual = results.getListPayActual()
            diff = [a_i - b_i for a_i, b_i in zip(listPayMax, listPayActual)]
            dictResults[numParcels].append(statistics.mean(diff))

            letter='a'
            for weightName in Simulator.namesOfWeights:
                dictResults=dictResultsAllWeight[weightName]
                with open(f'{prePath}/resultsNonUniform/{numParcels}/{index}{letter}.json') as json_file:
                    results = json.load(json_file)
                results = Result(results)
                listPayMax = results.getListPayMax()
                listPayActual = results.getListPayActual()
                diff = [a_i-b_i for a_i, b_i in zip(listPayMax, listPayActual)]
                dictResults[numParcels].append(statistics.mean(diff))

                letter = chr(ord(letter) + 1)  # the next letter in alphbet



        return dictResults

    for i in range(100):
        DBdiffCostOneIndex(index=str(i))

    plotDBddiffCost(numParcels,dictResultsAllWeight)



def succ(numParcels):
    parcels = chooseParcels(numParcels)

    succsListAvg = []
    succsListMedian = []
    succsListStdev = []

    driversRange=range(100,601,100)

    for numDrivers in driversRange:
        resultsPerAmount = []

        for i in range(10):
            drivers = chooseRoutes(numDrivers)
            graphSimulator = Simulator(routes=drivers, numberOfSP=sp.numOfSP, numDrivers=numDrivers*2, stopTime=stopTime,
                                       maxTimeMin=maxTimeMin*2, maxDistanceMeters=maxDistanceMeters,
                                       costDistance=costDistance, costDrivers=costDrivers)
            results=graphSimulator.sendParcelsByRandomWeight(parcels)
            succ=results.getAmountOfSucc()
            resultsPerAmount.append(succ/numParcels)

        succsListAvg.append(statistics.mean(resultsPerAmount))
        succsListMedian.append(statistics.median(resultsPerAmount))
        succsListStdev.append(statistics.stdev(resultsPerAmount))

    plotSucc(driversRange,succsListAvg,succsListMedian,succsListStdev)

if __name__=='__main__':
    costDistance = 0.001
    costDrivers = 3
    stopTime = 1
    maxTimeMin = minutesInDay*2
    maxDistanceMeters = 60000000

    numParcels=300
    folderName='resultsUniform'


    # ################DONT CALL THIS FUNCTION
    buildDBsameParcels(numParcels,folderName)

    # DBpsucc(numParcels,folderName)
    # DBpduration(numParcels,folderName)
    # DBpdistance(numParcels,folderName)
    # DBpdiffCost(numParcels,folderName)

    numDrivers=200
    # ################DONT CALL THIS FUNCTION buildDBsameDrivers(numDrivers,folderName)
    # DBddiffCost(numDrivers,folderName)




    # numDrivers=50
    # numParcels=100
    # # parcels=chooseParcels(numParcels)
    # with open(f'parcels/uniformDistribution100000.json') as json_file:
    #     parcels = json.load(json_file, object_hook=convertStrToDate)
    # sampleParcels = parcels[:numParcels]
    # for i, route in enumerate(sampleParcels):
    #     route['idParcel'] = i + 1
    # parcels= sampleParcels
    # print("-------parcels------")
    # pprint(parcels)
    # # drivers = chooseRoutes(numDrivers)
    # with open(f'paths/uniformDistribution10000.json') as json_file:
    #     routes = json.load(json_file, object_hook=convertStrToDate)
    # sampleRoutes = routes[:numDrivers]
    # for i, route in enumerate(sampleRoutes):
    #     route['driver'] = i + 1
    # drivers= sampleRoutes
    # print("-------drivers------")
    # pprint(drivers)
    #
    # graphSimulator = Simulator(routes=drivers, numberOfSP=sp.numOfSP, numDrivers=numDrivers, stopTime=stopTime,
    #                            maxTimeMin=maxTimeMin, maxDistanceMeters=maxDistanceMeters,
    #                            costDistance=costDistance, costDrivers=costDrivers)
    # resultsNonUniform = graphSimulator.sendParcelsBySameWeight(parcels,'weightPriortyDistanceDriverTime')
    # pprint(resultsNonUniform.getResult())
    # print(resultsNonUniform.getAmountOfSucc())

