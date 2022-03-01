import json
import statistics

import matplotlib.pyplot as plt

prettyNames = {'weightPriortyTimeDriverDistance': 'Time, Drivers, Distance',
               'weightPriortyTimeDistanceDriver': 'Time, Distance, Drivers',
               'weightPriortyDistanceDriverTime': 'Distance, Drivers, Time',
               'weightPriortyDistanceTimeDriver': 'Distance, Time, Drivers',
               'weightPriortyDriverDistanceTime': 'Drivers, Distance, Time',
               'weightPriortyDriverTimeDistance': 'Drivers, Time, Distance',
               'random': 'Random'}

def averageDrivers():
    x = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    y = [0.232, 0.41200000000000003, 0.586, 0.702, 0.746, 0.8, 0.802, 0.858, 0.852, 0.86] # avg

    plt.plot(x, y)
    plt.xlabel('number of drivers')
    plt.xticks(x, x)
    plt.ylabel('average of success')
    plt.title('50 parcels')
    plt.show()

def medianDrivers():
    x = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    y = [0.24, 0.4, 0.6, 0.69, 0.76, 0.82, 0.8, 0.86, 0.86, 0.86] #median

    plt.plot(x, y)
    plt.xlabel('number of drivers')
    plt.xticks(x, x)
    plt.ylabel('median of success')
    plt.title('50 parcels')
    plt.show()

def profits():
    x = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    y = [0.9579294217734499, 1.0, 0.9767728893671903, 1.0, 1.0, 0.9888679507545363, 1.0, 1.0, 1.0, 1.0] #median

    plt.plot(x, y)
    plt.xlabel('number of drivers')
    plt.xticks(x, x)
    plt.ylabel('median of median of profit')
    plt.title('50 parcels')
    plt.show()


def medianFunc1(yPayMax=[],yPayActual=[]):
    x = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
    # try1 (200)
    yPayMax = [13.65, 13.2405, 14.707, 12.784500000000001, 14.506499999999999, 13.656, 13.651, 14.066, 13.517, 14.7515, 13.167, 13.6395, 13.206, 13.621, 14.152000000000001, 13.808, 13.4835, 13.6365, 13.8045, 13.361]
    yPayActual=[12.933, 10.21822619047619, 10.851142857142857, 9.452116071428572, 9.64995009920635, 9.141, 7.487303571428571, 8.4724, 6.9744807692307695, 9.162769553982699, 6.59841947128958, 6.71175177045177, 6.473568333333334, 6.426501588762115, 6.605137841111287, 6.337722689075631, 6.335753613155889, 6.274623187132882, 6.2685931179419665, 6.205945102072932]
    # try2 (200)
    yPayMax=[12.661000000000001, 14.232, 15.0115, 13.36, 14.439, 13.272, 12.774999999999999, 13.814, 12.362, 13.546, 13.3305, 13.634, 13.6295, 14.245000000000001, 14.506, 13.783000000000001, 12.954, 13.342, 13.471, 13.5205]
    yPayActual=[12.55, 11.651291666666667, 10.93812738095238, 9.862742857142857, 9.607001236963214, 9.324371573116427, 7.051800438596491, 8.5655, 6.6645, 9.048605476190476, 6.775172222222222, 6.766671153846154, 6.75498373015873, 6.6781869188337275, 9.046533288081905, 8.082425, 6.217878249474193, 6.436210916966369, 6.329806864545084, 6.22001885402609]
    # try 3 (100)
    # yPayMax=[13.251000000000001, 12.155000000000001, 12.7025, 11.996500000000001, 13.2135, 11.256, 13.349, 11.0465, 12.706, 12.8705, 11.731, 12.111, 13.256, 13.349, 13.560500000000001, 12.318999999999999, 11.729, 12.259, 10.457, 13.189499999999999]
    # yPayActual=[13.251000000000001, 11.1265, 10.436583333333335, 8.029958333333333, 8.832291666666666, 7.281179348940533, 7.913569444444445, 6.628425, 9.109661811325886, 6.594374603174604, 6.417588611388611, 6.409837324929972, 6.527173843520934, 6.342040190135128, 6.695019140383426, 6.255080952380952, 6.326419279710516, 6.195322333811573, 6.10833254917597, 6.2599528111515905]


    plt.plot(x, yPayMax,label='median pay-max')
    plt.plot(x, yPayActual,label='median pay-actual')
    plt.legend()
    plt.xlabel('number of parcels')
    plt.xticks(x, x)
    plt.ylabel('median of of pay')
    plt.title('100 drivers')
    plt.show()

def avgFunc1(yPayMax=[],yPayActual=[]):
    x = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
    #try1 (200)
    yPayMax = [14.66395652173913, 14.023954545454545, 14.388942528735633, 14.103355555555556, 14.929091836734694, 14.487706766917293, 13.998, 14.705502645502646, 14.323278538812785, 14.76527927927928, 13.942593023255814, 13.993658620689656, 14.145422740524781, 14.213897832817338, 14.273111436950147, 14.051255813953489, 14.59394191919192, 14.596308962264152, 14.573837155963304, 14.15958568329718]
    yPayActual=[13.92017391304348, 11.065315476190476, 10.565207922824301, 9.36413713081428, 9.712397831081317, 8.914005958048664, 8.415013802451027, 8.756640182033218, 8.126444253774267, 8.143337817799768, 7.9065035931268675, 7.911746169882018, 7.7343440775085694, 7.865237920955458, 7.932783485583733, 7.549516469031061, 7.742196148305583, 7.793864132307001, 7.784900462262626, 7.562053755384643]
    # try2 (200)
    yPayMax = [12.980227272727273, 13.91402380952381, 15.604426470588235, 14.825452631578948, 15.173490566037737, 14.160469026548673, 13.406431506849316, 14.6383216374269, 13.84029479768786, 14.766564444444445, 14.515569105691057, 14.272941634241246, 13.980850746268658, 14.254252491694352, 15.129903426791277, 14.489469444444445, 14.29614360313316, 14.42254739336493, 14.413193548387097, 14.283680995475112]
    yPayActual = [12.236772727272728, 11.77554365079365, 11.117253151260504, 9.946658602187286, 9.808653436448301, 8.90790510287656, 8.015668280102432, 8.529866562297332, 8.166160535250235, 8.595020606049257, 8.107186332899143, 7.939955475110615, 7.817959885042589, 7.806420115973553, 8.285404910773723, 7.979209283311688, 7.629254530931949, 7.819221168295134, 7.731214488286847, 7.634515038369287]
    # try 3 (100)
    # yPayMax=[14.18825, 13.187913043478261, 13.9705, 13.074522727272727, 13.695384615384615, 12.425166666666668, 14.095292307692308, 12.124383720930233, 13.4496, 13.326578947368422, 12.451702127659575, 12.753717948717949, 13.331253846153846, 12.920362962962963, 14.341623188405798, 12.336073619631902, 12.574909090909092, 12.971377245508982, 11.643801169590644, 13.910787735849057]
    # yPayActual=[13.916583333333334, 11.70286956521739, 11.756376515151516, 9.415360434704185, 8.987803456959707, 7.795955927146365, 8.671626615625721, 7.400303443187307, 8.198574443637474, 7.483658701227555, 7.459949702383735, 7.445670651836709, 7.392059340133485, 7.25407174968261, 7.904149638153194, 6.940768950519024, 7.317839272866881, 6.993293511364851, 6.472959723903723, 7.72864145671459]

    plt.plot(x, yPayMax,label='average pay-max')
    plt.plot(x, yPayActual,label='average pay-actual')
    plt.legend()
    plt.xlabel('number of parcels')
    plt.xticks(x, x)
    plt.ylabel('average of of pay')
    plt.title('100 drivers')
    plt.show()


def compareWeightsActual(x,dictOfNames):
    for name,lis in dictOfNames.items():
        plt.plot(x, lis, label=name)

    plt.xlabel('number of parcels')
    plt.xticks(x, x)
    plt.ylabel('median of actual pay')
    plt.title('200 drivers')
    plt.legend()
    plt.show()


def compareWeightsMax(x, dictOfNames):
    for name, lis in dictOfNames.items():
        plt.plot(x, lis, label=name)

    plt.xlabel('number of parcels')
    plt.xticks(x, x)
    plt.ylabel('median of max pay')
    plt.title('200 drivers')
    plt.legend()
    plt.show()


def durationFunc3(x,y):

    plt.plot(x, y)
    plt.legend()
    plt.xlabel('Number of drivers')
    plt.xticks(x, x)
    plt.ylabel('Average of duration')
    plt.title('100 parcels')
    plt.show()


def plotSucc(x,avg,median,stdev):
    plt.plot(x, avg, label='Average')
    plt.plot(x, median, label='Median')
    plt.errorbar(x, avg ,stdev, linestyle='None', marker='^' ,label='Stdev')


    plt.legend()
    plt.xlabel('Number of drivers')
    plt.xticks(x, x)
    plt.ylabel('Success rates')
    plt.title('300 parcels')
    plt.show()


def plotDiffPriority(ytitle, type1):
    path=f'results/comparePriority100{type1}'
    with open(f'{path}.json') as json_file:
        res = json.load(json_file)
    namesOfWeights = ['weightPriortyTimeDriverDistance', 'weightPriortyTimeDistanceDriver',
                           'weightPriortyDistanceDriverTime', 'weightPriortyDistanceTimeDriver',
                           'weightPriortyDriverDistanceTime', 'weightPriortyDriverTimeDistance']
    prettyNames={'weightPriortyTimeDriverDistance': 'Time, Drivers, Distance',
                 'weightPriortyTimeDistanceDriver': 'Time, Distance, Drivers',
                 'weightPriortyDistanceDriverTime': 'Distance, Drivers, Time',
                 'weightPriortyDistanceTimeDriver': 'Distance, Time, Drivers',
                  'weightPriortyDriverDistanceTime': 'Drivers, Distance, Time',
                 'weightPriortyDriverTimeDistance': 'Drivers, Time, Distance'}

    dict={k: [] for k in namesOfWeights}
    parcelsRange=range(50,1001,50)

    for name in namesOfWeights:
        for j,parcel in enumerate(parcelsRange):
            temp = []
            for i in range(10):
                temp.append(res[str(i)][name][j])
            dict[name].append(statistics.mean(temp))

    for name, lis in dict.items():
        plt.plot(parcelsRange, lis, label=prettyNames[name])
    plt.legend()
    plt.xlabel('Number of parcels')
    plt.xticks(parcelsRange, parcelsRange)
    plt.ylabel(ytitle)
    plt.title('100 Drivers')
    plt.show()

def plotDuration(x,durationsRandom,durationsTimeDriverDistance,durationsDriverDistanceTime):
    plt.plot(x, durationsRandom,label='Random priority')
    plt.plot(x, durationsTimeDriverDistance,label='Time, Drivers, Distance')
    plt.plot(x, durationsDriverDistanceTime,label='Drivers, Distance, Time')

    plt.legend()
    plt.xlabel('Number of drivers')
    plt.xticks(x, x)
    plt.ylabel('Average of duration')
    plt.title('100 parcels')
    plt.show()

#########from here


def plotDBSucc(numParcels,dictDriversList):
    myList = dictDriversList.items()
    myList = sorted(myList)
    x, y = zip(*myList)
    avg=list(map(lambda lis:statistics.mean(lis),y))
    median= list(map(lambda lis:statistics.median(lis),y))
    stdev= list(map(lambda lis:statistics.stdev(lis),y))

    plt.title(f'{numParcels} parcels')
    plt.ylabel('Success rate')
    plt.xlabel('Number of drivers')
    plt.plot(x,avg ,label='Average')
    plt.plot(x,median,label='Median')
    plt.errorbar(x, avg ,stdev, linestyle='None', marker='^' ,label='Stdev')

    plt.legend()
    plt.show()


def plotDBduration(numParcels,dictWeightDriversList):
    maximum=-float('inf')
    minimum=float('inf')

    for nameOfWeight,dictDriversList in dictWeightDriversList.items():
        myList = dictDriversList.items()
        myList = sorted(myList)
        x, y = zip(*myList)
        avg=list(map(lambda lis:statistics.mean(lis),y))
        plt.plot(x,avg,label=prettyNames[nameOfWeight])

        maximum=max(maximum,max(avg))
        minimum=min(minimum,min(avg))


    plt.title(f'{numParcels} parcels')
    plt.ylabel('Duration average in hours')
    yRange=range(int(minimum-int(minimum%60)),int(maximum),30)
    def addZero2Str(x):
        if x==0:
            return '00'
        else:
            return x
    plt.yticks(yRange,list(map(lambda x:f'{int(x/60)}:{addZero2Str(x%60)}',yRange)))
    plt.xlabel('Number of drivers')
    plt.legend()
    plt.show()


def plotDBdistance(numParcels,dictWeightDriversList):

    for nameOfWeight,dictDriversList in dictWeightDriversList.items():
        myList = dictDriversList.items()
        myList = sorted(myList)
        x, y = zip(*myList)
        avg=list(map(lambda lis:statistics.mean(lis),y))
        plt.plot(x,avg,label=prettyNames[nameOfWeight])



    plt.title(f'{numParcels} parcels')
    plt.ylabel('Distance average in meters')
    plt.xlabel('Number of drivers')
    plt.legend()
    plt.show()


def plotDBdiffCost(numParcels,dictWeightDriversList):

    for nameOfWeight,dictDriversList in dictWeightDriversList.items():
        myList = dictDriversList.items()
        myList = sorted(myList)
        x, y = zip(*myList)
        avg=list(map(lambda lis:statistics.mean(lis),y))
        plt.plot(x,avg,label=prettyNames[nameOfWeight])



    plt.title(f'{numParcels} parcels')
    plt.ylabel('Average profit percentage between maximum and actual cost')
    plt.xlabel('Number of drivers')
    plt.legend()
    plt.show()

if __name__=='__main__':

    # averageDrivers()
    # medianDrivers()
    # profits()
    # medianFunc1()
    # avgFunc1()

    plotDiffPriority('Difference between a maximum cost and a actual cost', 'Diff')
    plotDiffPriority('Relative profit between between a maximum cost and a actual cost', 'Ratio')