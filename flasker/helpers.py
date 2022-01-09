import datetime


initialDate=datetime.datetime(2022, 1, 2, 0, 0)
minutesInDay=1440-1

def addMin(tm, min):
    """ get a dateTime object and minutes
    :return their sum"""
    tm = tm + datetime.timedelta(minutes=min)
    return tm