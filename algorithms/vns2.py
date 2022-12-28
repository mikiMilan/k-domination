from time import time
from random import shuffle
from math import sqrt
from networkx import \
    DiGraph, \
    Graph, \
    gnp_random_graph as rand_graph, \
    is_connected
from beamSearchHeuristic import objective_function, found_d


def add_in_s(s, complemant, s_len):
    obj = objective_function(s)

    i = 0
    while len(s) < s_len and i < s_len:
        rand_node_out = complemant[0]
        del complemant[0]

        s.insert(0, rand_node_out)
        obj_new = objective_function(s)
        if obj_new < obj:
            # print("Element ", s[0], " nije ubacen")
            del s[0]
            complemant.append(rand_node_out)
        else:
            obj = obj_new

        i += 1


def vns(graph: DiGraph or Graph, k: int) -> list:
    # s_len: int = int(sqrt(len(graph)))
    s_len: int = int(len(graph)/7)

    nodes = list(graph.nodes)
    shuffle(nodes)
    s = nodes[:s_len]
    s_complement = nodes[s_len:]
    print(s)

    iteration = 0
    iteration_max = 500
    start_time = time()
    objective_function.graph = graph
    objective_function.k = k

    s_opt = nodes
    while iteration < iteration_max and time()-start_time < 200 and len(s_complement) > 0:

        # nakon sto su svi elementi 'popravljeni' u @s, @s pretumbavamo
        if (iteration+1) % (s_len*2) == 0:
            # print("Skoro savrseno s: ", s)
            # -1- opcija - pokusamo da dodamo nesto novo
            # skoro nikakvi rezultati
            # add_in_s(s, s_complement, s_len)
            # -2- opcija - uzimamo novi komad iz s_complement
            # s = s_complement[:s_len]
            # s_complement = s_complement[s_len:]
            # -3- opcija - ciklicki pomjeramo inicijalni s
            obilazak = int((iteration+1) / s_len)
            s = nodes[:s_len]
            l1 = s[obilazak:]
            l2 = s[:obilazak]
            s = l1+l2
            # print("novo s: ", s)

        obj = objective_function(s)
        # print("Obj: ", obj, " od ", s)

        # -- uklanjamo prvi ili mjenjemo sa nekim njegovim susjedom ako je to bolje
        rand_node_in = s[0]
        del s[0]
        obj_rem = objective_function(s)

        node_new = -1
        for v in set(graph[rand_node_in]):
            s.append(v)
            obj_new = objective_function(s)
            if obj_new > obj:
                obj_rem = obj_new
                node_new = v
            s.pop()

        # nisu dobra poredjenja
        if obj > obj_rem:
            s.append(rand_node_in)
        elif obj < obj_rem and node_new != -1:
            s.append(node_new)

        # -- uklanjamo prvi ili mjenjemo sa nekim njegovim susjedom ako je to bolje - end

        # print(s)

        if found_d(graph, s, k) and len(s_opt) > len(s):
            print("Pronadjen!!!!!!!!!")
            obj = objective_function(s)
            print("Obj: ", obj, " od ", s)
            s_opt = list(s)

        iteration += 1
    return s_opt


if __name__ == '__main__':
    g = rand_graph(800, 0.2, seed=1)
    print("Connected: {}".format(is_connected(g)))
    curr = time()
    d1 = vns(g, 1)
    time_execute = time() - curr
    print(time_execute, d1)
