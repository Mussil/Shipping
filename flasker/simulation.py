from flasker.createPaths import createRandomPaths, createPathsByHP
from flasker.createGraph import buildGraph
from flasker.createParcels import createRandomParcels


def run():
    numDrivers = 13
    numberOfSP = 20
    numParcels=15
    maxStopsPerDriver=12
    # routes=createRandomPaths(numDrivers=numDrivers, numSP=maxSp,maxStops=10)
    routes=createPathsByHP(numberOfSP,maxStops=maxStopsPerDriver,numDrivers=numDrivers)

    parcels=createRandomParcels(numParcels=numParcels, maxSp=numberOfSP)
    g=buildGraph(routes=routes,maxSp=numberOfSP,maxDrivers=numDrivers,stopTime=1,maxTimeMin=400,maxDistanceMeters=10000)

    g.addWeights(nameOfWeight='weightPriortyTimeDriverDistance',A='time',B='driver',C='distance',alph=0,beta=0)

    for parcel in parcels:
        source=parcel['source']
        target=parcel['target']
        time=parcel['startTime']

        path = g.getDetailsShortestPath(source, target, time,weight='weightPriortyTimeDriverDistance')
        print("-----")
        print(parcel)
        print(path)

if __name__=='__main__':
    run()