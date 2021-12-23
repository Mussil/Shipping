import igraph

class GraphAPI(object):
    """ the purpose of the class is to create API for the graph,
    in case we will change the libary
    and for easy access"""

    def __init__(self,stopTime=0):
        self._g=igraph.Graph(directed=True)
        self.stopTime=stopTime

        self._idNode=0 #the next empty ID for a new node
        self._idEdge=0 #the next empty ID for a new Edge

        #TODO - think if the dicts are really necessary
        # nodes dictionaries
        # self._idNode_Location={}
        # self._idNode_SP={}
        # self._idNode_Time={}

    @property
    def lenEdges(self):
        return self._g.ecount()
    @property
    def lenNodes(self):
        return self._g.vcount()

    def findNodeIndexById(self,id):
        """ the function get id (that we defined) of node
        and return its index that igraph created"""
        vertex=self._g.vs.find(ID=id)
        return vertex.index

    def findEdgeIndexById(self,id):
        """ the function get id (that we defined) of edge
        and return its index that igraph created"""
        edge=self._g.es.find(ID=id)
        return edge.index

    def add_node(self,driverId=None,spId=None,time=None,type='eventNode'):
        self._g.add_vertices(1)
        newNodeIndex=self.lenNodes-1
        self._g.vs[newNodeIndex]['ID']=self._idNode
        self._idNode+=1 #increase the id for the next new node
        self._g.vs[newNodeIndex]['driverId']=driverId
        self._g.vs[newNodeIndex]['spId']=spId
        self._g.vs[newNodeIndex]['time']=time
        self._g.vs[newNodeIndex]['type']=type

        return self._g.vs[newNodeIndex]['ID']


    def add_edge(self,node1Id,node2Id,weight=0,type=None,time=None,distance=None):
        """ get the id (that we defined) of 2 nodes and the weight between them
        and create new edge"""
        indexNode1=self.findNodeIndexById(node1Id)
        indexNode2=self.findNodeIndexById(node2Id)
        self._g.add_edges([(indexNode1,indexNode2)]) #add the edge
        newEdgeindex=self.lenEdges-1
        self._g.es[newEdgeindex]['ID']=self._idEdge
        self._idEdge+=1 #increase the id for the next new edge
        self._g.es[newEdgeindex]['weight'] = weight #add the weight to the edge
        self._g.es[newEdgeindex]['type'] = type

        #TODO- add those attibutes by real data
        self._g.es[newEdgeindex]['time'] = time
        self._g.es[newEdgeindex]['distance'] = distance

        return self._g.es[newEdgeindex]['ID']


    def dijkstra(self,source,target,weight='weight'):
        """ find the shortest path from source node to target node
        IN THE FUTURE
        could get different weight functions for different calculations
        also could work with list of sources and list of targets
        """
        weights=self._g.es[weight]
        path = self._g.get_shortest_paths(source, to=target,weights=weights)
        # for n in path[0]:
        #     print("{}".format(self._g.vs[n]['ID']),end=',')
        return path[0]



g=GraphAPI()
x=g.add_node()
print(x)
g.add_node()
g.add_node()
g.add_node()
g.add_node()
g.add_node()
g.add_edge(0,1,8)
g.add_edge(0,2)
g.add_edge(2,3)
g.add_edge(1,3)
g.add_edge(3,4)
g.add_edge(4,5)
print(list(g._g.es))

print(g.lenEdges)
print(g.lenNodes)

g.dijkstra(1,5)