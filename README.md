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

1. Modela **22 bairros de João Pessoa** como grafo (cruzamentos = nós), com coordenadas geográficas aproximadas para calcular a heurística do A*.
2. Implementa Dijkstra e A* do zero usando uma fila de prioridade (`heapq`).
3. Compara as duas rotas e o número de nós explorados por cada algoritmo.
4. Simula um acidente de trânsito (peso de aresta aumenta) e mostra o recálculo de rota em tempo real — a feature central do Waze.

## Grafo Modelado

22 bairros de João Pessoa, organizados de oeste a leste:

```
[OESTE]                    [CENTRO]                        [LESTE]

Mandacaru── Cristo ── Bairro dos Estados
    │           │              │
Roger ── Varadouro ── Tambia ── Torre ── Expedicionarios ── Miramar ── Aeroclube ── Manaira ── Portal do Sol
    │           │         │                    │                │                       │
Funcionarios ── Centro ── Jaguaribe       Bancarios         Bancarios              Tambau ── Altiplano
    │           │
Agua Fria ── Valentina
    │
Mangabeira ── Cabo Branco
```

**Origem:** Roger (extremo oeste) → **Destino:** Portal do Sol (extremo leste)

A grande distância entre origem e destino, combinada com os bairros perpendiculares ao trajeto ótimo (norte/sul), é o que evidencia a superioridade do A*: enquanto Dijkstra explora praticamente todo o grafo, o A* descarta cedo os nós fora da direção do destino.

## Como Executar

```bash
python demo_rotas.py
```

Exemplo de saída:

```
============================================================
  ROTA NORMAL (sem trafego)
============================================================
  Origem : Roger
  Destino: Portal do Sol
  Total de nos no grafo: 22

  [Dijkstra]
    Caminho        : Roger -> Varadouro -> Tambia -> Expedicionarios -> Miramar -> Bancarios -> Aeroclube -> Manaira -> Portal do Sol
    Tempo          : 33 min
    Nos explorados : 18 / 22

  [A*      ]
    Caminho        : Roger -> Varadouro -> Tambia -> Expedicionarios -> Miramar -> Bancarios -> Aeroclube -> Manaira -> Portal do Sol
    Tempo          : 33 min
    Nos explorados : 10 / 22

  >> Mesmo caminho otimo? SIM (custo: 33 min)
  >> A* explorou 10 nos, Dijkstra explorou 18 nos.
  >> A* economizou 8 exploracoes (44% menos trabalho).
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
