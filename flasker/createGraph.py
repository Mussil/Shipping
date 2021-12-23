
from flasker.graphAPIigraph import Graph
import datetime

g=Graph()



def addMin(tm, min):
    tm = tm + datetime.timedelta(minutes=min)
    return tm

def createTravelEdges(route):
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


def draw(g):
    """ visualize the graph """
    import networkx as nx
    import matplotlib.pyplot as plt
    g=g._g
    G = g.to_networkx()
    labels={}
    for i,x in enumerate(g.vs):
        labels[i]=x.attributes()

    edgeLabels={}
    for i,x in enumerate(g.es):
        edgeLabels[(x.source,x.target)]=x.attributes()
    layout=nx.shell_layout(G)
    nx.draw_networkx_nodes(G,pos=layout)
    nx.draw_networkx_edges(G,pos=layout)
    nx.draw_networkx_labels(G,pos=layout ,labels=labels,font_size=4)
    nx.draw_networkx_edge_labels(G,pos=layout ,edge_labels=edgeLabels,font_size=4)

    plt.show()



if __name__=='__main__':
    route1 = {
        'driver': 'John',
        'start': datetime.datetime(2022, 1, 1, 23, 21),
        'path': [1, 2, 3, 4, 5]
    }
    createTravelEdges(route1)
    route2 = {
        'driver': 'Dani',
        'start': datetime.datetime(2022, 1, 1, 12, 0),
        'path': [3, 6, 7]
    }
    createTravelEdges(route2)
    # draw(g)


    # x=list(g._g.es)
    # y=g._g.vs
    # for edge in g._g.es:
    #     print(edge)
    #     print(y[edge.source].attributes(),y[edge.target].attributes())
    #     print( )
