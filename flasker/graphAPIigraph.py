import warnings
import igraph
import datetime
import matplotlib.pyplot as plt
import numpy as np
from flasker.helpers import addMin



class Graph(object):
    """using igraph
    the purpose of the class is to create API for the graph,
    in case we will change the libary
    and for easy access"""

    def __init__(self,stopTime,numberOfSP,maxDriver,maxTimeMin,maxDistanceMeters ):
        self._g=igraph.Graph(directed=True)
        self.stopTimeMin=stopTime
        self.numberOfSP=numberOfSP

        # max
        self.maxDriver= maxDriver
        self.maxTimeMin=maxTimeMin
        self.maxDistanceMeters= maxDistanceMeters

        #weights priority
        self.nameOfWeights={}

        #TODO - think if i need this IDs ,
        # beacuse i am not deleting nodes from the graph so the indexs not suppose to change
        # and anyway meanwhile i use the index stright after i get it so it won't changes and there is no use for the artifical IDs
        self._idNode=0 #the next empty ID for a new node
        self._idEdge=0 #the next empty ID for a new Edge


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

    def getNodesIdAndTime(self):
        """ :return an iterator of the IDs of all the nodes and their time """
        return zip(self._g.vs['ID'],self._g.vs['time']) #pairs of id and time of all the nodes

    def getNodesIdEventNodes(self):
        return self._g.vs.select(type_eq='eventNode')['ID']

    def getDestinationNodeIdSameSP(self,id):
        node=self._g.vs.select(ID_eq=id)
        spId=node['spId'][0]
        return self._g.vs.find(type_eq='destinationNode',spId_eq=spId)['ID']

    def getNodesSameSPAboveTime(self,idNode):
        """ :return an iterator of the IDs and time of all the nodes that:
         has the same service point - SP as the input
         the time is after the time from the input + stop time """
        # node=self._g.vs.select(ID_eq=idNode,type_eq='eventNode')
        # print(node['spId'])

        try:
            node = self._g.vs.find(ID_eq=idNode, type_eq='eventNode') #from id to know the spId
        except ValueError:
            return
        # print(node['spId'])
        # spId=node['spId'][0]
        # if not spId:
        #     return
        # time=node['time'][0]
        spId=node['spId']
        time=node['time']

        timePlusStopTime=addMin(time,self.stopTimeMin)

        matchNodes=self._g.vs.select(spId_eq=spId,time_ge=timePlusStopTime,type_eq='eventNode')

        return zip(matchNodes['ID'],matchNodes['time']) #pairs of id and time of all the nodes that has the same sp and later time





    def _checkIfNodeExist(self,driverId,spId,time):
        """ check if the node already exist """
        try:
            node = self._g.vs.find(driverId_eq=driverId, spId_eq=spId, time_eq=time)
            return node['ID']
        except ValueError:
            return None
        # if node:
        #     return self._findNodeIndexById(node[0].index)
        # else:
        #     return None


    def add_node(self,driverId=None,spId=None,time=None,type=None):
        if self.lenNodes: #need to check if the graph is empty, otherwise will throw error
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


    def add_edge(self,node1Id,node2Id,type=None,duration=0,distance=0):
        """ get the id (that we defined) of 2 nodes
        and create new edge"""
        indexNode1=self._findNodeIndexById(node1Id)
        indexNode2=self._findNodeIndexById(node2Id)
        self._g.add_edges([(indexNode1,indexNode2)]) #add the edge
        newEdgeindex=self.lenEdges-1
        self._g.es[newEdgeindex]['ID']=self._idEdge
        self._idEdge+=1 #increase the id for the next new edge
        self._g.es[newEdgeindex]['type'] = type

        self._g.es[newEdgeindex]['duration'] = duration
        self._g.es[newEdgeindex]['distance'] = distance

        return self._g.es[newEdgeindex]['ID']


    def _dijkstra(self,source,target,weight,output='vpath'):
        """ find the shortest path from source index node to target index node
        could get different weight functions for different calculations
        """

        # suppress warnings
        warnings.filterwarnings('ignore') #in case there is no path to the destination
        weights=self._g.es[weight]
        path = self._g.get_shortest_paths(source, to=target,weights=weights,mode=igraph.OUT,output=output)
        return path[0]



    #
    # def _manySourcesDijkstra(self,sources,target,weight):
    #     """find the source from all the sources that will provide the minimum path"""
    #     def calcSumWeightsOfPath(path):
    #         weights = self._g.es[weight]
    #         sumOfPath = sum(map(lambda edge: weights[edge], path))
    #         return sumOfPath
    #
    #     minSum=float('inf')
    #     for source in sources:
    #         path = self._dijkstra(source, target, weight,output='epath')
    #         if path:
    #             tempSum=calcSumWeightsOfPath(path)
    #             if tempSum<minSum:
    #                 minSum=tempSum
    #                 minSource=source
    #
    #             #just to ceck- need to be delted
    #             # path = self._dijkstra(source, target, weight,output='vpath')
    #             # for n in path:
    #             #     print(f" sp={self._g.vs[n]['spId']}, driver={self._g.vs[n]['driverId']}")
    #             # print(tempSum)
    #
    #     return self._dijkstra(minSource, target, weight,output='vpath')

    def _addStartNodeEdges(self,spId,time,otherNodes,weightName):
        #add startNode
        startNode=self.add_node(driverId=None,spId=spId,time=time, type='startNode')
        #add startEdges
        for node in otherNodes['ID']:
            timeOfNode=self._g.vs.find(ID_eq=node)['time']
            duration=(timeOfNode-time).total_seconds() / 60.0 #working with minutes
            edge=self.add_edge(startNode,node,type='startEdge',duration=duration,distance=0)

            #add weight to edge
            self._g.es.find(ID_eq=edge, type_eq='startEdge')[weightName]=self.nameOfWeights[weightName]['weightTime']*duration

        return startNode

    def getDetailsShortestPath(self,source,target,minTime,weight):
        """
        :parameter source - spId of the source service point
        :parameter target - spId of the target service point
        :parameter minTime - DateTime of the arrive of a new parcel, only later nodes are accepted
        :parameter weight - the name of the weight function

        :returns the shortest path by dijkstra algorithm
        """


        #find node which has is larger that minTime and the same sp source
        sameSp=self._g.vs.select(spId_eq=source,type_eq='eventNode',time_ge=minTime)
        startNode=self._addStartNodeEdges(spId=source,time=minTime,otherNodes=sameSp,weightName=weight)

        sourceIndex=self._g.vs.find(ID_eq=startNode,type_eq='startNode').index
        targetIndex=self._g.vs.find(spId_eq=target,type_eq='destinationNode').index

        path=self._dijkstra(sourceIndex,targetIndex,weight)


        #the next 2 lines are for many sources
        # sourcesIndex=list(map(lambda vertex: vertex.index,sameSp))
        # path=self._manySourcesDijkstra(sourcesIndex,targetIndex,weight)


        pathSpDriver=[]
        allSPid=[]
        allDriversID=[]

        for n in path:
            allSPid.append(self._g.vs[n]['spId'])
            allDriversID.append(self._g.vs[n]['driverId'])
            # pathSpDriver.append((self._g.vs[n]['spId'],self._g.vs[n]['driverId']))
            # print(f" sp={self._g.vs[n]['spId']}, driver={self._g.vs[n]['driverId']}")
        pathSpDriver=list(zip(allSPid,allDriversID))
        # edges=[]
        totalDuration=0
        totalDistance=0
        totalDrivers=len(set(allDriversID[1:-1]))#exlude the destination and start nodes
        for id1, id2 in zip(path[0:-1], path[1:]):
            # edges.append((id1,id2))
            totalDuration+=self._g.es.find(_source=id1,_target=id2)['duration']
            totalDistance+=self._g.es.find(_source=id1,_target=id2)['distance']



        #TODO : delete temp node and edges
        self._g.delete_vertices(self._findNodeIndexById(startNode))

        return pathSpDriver,totalDistance,totalDuration,totalDrivers

    def addWeights(self,nameOfWeight,A='time',B='driver',C='distance',alph=0,beta=0):

        def getMaxOfPriority(A):
            if A=='driver':
                return self.maxDriver
            elif A=='time':
                return self.maxTimeMin
            elif A=='distance':
                return self.maxDistanceMeters


        maxB=getMaxOfPriority(B)
        maxC=getMaxOfPriority(C)

        weightC=1
        weightB=maxC-beta
        weightA=(maxB-alph)*weightB

        def getWeightDriver():
            if A=='driver':
                return weightA
            elif B=='driver':
                return weightB
            elif C=='driver':
                return weightC
        def getWeightTime():
            if A=='time':
                return weightA
            elif B=='time':
                return weightB
            elif C=='time':
                return weightC
        def getWeightDistance():
            if A=='distance':
                return weightA
            elif B=='distance':
                return weightB
            elif C=='distance':
                return weightC
        es=self._g.es
        weightDriver=getWeightDriver()
        weightTime=getWeightTime()
        weightDistance=getWeightDistance()
        for i,edge in enumerate(es):
            duration = es[i]['duration']
            distance = es[i]['distance']

            if edge['type']=='destinationEdge':
                es[i][nameOfWeight]=0
            elif edge['type']=='stayEdge':
                es[i][nameOfWeight]=weightDriver+weightTime*duration
            elif edge['type']=='travelEdge':
                es[i][nameOfWeight]=weightTime* duration+ weightDistance*distance

        self.nameOfWeights[nameOfWeight]={'weightDriver': weightDriver,
                                          'weightTime':weightTime,
                                          'weightDistance':weightDistance
                                          }

    def draw(self):
        #edge label (meters,minutes)
        #color of node represnt driver
        #name of node represnt service point

        g=self._g

        #TODO: make the colors of the drivers to be more generic
        # driversName = set(g.vs["driverId"])#for all the unique names
        # colors = list(np.random.choice(range(256), size=len(driversName)))
        # colors=tuple((np.random.randint(256),) + (np.random.randint(256),) +(np.random.randint(256),)+(np.random.randint(256),) for name in driversName)
        # color_node_dict=dict(zip(driversName,colors))
        # print(color_node_dict)
        # print(igraph.drawing.colors.known_colors)

        color_node_dict = {'John': 'blue', 'Dani': 'green', 'Mia':'pink',None:'grey'}


        shape_node_dict={'eventNode':'circle', 'destinationNode' :'rectangle'}

        color_edge_dict={'travelEdge':'black', 'stayEdge':'yellow', 'destinationEdge':'grey'}
        layout = g.layout("tree")

        visual_style = {}
        #vetrex
        visual_style["vertex_size"] = 40
        visual_style["vertex_shape"] = [shape_node_dict[type] for type in g.vs["type"]]
        visual_style["vertex_color"] = [color_node_dict[name] for name in g.vs["driverId"]]

        vertex_id_time=[]
        for spId,time in zip(g.vs['spId'],g.vs['time']):
            if time:
                vertex_id_time.append(str(spId)+'\n'+str(time.time())[0:5])
            else :
                vertex_id_time.append(str(spId))
        visual_style["vertex_label"] = vertex_id_time
        # visual_style["vertex_label"] =  g.vs["spId"]

        #edges
        visual_style["edge_label"] = list(map(lambda x: '' if x==(0,0) else x, zip(g.es["distance"],map(lambda x: round(x),g.es["duration"])))) #if the edge is (0,0) print nothing, in case of destination edges
        visual_style["edge_color"] = [color_edge_dict[type] for type in g.es["type"]]
        visual_style["edge_label_color"] = [color_edge_dict[type] for type in g.es["type"]]

        visual_style["edge_curved"] = 0.03

        visual_style["layout"] = layout

        igraph.plot(g, **visual_style,target='graphImage.png',margin = 40)


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
    print("--")

    print(g.lenEdges)
    print(g.lenNodes)
    # g.dijkstra(1,5)