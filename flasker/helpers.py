import datetime


initialDate=datetime.datetime(2022, 1, 2, 0, 0)
minutesInDay=1440-1
access_token = 'pk.eyJ1IjoibXVzc2lsIiwiYSI6ImNreGFhMHk0czF6aWgycG81NHBicmZuOGkifQ.Ki0DCgxNto32avvcUQWJxQ'


def addMin(tm, min):
    """ get a dateTime object and minutes
    :return their sum"""
    tm = tm + datetime.timedelta(minutes=min)
    return tm