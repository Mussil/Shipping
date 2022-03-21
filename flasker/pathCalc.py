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
                time0, dist0 = getDistTime(station_name, station2,datetime.datetime(initialDate.year, initialDate.month, initialDate.day, 1,30))  # 23:00 - 3:00
                time1, dist1 = getDistTime(station_name, station2, datetime.datetime(initialDate.year, initialDate.month, initialDate.day, 4,30))  # 3:00 - 6:00
                time2, dist2 = getDistTime(station_name, station2,datetime.datetime(initialDate.year, initialDate.month, initialDate.day, 7,0))  # 6:00 - 8:00
                time3, dist3 = getDistTime(station_name, station2,datetime.datetime(initialDate.year, initialDate.month, initialDate.day, 9,0))  # 8:00 - 10:00
                time4, dist4 = getDistTime(station_name, station2,datetime.datetime(initialDate.year, initialDate.month, initialDate.day, 12, 0))  # 10:00 - 14:00
                time5, dist5 = getDistTime(station_name, station2,datetime.datetime(initialDate.year, initialDate.month, initialDate.day, 15,30))  # 14:00 - 17:00
                time6, dist6 = getDistTime(station_name, station2,datetime.datetime(initialDate.year, initialDate.month, initialDate.day, 18,30))  # 17:00 - 20:00
                time7, dist7 = getDistTime(station_name, station2,datetime.datetime(initialDate.year, initialDate.month, initialDate.day, 21, 0))  # 20:00 - 23:00

                stationsJson[f'{station_name}-{station2}'] = {
                                                            "1:30": (time0, dist0),
                                                            "4:30": (time1, dist1),
                                                            "7:00": (time2, dist2),
                                                            "9:00": (time3, dist3),
                                                            "12:00": (time4, dist4),
                                                            "15:30": (time5, dist5),
                                                            "18:30": (time6, dist6),
                                                            "21:00": (time7, dist7)
                                                        }
                file.seek(0)
                json.dump(stationsJson, file)

def stationsCalc():
    '''
    :return: initialization of all files and creating them
    '''
    for station1 in range(40, 71):  # start stations
        stationTimes(station1)

def calcDistTime(org, dst, search_time):
    '''
    :param org: origin station
    :param dst: destination station
    :param search_time: time search
    :return: meters and min bewteen 2 stations
    '''
    with open(f"stationsFiles/{org}.json", "r") as file:
        data = json.load(file)

        time = search_time.strftime("%H:%M")
        hour, min = time.split(":")

        if hour[0] is '0':
            hour = hour[1]
        if min[0] is '0':
            min = min[1]

        search_time = f'{hour}:{min}'

        if search_time in data[f'{org}-{dst}']:
            return data[f'{org}-{dst}'][search_time]

        else:
            hour = int(hour)
            min = int(min)

            if hour >= 1 and hour < 4: # middle 3:00
                if hour <= 2 or (hour == 3 and min == 0):
                    return data[f'{org}-{dst}']['1:30']
                return data[f'{org}-{dst}']['4:30']

            elif hour >= 4 and hour < 6: # middle 5:15
                if hour <= 4 or (hour == 5 and min <= 15):
                    return data[f'{org}-{dst}']['4:30']
                return data[f'{org}-{dst}']['6:00']

            elif hour >= 6 and hour < 7:
                if hour == 6 and min <= 30:
                    return data[f'{org}-{dst}']['6:00']
                return data[f'{org}-{dst}']['7:00']

            elif hour >= 7 and hour < 8:
                if hour == 7 and min <= 30:
                    return data[f'{org}-{dst}']['7:00']
                return data[f'{org}-{dst}']['8:00']

            elif hour >= 8 and hour < 9:
                if hour == 8 and min <= 30:
                    return data[f'{org}-{dst}']['8:00']
                return data[f'{org}-{dst}']['9:00']

            elif hour >= 9 and hour < 10:
                if hour == 9 and min <= 30:
                    return data[f'{org}-{dst}']['9:00']
                return data[f'{org}-{dst}']['10:00']

            elif hour >= 10 and hour < 11:
                if hour == 10 and min <= 30:
                    return data[f'{org}-{dst}']['10:00']
                return data[f'{org}-{dst}']['11:00']

            elif hour >= 11 and hour < 12:
                if hour == 11 and min <= 30:
                    return data[f'{org}-{dst}']['11:00']
                return data[f'{org}-{dst}']['12:00']

            elif hour >= 12 and hour < 13:
                if hour == 12 and min <= 30:
                    return data[f'{org}-{dst}']['12:00']
                return data[f'{org}-{dst}']['13:30']

            elif hour >= 13 and hour < 15:
                if hour <= 14 or (hour == 14 and min <= 30):
                    return data[f'{org}-{dst}']['13:30']
                return data[f'{org}-{dst}']['15:30']

            elif hour >= 15 and hour < 16:
                if hour == 15 and min >= 30:
                    return data[f'{org}-{dst}']['15:30']
                return data[f'{org}-{dst}']['16:30']

            elif hour >= 16 and hour < 18:
                if hour <= 17 or (hour == 17 and min <= 30):
                    return data[f'{org}-{dst}']['16:30']
                return data[f'{org}-{dst}']['18:30']

            elif hour >= 18 and hour < 21:
                if hour < 19 or (hour == 19 and min <= 55):
                    return data[f'{org}-{dst}']['18:30']
                return data[f'{org}-{dst}']['21:00']

            elif hour >= 21 and hour < 23:
                if hour < 22 :
                    return data[f'{org}-{dst}']['21:00']
                return data[f'{org}-{dst}']['23:00']

            elif hour == 0 and min <= 25:
                return data[f'{org}-{dst}']['23:00']

            return data[f'{org}-{dst}']['1:30']


def addWazeCalls(hours_lst):
    for station1 in range(1, 71):
        for station2 in range(1, 71):
            if(station1 != station2):
                with open(f"stationsFiles/{station1}.json", "r+") as f:
                    data = json.load(f)
                    new_data = {}
                    for hour in hours_lst:
                        time = hour.split(":")
                        new_data.update({f'{hour}':getDistTime(station1, station2,datetime.datetime(initialDate.year, initialDate.month, initialDate.day, int(time[0]),int(time[1])))})
                    data[f'{station1}-{station2}'].update(new_data) # <--- add hour value.
                    f.seek(0)  # <--- should reset file position to the beginning.
                    json.dump(data, f)
            print("Done with", station1, station2)

if __name__ == '__main__':
    pass

    # Run these lines if you want to recalculate hours or add hours to files (!)
    # initialize stations from geojson file
    # stations = initStations()

    # creating all files with hours waze calls
    # stationsCalc()

    # add hours to json files
    # addWazeCalls(['6:00', '10:00', '11:00'])

    # call func for calc time & route between 2 stations

    # print(calcDistTime(46, 1, datetime.datetime(2018, 3, 13, 3, 36)))



