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

    def __init__(self,stopTime=1,numberOfSP=10):
        self._g=igraph.Graph(directed=True)
        self.stopTimeMin=stopTime
        self.numberOfSP=numberOfSP

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

    def getNodesIdEventNodes(self):
        return self._g.vs.select(type_eq='eventNode')['ID']

    def getDestinationNodeIdSameSP(self,id):
        node=self._g.vs.select(ID_eq=id)
        spId=node['spId'][0]
        return self._g.vs.find(type_eq='destinationNode',spId_eq=spId)['ID']

    def getNodesSameSPAboveTime(self,idNode):
        """ :return an iterator of the IDs of all the nodes that:
         has the same service point - SP as the input
         the time is after the time from the input + stop time """
        node=self._g.vs.select(ID_eq=idNode,type_eq='eventNode')
        spId=node['spId'][0]
        if not spId:
            return
        time=node['time'][0]

        timePlusStopTime=addMin(time,self.stopTimeMin)

        matchNodes=self._g.vs.select(spId_eq=spId,time_ge=timePlusStopTime,type_eq='eventNode')
        matchNodesId=list(map(lambda x: x['ID'] , matchNodes))

        return matchNodesId






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


    def add_edge(self,node1Id,node2Id,weight=0,type=None,duration=0,distance=0):
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


    def _dijkstra(self,source,target,weight):
        """ find the shortest path from source node to target node
        #TODO  - IN THE FUTURE
        could get different weight functions for different calculations
        also could work with list of sources and list of targets
        """

        #todo - handle error
        # RuntimeWarning: Couldn't reach some vertices at src/paths/dijkstra.c:441
        weights=self._g.es[weight]
        path = self._g.get_shortest_paths(source, to=target,weights=weights)
        print(path)

        # for n in path[0]:
        #     print("{}".format(self._g.vs[n]['ID']),end=',')
        return path[0]


    def getDetailsShortestPath(self,source,target,minTime,weight='weight'):
        """
        :parameter source - spId of the source service point
        :parameter target - spId of the target service point
        :parameter minTime - DateTime of the arrive of a new parcel, only later nodes are accepted
        :parameter weight - the name of the weight function

        :returns the shortest path by dijkstra algorithm
        """

        #find node which has minimum time and the same sp source
        sameSp=self._g.vs.select(spId_eq=source,type_eq='eventNode',time_ge=minTime)
        minimumSource=min(sameSp, key=lambda x: x['time'])
        sourceID=minimumSource.index
        targetID=self._g.vs.find(spId_eq=target,type_eq='destinationNode')
        path=self._dijkstra(sourceID,targetID,weight)
        #todo- return the deatils of the path
        print(path)
        # print(path)






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
    # g.dijkstra(1,5)