import WazeRouteCalculator
import json
import time
import datetime

from flasker.helpers import initialDate

def list2stringCoordinates(lst):
    ''' :return: converted list to string  '''
    return str(lst[1])+","+str(lst[0])

def KM2meter(distance):
    ''' :return: converted KM distance to meters distance '''
    return distance * 1000.0

def initStations():
    '''
    :return: dict of all stations
    '''

    path = 'servicePointGlobal.geojson'

    with open(path, 'r') as stationsFile:
        stationsJson = json.load(stationsFile)

    stationsJson = stationsJson["features"]

    stationsDict = {}
    for station in stationsJson:
        stationsDict[station['properties']['fid']] = station

    return stationsDict

def getDistTime(org, dst, search_time):
    '''
        :param org: origin station name
        :param dst: destination station name
        :param time: search time
        :return:
            route-time between 2 points in seconds
            route-distance between 2 points in meters
    '''

    region = 'IL'  # Israel
    org_coords = list2stringCoordinates(stations[org]['geometry']['coordinates'])
    dst_coords = list2stringCoordinates(stations[dst]['geometry']['coordinates'])

    retry_cnt = 0
    while retry_cnt < 5:
        try:
            route = WazeRouteCalculator.WazeRouteCalculator(org_coords, dst_coords, region)

            real_time = datetime.datetime.now()
            _time = ((search_time-real_time).total_seconds())/ 60.0
            res = route.calc_route_info(time_delta = round(_time), real_time=False)

            route_time = res[0]
            route_distance = KM2meter(res[1])

            retry_cnt = 5 # if no error - get out of loop
        except WazeRouteCalculator.WRCError as err:
            retry_cnt += 1
            print(f"Waze Server Error (#{retry_cnt}), Retrying, Type-{err}")
        except Exception as err:
            time.sleep(5)  # Delays for 5 seconds
            retry_cnt += 1
            print(f"Waze Server Error (#{retry_cnt}), Retrying, Type-{err}")

    return route_time, route_distance

def stationTimes(station_name):
    '''
    :param station_name: name of station
    :return: calc destination from station to all other stations
    '''
    with open(f"stationsFiles/{station_name}.json", "w") as file:
        my_json = {}
        json.dump(my_json, file)

        stationsJson = {}
        for station2 in range(1, 71): # end stations

            if station_name != station2:
                stationsJson[f'{station_name}-{station2}'] = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, 12, 0))

        my_json.update(stationsJson)
        print(my_json)
        file.seek(0)
        json.dump(my_json, file)

def stationsCalc():
    '''
    :return: initialization of all files and creating them
    '''
    for station1 in range(1, 71):  # start stations
        stationTimes(station1)

def calcDistTime(org, dst, search_time):
    '''
    :param org: origin station
    :param dst: destination station
    :param search_time: time search
    :return: meters and min bewteen 2 stations
    '''
    with open(f"stationsFilesNoTimes/{org}.json", "r") as file:
        data = json.load(file)
        return data[f'{org}-{dst}']


if __name__ == '__main__':

    # initialize stations from geojson file
    stations = initStations()
    # stationsCalc()

    # call func for calc time & route between 2 stations
    # print(calcTimeDist(1, 2, "yuyu"))