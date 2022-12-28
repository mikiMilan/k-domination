# import matplotlib.pyplot as plt
from time import time
from networkx import \
    DiGraph, \
    Graph, \
    gnp_random_graph as rand_graph, \
    is_connected, \
    draw_networkx








def found_u(graph: DiGraph or Graph, D: list, k: int) -> int:
    node = -1
    valmax = 0

    for u in graph.nodes:
        if u not in D:
            sumU = 0
            D.append(u)
            for v in graph.nodes:
                if v != u and v not in D:
                    neighborsV = set(graph[v])
                    sumU += min(k, number_same_elements(neighborsV, D))
            D.pop()

            if sumU > valmax:
                valmax = sumU
                node = u

    return node


def greedy(graph: DiGraph or Graph, k: int) -> list:
    D = list()
    while not found_d(graph, D, k):
        # print("I am looking for a node...")
        node = found_u(graph, D, k)
        D.append(node)
        # print("Append {} in D".format(node))
    return D


if __name__ == '__main__':
    g = rand_graph(200, 0.2, seed=1)
    print("Connected: {}".format(is_connected(g)))
    curr = time()
    d1 = greedy(g, 1)
    time_execute = time() - curr
    print(time_execute, d1)
    #
    # curr = time()
    # d2 = greedy(g, 2)
    # time_execute = time() - curr
    # print(time_execute, d2)

    # curr = time()
    # d3 = greedy(g, 4)
    # time_execute = time() - curr
    # print(time_execute, d3)

    # draw_networkx(g)
    # plt.show()


