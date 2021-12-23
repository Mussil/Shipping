import igraph
import datetime


def addMin(tm, min):
    """ get a dateTime object and minutes
    :return their sum"""
    tm = tm + datetime.timedelta(minutes=min)
    return tm

class Graph(object):
    """using igraph
    the purpose of the class is to create API for the graph,
    in case we will change the libary
    and for easy access"""

    def __init__(self,stopTime=1):
        self._g=igraph.Graph(directed=True)
        self.stopTimeMin=stopTime

        #TODO - think if i need this IDs ,
        # beacuse i am not deleting nodes from the graph so the indexs not suppose to change
        # and anyway meanwhile i use the index stright after i get it so it won't changes and there is no use for the artifical IDs
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

    def _findNodeIndexById(self,id):
        """ the function get id (that we defined) of node
        :return its index that igraph created"""
        vertex=self._g.vs.find(ID=id)
        return vertex.index

    def _findEdgeIndexById(self,id):
        """ the function get id (that we defined) of edge
        :return its index that igraph created"""
        edge=self._g.es.find(ID=id)
        return edge.index

    def getNodesId(self):
        """ :return an iterator of the IDs of all the nodes """
        return iter(self._g.vs['ID'])


    def getNodesSameSPAboveTime(self,idNode):
        """ :return an iterator of the IDs of all the nodes that:
         has the same service point - SP as the input
         the time is after the time from the input + stop time """
        node=self._g.vs.select(ID_eq=idNode)
        spId=node['spId'][0]
        if not spId:
            return
        time=node['time'][0]

        timePlusStopTime=addMin(time,self.stopTimeMin)

        matchNodes=self._g.vs.select(spId_eq=spId,time_ge=timePlusStopTime)
        matchNodesId=list(map(lambda x: x['ID'] , matchNodes))
        if matchNodesId:
            return matchNodesId[0]
        else:
            return None




    def _checkIfNodeExist(self,driverId,spId,time):
        """ check if the node already exist """
        node = self._g.vs.select(driverId_eq=driverId, spId_eq=spId, time_eq=time)
        if node:
            return self._findNodeIndexById(node[0].index)
        else:
            return None


    def add_node(self,driverId=None,spId=None,time=None,type='eventNode'):
        if self.lenNodes: #need to check if the graph is empty
            nodeId=self._checkIfNodeExist(driverId,spId,time)
            if nodeId: #in case the node already exist, no need to create it again
                return nodeId

        self._g.add_vertices(1)
        newNodeIndex=self.lenNodes-1
        self._g.vs[newNodeIndex]['ID']=self._idNode
        self._idNode+=1 #increase the id for the next new node
        self._g.vs[newNodeIndex]['driverId']=driverId
        self._g.vs[newNodeIndex]['spId']=spId
        self._g.vs[newNodeIndex]['time']=time
        self._g.vs[newNodeIndex]['type']=type

        return self._g.vs[newNodeIndex]['ID']


    def add_edge(self,node1Id,node2Id,weight=0,type=None,duration=None,distance=None):
        """ get the id (that we defined) of 2 nodes and the weight between them
        and create new edge"""
        indexNode1=self._findNodeIndexById(node1Id)
        indexNode2=self._findNodeIndexById(node2Id)
        self._g.add_edges([(indexNode1,indexNode2)]) #add the edge
        newEdgeindex=self.lenEdges-1
        self._g.es[newEdgeindex]['ID']=self._idEdge
        self._idEdge+=1 #increase the id for the next new edge
        self._g.es[newEdgeindex]['weight'] = weight #add the weight to the edge
        self._g.es[newEdgeindex]['type'] = type

        #TODO- add those attibutes by real data
        self._g.es[newEdgeindex]['duration'] = duration
        self._g.es[newEdgeindex]['distance'] = distance

        return self._g.es[newEdgeindex]['ID']


    def dijkstra(self,source,target,weight='weight'):
        """ find the shortest path from source node to target node
        #TODO  - IN THE FUTURE
        could get different weight functions for different calculations
        also could work with list of sources and list of targets
        """
        weights=self._g.es[weight]
        path = self._g.get_shortest_paths(source, to=target,weights=weights)
        # for n in path[0]:
        #     print("{}".format(self._g.vs[n]['ID']),end=',')
        return path[0]






if __name__=='__main__':
    g=Graph()
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