import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.DiGraph()
        self._idMap={}
        self._best=[]
        self._OptPath=[]
        self._bestCosto=0


    def getAllStores(self):
        return DAO.getAllStores()

    def buildGraph(self, store_id):
        self._graph = nx.DiGraph()
        self._idMap={}
        nodes=DAO.getAllNodes(store_id)
        self._graph.add_nodes_from(nodes)
        for n in nodes:
            self._idMap[n.order_id]=n
        edges=DAO.getAllEdges(store_id, self._idMap)
        for e in edges:
            self._graph.add_edge(e.o1, e.o2, weight=e.weight)


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getLongestPath(self, source):
        self._best=[]
        parziale=[source]
        self._ricorsioneLongest(parziale, list(self._graph.successors(parziale[-1])))
        return self._best[1:]


    def _ricorsioneLongest(self, parziale, rimanenti):
        if len(rimanenti)==0:
            if len(parziale)>len(self._best):
                self._best=copy.deepcopy(parziale)
        else:
            for n in rimanenti:
                parziale.append(n)
                self._ricorsioneLongest(parziale, list(self._graph.successors(parziale[-1])))
                parziale.pop()

    def getOptPath(self, source):
        self._OptPath=[]
        self._bestCosto=0

        parziale=[source]
        rimanenti=list(self._graph.successors(parziale[-1]))
        self._ricorsione(parziale, rimanenti)
        return self._OptPath, self._bestCosto

    def _ricorsione(self, parziale, rimanenti):

            for n in rimanenti:
                costo = self._calcolacosto(parziale)
                if costo > self._bestCosto:
                    self._OptPath = copy.deepcopy(parziale)
                    self._bestCosto = costo
                if len(parziale)>1:
                    if n not in parziale and self._graph[parziale[-2]][parziale[-1]]['weight']>self._graph[parziale[-1]][n]['weight']:
                        parziale.append(n)
                        nuovi_rimanenti=list(self._graph.successors(parziale[-1]))
                        self._ricorsione(parziale, nuovi_rimanenti)
                        parziale.pop()
                else:
                    parziale.append(n)
                    nuovi_rimanenti=list(self._graph.successors(parziale[-1]))
                    self._ricorsione(parziale, nuovi_rimanenti)
                    parziale.pop()

    def _calcolacosto(self, parziale):
        costo=0
        for i in range(len(parziale)-1):
            costo+=self._graph[parziale[i]][parziale[i+1]]['weight']
        return costo
