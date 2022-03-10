from flask import Flask
from flask import render_template
from flasker.SPutils import sp
import datetime
import time
import json

app = Flask(__name__)


@app.route('/')
def showMapForAll():

    paths = [
        {
            "driver": 11,
            "path": [
                11,
                14,
                15,
                24,
                22],
            "start": datetime.datetime(2022, 1, 2, 11, 28),
            "times": [
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 11, 28, 0).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 11, 33, 48).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 11, 33, 51).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 11, 41, 17).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 11, 43, 5).timetuple())) * 1000
            ]
        },
        {
            "driver": 23,
            "path": [
                38,
                37,
                36,
                54,
                11
            ],
            "start": datetime.datetime(2022, 1, 2, 9, 26),
            "times": [
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 9, 26, 0).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 9, 27, 1).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 9, 27, 45).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 9, 31, 40).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 9, 32, 38).timetuple())) * 1000
            ]
        },
        {
            "driver": 30,
            "path": [
                7,
                8,
                6,
                4,
                28
            ],
            "start": datetime.datetime(2022, 1, 2, 14, 17),
            "times": [
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 14, 17, 0).timetuple())) * 1000,
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
            "driver": 41,
            "path": [
                61,
                14,
                15,
                7,
                17,
                18
            ],
            "start": datetime.datetime(2022, 1, 2, 12, 31),
            "times": [
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 12, 31, 0).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 12, 37, 27).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 12, 37, 30).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 12, 44, 4).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 12, 45, 5).timetuple())) * 1000,
                int(time.mktime(datetime.datetime(
                    2022, 1, 2, 12, 45, 45).timetuple())) * 1000,
            ]
        }
    ]

    results = {
        "2": {
            "path": [
                [54, None],
                [54, 23],
                [11, 23],
                [11, 11],
                [14, 11],
                [14, 41],
                [15, 41],
                [7, 41],
                [7, 30],
                [8, 30],
                [6, 30],
                [4, 30],
                [28, 30],
                [28, None]
            ],
            "startTime": int(time.mktime(datetime.datetime(2022, 1, 2, 9, 20, 0).timetuple())) * 1000
        }
    }

    return render_template('map.html', stations=sp.stations, paths=paths, results=results)
