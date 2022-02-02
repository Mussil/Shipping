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

                "departureTime": "2022-01-27T08:00:00+11"
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

lineCoords=[[34.65267978180447, 31.79653581609056], [34.6529108074645, 31.796622836740987], [34.658266577330146, 31.8095198785306], [34.65998456814748, 31.80985125376073], [34.65680726524424, 31.811224410665826], [34.65991666060499, 31.810352776309365], [34.654529037201335, 31.812626772099204], [34.65551509672302, 31.81477667621152]]
lineCoords=[[34.66692960203274, 31.81196798166902], [34.66580413952755, 31.811076052698642], [34.6529108074645, 31.796622836740987], [34.65267978180447, 31.79653581609056], [34.63339201093926, 31.76932374718557], [34.61974873665147, 31.772700974698733]]
stringPoints=";".join(list(map(lambda coords: ",".join([str(x) for x in coords]),lineCoords)))
x = requests.get("https://api.mapbox.com/optimized-trips/v1/mapbox/driving/"+
        stringPoints+"?access_token=pk.eyJ1IjoibXVzc2lsIiwiYSI6ImNreGFhMHk0czF6aWgycG81NHBicmZuOGkifQ.Ki0DCgxNto32avvcUQWJxQ")
waypoints=x.json()['waypoints']
locs=list(map(lambda x: x['location'],sorte


