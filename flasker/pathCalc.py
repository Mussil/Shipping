import json
import WazeRouteCalculator
import logging
import datetime

def list2stringCoordinates(lst):
    ''' :return: converted list to string  '''
    return str(lst[1])+","+str(lst[0])

def KM2meter(distance):
    ''' :return: converted KM distance to meters distance '''
    return distance * 1000.0

def initStations():
    '''
    :return:
        1. dict of all stations
        2. service obj for directions calc
    '''

    path = 'servicePointGlobal.geojson'

    with open(path, 'r') as stationsFile:
        stationsJson = json.load(stationsFile)

    stationsJson = stationsJson["features"]
    # print(stationsJson)

    stationsDict = {}
    for station in stationsJson:
        stationsDict[station['properties']['fid']] = station
    # print(stationsDict)

    return stationsDict

def calcDistTime(org, dst, search_time):
    '''
        :param org: origin station name
        :param dst: destination station name
        :param time: search time
        :return:
            route-time between 2 points in seconds
            route-distance between 2 points in meters
    '''

    # logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
    # logger.setLevel(logging.DEBUG)
    # handler = logging.StreamHandler()
    # logger.addHandler(handler)

    region = 'IL'  # Israel
    org_coords = list2stringCoordinates(stations[org]['geometry']['coordinates'])
    dst_coords = list2stringCoordinates(stations[dst]['geometry']['coordinates'])
    route = WazeRouteCalculator.WazeRouteCalculator(org_coords, dst_coords, region)

    real_time = datetime.datetime.now()
    time = ((search_time-real_time).total_seconds())/ 60.0
    res = route.calc_route_info(time_delta = round(time), real_time=False)

    route_time = res[0]
    route_distance = KM2meter(res[1])

    return round(route_time), round(route_distance)

stations = initStations()

# time, dis = calcDistTime(1, 70, datetime.datetime(2021, 12, 28, 12, 0))
# print(time, dis)
