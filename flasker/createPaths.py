import random
from flasker.helpers import addMin,initialDate,minutesInDay


def createRandomPaths(numDrivers,maxSp):
    paths=[]
    #TODO: FIX ValueError: Sample larger than population or is negative

    for i in range(numDrivers):
        path={}
        path['driver']=i+1 #the name of the driver
        path['start']=addMin(initialDate,random.randint(0, minutesInDay)) #add to inital day some random minutes
        numOfSp=random.randint(2, maxSp)
        print(numOfSp)
        print(maxSp)

        path['path']=random.sample(range(1,maxSp+1), numOfSp)
        paths.append(path)


    # TODO: save paths to file (in dictory)
    return paths

