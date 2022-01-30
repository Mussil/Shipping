import datetime

from flasker.createPaths import createRandomPaths
from flasker.graphAPIigraph import Graph
from flasker.pathCalc import calcDistTime
from flasker.helpers import addMin



def createTravelEdges(g,route):
    """ this function get a route of a driver and crate all the travel edges related to this path
    also it creates the nodes for the path A.K.A event nodes"""
    path=route['path']
    startTime=route['start']
    driver=route['driver']

    #travel edges
    #the first 2
    node1 = g.add_node(driverId=driver, spId=path[0], time=startTime,type='eventNode')
    duration, distance=calcDistTime(path[0],path[1],startTime)
    new_time = addMin(startTime,duration)
    node2 = g.add_node(driverId=driver, spId=path[1], time=new_time,type='eventNode')
    g.add_edge(node1, node2, type='travelEdge',duration=duration,distance=distance)

    for sp1,sp2 in zip(path[1:-1],path[2:]):
        # node1=g.add_node(driverId=driver,spId=sp1,time=new_time,type='eventNode')
        node1=node2
        duration, distance = calcDistTime(sp1, sp2, new_time)
        new_time = addMin(new_time, duration)
        node2=g.add_node(driverId=driver,spId=sp2,time=new_time,type='eventNode')
        g.add_edge(node1, node2, type='travelEdge', duration=duration, distance=distance)


def createStayEdges(g):
    """ this function will create edges between existing nodes of the same service point
    the edges are from the earlier time to the later"""
    #todo- check that i didnt ruined it

    for nodeId,time1 in g.getNodesIdAndTime(): #all the nodes, and get list of tuple of id and time

        for node2id,time2 in g.getNodesSameSPAboveTime(nodeId):#just the nodes that are the same sp and the time is later
            delta=(time2-time1).total_seconds() / 60.0 #working with minutes
            g.add_edge(nodeId, node2id,type='stayEdge',distance=0,duration=delta )

def createDestinationEdges(g):

    def createDestinationNodes(g):
        numberOfSP=g.numberOfSP
        for sp in range(1,numberOfSP+1):
            g.add_node(driverId=None, spId=sp, time=None, type='destinationNode')

    createDestinationNodes(g)

    idAllEventNodes=g.getNodesIdEventNodes()
    for id in idAllEventNodes:
        id2=g.getDestinationNodeIdSameSP(id)
        g.add_edge(id, id2,type='destinationEdge')





def buildGraph(routes,maxDrivers,maxSp,stopTime,maxTimeMin,maxDistanceMeters):
    print('BUILDING THE TIME EXPANDED GRAPH')
    # g = Graph()
    #TODO: change the parms to real one
    g = Graph(stopTime=stopTime, numberOfSP=maxSp, maxDriver=maxDrivers, maxTimeMin=maxTimeMin, maxDistanceMeters=maxDistanceMeters)

    for route in routes:
        createTravelEdges(g, route)
    createStayEdges(g)
    createDestinationEdges(g)
    return g



if __name__=='__main__':
    g = Graph(stopTime=1, numberOfSP=7, maxDriver=5, maxTimeMin=400, maxDistanceMeters=10000)

    route1 = {
        'driver': 'John',
        'start': datetime.datetime(2022, 1, 1, 23, 21),
        'path': [1,3,2, 4]
    }
    createTravelEdges(g,route1)
    route2 = {
        'driver': 'Dani',
        'start': datetime.datetime(2022, 1, 1, 12, 0),
        'path': [3,4 ,6, 1]
    }
    createTravelEdges(g,route2)
    route3 = {
            'driver': 'Mia',
            'start': datetime.datetime(2022, 1, 1, 13, 40),
            'path': [4 ,1]
        }
    createTravelEdges(g,route3)
    createStayEdges(g)
    createDestinationEdges(g)
    g.addWeights(nameOfWeight='weightPriortyTimeDriverDistance',A='time',B='driver',C='distance',alph=0,beta=0)
    # g.draw()
    path=g.getDetailsShortestPath(4,1,datetime.datetime(2022, 1, 1, 1, 0),weight='weightPriortyTimeDriverDistance')
    print(path)
    path=g.getDetailsShortestPath(4,2,datetime.datetime(2022, 1, 1, 1, 0),weight='weightPriortyTimeDriverDistance')
    print(path)

    # print(path)
    # g.getDetailsShortestPath(2,1,datetime.datetime(2022, 1, 1, 1, 0),weight='weightPriortyTimeDriverDistance')

    # routes=createRandomPaths(numDrivers=5, maxSp=20)
    # # print(routes)
    # g=buildGraph(routes,maxSp=20,maxDrivers=5)
    # g.draw()

