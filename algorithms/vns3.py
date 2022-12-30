from time import time
from random import shuffle, random
from math import sqrt
from networkx import \
    DiGraph, \
    Graph, \
    gnp_random_graph as rand_graph, \
    is_connected
from unit import fitness, is_acceptable_solution, fitness_rec_rem, fitness_rec_add


def shaking(s: set, div: int, nodes: list) -> set:
    sl = list(s)
    shuffle(sl)
    shak = set(sl[:len(sl)-div])

    shuffle(nodes)
    shak.union(set(nodes[:div]))

    return shak


def random_nodes(g: Graph or DiGraph) -> set:
    s = set()

    for v in g.nodes:
        if random() < 0.5:
            s.add(v)

    return s


def local_search(s: set, g: Graph or DiGraph, nodes: list, k: int):
    improved = True
    curr_fit = fitness(s, g, k)

    while improved:
        improved = False

        shuffle(nodes)
        for v in nodes:
            if v in s:
                new_fit = fitness_rec_rem(s, v, curr_fit, g, k)
                if new_fit > curr_fit:
                    curr_fit = new_fit
                    s.remove(v)
                    improved = True
                    break
            else:
                new_fit = fitness_rec_add(s, v, curr_fit, g, k)
                if new_fit > curr_fit:
                    curr_fit = new_fit
                    s.add(v)
                    improved = True
                    break

    return curr_fit


def vns(graph: DiGraph or Graph, k: int) -> list:
    divmin = 1
    divmax = min(20, len(graph)/5)
    div = divmin
    iteration = 0
    iteration_max = 3900
    start_time = time()
    time_execution = 600 #sec
    nodes = list(graph.nodes) # kopiram cvorove zbog MJESANJA - necu da mjesam original

    s: set = random_nodes(graph)
    fit = fitness(s, graph, k)

    s_accept = set(graph.nodes)
    while iteration < iteration_max and time()-start_time < time_execution:
        s_new = shaking(s, div, nodes)
        fit_new = local_search(s_new, graph, nodes, k)

        if fit_new > fit:
            s = s_new
            div = divmin
            fit = fit_new

            # print("Fit: ", fit, "velicine ", len(s), " od ", s)
            if len(s_accept) > len(s) and is_acceptable_solution(graph, s, k):
                print("Pronadjen!!!!!!!!!")
                print("Fit: ", fit, "velicine ", len(s), " od ", s)
                s_accept = list(s)
        else:
            div += 1
            if div >= divmax:
                div = divmin

        iteration += 1
    return s_accept


if __name__ == '__main__':
    g = rand_graph(300, 0.2, seed=1)
    # for i in range(10):
    #     print(i, " - ", list(g[i]))
    print("Connected: {}".format(is_connected(g)))
    curr = time()
    d1 = vns(g, 3)
    time_execute = time() - curr
    print(time_execute, d1, len(d1))
