import json
import os
import pickle
from pprint import pprint

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flasker.SPutils import sp
from flasker.helpers import addMin, initialDate, minutesInDay, convertDateToStr
import random
random.seed()


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


def createNonUniformTimeParcels(numParcels, maxSp):
    print("CREATING RANDOM NON UNIFORM PARCELS")
    paths = []
    listMin=getMinNormalDistrubation(amount=numParcels, size=minutesInDay)


    for i in range(numParcels):
        path = {}
        path['idParcel']=i+1
        min=listMin[i].item()
        path['startTime'] = addMin(initialDate,min )  # add to inital day some random minutes
        path['source'] ,path['target']= random.sample(range(1, maxSp + 1), 2)
        paths.append(path)

    #one big file
    with open(f'parcels/NonUniformTimeDistribution{numParcels}.json', 'w', encoding='utf-8') as f:
        json.dump(paths, f, indent=4, default=convertDateToStr)
    return paths

def getMinNormalDistrubation(amount,size):

    def normal_dist(x, mean, sd):
        prob_density = (np.pi * sd) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
        return prob_density

    x=np.arange(1,size+1)
    sd = np.std(x) #415
    mean=np.mean(x) #720
    mean = 360 # 6 AM
    sd=200
    xxRange=range(0,minutesInDay,60)
    plt.xticks(xxRange,list(map(lambda x:f'{int(x/60)}:00',xxRange)),size=7)
    plt.xlabel('Hours')
    plt.ylabel('Probability')

    pdf = normal_dist(x, mean, sd)
    sumOfPdf=sum(pdf)
    distrubtion=[]
    for i in pdf:
        distrubtion.append(i/sumOfPdf)
    plt.plot(x, distrubtion)
    plt.show()
    plt.xlabel('Hours')
    plt.ylabel('Amount of parcels')
    plt.xticks(xxRange,list(map(lambda x:f'{int(x/60)}:00',xxRange)),size=7)

    times = np.random.choice(minutesInDay, p=distrubtion, size=(amount))

    plt.hist(times, size)
    plt.show()

    return times


if __name__=='__main__':
    numParcels=100000
    maxSp = sp.numOfSP
    # createRandomParcels(numParcels, maxSp)

    createNonUniformTimeParcels(numParcels,maxSp)



