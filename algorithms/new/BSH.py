from time import time
from networkx import DiGraph, Graph
from unit import is_acceptable_solution, number_same_elements
from read_graph import read_graph
from random import shuffle


def get_0(s: tuple) -> int:
    return s[0]


def obj_rec_add(s: frozenset, v: int, obj: int, g: Graph or DiGraph, k: int) -> int:
    neighbors = set(g[v])
    nse = number_same_elements(neighbors, s)
    obj -= min(k, nse)

    obj_neg: int = 0

    for u in g[v]:
        if u not in s:
            neighbors = set(g[u])
            nse = number_same_elements(neighbors, s)
            obj_neg += min(k, nse)
    obj -= obj_neg

    srem = list(s)
    srem.append(v)
    srem = set(srem)
    obj_neg = 0

    for u in g[v]:
        if u not in srem:
            neighbors = set(g[u])
            nse = number_same_elements(neighbors, srem)
            obj_neg += min(k, nse)
    obj += obj_neg

    return obj


def beam_search_heuristic(graph: DiGraph or Graph, k: int, b: int) -> list:
    d = []
    s = {(0, frozenset({}))}

    nodes = list(graph.nodes)
    while not d:
        s_prim = set()

        # shuffle(nodes)
        for parcial_s in s:
            for v in nodes:
                if v not in parcial_s[1]:
                    new_s = set(parcial_s[1])
                    new_rec_obj = obj_rec_add(parcial_s[1], v, parcial_s[0], graph, k)
                    new_s.add(v)
                    # new_obj = objective_function(list(new_s), graph, k)
                    if b > 1 and parcial_s[0] <= new_rec_obj:
                        s_prim.add((new_rec_obj, frozenset(new_s)))
                    else:
                        s_prim.add((new_rec_obj, frozenset(new_s)))

        s = s_prim
        l = list(s)
        shuffle(l)
        l.sort(key=get_0, reverse=True)
        l = l[:b]
        s = set(l)

        for parcial_s in s:
            if is_acceptable_solution(graph, list(parcial_s[1]), k):
                d = parcial_s[1]

    return d


if __name__ == '__main__':
    # n = 300
    # g = rand_graph(n, 0.2, seed=2)
    g = read_graph("cities_small_instances/belfast.txt")

    print("The graph has been loaded!!!")

    for i in range(1):
        curr = time()
        d1 = beam_search_heuristic(g, 4, b=4)
        time_execute = time() - curr

        print(len(d1), time_execute)
