from time import time
from random import randint, choice, shuffle
from math import sqrt
from networkx import \
    DiGraph, \
    Graph, \
    gnp_random_graph as rand_graph, \
    is_connected
from beamSearchHeuristic import objective_function, found_d


def vns(graph: DiGraph or Graph, k: int) -> list:
    s_len: int = int(sqrt(len(graph)))

    nodes = list(graph.nodes)
    shuffle(nodes)
    s = nodes[:s_len]
    s_complement = nodes[s_len:]

    for i in s_complement:
        if len(list(graph[i])) < k:
            s.append(i)

    iteration = 0
    iteration_max = 100
    start_time = time()
    objective_function.graph = graph
    objective_function.k = k

    s_opt = nodes
    while iteration < iteration_max and time()-start_time < 60 and len(s_complement)>0:

        obj = objective_function(s)

        # -- ubacujemo novi cvor ako poboljsavamo rjesenje
        rand_node_out = s_complement[0]
        del s_complement[0]

        s.append(rand_node_out)
        obj_new = objective_function(s)
        if obj_new < obj:
            s.pop()
            s_complement.append(rand_node_out)
        else:
            obj = obj_new
        # ubacujemo novi cvor ako poboljsavamo rjesenje - end

        # -- uklanjamo prvi ili mjenjemo sa nekim njegovim susjedom ako je to bolje
        rand_node_in = s[0]
        del s[0]

        obj_new = objective_function(s)

        node_new = -1
        for v in set(graph[rand_node_in]):
            s.append(v)
            obj_new2 = objective_function(s)
            if obj_new2 > obj_new:
                obj_new = obj_new2
                node_new = v
            s.pop()

        if obj > obj_new:
            s.append(rand_node_in)
        elif obj < obj_new and node_new != -1:
            s.append(node_new)

        # -- uklanjamo prvi ili mjenjemo sa nekim njegovim susjedom ako je to bolje - end

        print(s)

        if found_d(graph, s, k) and len(s_opt) >= len(s):
            print("Pronadjen!!!")
            s_opt = list(s)

        iteration += 1
    return s_opt


if __name__ == '__main__':
    g = rand_graph(200, 0.2, seed=1)
    print("Connected: {}".format(is_connected(g)))
    curr = time()
    d1 = vns(g, 1)
    time_execute = time() - curr
    print(time_execute, d1)
