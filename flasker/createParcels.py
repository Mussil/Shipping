import json
import os
import pickle

from flasker.SPutils import sp
from flasker.helpers import addMin, initialDate, minutesInDay, convertDateToStr
import random

def createRandomParcels(numParcels, maxSp):
    print("CREATING RANDOM PARCELS")
    paths = []

    for i in range(numParcels):
        path = {}
        path['idParcel']=i+1
        path['startTime'] = addMin(initialDate, random.randint(0, minutesInDay))  # add to inital day some random minutes
        path['source'] ,path['target']= random.sample(range(1, maxSp + 1), 2)
        paths.append(path)

    # i=1
    # while os.path.exists(f'parcels/parcelsRandomFile{i}.json'):
    #     i+=1
    #
    # with open(f'parcels/parcelsRandomFile{i}.json', 'w', encoding='utf-8') as f:
    #     json.dump(paths, f, indent=4, default=convertDateToStr)
    #
    # return paths

    #seprate to many dircatory and files
    # path=f'parcels/numParcels{numParcels}'
    # # Check whether the specified path exists or not
    # isExist = os.path.exists(path)
    # if not isExist:
    #     # Create a new directory because it does not exist
    #     os.makedirs(path)
    # i=1
    # while os.path.exists(f'parcels/numParcels{numParcels}/parcelsFile{i}.json'):
    #     i+=1
    # with open(f'parcels/numParcels{numParcels}/parcelsFile{i}.json', 'w', encoding='utf-8') as f:
    #     json.dump(paths, f, indent=4, default=convertDateToStr)
    #
    # return paths


    #one big file
    with open(f'parcels/uniformDistribution{numParcels}.json', 'w', encoding='utf-8') as f:
        json.dump(paths, f, indent=4, default=convertDateToStr)
    return paths

if __name__=='__main__':
    numParcels=100000
    maxSp = sp.numOfSP
    createRandomParcels(numParcels, maxSp)