from time import time
from cplexKD import ILP
from read_graph import read_graph
from multiprocessing import Process, Manager
from math import ceil
from networkx import DiGraph, Graph


def task(fun, g: Graph or DiGraph, k: int, time_limit: float, r, i: str):
    curr = time()
    best_sol, best_bound, opt = fun(g, k, time_limit)
    time_execute = time() - curr
    r[i] = [best_sol, best_bound, opt, time_execute]


if __name__ == '__main__':
    time_limit = 3600.0
    # paralellism = 3
    #
    # city_instances = ['bath.txt', 'belfast.txt', 'brighton.txt', 'bristol.txt',
    #                   'cardiff.txt', 'coventry.txt', 'exeter.txt', 'glasgow.txt',
    #                   'leeds.txt', 'leicester.txt', 'liverpool.txt', 'manchester.txt',
    #                   'newcastle.txt', 'nottingham.txt', 'oxford.txt', 'plymouth.txt',
    #                   'sheffield.txt', 'southampton.txt', 'sunderland.txt', 'york.txt']
    # batches = ceil(len(city_instances) / paralellism)

    number_vertex = [200, 500, 1000, 2000]
    probability = [0.025, 0.05, 0.1, 0.2, 0.5, 0.8]
    number_graphs = 10

    for n in number_vertex:
        for k in [1, 2, 4]:
            for p in probability:
                for i in range(number_graphs):
                    instance = "NEW-V" + str(n) + "-P" + str(p) + "-G" + str(i) + ".txt"
                    graph_location = "random_instances/" + instance
                    file_name_res = 'results/CPLEX/random_instances/' + 'k' + str(k) + "-" + instance

                    print("Reading graph!")
                    g: Graph or DiGraph = read_graph(graph_location)
                    print("End: ", graph_location)

                    curr = time()
                    best_sol, best_bound, opt = ILP(g, k, time_limit)
                    time_execute = time() - curr

                    with open(file_name_res, 'a') as f:
                        f.write('{}, {}, {}, {}, {:.2f}\n'.format(instance,best_sol, best_bound, opt, time_execute))
                    print('{}, {}, {}, {}, {:.2f}\n'.format(instance, best_sol, best_bound, opt, time_execute))
