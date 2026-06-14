
import heapq
import math
import time



# 1. MODELAGEM DO GRAFO

mapa = {
    "Parque da Cidade": {"Aeroclube": 3, "Cabo Branco": 6},
    "Aeroclube": {"Parque da Cidade": 3, "Manaira": 4, "Bessa": 6},
    "Manaira": {"Aeroclube": 4, "Tambau": 2, "Bessa": 5},
    "Bessa": {"Aeroclube": 6, "Manaira": 5, "Tambau": 7},
    "Tambau": {"Manaira": 2, "Cabo Branco": 4, "Bessa": 7},
    "Cabo Branco": {"Tambau": 4, "Parque da Cidade": 6},
}


coordenadas = {
    "Parque da Cidade": (0, 0),
    "Aeroclube": (3, 1),
    "Cabo Branco": (3, -3),
    "Manaira": (6, 1.5),
    "Tambau": (6, -2),
    "Bessa": (4.5, -4.5),
}


def heuristica(a, b):

    ax, ay = coordenadas[a]
    bx, by = coordenadas[b]
    return math.dist((ax, ay), (bx, by))



# 2. ALGORITMO DE DIJKSTRA

def dijkstra(grafo, origem, destino):
    distancia = {n: float("inf") for n in grafo}
    distancia[origem] = 0
    anterior = {n: None for n in grafo}

    fila = [(0, origem)]
    visitados = set()
    nos_explorados = 0

    while fila:
        custo_atual, no_atual = heapq.heappop(fila)

        if no_atual in visitados:
            continue
        visitados.add(no_atual)
        nos_explorados += 1

        if no_atual == destino:
            break

        for vizinho, peso in grafo[no_atual].items():
            novo_custo = custo_atual + peso
            if novo_custo < distancia[vizinho]:
                distancia[vizinho] = novo_custo
                anterior[vizinho] = no_atual
                heapq.heappush(fila, (novo_custo, vizinho))

    return _reconstruir_caminho(anterior, destino), distancia[destino], nos_explorados



# ALGORITMO A* (A-ESTRELA)

def a_estrela(grafo, origem, destino):
    g_score = {n: float("inf") for n in grafo}
    g_score[origem] = 0
    anterior = {n: None for n in grafo}

    # fila guarda (f_score, nó); f_score = g + h
    fila = [(heuristica(origem, destino), origem)]
    visitados = set()
    nos_explorados = 0

    while fila:
        _, no_atual = heapq.heappop(fila)

        if no_atual in visitados:
            continue
        visitados.add(no_atual)
        nos_explorados += 1

        if no_atual == destino:
            break

        for vizinho, peso in grafo[no_atual].items():
            novo_g = g_score[no_atual] + peso
            if novo_g < g_score[vizinho]:
                g_score[vizinho] = novo_g
                anterior[vizinho] = no_atual
                f_score = novo_g + heuristica(vizinho, destino)
                heapq.heappush(fila, (f_score, vizinho))

    return _reconstruir_caminho(anterior, destino), g_score[destino], nos_explorados


def _reconstruir_caminho(anterior, destino):
    caminho = []
    no = destino
    while no is not None:
        caminho.append(no)
        no = anterior[no]
    caminho.reverse()
    return caminho


# ---------------------------------------------------------------
# 4. FUNÇÕES DE APRESENTAÇÃO DO RESULTADO
# ---------------------------------------------------------------
def mostrar_rota(nome_algoritmo, caminho, custo, nos_explorados):
    print(f"\n[{nome_algoritmo}]")
    print(f"  Caminho        : {' -> '.join(caminho)}")
    print(f"  Tempo          : {custo} min")
    print(f"  Nos explorados : {nos_explorados} / {len(mapa)}")


def comparar(grafo, origem, destino, titulo):
    print(f"\n=== {titulo} ===")
    print(f"Origem : {origem}")
    print(f"Destino: {destino}")

    caminho_d, custo_d, exp_d = dijkstra(grafo, origem, destino)
    mostrar_rota("Dijkstra", caminho_d, custo_d, exp_d)

    caminho_a, custo_a, exp_a = a_estrela(grafo, origem, destino)
    mostrar_rota("A*", caminho_a, custo_a, exp_a)

    print(
        f"\n  -> Mesmo caminho otimo? "
        f"{'SIM' if caminho_d == caminho_a else 'NAO'} "
        f"(tempo {custo_d} min em ambos)"
    )
    print(
        f"  -> A* explorou {exp_a} nos contra {exp_d} do Dijkstra "
        f"({'menos' if exp_a < exp_d else 'igual/mais'} trabalho)."
    )


# ---------------------------------------------------------------
# 5. EXECUÇÃO DA DEMO
# ---------------------------------------------------------------
if __name__ == "__main__":
    origem = "Parque da Cidade"
    destino = "Cabo Branco"

    comparar(mapa, origem, destino, "ANTES DO TRANSITO (rota normal)")

    print("\n... 5 minutos depois: acidente bloqueia a Av. Beira Rio (Parque da Cidade -> Cabo Branco) ...")
    time.sleep(1)

    # Simula transito: 
    mapa["Parque da Cidade"]["Cabo Branco"] = 25
    mapa["Cabo Branco"]["Parque da Cidade"] = 25

    comparar(mapa, origem, destino, "DEPOIS DO TRANSITO (rota recalculada)")