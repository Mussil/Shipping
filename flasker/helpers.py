import datetime
import json
import time

initialDate=datetime.datetime(2022, 1, 2, 0, 0)
minutesInDay=1440
# access_token = 'pk.eyJ1IjoibXVzc2lsIiwiYSI6ImNreGFhMHk0czF6aWgycG81NHBicmZuOGkifQ.Ki0DCgxNto32avvcUQWJxQ' #Mussi
access_token='pk.eyJ1IjoicmxldmkxMjkzIiwiYSI6ImNrenh0bnh0MjA0eG0ydm8zajJ6ZW9odXcifQ.loa-SroNLMPU0Px4LkBOzA' #Rachel



def addMin(tm, min):
    """ get a dateTime object and minutes
    :return their sum"""
    tm = tm + datetime.timedelta(minutes=min)
    return tm

def listCorrdsToString(listCoords):
    stringPoints=";".join(list(map(lambda coords: ",".join([str(x) for x in coords]),listCoords)))
    return stringPoints

# class DatetimeEncoder(json.JSONEncoder):
#     def default(self, obj):
#         try:
#             return super().default(obj)
#         except TypeError:
#             return str(obj)

def convertDateToStr(o):
    if isinstance(o, datetime.datetime):
        return datetime.datetime.strftime(o, '%Y-%m-%d %H:%M:%S')

def convertStrToDate(json_dict):
    for (key, value) in json_dict.items():
        try:
            if type(value) == list:
                json_dict[key]=list(map(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), json_dict[key]))
            else:
                json_dict[key] = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except:
            pass
    return json_dict


def convertStrToDateJSForamt(json_dict):

    def str2date(x):
        return int(time.mktime(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').timetuple())) * 1000

    for (key, value) in json_dict.items():
        try:
            if type(value) == list:
                json_dict[key]=list(map(lambda x:str2date(x), json_dict[key]))
            else:
                json_dict[key] = str2date(value)
        except:
            pass
    return json_dict

def getDemoFiles():
    with open(f'0.json') as json_file:
        drivers = json.load(json_file,object_hook=convertStrToDateJSForamt)
    with open(f'0results.json') as json_file:
        results = json.load(json_file,object_hook=convertStrToDateJSForamt)
    with open(f'demoParcelsFile.json') as json_file:
        parcels = json.load(json_file, object_hook=convertStrToDateJSForamt)
    return drivers,results,parcels

def getFiles(numDrivers,numParcels,userChoice):
    if userChoice=='random':
        letter='0'
    else:
        letter='0'+userChoice
    path=f'resultsFile'
    with open(f'{path}/driversDB/{numDrivers}.json') as json_file:
        drivers = json.load(json_file,object_hook=convertStrToDateJSForamt)
    with open(f'{path}/results/{numParcels}parcels{numDrivers}drivers{letter}.json') as json_file:
        results = json.load(json_file,object_hook=convertStrToDateJSForamt)
    with open(f'{path}/parcelsDB/{numParcels}.json') as json_file:
        parcels = json.load(json_file, object_hook=convertStrToDateJSForamt)
    return drivers,results,parcels

def convertSpeedToRatio(speed):
    if speed == '1': 
        return 6
    elif speed == '1.5': 
        return 3
    elif speed == '2':
        return 1
    elif speed == '2.5':
        return 0.5
    return 0.25