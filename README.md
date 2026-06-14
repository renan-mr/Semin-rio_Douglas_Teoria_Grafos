# Seminário: Algoritmos de Roteamento — Dijkstra vs A*

Demo interativa desenvolvida para o seminário de Teoria dos Grafos, simulando como aplicativos como Waze e Google Maps calculam rotas mínimas em tempo real.

## Contexto

Imagine que somos a equipe de engenharia do Waze. O mapa da cidade possui milhares de cruzamentos (vértices) e ruas (arestas) com pesos diferentes representando o tempo estimado de percurso. Calcular a rota na força bruta — testando todos os caminhos possíveis — é computacionalmente inviável.

A solução é modelar a cidade como um **grafo ponderado** e aplicar algoritmos eficientes de caminho mínimo.

## Algoritmos Comparados

### Dijkstra
Explora o grafo em todas as direções igualmente, expandindo sempre o nó de menor custo acumulado. **Garante** o caminho ótimo, mas pode analisar muitos nós que claramente não levam ao destino.

### A* (A-Estrela)
Igual ao Dijkstra, porém usa uma **heurística** — a distância euclidiana até o destino — para priorizar nós que parecem estar na direção certa. Resultado: explora **menos nós** chegando ao mesmo caminho ótimo.

```
f(n) = g(n) + h(n)
       ↑        ↑
  custo real   estimativa até o destino
```

## O que a demo faz

1. Modela um pequeno bairro de João Pessoa como grafo (cruzamentos = nós), com coordenadas aproximadas para calcular a heurística do A*.
2. Implementa Dijkstra e A* do zero usando uma fila de prioridade (`heapq`).
3. Compara as duas rotas e o número de nós explorados por cada algoritmo.
4. Simula um acidente de trânsito (peso de aresta aumenta) e mostra o recálculo de rota em tempo real — a feature central do Waze.

## Grafo Modelado

```
Parque da Cidade ──3── Aeroclube ──4── Manaira
       │                   │               │
       6               6   └────5────  Bessa
       │                               │
    Cabo Branco ──4── Tambau ──7───────┘
```

Nós: Parque da Cidade, Aeroclube, Cabo Branco, Manaira, Tambau, Bessa

## Como Executar

```bash
python demo_rotas.py
```

Exemplo de saída:

```
=== ANTES DO TRANSITO (rota normal) ===
Origem : Parque da Cidade
Destino: Cabo Branco

[Dijkstra]
  Caminho        : Parque da Cidade -> Aeroclube -> Manaira -> Tambau -> Cabo Branco
  Tempo          : 13 min
  Nos explorados : 5 / 6

[A*]
  Caminho        : Parque da Cidade -> Aeroclube -> Manaira -> Tambau -> Cabo Branco
  Tempo          : 13 min
  Nos explorados : 4 / 6

  -> Mesmo caminho otimo? SIM (tempo 13 min em ambos)
  -> A* explorou 4 nos contra 5 do Dijkstra (menos trabalho).

... 5 minutos depois: acidente bloqueia a Av. Beira Rio ...

=== DEPOIS DO TRANSITO (rota recalculada) ===
...
```

## Requisitos

- Python 3.8+
- Sem dependências externas (usa apenas `heapq`, `math` e `time` da stdlib)

## Conceitos de Teoria dos Grafos Envolvidos

| Conceito | Aplicação |
|---|---|
| Grafo ponderado | Ruas com tempos diferentes |
| Vértice / nó | Cruzamentos do bairro |
| Aresta bidirecional | Ruas de mão dupla |
| Caminho mínimo | Rota mais rápida |
| Fila de prioridade (heap) | Núcleo dos dois algoritmos |
| Heurística admissível | Distância euclidiana no A* |
