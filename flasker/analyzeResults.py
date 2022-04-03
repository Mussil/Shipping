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


if __name__=='__main__':
    numRuns=numRunsG
    driversRange=driversRangeG
    folderName=folderNameG


    numParcels=500
    dictResults=DBpsucc(numParcels, folderName)




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
