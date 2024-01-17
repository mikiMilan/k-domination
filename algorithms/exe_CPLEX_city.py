from time import time
from cplexKD import ILP
from read_graph import read_graph
from multiprocessing import Process, Manager
from math import ceil
from networkx import DiGraph, Graph

def task(g: Graph or DiGraph, k: int, time_limit: float, r, i: str, ind:int):
    curr = time()
    best_sol, best_bound, opt = ILP(g, k, time_limit, ind)
    time_execute = time() - curr
    r[ind] = [best_sol, best_bound, opt, time_execute]

if __name__ == '__main__':
    time_limit = 1800.0
    instance_dir = '../instances/cities_small_instances'
    city_instances = ['bath.txt', 'belfast.txt', 'brighton.txt', 'bristol.txt',
                      'cardiff.txt', 'coventry.txt', 'exeter.txt', 'glasgow.txt',
                      'leeds.txt', 'leicester.txt', 'liverpool.txt', 'manchester.txt',
                      'newcastle.txt', 'nottingham.txt', 'oxford.txt', 'plymouth.txt',
                      'sheffield.txt', 'southampton.txt', 'sunderland.txt', 'york.txt']


    for city in city_instances:
        graph_location = instance_dir + "/" + city
        print("Reading graph!")
        g: Graph or DiGraph = read_graph(graph_location)
        print("End: ", graph_location)
        manager = Manager()
        return_dict = manager.dict()
        procs = []
        k_range = [7,10,11,16]

        for k in range(len(k_range)):
            print("Creating process: ", k_range[k])
            p = Process(target=task, args=(g, k_range[k], time_limit, return_dict, city, k))
            procs.append(p)

        for k in range(len(k_range)):
            print("Starting process "+str(k_range[k]))
            procs[k].start()
                        
        for k in range(len(k_range)):
            procs[k].join()
            print("Process "+str(k)+" finished")

        for k in range(len(k_range)):
            file_name_res = '../results/ILPvsVNS_city/ILP/k_' + str(k_range[k]) + ".txt"
            with open(file_name_res, 'a') as f:
                instance = city
                f.write('{}, {}, {}, {}, {:.2f}\n'.format(instance, return_dict[k][0], return_dict[k][1], return_dict[k][2], return_dict[k][3]))
                print('{}, {}, {}, {}, {:.2f}\n'.format(instance, return_dict[k][0], return_dict[k][1], return_dict[k][2], return_dict[k][3]))
