import heapq
import math
import time


# 1. MODELAGEM DO GRAFO (22 bairros de Joao Pessoa)

mapa = {
    # Zona Oeste
    "Roger":              {"Varadouro": 5, "Mandacaru": 8, "Funcionarios": 7},
    "Varadouro":          {"Roger": 5, "Centro": 4, "Mandacaru": 6, "Tambia": 5},
    "Funcionarios":       {"Roger": 7, "Centro": 5, "Agua Fria": 4},

    # Centro / Centro-Sul
    "Mandacaru":          {"Roger": 8, "Varadouro": 6, "Cristo": 4, "Jaguaribe": 5},
    "Centro":             {"Varadouro": 4, "Funcionarios": 5, "Tambia": 3, "Agua Fria": 4},
    "Agua Fria":          {"Funcionarios": 4, "Centro": 4, "Valentina": 4, "Mangabeira": 6},
    "Valentina":          {"Agua Fria": 4, "Mangabeira": 5},

    # Faixa Central
    "Cristo":             {"Mandacaru": 4, "Jaguaribe": 3, "Bairro dos Estados": 5},
    "Jaguaribe":          {"Mandacaru": 5, "Cristo": 3, "Torre": 3, "Tambia": 4},
    "Torre":              {"Jaguaribe": 3, "Tambia": 3, "Expedicionarios": 4},
    "Tambia":             {"Varadouro": 5, "Centro": 3, "Jaguaribe": 4, "Torre": 3, "Expedicionarios": 4},
    "Mangabeira":         {"Agua Fria": 6, "Valentina": 5, "Cabo Branco": 8},

    # Centro-Leste
    "Bairro dos Estados": {"Cristo": 5, "Bancarios": 4},
    "Expedicionarios":    {"Torre": 4, "Tambia": 4, "Miramar": 4, "Bancarios": 5},
    "Cabo Branco":        {"Mangabeira": 8, "Tambau": 5, "Altiplano": 4},

    # Zona Leste (Norte)
    "Miramar":            {"Expedicionarios": 4, "Bancarios": 3, "Aeroclube": 4},
    "Bancarios":          {"Bairro dos Estados": 4, "Expedicionarios": 5, "Miramar": 3, "Aeroclube": 3},

    # Zona Leste (Litoral)
    "Aeroclube":          {"Miramar": 4, "Bancarios": 3, "Manaira": 4},
    "Manaira":            {"Aeroclube": 4, "Tambau": 3, "Portal do Sol": 5},
    "Tambau":             {"Manaira": 3, "Cabo Branco": 5, "Altiplano": 4},
    "Altiplano":          {"Tambau": 4, "Cabo Branco": 4, "Portal do Sol": 3},
    "Portal do Sol":      {"Manaira": 5, "Altiplano": 3},
}

coordenadas = {
    "Roger":              (-6,  2),
    "Varadouro":          (-4,  1),
    "Funcionarios":       (-4, -2),
    "Mandacaru":          (-2,  4),
    "Centro":             (-2,  0),
    "Agua Fria":          (-2, -3),
    "Valentina":          (-1, -5),
    "Cristo":             ( 0,  5),
    "Jaguaribe":          ( 0,  3),
    "Torre":              ( 1,  2),
    "Tambia":             ( 0,  0),
    "Mangabeira":         ( 1, -4),
    "Bairro dos Estados": ( 3,  5),
    "Expedicionarios":    ( 3,  1),
    "Cabo Branco":        ( 4, -4),
    "Miramar":            ( 5,  2),
    "Bancarios":          ( 5,  4),
    "Aeroclube":          ( 7,  2),
    "Manaira":            ( 8,  1),
    "Tambau":             ( 8, -1),
    "Altiplano":          ( 9, -2),
    "Portal do Sol":      (10,  0),
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


# 3. ALGORITMO A* (A-ESTRELA)

def a_estrela(grafo, origem, destino):
    g_score = {n: float("inf") for n in grafo}
    g_score[origem] = 0
    anterior = {n: None for n in grafo}

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


# 4. APRESENTACAO DOS RESULTADOS

def mostrar_rota(nome_algoritmo, caminho, custo, nos_explorados, total_nos):
    print(f"\n  [{nome_algoritmo}]")
    print(f"    Caminho        : {' -> '.join(caminho)}")
    print(f"    Tempo          : {custo} min")
    print(f"    Nos explorados : {nos_explorados} / {total_nos}")


def comparar(grafo, origem, destino, titulo):
    total = len(grafo)
    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")
    print(f"  Origem : {origem}")
    print(f"  Destino: {destino}")
    print(f"  Total de nos no grafo: {total}")

    caminho_d, custo_d, exp_d = dijkstra(grafo, origem, destino)
    mostrar_rota("Dijkstra", caminho_d, custo_d, exp_d, total)

    caminho_a, custo_a, exp_a = a_estrela(grafo, origem, destino)
    mostrar_rota("A*      ", caminho_a, custo_a, exp_a, total)

    economia = exp_d - exp_a
    pct = (economia / exp_d * 100) if exp_d else 0
    print(f"\n  >> Mesmo caminho otimo? {'SIM' if caminho_d == caminho_a else 'NAO'} (custo: {custo_d} min)")
    print(f"  >> A* explorou {exp_a} nos, Dijkstra explorou {exp_d} nos.")
    print(f"  >> A* economizou {economia} exploracoes ({pct:.0f}% menos trabalho).")


# 5. EXECUCAO DA DEMO

if __name__ == "__main__":
    origem  = "Roger"
    destino = "Portal do Sol"

    comparar(mapa, origem, destino, "ROTA NORMAL (sem trafego)")

    print("\n\n... Acidente bloqueia a Av. Epitacio Pessoa (Tambia <-> Expedicionarios) ...")
    time.sleep(1)

    mapa["Tambia"]["Expedicionarios"] = 30
    mapa["Expedicionarios"]["Tambia"] = 30

    comparar(mapa, origem, destino, "ROTA RECALCULADA (apos acidente na arteria central)")
