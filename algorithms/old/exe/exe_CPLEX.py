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
    
    city_instances = ['belgrade.txt', 'berlin.txt', 
                      'boston.txt', 'dublin.txt',
                      'minsk.txt']


    for k in [2, 4]:
        for city in city_instances:
            instance = city
            graph_location = "cities_big_instances/" + instance
            file_name_res = 'results/CPLEX/cities_big_instances/' + 'k' + str(k) + ".txt"

            print("Reading graph!")
            g: Graph or DiGraph = read_graph(graph_location)
            print("End: ", graph_location)

            curr = time()
            best_sol, best_bound, opt = ILP(g, k, time_limit)
            time_execute = time() - curr

            with open(file_name_res, 'a') as f:
                f.write('{}, {}, {}, {}, {:.2f}\n'.format(instance,best_sol, best_bound, opt, time_execute))
            print('{}, {}, {}, {}, {:.2f}\n'.format(instance, best_sol, best_bound, opt, time_execute))
