import datetime
import json
import random
import time
from collections import OrderedDict
from pprint import pprint
import os.path

import networkx as nx
from collections import defaultdict

import numpy as np
import requests
from shapely.ops import nearest_points

from flasker.helpers import addMin, initialDate, minutesInDay, access_token, listCorrdsToString, convertDateToStr
import igraph
from flasker.pathCalc import calcDistTime
import pickle
from shapely.geometry import Point, LineString
from mapbox import Directions

from SPutils import sp

def createRandomPaths(numDrivers,numSP,maxStops):
    paths=[]

    for i in range(numDrivers):
        path={}
        path['driver']=i+1 #the name of the driver
        path['start']=addMin(initialDate,random.randint(0, minutesInDay)) #add to inital day some random minutes
        numberOfNodesInPath=random.randint(2, maxStops)

        wayFid=random.sample(range(1,numSP+1), numberOfNodesInPath)
        wayCoords = sp.listFidToCorrds(wayFid)

        stringPoints = listCorrdsToString(wayCoords)
        x = requests.get("https://api.mapbox.com/optimized-trips/v1/mapbox/driving/" +
                         stringPoints +
                         "?access_token="+
                         access_token)
        waypoints = x.json()['waypoints']
        #todo: check what fid is each point,
        #todo: check the order of the optimizion
        locs = list(map(lambda x: x['location'], sorted(waypoints, key=lambda x: x['waypoint_index'])))


        # path['path']=random.sample(range(1,numSP+1), numberOfNodesInPath)
        paths.append(path)

    with open('paths/temp/pathRandomFile.json', 'w', encoding='utf-8') as f:
        json.dump(paths, f, indent=4, default=str)
    return paths


def getDist(coor1,coor2):
    stringPoints = listCorrdsToString([coor1,coor2])
    res = requests.get("https://api.mapbox.com/directions-matrix/v1/mapbox/driving/"
                                     + stringPoints
                                     + "?access_token="
                                     + access_token
                                     + "&annotations=distance"
                                     + "&approaches=curb;curb"
                                     + "&destinations=1"
                                     + "&sources=0"
                                     )
    print(res.json())
    return res.json()['distances'][0][0]



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

    coordList=sp.getListOfFidCoords()
    line = LineString(line)

    pointDistFromStart=[]
    originPoint=Point(origin)

    for id,point in coordList:
        point2 = Point(point)
        dist=line.distance(point2)
        if  dist< 1e-3 -4e-4 : #1e-3
            # print(line.distance(point2))
            # pointOnline = nearest_points(line, point2)[0]
            # print(pointOnline)
            # print(point2)
            # dist=getDist([pointOnline.x,pointOnline.y],[point2.x,point2.y])
            # print(dist)
            # if dist <=1500:
            pointDistFromStart.append((point,id,originPoint.distance(point2),dist))

    # print(pointDistFromStart)
    while len(pointDistFromStart) >12:
        # print(pointDistFromStart)
        pointDistFromStart.remove(max(pointDistFromStart,key=lambda x:x[3]))

    sortedPoints=sorted(pointDistFromStart,key=lambda x: x[2])

    spNames=list(map(lambda x: x[1],sortedPoints))

    return optimize(spNames)



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



# def distanceMatrix(line,coordDict):
#     '''
#     :param line: list of coords
#     :param coordList: dict of fid: [coords]
#     :return: matrix of distance between line to coordList
#     '''
#
#     spFid=coordDict.keys()
#     spCoords=coordDict.values()
#
#     resultDict=defaultdict(list)
#     lineLength= len(line)
#     for sp,coords in coordDict.items():
#         count=0
#         tempLine=[coords]
#         for tempCoords in line:
#             count+=1
#             tempLine.append(tempCoords)
#             if count%24==0 or count>=lineLength:
#                 stringPoints = listCorrdsToString(tempLine)
#                 curb="curb"
#                 curb+=";curb"*(len(tempLine)-1)
#                 res = requests.get("https://api.mapbox.com/directions-matrix/v1/mapbox/driving/"
#                                  + stringPoints
#                                  + "?access_token="
#                                  + access_token
#                                  + "&annotations=distance"
#                                  + "&approaches="+curb
#                                  + "&destinations=0"
#                                  + "&sources=all"
#                                  )
#                 if not res.ok:
#                     time.sleep(120)
#                 res = requests.get("https://api.mapbox.com/directions-matrix/v1/mapbox/driving/"
#                                  + stringPoints
#                                  + "?access_token="
#                                  + access_token
#                                  + "&annotations=distance"
#                                  + "&approaches="+curb
#                                  + "&destinations=0"
#                                  + "&sources=all"
#                                  )
#                 # res.raise_for_status()
#                 res=res.json()
#                 print(res)
#
#                 sources=list(map(lambda x:x['location'],res['sources']))
#                 destinations=list(map(lambda x:x['location'],res['destinations']))
#                 distanceMatrix=list(map(lambda x:x[0],res['distances']))
#                 resultDict[sp]+=distanceMatrix[1:]
#                 #
#                 # print("*")
#                 # print(sources)
#                 # print(destinations)
#                 #
#                 # print(tempLine)
#                 # print('-')
#                 # pprint(distanceMatrix)
#
#                 tempLine=[]
#
#     return resultDict
#
#
#
#
#
#
# def getPathMapBoxKMNew(origin,destination):
#     '''
#     :param origin: coords of orignal point
#     :param destination: coords of destination point
#     :return: stations that are around the path between orgin and dest
#     the calc is based on stations that are closed (by km) to points in the paths
#     '''
#     service = Directions(access_token=access_token)
#     response = service.directions([origin, destination],'mapbox/driving',overview='full')
#     driving_routes = response.geojson()
#     line=driving_routes['features'][0]['geometry']['coordinates']
#     coordDict=sp.getDictFidCoords()
#     # print(line)
#     # print(coordDict)
#     dictMatrix=distanceMatrix(line,coordDict)
#     print(dictMatrix)







def createPaths(numDrivers,numSP,funGetPathMapBox=getPathMapBoxLine):
    print('CREATING PATHS')
    paths=[]

    for i in range(numDrivers):

        # if i%10==0:
        #     print(i)
        #     time.sleep(3)
        path={}
        path['driver']=i+1 #the name of the driver
        path['start']=addMin(initialDate,random.randint(0, minutesInDay)) #add to inital day some random minutes
        originSp,destinationSp=random.sample(range(1,numSP+1), 2)

        # origin = getStationDeatils(originSp)
        # destination = getStationDeatils(destinationSp)

        origin = sp.getStationCoords(originSp)
        destination = sp.getStationCoords(destinationSp)

        flag=1
        while flag:
            try:
                path['path']=funGetPathMapBox(origin, destination)
                flag=0
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue

        path['times']=getTimesOfPath( path['path'], path['start'])
        paths.append(path)

    #seprate to many dircatory and files
    # path=f'paths/numDrivers{numDrivers}'
    # # Check whether the specified path exists or not
    # isExist = os.path.exists(path)
    # if not isExist:
    #     # Create a new directory because it does not exist
    #     os.makedirs(path)
    # i=1
    # while os.path.exists(f'{path}/pathsFile{i}.json'):
    #     i+=1
    #
    # with open(f'{path}/pathsFile{i}.json', 'w', encoding='utf-8') as f:
    #     json.dump(paths, f, indent=4, default=convertDateToStr)
    # return paths

    #one big file
    with open(f'paths/uniformDistribution{numDrivers}.json', 'w', encoding='utf-8') as f:
        json.dump(paths, f, indent=4, default=convertDateToStr)
    return paths


def getTimesOfPath(path,startTime):
    '''
    :param path: list of names of sp
    :param path: datetime obj of the start time of the path
    :return: the time that the driver get to each sp
    '''
    times=[]
    times.append(startTime)
    for i in range(len(path)-1): #no need for the first one
        tempTime=times[i]
        duration, _ = calcDistTime(path[i], path[i+1],tempTime )
        new_time = addMin(tempTime,duration)
        times.append(new_time)
    # print(path)
    # print(times)
    return times

def optimize(wayFid):
    wayCoords = sp.listFidToCorrds(wayFid)
    stringPoints = listCorrdsToString(wayCoords)
    x = requests.get("https://api.mapbox.com/optimized-trips/v1/mapbox/driving/"
                     + stringPoints
                     + "?access_token="
                     + access_token
                     + "&roundtrip=false&source=first&destination=last"
                     )
    # print(x.status_code)

    # errors:
    while (x.status_code!=200):
        print(x.json())
        # time.sleep(2)
        x = requests.get("https://api.mapbox.com/optimized-trips/v1/mapbox/driving/"
                         + stringPoints
                         + "?access_token="
                         + access_token
                         + "&roundtrip=false&source=first&destination=last"
                         )

    waypoints = x.json()['waypoints']
    # print(x.json())
    fids = []
    for i, wayPoint in enumerate(waypoints):
        fids.append((wayFid[i], wayPoint['location'], wayPoint['waypoint_index']))

    path = list(map(lambda x: x[0], sorted(fids, key=lambda x: x[2])))

    return path


if __name__=='__main__':
    numberOfSP=sp.numOfSP
    numDrivers=10000



    createPaths(numDrivers=numDrivers, numSP=numberOfSP,funGetPathMapBox=getPathMapBoxLine)
