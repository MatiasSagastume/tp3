from collections import deque

funciones_implementadas = {"camino": 1, "conectados": 1, "comunidad": 1, "rango": 1,
                           "lectura": 1, "diametro": 1, "navegacion": 1, "clustering": 1}

REPETICIONES_LABEL_PROPAGATION = 3
REPETICIONES_NAVEGACION = 21
MINIMOS_ADYACENTES = 2
POS_ACTUAL = 0


def listar_operaciones():
    for f in funciones_implementadas.keys():
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
        lista = arr_cfcs[0]
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
    vertices = set(vertices)
    visitados = set()
    res = []
    for v in vertices:
        if v not in visitados:
            hay_ciclo = lectura_(grafo, v, vertices, visitados, set(), res)
            if hay_ciclo:
                return None
    return res


def lectura_(grafo, v, vertices, visitados, visitados_actuales, res):
    visitados.add(v)
    visitados_actuales.add(v)
    for w in grafo.adyacentes(v):
        if w in vertices:
            if w in visitados_actuales:
                return True
            if w in visitados:
                continue
            ciclo = lectura_(grafo, w, vertices, visitados, visitados_actuales, res)
            if ciclo:
                return True
    res.append(v)
    return False
def comunidad(grafo, origen):
    label = {}
    i = 0
    for v in grafo:
        label[v] = i
        i += 1
    aristas_entrada = obtener_aristas_entrada(grafo)
    grupo = []
    for i in range(REPETICIONES_LABEL_PROPAGATION):
        bfs_comunidad(grafo, origen, aristas_entrada, label)
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


def bfs_comunidad(grafo, origen, aristas, label):
    visitados = set()
    visitados.add(origen)
    cola = deque()
    cola.append(origen)
    while cola:
        v = cola.popleft()
        label[v] = max_freq(label, aristas[v])
        for w in grafo.adyacentes(v):
            if w not in visitados:
                cola.append(w)
                visitados.add(w)


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
    if pagina != None:
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
            if j != i:
                if grafo.estan_unidos(adyacentes[i], adyacentes[j]):
                    ady_conectados += 1
    return ady_conectados / (len(adyacentes) * (len(adyacentes) - 1))
