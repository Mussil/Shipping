import json
import random
from flasker.helpers import addMin,initialDate,minutesInDay
import igraph
from flasker.pathCalc import calcDistTime
import pickle



def createRandomPaths(numDrivers,numSP,maxStops):
    paths=[]
    #TODO: FIX ValueError: Sample larger than population or is negative

    for i in range(numDrivers):
        path={}
        path['driver']=i+1 #the name of the driver
        path['start']=addMin(initialDate,random.randint(0, minutesInDay)) #add to inital day some random minutes
        numOfSp=random.randint(2, maxStops)
        # print(numOfSp)
        # print(maxSp)

        path['path']=random.sample(range(1,numSP+1), numOfSp)
        paths.append(path)


    # TODO: save paths to file (in directory)

    with open('pathRandomFile.json', 'w', encoding='utf-8') as f:
        json.dump(paths, f, indent=4, default=str)
    return paths

def createGraphOfSP(numberOfSP):
    g=igraph.Graph(directed=True)
    g.add_vertices(numberOfSP)

    edgesTuple=[]
    durationsList=[]
    #create edges
    for i in range(numberOfSP):
        for j in range(numberOfSP):
            print(i,j)
            if i!=j: #no self-edges
                duration, distance=calcDistTime(i+1,j+1,initialDate)
                edgesTuple.append((i,j))
                durationsList.append(duration)

    g.add_edges(edgesTuple,{'duration':durationsList})
    # g.write_pickle('tempGraph20Sp.gml')
    return g


def createPathsByDijkstra(g,numDrivers,numberOfSP):
    paths=[]
    for i in range(numDrivers):
        path = {}
        path['driver'] = i + 1  # the name of the driver
        path['start'] = addMin(initialDate, random.randint(0, minutesInDay))  # add to inital day some random minutes
        source,target=random.sample(range(0,numberOfSP), 2)
        duration=g.es.find(_source=source,_target=target)['duration']
        g.es.find(_source=source, _target=target)['duration']=float('inf')
        path = g.get_shortest_paths(source, to=target,weights='duration',mode=igraph.OUT,output='vpath')
        print(source,target)
        print(path[0])
        g.es.find(_source=source, _target=target)['duration']=duration



if __name__=='__main__':
    numberOfSP=20
    numDrivers=20
    g=createGraphOfSP(numberOfSP)
    # f=igraph.Graph(directed=True)
    # f=igraph.read_pickle('tempGraph20Sp.gml')
    createPathsByDijkstra(g,numDrivers,numberOfSP)
