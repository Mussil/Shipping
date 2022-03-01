import datetime
import json

initialDate=datetime.datetime(2022, 1, 2, 0, 0)
minutesInDay=1440-1
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
            json_dict[key] = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except:
            pass
    return json_dict