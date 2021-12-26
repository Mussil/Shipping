import datetime

from flasker.graphAPIigraph import Graph, addMin

g=Graph()




def createTravelEdges(g,route):
    """ this function get a route of a driver and crate all the travel edges related to this path
    also it creates the nodes for the path A.K.A event nodes"""
    path=route['path']
    startTime=route['start']
    driver=route['driver']

    #travel edges
    node1 = g.add_node(driver, path[0], startTime)
    #TODO- change the time from 10 min to be the correct time
    new_time = addMin(startTime,10)
    node2 = g.add_node(driver, path[1], new_time)
    #TODO- add to the edge the weight , duration and distance
    g.add_edge(node1, node2, type='TravelEdge')

    for sp1,sp2 in zip(path[1:-1],path[2:]):
        node1=g.add_node(driver,sp1,new_time)
        # TODO- change the time from 10 min to be the correct time
        new_time = addMin(new_time, 10)
        node2=g.add_node(driver,sp2,new_time)
        # TODO- add to the edge the weight , duration and distance
        g.add_edge(node1, node2,type='TravelEdge')


def createStayEdges(g):
    """ this function will create esges between existing nodes of the same service point
    the edges are from the earlier time to the later"""
    for node in g.getNodesId():
        listNode2=g.getNodesSameSPAboveTime(node)

        for node2 in listNode2:
            # TODO- add to the edge the weight
            g.add_edge(node, node2,type='StayEdge')

def createDestinationEdges(g):

    def createDestinationNodes(g):
        numberOfSP=g.numberOfSP
        for sp in range(1,numberOfSP+1):
            g.add_node(None, sp, None,type='destinationNode')

    createDestinationNodes(g)

    idAllEventNodes=g.getNodesIdEventNodes()
    for id in idAllEventNodes:
        id2=g.getDestinationNodeIdSameSP(id)
        g.add_edge(id, id2,type='DestinationEdge')



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
    # edgeColors=[]
    for i,x in enumerate(g.es):
        edgeLabels[(x.source,x.target)]=x.attributes()
        # if x.attributes()['type']=='StayEdge':
        #     edgeColors.append('yellow')
        # elif x.attributes()['type']=='TravelEdge':
        #     edgeColors.append('red')
        # elif x.attributes()['type'] == 'DestinationEdge':
        #     edgeColors.append('blue')

    layout=nx.shell_layout(G)
    nx.draw_networkx_nodes(G,pos=layout,node_color=nodeColors)
    nx.draw_networkx_edges(G,pos=layout,)
    nx.draw_networkx_labels(G,pos=layout ,labels=labels,font_size=4)
    nx.draw_networkx_edge_labels(G,pos=layout ,edge_labels=edgeLabels,font_size=4,alpha=0.4)

    plt.show()



if __name__=='__main__':
    route1 = {
        'driver': 'John',
        'start': datetime.datetime(2022, 1, 1, 23, 21),
        'path': [1, 2, 3, 4, 5]
    }
    createTravelEdges(g,route1)
    route2 = {
        'driver': 'Dani',
        'start': datetime.datetime(2022, 1, 1, 12, 0),
        'path': [3,4 ,6, 1,7]
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
    draw(g)
    g.getDetailsShortestPath(6,5,datetime.datetime(2022, 1, 1, 1, 0))


    # x=list(g._g.es)
    # y=g._g.vs
    # for edge in g._g.es:
    #     print(edge)
    #     print(y[edge.source].attributes(),y[edge.target].attributes())
    #     print( )
