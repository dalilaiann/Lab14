import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.DiGraph()
        self._idMap={}

    def getAllStores(self):
        return DAO.getAllStores()

    def buildGraph(self, store_id):
        self._graph = nx.DiGraph()
        self._idMap={}
        nodes=DAO.getAllNodes(store_id)
        self._graph.add_nodes_from(nodes)
        for n in nodes:
            self._idMap[n.order_id]=n
        edges=DAO.getAllEdges()


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)
