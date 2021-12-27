import json
import WazeRouteCalculator
import logging
import datetime

from pathCalcHelpers import list2string, KM2meter

def initStations():
    '''
    :return:
        1. dict of all stations
        2. service obj for directions calc
    '''

    path = 'try.geojson'

    with open(path, 'r') as stationsFile:
        stationsJson = json.load(stationsFile)

    stationsJson = stationsJson["features"]

    stationsDict = {}
    for station in stationsJson:
        stationsDict[station['properties']['fid']] = station

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

    logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    region = 'IL'  # Israel
    org_coords = list2string(stations[org]['geometry']['coordinates'])
    dst_coords = list2string(stations[dst]['geometry']['coordinates'])
    route = WazeRouteCalculator.WazeRouteCalculator(org_coords, dst_coords, region)

    real_time = datetime.datetime.now()
    time = ((search_time-real_time).total_seconds())/ 60.0
    res = route.calc_route_info(time_delta = round(time))

    route_time = res[0]
    route_distance = KM2meter(res[1])

    return round(route_time), round(route_distance)

stations = initStations()
time, dis = calcDistTime(1, 3, datetime.datetime(2022, 1, 1, 18, 10))
