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
    paralellism = 3
    time_limit = 3600.0

    city_instances = ['bath.txt', 'belfast.txt', 'brighton.txt', 'bristol.txt',
                      'cardiff.txt', 'coventry.txt', 'exeter.txt', 'glasgow.txt',
                      'leeds.txt', 'leicester.txt', 'liverpool.txt', 'manchester.txt',
                      'newcastle.txt', 'nottingham.txt', 'oxford.txt', 'plymouth.txt',
                      'sheffield.txt', 'southampton.txt', 'sunderland.txt', 'york.txt']
    batches = ceil(len(city_instances) / paralellism)

    for k in [4]:
        file_name_res = 'results/CPLEX/k' + str(k) + '.txt'
        times = []
        results = []
        manager = Manager()
        return_dict = manager.dict()
        procs = []

        for instance in city_instances:
            graph_open = 'cities_small_instances/' + instance
            print("Reading graph!")
            g: Graph or DiGraph = read_graph(graph_open)
            print("Creating process: ", graph_open)

            curr = time()
            best_sol, best_bound, opt = ILP(g, k, time_limit)
            time_execute = time() - curr

            with open(file_name_res, 'a') as f:
                f.write('{}, {}, {}, {}, {:.2f}\n'.format(instance,best_sol, best_bound, opt, time_execute))
            print('{}, {}, {}, {}, {:.2f}\n'.format(instance, best_sol, best_bound, opt, time_execute))
