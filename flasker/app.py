from flask import Flask, request, render_template, redirect
from flasker.SPutils import sp
import datetime
import time
import json
import sys

app = Flask(__name__)


@app.route('/')
def showMapForAll():

    paths = [
        {
            'driver': 41,
            'path': [61, 14, 15, 7, 17, 18],
            'start': datetime.datetime(2022, 1, 2, 12, 31),
            'times': [
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 12, 31).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 12, 37, 27).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 12, 37, 30).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 12, 44, 4).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 12, 45, 5).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 12, 45, 45).timetuple())) * 1000
            ],
        },
        {
            'driver': 30,
            'path': [7, 8, 6, 4, 28],
            'start': datetime.datetime(2022, 1, 2, 14, 17),
            'times': [
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 14, 17).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 14, 17, 5).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 14, 18, 12).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 14, 21, 27).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 14, 27, 5).timetuple())) * 1000
            ]
        },
        {
            'driver': 22,
            'path': [14, 15, 17, 19, 7, 18, 27],
            'start': datetime.datetime(2022, 1, 2, 3, 41),
            'times': [
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 3, 41).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 3, 41, 3).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 3, 46, 6).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 3, 46, 52).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 3, 50, 57).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 3, 52, 37).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 3, 54, 32).timetuple())) * 1000
            ]

        },
        {
            'driver': 23,
            'path': [38, 37, 36, 54, 11],
            'start': datetime.datetime(2022, 1, 2, 9, 26),
            'times': [
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 9, 26).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 9, 27, 1).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 9, 27, 45).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 9, 31, 40).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 9, 32, 38).timetuple())) * 1000
            ]

        }
    ]

    results = {
        "15": {
            'path': [
                (61, None),
                (61, 41),
                (14, 41),
                (15, 41),
                (7, 41),
                (7, 30),
                (8, 30),
                (8, None)
            ],
            'payActual': 10.348666666666666,
            'payMax': 12.422,
            'startTime': int(time.mktime(datetime.datetime(2022, 1, 2, 11, 5).timetuple())) * 1000,
            'totalDistance': 6422.0,
            'totalDrivers': 2,
            'totalDuration': 192.08333333333334
        },
        "91": {
            'path': [
                (38, None),
                (38, 23),
                (37, 23),
                (36, 23),
                (36, None)
            ],
            'payActual': 3.4065,
            'payMax': 3.813,
            'startTime': int(time.mktime(datetime.datetime(2022, 1, 2, 9, 20).timetuple())) * 1000,
            'totalDistance': 813.0,
            'totalDrivers': 1,
            'totalDuration': 530.75,
        }
    }

    return render_template('map.html', stations=sp.stations, paths=paths, results=results)


@app.route('/try')
def start():
    return render_template('userInputs.html')


@app.route('/UserInputs/<int:drivers>/<int:parcels>', methods=['POST'])
def ProcessUserinfo(drivers: int, parcels: int):
    print()
    print(drivers, parcels)
    print()
    
    return('/')
    