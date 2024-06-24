from collections import deque
import random
from grafo import Grafo
import heapq
funciones_implementadas = ["camino", "conectados", "comunidad", "rango", "lectura", "diametro", "navegacion",
                           "clustering", "mas_importantes"]

REPETICIONES_LABEL_PROPAGATION = 20
REPETICIONES_NAVEGACION = 21
MINIMOS_ADYACENTES = 2
POS_ACTUAL = 0
K_PAGERANK = 40


def listar_operaciones():
    for f in funciones_implementadas:
        print(f)


def camino(g, inicio, fin):
    visitados = set()
    padres = {}
    distancia = {}
    cola = deque()
    padres[inicio] = None
    visitados.add(inicio)
    distancia[inicio] = 0
    cola.append(inicio)
    while cola:
        v = cola.popleft()
        for w in g.adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                padres[w] = v
                distancia[w] = distancia[v] + 1
                if w == fin:
                    return reconstruir_camino(inicio, fin, padres)
                cola.append(w)
    return None


def reconstruir_camino(inicio, fin, padres):
    v = fin
    res = []
    while v != inicio:
        res.append(v)
        v = padres[v]
    res.append(inicio)
    return res[::-1]


def conectados(grafo, vertice,  arr_cfcs, dict_cfcs):
    pila = deque()
    visitados = set()
    apilados = set()
    orden = {}
    mas_bajo = {}
    indice = [0]
    orden[vertice] = 0
    cfc(grafo, vertice, visitados, pila, apilados, orden, mas_bajo, arr_cfcs, indice)
    for i in range(len(arr_cfcs)):
        lista = arr_cfcs[i]
        for elem in lista:
            dict_cfcs[elem] = i


def cfc(grafo, v, visitados, pila, apilados, orden, mas_bajo, cfcs, indice):
    visitados.add(v)
    pila.append(v)
    apilados.add(v)
    mas_bajo[v] = orden[v]
    for w in grafo.adyacentes(v):
        if w not in visitados:
            orden[w] = indice[0] + 1
            indice[0] += 1
            cfc(grafo, w, visitados, pila, apilados, orden, mas_bajo, cfcs, indice)
            mas_bajo[v] = min(mas_bajo[v], mas_bajo[w])
        elif w in apilados:
            mas_bajo[v] = min(mas_bajo[v], orden[w])
    if mas_bajo[v] == orden[v]:
        nueva_cfc = []
        while True:
            w = pila.pop()
            apilados.remove(w)
            nueva_cfc.append(w)
            if w == v:
                break
        cfcs.append(nueva_cfc)


def rango(grafo, origen, n):
    visitados = set()
    cola = deque()
    distancia = {}
    visitados.add(origen)
    cola.append(origen)
    distancia[origen] = 0
    contador = 0
    while cola:
        v = cola.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                distancia[w] = distancia[v] + 1
                visitados.add(w)
                if distancia[w] == n:
                    contador += 1
                    continue
                cola.append(w)
    return contador


def navegacion(grafo, origen):
    res = []
    actual = origen
    for i in range(REPETICIONES_NAVEGACION):
        res.append(actual)
        ady = grafo.adyacentes(actual)
        if len(ady) == 0:
            break
        actual = ady[POS_ACTUAL]
    return res


def diametro(grafo):
    maximo = 0
    inicio = None
    fin = None
    padres = {}
    for v in grafo:
        dist, ver, dicc = bfs(grafo, v)
        if dist > maximo:
            maximo = dist
            inicio = v
            fin = ver
            padres = dicc
    return reconstruir_camino(inicio, fin, padres)


def bfs(grafo, origen):
    visitados = set()
    padres = {}
    distancia = {}
    cola = deque()
    padres[origen] = None
    vertice = None
    max_dist = 0
    visitados.add(origen)
    distancia[origen] = 0
    cola.append(origen)
    while cola:
        v = cola.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                padres[w] = v
                distancia[w] = distancia[v] + 1
                if distancia[w] > max_dist:
                    max_dist = distancia[w]
                    vertice = w
                cola.append(w)
    return max_dist, vertice, padres


def lectura(grafo, vertices):
    nuevo = Grafo(es_dirigido=True)
    vertices_indicados = set(vertices)
    for v in vertices:
        nuevo.agregar_vertice(v)
    for v in vertices:
        for w in grafo.adyacentes(v):
            if w in vertices_indicados:
                nuevo.agregar_arista(w, v, grafo.peso_arista(v, w))
    grados = grados_entrada(nuevo, vertices)
    cola_aux = deque()
    for v in vertices:
        if grados[v] == 0:
            cola_aux.append(v)
    res = []
    while cola_aux:
        v = cola_aux.popleft()
        res.append(v)
        for w in nuevo.adyacentes(v):
            grados[w] -= 1
            if grados[w] == 0:
                cola_aux.append(w)
    if len(res) == len(nuevo):
        return res
    return None


def grados_entrada(grafo, vertices):
    grados = {}
    for v in vertices:
        grados[v] = 0
    for v in vertices:
        for w in grafo.adyacentes(v):
            if w not in grados:
                continue
            grados[w] += 1
    return grados


def comunidad(grafo, origen):
    nuevo = Grafo(es_dirigido=True)
    for v in grafo:
        nuevo.agregar_vertice(v)
    for v in grafo:
        for w in grafo.adyacentes(v):
            nuevo.agregar_arista(w, v, grafo.peso_arista(v, w))
    label = {}
    i = 0
    vertices = []
    for v in nuevo:
        label[v] = i
        vertices.append(v)
        i += 1
    aristas_entrada = obtener_adyacentes(nuevo)
    grupo = []
    random.shuffle(vertices)
    for i in range(REPETICIONES_LABEL_PROPAGATION):
        for v in vertices:
            label[v] = max_freq(label, aristas_entrada[v])
    for v in grafo:
        if label[v] == label[origen]:
            grupo.append(v)
    return grupo


def obtener_aristas_entrada(grafo):
    aristas = {}
    for v in grafo:
        aristas[v] = []
    for v in grafo:
        for w in grafo.adyacentes(v):
            aristas[w].append(v)
    return aristas


def obtener_adyacentes(grafo):
    aristas = {}
    for v in grafo:
        aristas[v] = grafo.adyacentes(v)
    return aristas


def max_freq(label, adyacentes):
    apariciones = {}
    for v in adyacentes:
        apariciones[label[v]] = 0
    for v in adyacentes:
        apariciones[label[v]] += 1
    cant = 0
    maximo = None
    for indice, valor in apariciones.items():
        if valor > cant:
            cant = valor
            maximo = indice
    return maximo


def clustering(grafo, pagina=None):
    coeficiente = 0
    if pagina:
        return coeficiente_clustering(grafo, pagina)
    for v in grafo:
        coeficiente += coeficiente_clustering(grafo, v)
    return coeficiente / len(grafo)


def coeficiente_clustering(grafo, vertice):
    adyacentes = grafo.adyacentes(vertice)
    ady_conectados = 0
    if len(adyacentes) < MINIMOS_ADYACENTES:
        return 0
    for i in range(len(adyacentes)):
        for j in range(len(adyacentes)):
            if j == i:
                continue
            if grafo.estan_unidos(adyacentes[i], adyacentes[j]):
                ady_conectados += 1
    return ady_conectados / (len(adyacentes) * (len(adyacentes) - 1))


def pagerank(grafo):
    d = 0.85
    pagerank_elementos = {}
    largo = len(grafo)
    constante_pr = (1 - d) / largo
    for v in grafo:
        pagerank_elementos[v] = constante_pr
    aristas_entrada = obtener_aristas_entrada(grafo)
    grados_salida = obtener_grados_salida(grafo)
    for i in range(K_PAGERANK):
        for v in grafo:
            suma = 0
            for w in aristas_entrada[v]:
                suma += pagerank_elementos[w] / grados_salida[w]
            pagerank_elementos[v] = constante_pr + suma * d
    array_clave_valor = []
    for clave, valor in pagerank_elementos.items():
        array_clave_valor.append((-valor, clave))
    heapq.heapify(array_clave_valor)
    return array_clave_valor


def obtener_grados_salida(grafo):
    grados = {}
    for v in grafo:
        grados[v] = len(grafo.adyacentes(v))
    return grados
