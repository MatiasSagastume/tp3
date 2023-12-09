import sys
from grafo import Grafo
from biblioteca import *

RUTA_ARCHIVO = 1
VERTICE = 0
ADYACENTES = 1
CANT_PARAMETROS = 2
SEPARADOR = "\t"
FIN_DE_LINEA = "\n"
SEPARADOR_COMANDO = " "
SEPARADOR_PARAMETROS = ","
COMANDO = 0
PARAMETROS_INPUT = 1
TIENE_PARAMETROS = 1
FLECHAS_CAMINO = " -> "
UNION_CONECTADOS = ", "
CAMINO = "camino"
CONECTADOS= "conectados"
COMUNIDAD = "comunidad"
RANGO = "rango"
LECTURA = "lectura"
DIAMETRO = "diametro"
NAVEGACION = "navegacion"
CLUSTERING = "clustering"
LARGO_CAMINO = 2
LARGO_CONECTADOS = 1
LARGO_COMUNIDAD = 1
LARGO_RANGO = 2
LARGO_MINIMO_LECTURA = 1
LARGO_DIAMETRO = 0
LARGO_NAVEGACION = 1
LARGO_MAX_CLUSTERING = 1
POS_VERTICE = 0

sys.setrecursionlimit(75000)


def main():
    if len(sys.argv) != CANT_PARAMETROS:
        raise Exception("Error: Parametros Incorrectos")
    ruta = sys.argv[RUTA_ARCHIVO]
    grafo = Grafo(es_dirigido=True)
    arr_cfcs = []
    dict_cfcs = {}
    with open(ruta) as arch:
        for linea in arch:
            palabras = linea.rstrip(FIN_DE_LINEA)
            palabras = palabras.split(SEPARADOR)
            v = palabras[VERTICE]
            grafo.agregar_vertice(v)
            adyacentes = palabras[ADYACENTES:]
            for w in adyacentes:
                grafo.agregar_arista(v, w)
    while True:
        entrada = input()
        entrada = entrada.split(SEPARADOR_COMANDO)
        procesar_entrada(grafo, entrada, arr_cfcs, dict_cfcs)


def procesar_entrada(grafo, entrada, arr_cfcs, dict_cfcs):
    comando = entrada[COMANDO]
    parametros = []
    if len(entrada) > TIENE_PARAMETROS:
        parametros = SEPARADOR_COMANDO.join(entrada[PARAMETROS_INPUT:]).split(SEPARADOR_PARAMETROS)
    if comando == CAMINO:
        funcion_camino(grafo, parametros)
    elif comando == CONECTADOS:
        funcion_conectados(grafo, parametros, arr_cfcs, dict_cfcs)
    elif comando == COMUNIDAD:
        funcion_comunidad(grafo, parametros)
    elif comando == RANGO:
        funcion_rango(grafo, parametros)
    elif comando == LECTURA:
        funcion_lectura(grafo, parametros)
    elif comando == DIAMETRO:
        funcion_diametro(grafo, parametros)
    elif comando == NAVEGACION:
        funcion_navegacion(grafo, parametros)
    elif comando == CLUSTERING:
        funcion_clustering(grafo, parametros)
    else:
        print(f"{comando}: la opcion ingresada es invalida")


def funcion_camino(grafo, parametros):
    if len(parametros) != LARGO_CAMINO:
        print("Error: los parametros ingresados son invalidos")
        return
    a, b = parametros
    if a not in grafo or b not in grafo:
        print("Error: paginas invalidas")
        return
    res = camino(grafo, a, b)
    if not res:
        print("No se encontro recorrido")
        return
    costo = len(res) - 1
    print(FLECHAS_CAMINO.join(res))
    print(f"Costo: {costo}")


def funcion_conectados(grafo, parametros, arr_cfcs, dict_cfcs):
    if len(parametros) != LARGO_CONECTADOS:
        print("Error: los parametros ingresados son invalidos")
        return
    v = parametros[POS_VERTICE]
    if v not in grafo:
        print("Error: pagina invalida")
        return'lectura'
    if v not in dict_cfcs:
        conectados(grafo, v, arr_cfcs, dict_cfcs)
    print(UNION_CONECTADOS.join(arr_cfcs[dict_cfcs[v]]))


def funcion_comunidad(grafo, parametros):
    if len(parametros) != LARGO_COMUNIDAD:
        print("Error: Los parametros ingresados son invalidos")
        return
    v = parametros[POS_VERTICE]
    if v not in grafo:
        print("Error: pagina invalida")
        return
    res = comunidad(grafo, v)
    print(UNION_CONECTADOS.join(res))


def funcion_rango(grafo, parametros):
    if len(parametros) != LARGO_RANGO:
        print("Error: Los parametros ingresados son invalidos")
        return
    pagina, n = parametros
    if pagina not in grafo or not n.isdigit():
        print("Error: Los parametros ingresados son invalidos")
        return
    print(rango(grafo, pagina, int(n)))


def funcion_lectura(grafo, parametros):
    if len(parametros) < LARGO_MINIMO_LECTURA:
        print("Error: Los parametros ingresados son invalidos")
        return
    for v in parametros:
        if v not in grafo:
            print("Error: Los parametros ingresados son invalidos")
            return
    res = lectura(grafo, parametros)
    if not res:
        print("No existe forma de leer las paginas en orden")
        return
    print(UNION_CONECTADOS.join(res))


def funcion_diametro(grafo, parametros):
    if len(parametros) != LARGO_DIAMETRO:
        print("Error: los parametros ingresados son invalidos")
        return
    res = diametro(grafo)
    costo = len(res) - 1
    print(FLECHAS_CAMINO.join(res))
    print(f"Costo: {costo}")


def funcion_navegacion(grafo, parametros):
    if len(parametros) != LARGO_NAVEGACION:
        print("Error: Los parametros ingresados son invalidos")
        return
    v = parametros[POS_VERTICE]
    if v not in grafo:
        print("Error: pagina invalida")
    res = navegacion(grafo, v)
    print(FLECHAS_CAMINO.join(res))


def funcion_clustering(grafo, parametros):
    if len(parametros) > LARGO_MAX_CLUSTERING:
        print("Error: Los parametros ingresados son invalidos")
        return
    v = None
    if len(parametros) > 0:
        v = parametros[POS_VERTICE]
    print(f"{clustering(grafo, v):.3f}")


main()
