from time import time
from random import shuffle, random
from math import sqrt
from networkx import DiGraph, Graph, gnp_random_graph as rand_graph
from unit import fitness, is_acceptable_solution, fitness_rec_rem, fitness_rec_add
from read_graph import read_graph


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
    iteration_max = 999900 #3900
    start_time = time()
    time_execution = 3600 # 3600 #sec
    best_time = 0
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
                print("Pronadjen!!!!!!!!! Vrijeme: ", time() - start_time)
                print("Fit: ", fit, "velicina dominacije ", len(s))
                s_accept = list(s)
                best_time = time() - start_time
        else:
            div += 1
            if div >= divmax:
                div = divmin

        iteration += 1
    return s_accept, best_time


if __name__ == '__main__':
    g = read_graph("cities_small_instances/bath.txt")

    print("The graph has been loaded!!!")

    curr = time()
    d1, bt = vns(g, 2, curr)
    time_execute = time() - curr

    print(len(d1), bt, time_execute)
