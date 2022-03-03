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
                    "driver": 1,
                    "start": datetime.datetime(2022, 1, 2, 3, 29, 0),

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
                        int(time.mktime(datetime.datetime(2022, 3, 3, 21, 10, 0).timetuple())) * 1000,
                        int(time.mktime(datetime.datetime(2022, 3, 3, 21, 10, 31).timetuple())) * 1000,
                        int(time.mktime(datetime.datetime(2022, 3, 3, 21, 11, 29).timetuple())) * 1000,
                        int(time.mktime(datetime.datetime(2022, 3, 3, 21, 12, 59).timetuple())) * 1000,
                        int(time.mktime(datetime.datetime(2022, 3, 3, 21, 13, 38).timetuple())) * 1000,
                        int(time.mktime(datetime.datetime(2022, 3, 3, 21, 13, 45).timetuple())) * 1000,
                        int(time.mktime(datetime.datetime(2022, 3, 3, 23, 59, 5).timetuple())) * 1000
                    ]
                },
                {
                    "driver": 2,
                    "start": datetime.datetime(2022, 1, 2, 21, 38, 0),
                    "path": [
                        62,
                        14,
                        15,
                        13
                    ],
                    "times": [
                        int(time.mktime( datetime.datetime(2022, 3, 3, 21, 10, 3).timetuple())) * 1000,
                        int(time.mktime( datetime.datetime(2022, 3, 3, 21, 10, 25).timetuple())) * 1000,
                        int(time.mktime( datetime.datetime(2022, 3, 3, 21, 11, 28).timetuple())) * 1000,
                        int(time.mktime( datetime.datetime(2022, 3, 3, 23, 59, 57).timetuple())) * 1000                   ]
                },
                {
                    "driver": 3,
                    "start": datetime.datetime(2022, 3, 1, 23, 52, 0),
                    "path": [
                        6,
                        4,
                        14,
                        15,
                        69
                    ],
                    "times": [
                        int(time.mktime(datetime.datetime(2022, 3, 3, 21, 12, 0).timetuple())) * 1000,
                        int(time.mktime(datetime.datetime(2022, 3, 3, 21, 12, 46).timetuple())) * 1000,
                        int(time.mktime(datetime.datetime(2022, 3, 3, 21, 13, 33).timetuple())) * 1000,
                        int(time.mktime(datetime.datetime(2022, 3, 3, 21, 13, 36).timetuple())) * 1000,
                        int(time.mktime(datetime.datetime(2022, 3, 3, 21, 59, 0).timetuple())) * 1000
                    ]
                }
            ]

    return render_template('map.html', stations=sp.stations, paths=paths)


