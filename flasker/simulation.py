from flasker.createPaths import createRandomPaths, createPaths
from flasker.createGraph import buildGraph
from flasker.createParcels import createRandomParcels


def run():
    numDrivers = 13
    numberOfSP = 70
    numParcels=15
    maxStopsPerDriver=15
    # routes=createRandomPaths(numDrivers=numDrivers, numSP=numberOfSP,maxStops=10)
    routes=createPaths(numSP=numberOfSP,numDrivers=numDrivers)
    print(routes)
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