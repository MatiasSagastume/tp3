import random

CONSTANTE_PESO = 1


class Grafo:
    def __init__(self, es_dirigido=False):
        self.es_dirigido = es_dirigido
        self.estructura = {}

    def __len__(self):
        return len(self.estructura)

    def __contains__(self, item):
        return item in self.estructura.keys()

    def __iter__(self):
        return iter(self.obtener_vertices())

    def agregar_vertice(self, vertice):
        if vertice in self:
            return
        self.estructura[vertice] = {}

    def borrar_vertice(self, vertice):
        if vertice not in self:
            raise Exception("El vertice no se encuentra en el grafo")

        self.estructura.pop(vertice)

        for v in self.estructura:
            if vertice in v:
                v.pop[vertice]

    def agregar_arista(self, a, b, peso=CONSTANTE_PESO):
        if a not in self:
            raise Exception(f"El vertice {a} no se encuentra en el grafo")

        self.estructura[a][b] = peso
        if not self.es_dirigido and b in self:
            self.estructura[b][a] = peso

    def borrar_arista(self, a, b):
        if not a not in self:
            raise Exception(f"El vertice {a} no se encuentra en el grafo")

        if b not in self.estructura[a]:
            raise Exception(f"La arista no se encuentra en el grafo")

        self.estructura[a].pop(b)

        if not self.es_dirigido and b in self:
            self.estructura[b].pop(a)

    def estan_unidos(self, a, b):
        if a not in self:
            raise Exception(f"El vertice {a} no se encuentra en el grafo")

        if b not in self:
            raise Exception(f"El vertice {b} no se encuentra en el grafo")

        return b in self.estructura[a]

    def peso_arista(self, a, b):
        if not self.estan_unidos(a, b):
            raise Exception(f"Los vertices {a} y {b} no estan unidos")
        return self.estructura[a][b]

    def obtener_vertices(self):
        return list(self.estructura.keys())

    def vertice_aleatorio(self):
        return random.choice(self.obtener_vertices())

    def adyacentes(self, v):
        if v not in self.estructura:
            raise Exception(f"El vertice {v} no se encuentra en el grafo")

        res = []
        for vertice in self.estructura[v].keys():
            if vertice in self:
                res.append(vertice)
        return res
