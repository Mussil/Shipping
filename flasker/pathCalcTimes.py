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

def stationTimesCalc(station_name, station2):
    '''
    :param station_name: name of station
    :return: calc destination from station to all other stations
    '''

    stationsJson = {}

    for hour in range(0, 24):
        time0, dis0 = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, hour, 0))
        # time5, dis5 = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, hour, 5))
        # time10, dis10 = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, hour, 10))
        # time15, dis15 = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, hour, 15))
        # time20, dis20 = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, hour, 20))
        # time25, dis25 = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, hour, 25))
        time30, dis30 = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, hour, 30))
        # time35, dis35 = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, hour, 35))
        # time40, dis40 = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, hour, 40))
        # time45, dis45 = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, hour, 45))
        # time50, dis50 = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, hour, 50))
        # time55, dis55 = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, hour, 55))

        # stationHourJson = {f'{hour}:00': (time0, dis0),
        #                     f'{hour}:05': (time5, dis5),
        #                     f'{hour}:10': (time10, dis10),
        #                     f'{hour}:15': (time15, dis15),
        #                     f'{hour}:20': (time20, dis20),
        #                     f'{hour}:25': (time25, dis25),
        #                     f'{hour}:30': (time30, dis30),
        #                     f'{hour}:35': (time35, dis35),
        #                     f'{hour}:40': (time40, dis40),
        #                     f'{hour}:45': (time45, dis45),
        #                     f'{hour}:50': (time50, dis50),
        #                     f'{hour}:55': (time55, dis55)
        #                     }

        stationHourJson = {f'{hour}:00': (time0, dis0),f'{hour}:30': (time30, dis30)}
        stationsJson.update(stationHourJson)

    # print(stationsJson)
    return stationsJson

def stationTimes(station_name):
    '''
    :param station_name: name of station
    :return: calc destination from station to all other stations
    '''
    with open(f"stationsFilesTimes/{station_name}.json", "w") as file:
        my_json = {}
        json.dump(my_json, file)

        station_data = {}
        for station2 in range(1, 71): # end stations

            if station_name != station2:
                    station_data.update({f'{station_name}-{station2}': stationTimesCalc(station_name, station2)})
                    print(station_data[f'{station_name}-{station2}'])
        my_json.update(station_data)
        # print(my_json)
        file.seek(0)
        json.dump(my_json, file)

def stationsCalc():
    '''
    :return: initialization of all files and creating them
    '''
    for station1 in range(1, 71):  # start stations
        stationTimes(station1)

def calcTimeDist(org, dst, search_time):
    '''
    :param org: origin station
    :param dst: destination station
    :param search_time: time search
    :return: meters and min bewteen 2 stations
    '''
    with open(f"stationsFiles/{org}.json", "r") as file:
        data = json.load(file)
        return data[f'{org}-{dst}']


if __name__ == '__main__':

    # initialize stations from geojson file
    stations = initStations()
    stationsCalc()

    # call func for calc time & route between 2 stations
    # print(calcTimeDist(1, 2, "yuyu"))