import pprint
from collections import defaultdict
from heapq import heapify, heappush, heappop

pretty_print = pprint.PrettyPrinter()
pprint = pretty_print.pprint
defaultDict=lambda :defaultdict(int)


class Graph(object):
    """ Directed graph data structure """

    def __init__(self, edges=[]):
        self._graph = defaultdict(defaultDict)
        self.addEdges(edges)

    def addNode(self,node):
        """ Add node """

        self._graph[node] #deafultdict will create the node if it doesnt exists


    def addEdges(self, edges):
        """ Add edges (list of tuple pairs) to graph """

        for node1, node2,weight in edges:
            self.addEdge(node1, node2,weight)

    def addEdge(self, node1, node2,weight):
        """ Add edge between node1 and node2 """
        self.addNode(node1)
        self.addNode(node2)
        adjacencyListOfNode1=self.getNode(node1)
        adjacencyListOfNode1[node2]=weight


    def removeNode(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.items():
            try:
                cxns.pop(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def removeEdge(self,node1,node2):
        """ Remove the edge (node1,node2) """
        try:
            self.getNode(node1).pop(node2)
        except KeyError:
            pass

    def getNode(self,node):
        return self._graph[node]

    def getEdgeWeight(self,node1,node2):
        return self._graph[node1][node2]

    def getListNodes(self):
        return list(self._graph.keys())

    def getListEdges(self):
        """ return list of all the edges include their weights
        [ (u,v,weight) ]"""
        edgesList=[]
        for u, adjacencyList in self._graph.items():
            for v,weight in adjacencyList.items():
                edgesList.append((u,v,weight))
        return edgesList     

    def getAdjacencyOfNode(self,node):
        """get all the nodes that node is connected to them"""
        return self._graph[node]      

    def isConnected(self, node1, node2):
        """ Is node1 directly connected to node2 """

        return node1 in self._graph and node2 in self.getNode(node1).keys()

    def findPath(self, node1, node2, path=[]):
        """ Find any path between node1 and node2 (may not be shortest) """

        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self.getNode(node1).keys():
            if node not in path:
                new_path = self.findPath(node, node2, path)
                if new_path:
                    return new_path
        return None

            


    def dijkstra(self,source,target):
        """get a source and calculate the shortest path by dijkstra to the target
        return the path and the weight of the path"""


        class Node(object):
            """ a temporry class to contain the data for each node in dijkstra algorithm"""
            def __init__(self, node,d=float('inf'),pi=None):
                self.node=node
                self.d=d
                self.pi=pi
            def getNode(self):
                return self.node
            def getd(self):
                return self.d                
            def getPi(self):
                return self.pi   


            def setd(self,d):
                self.d  =d              
            def setPi(self,pi):
                self.pi =pi             
            
            def __lt__(self, other):
                return self.getd() < other.getd()

            # def __gt__(self, other):
            #     return self.getd() > other.getd()

        def w(u,v):
            return self.getEdgeWeight(u,v)


        def relax(u,v):
            if allNodes[v].getd() > allNodes[u].getd()+w(u,v):
                allNodes[v].setd(allNodes[u].getd()+w(u,v)) 
                allNodes[v].setPi(u)


        #initialize 
        allNodes=dict()
        nodes=self.getListNodes()

        for u in nodes:
            if u == source:
                attr=Node(u,0,None)
            else:
                attr=Node(u,float('inf'),None)
            allNodes[u]=attr
        
        # Creating heap
        heap=list(allNodes)
        heapify(heap)
        
        while heap:
            u=heappop(heap)
            for v in self.getAdjacencyOfNode(u).keys():
                relax(u,v)
        
        def path(dest):
            """ return the shortest path of dijkstar
            a list of the nodes in the shortest path include the source and the target
            and the sum of weights"""
            listPath=[]
            dest=allNodes.get(dest,None)
            if not dest:
                return [], float('inf')
            distance=dest.getd()
            listPath.insert(0,dest.getNode())
            while dest.getPi():
                listPath.insert(0,dest.getPi())
                dest=allNodes[dest.getPi()]
            return listPath,distance
        
        return path(target)



    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))


def drive():
    connections = [('A', 'B',1), ('B', 'C',2), ('B', 'D',3),
                       ('C', 'D',4), ('E', 'F',5), ('F', 'C',6)]
    g = Graph(connections)
    # pprint(g._graph)
    # g.addNode('G')
    # pprint(g._graph)
    # g.removeEdge('B','D')
    # pprint(g._graph)
    # g.removeNode('B')
    # pprint(g._graph)
    # g.addEdge('B','G',9)
    # pprint(g._graph)

    # pprint(g.findPath('B','D'))
    # print(g.getNode('A'))
    # print(g.getEdgeWeight('C','D'))
    # print(g.getListNodes())
    print("=== Dijkstra ===")
    print(g.dijkstra("E", "D"))


    return g

drive()