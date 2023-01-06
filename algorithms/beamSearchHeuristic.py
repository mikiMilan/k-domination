from time import time
from networkx import DiGraph, Graph, gnp_random_graph as rand_graph
from unit import is_acceptable_solution, objective_function, number_same_elements
from read_graph import read_graph
from random import shuffle


def get_0(s: tuple) -> int:
    return s[0]


def remove_duplication(s: list):
    for i in range(len(s)-1, 0, -1):
        for j in range(0, i):
            if s[i][0] == s[j][0] and s[i][1] == s[j][1]:
                del s[i]
                break


def obj_rec_add(s: set, v: int, obj: int, g: Graph or DiGraph, k: int) -> float:
    """

    :rtype: object
    """
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
    s = [(0, set())]

    nodes = list(graph.nodes)
    while not d:
        s_prim = []

        shuffle(nodes)
        for parcial_s in s:
            for v in nodes:
                if v not in parcial_s[1]:
                    new_s = set(parcial_s[1])
                    new_rec_obj = obj_rec_add(parcial_s[1], v, parcial_s[0], graph, k)
                    new_s.add(v)
                    # new_obj = objective_function(list(new_s), graph, k)
                    s_prim.append((new_rec_obj, new_s))

        s = s_prim
        print("Current len: ", len(s[0][1]))
        remove_duplication(s)
        s.sort(key=get_0, reverse=True)

        while len(s) > b:
            s.pop()
        # print(s)

        for parcial_s in s:
            if is_acceptable_solution(graph, list(parcial_s[1]), k):
                d = parcial_s[1]

    return d


if __name__ == '__main__':
    # n = 300
    # g = rand_graph(n, 0.2, seed=2)
    g = read_graph("cities_small_instances/bath.txt")

    print("The graph has been loaded!!!")

    for i in range(10):
        curr = time()
        d1 = beam_search_heuristic(g, 2, b=1)
        time_execute = time() - curr

        print(len(d1), time_execute)
