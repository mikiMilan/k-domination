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
    city_instances_block = [['bath.txt', 'belfast.txt', 'brighton.txt', 'bristol.txt', 'cardiff.txt'], 
                             ['coventry.txt', 'exeter.txt', 'glasgow.txt', 'leeds.txt', 'leicester.txt'], 
                             ['liverpool.txt', 'manchester.txt', 'newcastle.txt', 'nottingham.txt', 'oxford.txt'], 
                             ['plymouth.txt', 'sheffield.txt', 'southampton.txt', 'sunderland.txt', 'york.txt']]
    k=4
    file_name_res = '../results/ILP_city/k_' + str(k) + ".txt"


    for city_instances in city_instances_block:
        manager = Manager()
        return_dict = manager.dict()
        procs = []
        for i in range(len(city_instances)):
            graph_location = instance_dir + "/" + city_instances[i]
            print("Reading graph!")
            g: Graph or DiGraph = read_graph(graph_location)
            print("End: ", graph_location)
            
            print("Creating process: ", city_instances[i])
            p = Process(target=task, args=(g, k, time_limit, return_dict, city_instances[i], i))
            procs.append(p)

        for i in range(len(city_instances)):
            print("Starting process "+str(city_instances[i]))
            procs[i].start()
                            
        for i in range(len(city_instances)):
            procs[i].join()
            print("Process "+str(city_instances[i])+" finished")


        with open(file_name_res, 'a') as f:
            for i in range(len(city_instances)):
                instance = city_instances[i]
                f.write('{}, {}, {}, {}, {:.2f}\n'.format(instance, return_dict[i][0], return_dict[i][1], return_dict[i][2], return_dict[i][3]))
                print('{}, {}, {}, {}, {:.2f}\n'.format(instance, return_dict[i][0], return_dict[i][1], return_dict[i][2], return_dict[i][3]))
