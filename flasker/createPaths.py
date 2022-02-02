import datetime
import json
import random
from collections import OrderedDict
from pprint import pprint

import networkx as nx
from collections import defaultdict

from flasker.helpers import addMin,initialDate,minutesInDay,access_token
import igraph
from flasker.pathCalc import calcDistTime
import pickle
from shapely.geometry import Point, LineString
from mapbox import Directions

from SPutils import sp

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

    with open('paths/pathRandomFile.json', 'w', encoding='utf-8') as f:
        json.dump(paths, f, indent=4, default=str)
    return paths

# def createGraphOfSP(numberOfSP):
#
#
#     edgesTuple=[]
#     distanceList=[]
#     edgesAndWeightList=[] #for nx
#     #create edges
#     for i in range(1,numberOfSP+1):
#         for j in range(1,numberOfSP+1):
#             print(i,j)
#             if i!=j: #no self-edges
#                 duration, distance=calcDistTime(i,j,initialDate)
#                 edgesTuple.append((i,j))
#                 distanceList.append(distance)
#                 edgesAndWeightList.append((i,j,{'distance':distance}))#for nx
#
#
#     # g=igraph.Graph(directed=True)
#     # g.add_vertices(numberOfSP)
#     # g.add_edges(edgesTuple,{'distance':distanceList})
#     # g.write_pickle('tempGraph20Sp.gml')
#
#     G = nx.DiGraph()
#     G.add_edges_from(edgesAndWeightList)
#
#     nx.write_gpickle(G,'spFullGraph.gpickle')
#
#     return G


# def createPathsByHP(numberOfSP,maxStops,numDrivers):
#     print("CREATING PATHS BY TSP")
#     # g=createGraphOfSP(numberOfSP)
#     g = nx.read_gpickle("spFullGraph.gpickle")
#
#     # subGraph=g.induced_subgraph(nodes, implementation='auto')
#     # MST=subGraph.spanning_tree(weights='distance',return_tree=True)
#     # igraph.plot(MST)
#
#     paths=[]
#     #TODO: FIX ValueError: Sample larger than population or is negative
#
#     for i in range(numDrivers):
#         path={}
#         path['driver']=i+1 #the name of the driver
#         path['start']=addMin(initialDate,random.randint(0, minutesInDay)) #add to inital day some random minutes
#         numberOfNodesInPath=random.randint(2, maxStops)
#         nodes = random.sample(range(1,numberOfSP), numberOfNodesInPath)
#         # print(nodes)
#         H = g.subgraph(nodes)
#
#
#         pathTSP=nx.approximation.traveling_salesman_problem(H, weight='distance', nodes=nodes, cycle=False, method=None)
#
#         path['path']= list(OrderedDict.fromkeys(pathTSP))
#         paths.append(path)
#
#
#
#     with open('paths/pathTSPFile.json', 'w', encoding='utf-8') as f:
#         json.dump(paths, f, indent=4, default=str)
#     return paths

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



def getPathMapBoxLine(origin,destination):
    '''
    :param origin: coords of orignal point
    :param destination: coords of destination point
    :return: stations that are around the path between orgin and dest
    the calc is based on stations that are closed to the line , air point of view, not realted to the roads and what really close by time or km
    '''
    service = Directions(access_token=access_token)
    response = service.directions([origin, destination],'mapbox/driving')
    # print(response.status_code)
    driving_routes = response.geojson()
    line=driving_routes['features'][0]['geometry']['coordinates']
    # print(driving_routes)
    # print(json.dumps(line))
    # print()

    # coordList=coordinatesAllSp()
    coordList=sp.getListOfFidCoords()
    line = LineString(line)

    pointDistFromStart=[]
    # originPoint=Point(origin['geometry']['coordinates'])
    originPoint=Point(origin)

    for id,point in coordList:
        point2 = Point(point)
        if line.distance(point2) < 1e-3 :
            pointDistFromStart.append((point,id,originPoint.distance(point2)))

    sortedPoints=sorted(pointDistFromStart,key=lambda x: x[2])
    spNames=list(map(lambda x: x[1],sortedPoints))
    return spNames



def getPathMapBoxKM(origin,destination):
    '''
    :param origin: coords of orignal point
    :param destination: coords of destination point
    :return: stations that are around the path between orgin and dest
    the calc is based on stations that are closed (by km) to points in the paths
    '''
    service = Directions(access_token=access_token)
    response = service.directions([origin, destination],'mapbox/driving',overview='full')#annotations = ['distance']
    driving_routes = response.geojson()
    line=driving_routes['features'][0]['geometry']['coordinates']
    # print(driving_routes['features'][0]['properties']['distance'])
    coordList=sp.getListOfFidCoords()

    pointDistFromStart=[]
    dictId=defaultdict(list)
    for point in line:
        for id,stationCoords in coordList:
            response = service.directions([point,stationCoords], 'mapbox/driving',annotations = ['distance'])
            driving_routes = response.geojson()
            dist=driving_routes['features'][0]['properties']['distance']
            if dist <= 300 :
                pointDistFromStart.append((stationCoords,id,dist))
                dictId[id].append((stationCoords,id,dist))
    # print(dictId)
    # print()
    keys=dictId.values()
    print("keys")
    print(keys)
    # print(keys)
    notDup=[]
    for lis in keys:
        # print(lis)
        mini=min(lis,key=lambda x:x[2])
        notDup.append(mini)
    print("notDup")
    print(notDup)
    # print(notDup)
    # print()
    # print(pointDistFromStart)
    # sortedPoints=sorted(notDup,key=lambda x: x[2])
    total=[]
    for point in pointDistFromStart:
        print(point)
        if point in notDup and point not in total:
            total.append(point)
    spNames=list(map(lambda x: x[1],total))
    return spNames

    # print(line)
    # pointDistFromStart=[]
    # # originPoint=Point(origin['geometry']['coordinates'])
    # originPoint=Point(origin)
    #
    # for id,point in coordList:
    #     point2 = Point(point)
    #     if line.distance(point2) < 1e-3 :
    #         pointDistFromStart.append((point,id,originPoint.distance(point2)))
    #
    # sortedPoints=sorted(pointDistFromStart,key=lambda x: x[2])
    # spNames=list(map(lambda x: x[1],sortedPoints))
    # return spNames





def createPaths(numDrivers,numSP,funGetPathMapBox=getPathMapBoxLine):
    paths=[]

    for i in range(numDrivers):
        path={}
        path['driver']=i+1 #the name of the driver
        path['start']=addMin(initialDate,random.randint(0, minutesInDay)) #add to inital day some random minutes
        originSp,destinationSp=random.sample(range(1,numSP+1), 2)

        # origin = getStationDeatils(originSp)
        # destination = getStationDeatils(destinationSp)

        origin = sp.getStationCoords(originSp)
        destination = sp.getStationCoords(destinationSp)


        path['path']=funGetPathMapBox(origin, destination)
        paths.append(path)

    with open('paths/pathsFile.json', 'w', encoding='utf-8') as f:
        json.dump(paths, f, indent=4, default=str)
    return paths


if __name__=='__main__':
    numberOfSP=70
    numDrivers=20
    # g=createGraphOfSP(numberOfSP)
    # createPathsByDijkstra(g,numDrivers,numberOfSP)
    # createPathsByHP(numberOfSP,maxStops=15,numDrivers=numDrivers)

    # createPaths(numDrivers=numDrivers, numSP=numberOfSP,funGetPathMapBox=getPathMapBoxLine)
    # createPaths(numDrivers=numDrivers, numSP=numberOfSP,funGetPathMapBox=getPathMapBoxKM)

    origin = sp.getStationCoords(1)
    destination = sp.getStationCoords(19)
    linePaths=getPathMapBoxLine(origin,destination)
    print(linePaths)
    lineCoords=[]
    for point in linePaths:
        lineCoords.append(sp.getStationCoords(point))
    print(lineCoords)

    # kmPaths=getPathMapBoxKM(origin,destination)
    # print(kmPaths)
    # kmCoords=[]
    # for point in kmPaths:
    #     kmCoords.append(sp.getStationCoords(point))
    # print(kmCoords)

    # randomPath=[
    #     17,
    #     10,
    #     4,
    #     15,
    #     12,
    #     14,
    #     11,
    #     13,
    #     18
    # ]
    # randCoords=[]
    # for point in randomPath:
    #     randCoords.append(sp.getStationCoords(point))
    # print(randCoords)