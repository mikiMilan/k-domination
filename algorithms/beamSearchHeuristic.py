from time import time
from networkx import DiGraph, Graph, gnp_random_graph as rand_graph
from unit import is_acceptable_solution, objective_function
import pickle


def get_0(s: tuple) -> int:
    return s[0]


def remove_duplication(s: list):
    for i in range(len(s)-1, 0, -1):
        for j in range(0, i):
            if s[i][0] == s[j][0] and s[i][1] == s[j][1]:
                del s[i]
                break


def beam_search_heuristic(graph: DiGraph or Graph, k: int, b: int) -> list:
    d = []
    s = [(0, set())]

    while not d:
        s_prim = []

        for parcial_s in s:
            for v in graph.nodes:
                if v not in parcial_s[1]:
                    new_s = set(parcial_s[1])
                    new_s.add(v)
                    s_prim.append((objective_function(list(new_s), graph, k), new_s))

        s = s_prim
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
    f = open("cities_small_instances/bath_pickle", "rb")
    st_obj = pickle.load(f)
    print(st_obj)


    # curr = time()
    # d1 = beam_search_heuristic(g, 1, b=4)
    # time_execute = time() - curr
    #
    # print(len(d1), time_execute)
