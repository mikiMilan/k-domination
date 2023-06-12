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
    r[i] = [best_sol, best_bound, opt, time_execute]


if __name__ == '__main__':
    time_limit = 1800.0
    
    number_vertex = [200, 500, 1000, 2000]
    probability = [0.025, 0.05, 0.1, 0.2, 0.5, 0.8]
    number_graphs = 10
    instance_dir = '../instances/random_instances'


    for k in [1, 2, 4]:
        file_name_res = '../results/CPLEX_random/random_' + 'k_' + str(k) + ".txt"
        for n in number_vertex:
            for gr in range(number_graphs):
                manager = Manager()
                return_dict = manager.dict()
                procs = []
                for pro in range(len(probability)):
                
                    instance = "NEW-V"+str(n)+"-P"+str(probability[pro])+"-G"+str(gr)+".txt"
                    graph_location = instance_dir + "/" + instance
                    print("Reading graph!")
                    g: Graph or DiGraph = read_graph(graph_location)
                    print("End: ", graph_location)
                    print("Creating process: ", probability[pro])
                    p = Process(target=task, args=(g, k, time_limit, return_dict, instance, pro))
                    procs.append(p)


                for pro in range(len(probability)):
                    print("Starting process "+str(pro) +". pro: "+str(probability[pro]))
                    procs[pro].start()
                                
                for pro in range(len(probability)):
                    procs[pro].join()
                    print("Process "+str(pro)+" finished")

                with open(file_name_res, 'a') as f:
                    for pro in range(len(probability)):
                        instance = "NEW-V"+str(n)+"-P"+str(probability[pro])+"-G"+str(gr)+".txt"
                        f.write('{}, {}, {}, {}, {:.2f}\n'.format(instance, return_dict[instance][0], return_dict[instance][1], return_dict[instance][2], return_dict[instance][3]))
                        print('{}, {}, {}, {}, {:.2f}\n'.format(instance, return_dict[instance][0], return_dict[instance][1], return_dict[instance][2], return_dict[instance][3]))
