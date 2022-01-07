import json
import pickle

from flasker.helpers import addMin,initialDate,minutesInDay
import random

def createRandomParcels(numParcels, maxSp):
    paths = []

    for i in range(numParcels):
        path = {}
        path['startTime'] = addMin(initialDate, random.randint(0, minutesInDay))  # add to inital day some random minutes
        path['source'] ,path['target']= random.sample(range(1, maxSp + 1), 2)
        paths.append(path)

    # TODO: save paths to file (in directory)

    with open('parcelsRandomFile.json', 'w', encoding='utf-8') as f:
        json.dump(paths, f, indent=4, default=str)

    return paths