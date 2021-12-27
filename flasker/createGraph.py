import datetime

from flasker.graphAPIigraph import Graph, addMin
from flasker.dist_time_calc import calcDistTime
g=Graph()


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
        new_time = addMin(startTime, duration)
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
        for sp in range(1,numberOfSP+1): #TODO: more genral approch of knowing the sp numbers
            g.add_node(driverId=None, spId=sp, time=None, type='destinationNode')

    createDestinationNodes(g)

    idAllEventNodes=g.getNodesIdEventNodes()
    for id in idAllEventNodes:
        id2=g.getDestinationNodeIdSameSP(id)
        g.add_edge(id, id2,type='destinationEdge')



def draw(g):
    """ visualize the graph """
    #TODO- use only the API and not _g
    import networkx as nx
    import matplotlib.pyplot as plt
    g=g._g
    G = g.to_networkx()
    labels={}
    nodeColors=[]

    for i,x in enumerate(g.vs):
        labels[i]=x.attributes()
        if x.attributes()['type']=='eventNode':
            # nodeColors.append('red')
            if x.attributes()['driverId']=='John':
                nodeColors.append('red')
            if x.attributes()['driverId'] == 'Dani':
                nodeColors.append('orange')
            if x.attributes()['driverId'] == 'Mia':
                nodeColors.append('yellow')

        elif x.attributes()['type']=='destinationNode':
            nodeColors.append('black')
        else:
            nodeColors.append('green')


    edgeLabels={}
    edgeColors={}
    for i,x in enumerate(g.es):
        edgeLabels[(x.source,x.target)]=x.attributes()
        if x.attributes()['type']=='stayEdge':
            edgeColors[(x.source,x.target)]=('yellow')
        elif x.attributes()['type']=='travelEdge':
            edgeColors[(x.source,x.target)]=('red')
        elif x.attributes()['type'] == 'destinationEdge':
            edgeColors[(x.source,x.target)]=('black')

    layout=nx.shell_layout(G)
    nx.draw_networkx_nodes(G,pos=layout,node_color=nodeColors)
    nx.draw_networkx_edges(G,pos=layout,edgelist=edgeColors.keys(),edge_color=edgeColors.values())
    nx.draw_networkx_labels(G,pos=layout ,labels=labels,font_size=4)
    nx.draw_networkx_edge_labels(G,pos=layout ,edge_labels=edgeLabels,font_size=5,alpha=0.6)

    plt.show()


def buildGraph(routes):
    g = Graph()
    for route in routes:
        createTravelEdges(g, route1)
    createStayEdges(g)
    createDestinationEdges(g)
    return g



if __name__=='__main__':

    route1 = {
        'driver': 'John',
        'start': datetime.datetime(2022, 1, 1, 23, 21),
        'path': [1, 2, 3, 4]
    }
    createTravelEdges(g,route1)
    route2 = {
        'driver': 'Dani',
        'start': datetime.datetime(2022, 1, 1, 12, 0),
        'path': [3,4 ,6, 1]
    }
    createTravelEdges(g,route2)
    # route3 = {
    #     'driver': 'Mia',
    #     'start': datetime.datetime(2022, 1, 1, 13, 40),
    #     'path': [3,4 ]
    # }
    # createTravelEdges(g,route3)
    createStayEdges(g)
    createDestinationEdges(g)
    g.addWeights(nameOfWeight='weightPriortyTimeDriverDistance',A='time',B='driver',C='distance',alph=0,beta=0)
    draw(g)
    g.getDetailsShortestPath(6,3,datetime.datetime(2022, 1, 1, 1, 0),weight='weightPriortyTimeDriverDistance')
    g.getDetailsShortestPath(2,1,datetime.datetime(2022, 1, 1, 1, 0),weight='weightPriortyTimeDriverDistance')


    # x=list(g._g.es)
    # y=g._g.vs
    # for edge in g._g.es:
    #     print(edge)
    #     print(y[edge.source].attributes(),y[edge.target].attributes())
    #     print( )
