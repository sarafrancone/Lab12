import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestPath = []
        self._bestValue = 0

    def buildGraph(self, country, year):
        self._graph.clear()
        nodi = DAO.getRetailers(country)
        for nodo in nodi:
            self._idMap[nodo.Retailer_code] = nodo

        self._graph.add_nodes_from(nodi)
        edges = DAO.getEdgesPesati(year, country)
        for edge in edges:
            v0 = self._idMap[edge[0]]
            v1 = self._idMap[edge[1]]
            peso = edge[2]
            if not self._graph.has_edge(v0, v1):
                self._graph.add_edge(v0, v1, weight=peso)


        return self._graph

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getVolumeVendita(self, retailer):

        vicini = self._graph.neighbors(retailer)
        volume = 0
        for v in vicini:
            volume += self._graph[retailer][v]['weight']
        return volume

    def volumiTotali(self):
        lista = []
        for nodo in self._graph.nodes:
            volume = self.getVolumeVendita(nodo)
            lista.append( (nodo, volume))
        lista.sort(key=lambda x:x[1], reverse=True)
        return lista

    def getRetailers(self, country):
        return DAO.getRetailers(country)

    def getNodes(self):
        return self._graph.nodes

    def getCountries(self):
        return DAO.getCountries()

    def calcolaPercorso(self, n):
        self._bestPath = []
        self._path_edge = []
        self._bestValue = 0

        parziale = []
        archi = []
        for nodo in self._graph.nodes:
            parziale.append(nodo)
            self._ricorsione(parziale, n, [])
            parziale.pop()

        return self._path_edge, self._bestValue

    def _ricorsione(self, parziale, n, archi_parziale):
        #condizione di terminazione:

        if len(archi_parziale) == (n-1):
            if self._graph.has_edge(parziale[-1], parziale[0]):
                archi_parziale.append( (parziale[-1], parziale[0], self._graph.get_edge_data(parziale[-1], parziale[0])["weight"]) )
                parziale.append( parziale[0] )
                peso_cammino = self.getScore(archi_parziale)
                if peso_cammino > self._bestValue:
                    self._bestValue = peso_cammino + 0.0
                    self._bestPath = copy.deepcopy(parziale)
                    self._path_edge = copy.deepcopy(archi_parziale)
                parziale.pop()
                archi_parziale.pop()
            return
        vicini = list(self._graph.neighbors(parziale[-1]))
        vicini = [i for i in vicini if i not in parziale]

        for nodo in vicini:
            archi_parziale.append( (parziale[-1], nodo, self._graph.get_edge_data(parziale[-1], nodo)["weight"]))
            parziale.append(nodo)
            self._ricorsione(parziale, n, archi_parziale)
            parziale.pop()
            archi_parziale.pop()

    def getScore(self, parziale):
        score = 0
        for edge in parziale:
            score += edge[2]
        return score

    def solution(self, path):
        list = []
        for i in range(len(path)-1):
            list.append(self._graph[path[i]][path[i+1]]["weight"])

        return list












