from flask import Flask
from flask import render_template
from flasker.SPutils import sp
import datetime
import json

app = Flask(__name__)

@app.route('/')
def showMapForAll():

    paths = [
                {
                    "driver": 1,
                    "start": datetime.datetime(2022, 1, 2, 3, 29, 0),
                    # "start":  3,

                    "path": [
                        21,
                        20,
                        8,
                        17,
                        18,
                        6,
                        41
                    ],
                    "times": [
                        datetime.datetime(2022, 1, 2, 3, 29, 0),
                        datetime.datetime(2022, 1, 2, 3, 29, 31),
                        datetime.datetime(2022, 1, 2, 3, 32, 29),
                        datetime.datetime(2022, 1, 2, 3, 32, 59),
                        datetime.datetime(2022, 1, 2, 3, 33, 38),
                        datetime.datetime(2022, 1, 2, 3, 35, 2),
                        datetime.datetime(2022, 1, 2, 3, 37, 50),
                        # "2022-01-02 03:29:00",
                        # "2022-01-02 03:29:31",
                        # "2022-01-02 03:32:29",
                        # "2022-01-02 03:32:59",
                        # "2022-01-02 03:33:38",
                        # "2022-01-02 03:35:02",
                        # "2022-01-02 03:37:50"
                    ]
                },
                {
                    "driver": 2,
                    "start": datetime.datetime(2022, 1, 2, 9, 38, 0),
                    # "start":  1,
                    "path": [
                        62,
                        14,
                        15,
                        13
                    ],
                    "times": [
                        datetime.datetime(2022, 1, 2, 9, 38, 0),
                        datetime.datetime(2022, 1, 2, 9, 45, 59),
                        datetime.datetime(2022, 1, 2, 9, 46, 2),
                        datetime.datetime(2022, 1, 2, 9, 54, 57),
                        # "2022-01-02 09:38:00",
                        # "2022-01-02 09:45:59",
                        # "2022-01-02 09:46:02",
                        # "2022-01-02 09:54:57"
                    ]
                },
                {
                    "driver": 3,
                    "start": datetime.datetime(2022, 1, 2, 23, 52, 0),
                    # "start":  4,
                    "path": [
                        6,
                        4,
                        14,
                        15,
                        69
                    ],
                    "times": [
                        datetime.datetime(2022, 1, 2, 23, 52, 0),
                        datetime.datetime(2022, 1, 2, 23, 54, 46),
                        datetime.datetime(2022, 1, 2, 23, 59, 33),
                        datetime.datetime(2022, 1, 2, 23, 59, 36),
                        datetime.datetime(2022, 1, 2, 0, 6, 23),
                        # "2022-01-02 23:52:00",
                        # "2022-01-02 23:54:46",
                        # "2022-01-02 23:59:33",
                        # "2022-01-02 23:59:36",
                        # "2022-01-03 00:06:23"
                    ]
                }
            ]

    return render_template('map.html', stations=sp.stations, paths=paths)


