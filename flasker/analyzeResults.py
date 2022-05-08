import json
import statistics

from matplotlib import pyplot as plt

from flasker.plots import plotDBSucc
from simulationNewParallel import Simulator, Result, numRunsG, driversRangeG, folderNameG


def DBpsucc(numParcels,folderName):
    dictResults={name : [] for name in driversRange}
    prePath=f'{folderName}/results/{numParcels}parcels'

    def DBsuccOneIndex(index):
        for numDrivers in driversRange:
            with open(f'{prePath}/{numDrivers}drivers/{index}.json') as json_file:
                results = json.load(json_file)
            results = Result(results)
            succ = results.getAmountOfSucc()
            dictResults[numDrivers].append(succ / numParcels)
        return dictResults

    for i in range(numRuns):
        DBsuccOneIndex(index=str(i))


    plotDBSucc(numParcels,dictResults)
    return dictResults

def DBcost():
    prePath='allResults/resultsUniform2days/results'
    driversFolder='300drivers'

    def OneIndex(index):
        with open(f'{prePath}/{numParcels}parcels/{driversFolder}/{index}.json') as json_file:
            results = json.load(json_file)
        results = Result(results)
        payMax = results.getListPayMax()
        payActual = results.getListPayActual()

        return statistics.mean(payMax),  statistics.mean(payActual)

    parcelsRange=range(100,1001,100)
    dictMax={name : [] for name in parcelsRange}
    dictActual={name : [] for name in parcelsRange}
    for numParcels in parcelsRange:
        for index in range(50):
            meanPayMax,meanPayActual =OneIndex(index)

            dictMax[numParcels].append(meanPayMax)
            dictActual[numParcels].append(meanPayActual)

    myList = dictMax.items()
    myList = sorted(myList)
    numParcels, yMax = zip(*myList)
    avgMax = list(map(lambda lis: statistics.mean(lis), yMax))
    medianMax=list(map(lambda lis: statistics.median(lis), yMax))
    stdevMax=list(map(lambda lis: statistics.stdev(lis), yMax))


    myList = dictActual.items()
    myList = sorted(myList)
    numParcels, yActual = zip(*myList)
    avgActual = list(map(lambda lis: statistics.mean(lis), yActual))
    medianActual=list(map(lambda lis: statistics.median(lis), yActual))
    stdevActual=list(map(lambda lis: statistics.stdev(lis), yActual))



    plt.plot(numParcels, avgMax,label='Average maximum cost')
    plt.errorbar(numParcels, avgMax ,stdevMax, linestyle='None', marker='^',color='green',label='Standard deviation')

    plt.plot(numParcels, avgActual,label='Average actual cost',color='orange')
    plt.errorbar(numParcels, avgActual ,stdevActual, linestyle='None', marker='^',color='green')



    plt.legend()
    plt.xlabel('Number of parcels')
    plt.xticks(numParcels, numParcels)
    plt.ylabel('Average of cost')
    plt.title('300 drivers')
    plt.show()


if __name__=='__main__':
    # numRuns=numRunsG
    # driversRange=driversRangeG
    # folderName=folderNameG
    #
    #
    # numParcels=1000
    # dictResults=DBpsucc(numParcels, folderName)




    # for numParcels in range(100,1001,100):
    #     dictResults=DBpsucc(numParcels, folderName)
    #     # plot
    #     myList = dictResults.items()
    #     myList = sorted(myList)
    #     x, y = zip(*myList)
    #     avg = list(map(lambda lis: statistics.mean(lis), y))
    #     plt.plot(x, avg, label=f'{numParcels} parcels')
    #
    # plt.ylabel('Success rate')
    # plt.xlabel('Number of drivers')
    # plt.legend()
    # plt.show()

    DBcost()