LS_API_KEY = "SFCT9i7qKVVOKzVComo6TZLudYgIqVFdGEVzG7rGgeA"

import datetime
import json
import requests
import time
from here_location_services import routing_api
from pprint import pprint

if __name__ == '__main__':

    # payload = {
    #     "apiKey": LS_API_KEY,
    #     "start0": "-33.795602,151.185366",
    #     "start1": "-33.865103,151.205627",
    #     "destination0": "-33.795602,151.185366",
    #     "destination1": "-33.865103,151.205627",
    #     "mode": "fastest;car;traffic:enabled",
    #     "departure": "2020-10-27T08:00:00+11",
    #     "summaryattributes": "all"
    # }
    # base_url = "https://matrix.route.ls.hereapi.com/routing/7.2/calculatematrix.json?"
    # r = requests.get(base_url, params=payload)
    # pprint(r.json())

    # 1. Request matrix (POST)
    # base_url = "https://matrix.router.hereapi.com/v8/matrix?"
    base_url = "https://matrix.router.hereapi.com/v8/matrix?apiKey=SFCT9i7qKVVOKzVComo6TZLudYgIqVFdGEVzG7rGgeA&async=false"

    # params = {"apiKey": LS_API_KEY,
    #           "async": "true",
    #           "departureTime": "2020-10-27T08:00:00+11"}
    # payload = {"origins": [{"lat": -33.759688, "lng": 151.156369}, {"lat": -33.865189, "lng": 151.208162},
    #                        {"lat": -33.677066, "lng": 151.302117}],
    #            "regionDefinition": {"type": "autoCircle", "margin": 10000},
    #            "matrixAttributes": ["travelTimes", "distances"]}
    # headers = {'Content-Type': 'application/json'}

    payload = {
                "origins": [
                    {
                        "lat": 47.673993,
                        "lng": -122.356108
                    },
                    {
                        "lat": 47.656910,
                        "lng": -122.362823
                    },
                    {
                        "lat": 47.648015,
                        "lng": -122.335674
                    },
                    {
                        "lat": 47.653022,
                        "lng": -122.312461
                    },
                    {
                        "lat": 47.675796,
                        "lng": -122.311520
                    }
                ],
                "destinations": [
                    {
                        "lat": 47.661438,
                        "lng": -122.336427
                    }
                ],
                "regionDefinition": {
                    "type": "world"
                },
                "departureTime": "2018-12-19T18:23:45+0100"
             }

    x = requests.post(base_url, json=payload)
    # print(x)
    pprint(x.json())


    # # pretty print
    # print(json.dumps(response, indent=4))
    #
    # # 2. Poll for status (GET)
    # time.sleep(3)
    # statusUrl = response['statusUrl']
    # params = {'apiKey': 'MY_API_KEY_HERE'}
    # headers = {'Content-Type': 'application/json'}
    # r = requests.get(statusUrl, params=params, headers=headers)
    # response = r.json()
    #
    # # pretty print
    # print(json.dumps(response, indent=4))

