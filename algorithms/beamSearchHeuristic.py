from time import time
from networkx import \
    DiGraph, \
    Graph, \
    gnp_random_graph as rand_graph, \
    is_connected
from greedy import found_d
from random import shuffle
from math import sqrt
from unit import number_same_elements


def eqauls(l1, l2):

    if len(l1) != len(l2):
        return False

    for i in range(0, len(l1)):
        if l1[i] != l2[i]:
            return False

    return True


def remove_duplication(s):
    for i in range(len(s)-1, 0, -1):
        for j in range(0, i):
            if eqauls(s[i], s[j]):
                # print(s[i], s[j])
                del s[i]
                break


def beam_search_heuristic(graph: DiGraph or Graph, k: int) -> list:
    # b = len(graph)/2
    b = int(sqrt(len(graph)))
    # print(b)

    objective_function.graph = graph
    objective_function.k = k

    d = []
    s = [[]]

    while not d:
        s_prim = []

        # print("Kreiram s prim")
        rand_node = list(graph.nodes)
        shuffle(rand_node)
        for parcial_s in s:
            # last_element = parcial_s[-1] if len(parcial_s) > 0 else -1
            for v in rand_node:
                if v not in parcial_s:
                    new_s = list(parcial_s)
                    new_s.append(v)
                    new_s.sort()
                    s_prim.append(new_s)

        remove_duplication(s)
        print(s)
        print("Sredjujem s")
        s = s_prim
        # print(s)
        s.sort(key=objective_function, reverse=True)
        # print(s)

        while len(s) > b:
            s.pop()
        # print(s)

        for parcial_s in s:
            if found_d(graph, parcial_s, k):
                d = parcial_s

    return d


if __name__ == '__main__':
    n = 200
    g = rand_graph(n, 0.2, seed=1)
    print("Connected: {}".format(is_connected(g)))
    curr = time()
    d1 = beam_search_heuristic(g, 1)
    time_execute = time() - curr
    print(time_execute, d1)
