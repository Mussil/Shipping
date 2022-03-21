import json
import os
import random
import statistics
from pprint import pprint

from flasker.SPutils import sp
from flasker.plots import avgFunc1, medianFunc1, compareWeightsMax, compareWeightsActual, durationFunc3, plotSucc, \
    plotDuration, plotDBSucc

random.seed()

from flasker.createGraph import buildGraph
from flasker.helpers import convertStrToDate, convertDateToStr


def chooseParcels(numParcels):
    with open(f'parcels/NonUniformTimeDistribution100000.json') as json_file:
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

    def __init__(self,routes,numberOfSP,numDrivers,stopTime,maxTimeMin,maxDistanceMeters,costDistance,costDrivers):
        self.g = buildGraph(routes=routes, maxSp=numberOfSP, maxDrivers=numDrivers, stopTime=stopTime, maxTimeMin=maxTimeMin,
                       maxDistanceMeters=maxDistanceMeters, costDistance=costDistance, costDrivers=costDrivers)

        # all the combination of priorities
        alph=0
        beta=0
        self.namesOfWeights=['weightPriortyTimeDriverDistance','weightPriortyTimeDistanceDriver','weightPriortyDistanceDriverTime','weightPriortyDistanceTimeDriver','weightPriortyDriverDistanceTime','weightPriortyDriverTimeDistance']
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



    def getResult(self):
        return self.result



def succ(numParcels):


    succsListAvg = []
    succsListMedian = []
    succsListStdev = []

    driversRange=range(100,601,100)

    for numDrivers in driversRange:
        resultsPerAmount = []

        for i in range(10):
            parcels = chooseParcels(numParcels)
            drivers = chooseRoutes(numDrivers)
            graphSimulator = Simulator(routes=drivers, numberOfSP=sp.numOfSP, numDrivers=numDrivers, stopTime=stopTime,
                                       maxTimeMin=maxTimeMin, maxDistanceMeters=maxDistanceMeters,
                                       costDistance=costDistance, costDrivers=costDrivers)
            results=graphSimulator.sendParcelsByRandomWeight(parcels)
            succ=results.getAmountOfSucc()
            resultsPerAmount.append(succ/numParcels)

        succsListAvg.append(statistics.mean(resultsPerAmount))
        succsListMedian.append(statistics.median(resultsPerAmount))
        succsListStdev.append(statistics.stdev(resultsPerAmount))

    plotSucc(driversRange,succsListAvg,succsListMedian,succsListStdev)

def comparePriority(numDrivers):
    drivers = chooseRoutes(numDrivers)
    graphSimulator = Simulator(routes=drivers, numberOfSP=sp.numOfSP, numDrivers=numDrivers, stopTime=stopTime,
                               maxTimeMin=maxTimeMin, maxDistanceMeters=maxDistanceMeters,
                               costDistance=costDistance, costDrivers=costDrivers)

    parcelsRange=range(50,1001,50)
    diffDict={}
    ratioDict={}
    # diffDict = {k: [] for k in graphSimulator.namesOfWeights}
    # ratioDict= {k: [] for k in graphSimulator.namesOfWeights}
    for i in range(10):
        diffDict[i]={k: [] for k in graphSimulator.namesOfWeights}
        ratioDict[i]={k: [] for k in graphSimulator.namesOfWeights}
        for numParcels in parcelsRange:
            parcels=chooseParcels(numParcels)

            for nameOfWeight in graphSimulator.namesOfWeights:
                results = graphSimulator.sendParcelsBySameWeight(parcels,nameOfWeight)
                payMax=results.getListPayMax()
                payActual=results.getListPayActual()
                diff=[a_i - b_i for a_i, b_i in zip(payMax, payActual)]
                ratio=[1-(b_i / a_i) for a_i, b_i in zip(payMax, payActual)]
                diffDict[i][nameOfWeight].append(statistics.mean(diff))
                ratioDict[i][nameOfWeight].append(statistics.mean(ratio))

    path= f'resultsNonUniform/comparePriority{numDrivers}Diff'
    with open(f'{path}.json', 'w') as json_file:
        json.dump(diffDict, json_file, indent=4)
    path= f'resultsNonUniform/comparePriority{numDrivers}Ratio'
    with open(f'{path}.json', 'w') as json_file:
        json.dump(ratioDict, json_file, indent=4)


def compareDurations(parcels):
    durationsRandom=[]
    durationsTimeDriverDistance=[]
    durationsDriverDistanceTime=[]

    driversRange=range(50,501,50)
    for numDrivers in driversRange:
        drivers = chooseRoutes(numDrivers)
        graphSimulator = Simulator(routes=drivers, numberOfSP=sp.numOfSP, numDrivers=numDrivers, stopTime=stopTime,
                                   maxTimeMin=maxTimeMin, maxDistanceMeters=maxDistanceMeters,
                                   costDistance=costDistance, costDrivers=costDrivers)
        results=graphSimulator.sendParcelsByRandomWeight(parcels)
        durationsRandom.append(statistics.mean(results.getListDuration()))
        results=graphSimulator.sendParcelsBySameWeight(parcels,'weightPriortyTimeDriverDistance')
        durationsTimeDriverDistance.append(statistics.mean(results.getListDuration()))
        results=graphSimulator.sendParcelsBySameWeight(parcels,'weightPriortyDriverDistanceTime')
        durationsDriverDistanceTime.append(statistics.mean(results.getListDuration()))
        # resultsNonUniform=graphSimulator.sendParcelsBySameWeight(parcels,'weightPriortyTimeDistanceDriver')
        # durationsTimeDistanceDriver.append(statistics.mean(resultsNonUniform.getListDuration()))

    plotDuration(driversRange,durationsRandom,durationsTimeDriverDistance,durationsDriverDistanceTime)

def func1(graphSimulator):
    payMaxAvg=[]
    payMaxMedian=[]

    payActualAvg=[]
    payActualMedian=[]

    parcelsRange=range(50,1001,50)

    for numParcels in parcelsRange:
        parcels=chooseParcels(numParcels)
        results=graphSimulator.sendParcelsBySameWeight(parcels,'weightPriortyTimeDriverDistance')

        payMax=results.getListPayMax()
        payMaxAvg.append(statistics.mean(payMax))
        payMaxMedian.append(statistics.median(payMax))
        payActual=results.getListPayActual()
        payActualAvg.append(statistics.mean(payActual))
        payActualMedian.append(statistics.median(payActual))

        # resultsNonUniform.printResult()
    print(payMaxAvg)
    print(payMaxMedian)
    print(payActualAvg)
    print(payActualMedian)
    print(list(parcelsRange))
    avgFunc1(yPayMax=payMaxAvg,yPayActual=payActualAvg)
    medianFunc1(yPayMax=payMaxMedian,yPayActual=payActualMedian)

def func2(graphSimulator):
    payMaxMedian={name : [] for name in graphSimulator.namesOfWeights}
    payActualMedian= {name : [] for name in graphSimulator.namesOfWeights}

    parcelsRange=range(50,1001,50)

    for numParcels in parcelsRange:
        parcels=chooseParcels(numParcels)

        for nameOfWeight in graphSimulator.namesOfWeights:
            results=graphSimulator.sendParcelsBySameWeight(parcels,nameOfWeight)

            payMax=results.getListPayMax()
            payMaxMedian[nameOfWeight].append(statistics.median(payMax))
            payActual=results.getListPayActual()
            payActualMedian[nameOfWeight].append(statistics.median(payActual))

    compareWeightsMax(parcelsRange,payMaxMedian)
    compareWeightsActual(parcelsRange,payActualMedian)


def func3(parcels):
    durations=[]
    driversRange=range(50,501,50)
    for numDrivers in driversRange:
        drivers = chooseRoutes(numDrivers)
        graphSimulator = Simulator(routes=drivers, numberOfSP=sp.numOfSP, numDrivers=numDrivers, stopTime=stopTime,
                                   maxTimeMin=maxTimeMin, maxDistanceMeters=maxDistanceMeters,
                                   costDistance=costDistance, costDrivers=costDrivers)
        results=graphSimulator.sendParcelsByRandomWeight(parcels)
        durations.append(statistics.mean(results.getListDuration()))
    durationFunc3(driversRange,durations)
    return durations


##################   from here

def buildDB():
    numParcels=300
    parcels=chooseParcels(numParcels)
    with open(f'resultsNonUniform/300parcels/parcelsFile.json', 'w', encoding='utf-8') as f:
        json.dump(parcels, f, indent=4,default=convertDateToStr)


    driversRange=range(100,601,100)


    for i in range(100):

        for numDrivers in driversRange:
            drivers = chooseRoutes(numDrivers)
            graphSimulator = Simulator(routes=drivers, numberOfSP=sp.numOfSP, numDrivers=numDrivers, stopTime=stopTime,
                                       maxTimeMin=maxTimeMin, maxDistanceMeters=maxDistanceMeters,
                                       costDistance=costDistance, costDrivers=costDrivers)

            # Check whether the specified path exists or not
            path= f'resultsNonUniform/300parcels/results/{numDrivers}'
            isExist = os.path.exists(path)
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)


            results = graphSimulator.sendParcelsByRandomWeight(parcels)
            with open(f'{path}/{i}.json', 'w', encoding='utf-8') as f:
                json.dump(results.getResult(), f, indent=4)

            letter='a'
            for nameOfWeight in graphSimulator.namesOfWeights:
                results = graphSimulator.sendParcelsBySameWeight(parcels,nameOfWeight)
                with open(f'{path}/{i}{letter}.json', 'w', encoding='utf-8') as f:
                    json.dump(results.getResult(), f, indent=4)
                letter = chr(ord(letter) + 1) #the next letter in alphbet


            #save the drivers details
            # Check whether the specified path exists or not
            path= f'resultsNonUniform/300parcels/driversDB/{numDrivers}'
            isExist = os.path.exists(path)
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)

            with open(f'{path}/{i}.json', 'w', encoding='utf-8') as f:
                json.dump(drivers, f, indent=4, default=convertDateToStr)




def buildDBpostCreationWithWeights():
    '''
    this function comes after the buildDB function that create all the graphs for 300 parcels,
    this function add the weight and save it also for the same data
    :return:
    '''
    with open(f'resultsNonUniform/db300parcels/parcelsFile.json') as json_file:
        parcels = json.load(json_file, object_hook=convertStrToDate)


    driversRange=range(100,501,100)


    for i in range(100):

        for numDrivers in driversRange:
            path= f'resultsNonUniform/db300parcels/driversDB/{numDrivers}'
            with open(f'{path}/{i}.json') as json_file:
                drivers = json.load(json_file, object_hook=convertStrToDate)

            graphSimulator = Simulator(routes=drivers, numberOfSP=sp.numOfSP, numDrivers=numDrivers, stopTime=stopTime,
                                       maxTimeMin=maxTimeMin, maxDistanceMeters=maxDistanceMeters,
                                       costDistance=costDistance, costDrivers=costDrivers)

            # Check whether the specified path exists or not
            path= f'resultsNonUniform/db300parcels/{numDrivers}'
            isExist = os.path.exists(path)
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs(path)


            letter='a'
            for nameOfWeight in graphSimulator.namesOfWeights:
                results = graphSimulator.sendParcelsBySameWeight(parcels,nameOfWeight)
                with open(f'{path}/{i}{letter}.json', 'w', encoding='utf-8') as f:
                    json.dump(results.getResult(), f, indent=4)
                letter = chr(ord(letter) + 1) #the next letter in alphbet




def DBsucc(numParcels):
    driversRange=range(100,601,100)
    dictResults={name : [] for name in driversRange}

    def DBsuccOneIndex(index):
        for numDrivers in driversRange:
            with open(f'resultsNonUniform/{numParcels}parcels/results/{numDrivers}/{index}.json') as json_file:
                results = json.load(json_file)
            results = Result(results)
            succ = results.getAmountOfSucc()
            dictResults[numDrivers].append(succ / numParcels)
        return dictResults

    for i in range(50):
        DBsucc(index=str(i))

    plotDBSucc(numParcels,dictResults)


if __name__=='__main__':
    numDrivers=200
    costDistance = 0.001
    costDrivers = 3
    stopTime = 1
    maxTimeMin = 1440
    maxDistanceMeters = 60000000

    # drivers=chooseRoutes(numDrivers)
    # graphSimulator=Simulator(routes=drivers,numberOfSP=sp.numOfSP,numDrivers=numDrivers,stopTime=stopTime,maxTimeMin=maxTimeMin,maxDistanceMeters=maxDistanceMeters,costDistance=costDistance,costDrivers=costDrivers)
    #

    numParcels=300
    # parcels=chooseParcels(numParcels)
    # resultsNonUniform=graphSimulator.sendParcelsByRandomWeight(parcels)
    # pprint(resultsNonUniform)

    # func1(graphSimulator)
    # func2(graphSimulator)
    # func3(parcels)

    # succ(numParcels)


    # numDrivers=100
    # # comparePriority(numDrivers)
    # numParcels=100
    # parcels=chooseParcels(numParcels)
    # compareDurations(parcels)

    # buildDB()
    numParcels=300
    DBsucc(numParcels)

