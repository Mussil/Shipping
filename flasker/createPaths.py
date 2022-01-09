import json
import random
from collections import OrderedDict

import networkx as nx

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
        numberOfNodesInPath=random.randint(2, maxStops)
        # print(numOfSp)
        # print(maxSp)

        path['path']=random.sample(range(1,numSP+1), numberOfNodesInPath)
        paths.append(path)


    # TODO: save paths to file (in directory)

    with open('pathRandomFile.json', 'w', encoding='utf-8') as f:
        json.dump(paths, f, indent=4, default=str)
    return paths

def createGraphOfSP(numberOfSP):


    edgesTuple=[]
    distanceList=[]
    edgesAndWeightList=[] #for nx
    #create edges
    for i in range(1,numberOfSP+1):
        for j in range(1,numberOfSP+1):
            print(i,j)
            if i!=j: #no self-edges
                duration, distance=calcDistTime(i,j,initialDate)
                edgesTuple.append((i,j))
                distanceList.append(distance)
                edgesAndWeightList.append((i,j,{'distance':distance}))#for nx


    # g=igraph.Graph(directed=True)
    # g.add_vertices(numberOfSP)
    # g.add_edges(edgesTuple,{'distance':distanceList})
    # g.write_pickle('tempGraph20Sp.gml')

    G = nx.DiGraph()
    G.add_edges_from(edgesAndWeightList)

    nx.write_gpickle(G,'spFullGraph.gpickle')

    return G


def createPathsByHP(numberOfSP,maxStops,numDrivers):
    print("CREATING PATHS BY TSP")
    # g=createGraphOfSP(numberOfSP)
    g = nx.read_gpickle("spFullGraph.gpickle")

    # subGraph=g.induced_subgraph(nodes, implementation='auto')
    # MST=subGraph.spanning_tree(weights='distance',return_tree=True)
    # igraph.plot(MST)

    paths=[]
    #TODO: FIX ValueError: Sample larger than population or is negative

    for i in range(numDrivers):
        path={}
        path['driver']=i+1 #the name of the driver
        path['start']=addMin(initialDate,random.randint(0, minutesInDay)) #add to inital day some random minutes
        numberOfNodesInPath=random.randint(2, maxStops)
        nodes = random.sample(range(1,numberOfSP), numberOfNodesInPath)
        # print(nodes)
        H = g.subgraph(nodes)


        pathTSP=nx.approximation.traveling_salesman_problem(H, weight='distance', nodes=nodes, cycle=False, method=None)

        path['path']= list(OrderedDict.fromkeys(pathTSP))
        paths.append(path)


    # TODO: save paths to file (in directory)

    with open('pathTSPFile.json', 'w', encoding='utf-8') as f:
        json.dump(paths, f, indent=4, default=str)
    return paths


#
# def createPathsByDijkstra(g,numDrivers,numberOfSP):
#     # TODO: right now, there is no sense in this function- fix or delete
#     paths=[]
#     for i in range(numDrivers):
#         path = {}
#         path['driver'] = i + 1  # the name of the driver
#         path['start'] = addMin(initialDate, random.randint(0, minutesInDay))  # add to inital day some random minutes
#         source,target=random.sample(range(0,numberOfSP), 2)
#         distance=g.es.find(_source=source,_target=target)['distance']
#         g.es.find(_source=source, _target=target)['distance']=float('inf')
#         path = g.get_shortest_paths(source, to=target,weights='distance',mode=igraph.OUT,output='vpath')
#         print(source,target)
#         print(path[0])
#         g.es.find(_source=source, _target=target)['distance']=distance



if __name__=='__main__':
    numberOfSP=20
    numDrivers=20
    g=createGraphOfSP(numberOfSP)

    # f=igraph.Graph(directed=True)
    # f=igraph.read_pickle('tempGraph20Sp.gml')
    # createPathsByDijkstra(g,numDrivers,numberOfSP)



    # createPathsByHP(numberOfSP,maxStops=15,numDrivers=numDrivers)