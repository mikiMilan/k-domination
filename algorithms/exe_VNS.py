from time import time
from vns import VNS
from statistics import mean
from read_graph import read_graph
from multiprocessing import Process, Manager
from math import ceil


def task(instance_name, g, k, d_min, d_max, time_limit, iteration_max, prob, penalty, seed, r, i):
    vns  = VNS(instance_name, g, k, d_min, d_max, time_limit, iteration_max, prob, penalty, seed)
    d, best_time, invalid_cnt, exe_time = vns.run()
    r[i] = [len(d), best_time, invalid_cnt, exe_time]


if __name__ == '__main__':
    paralellism = 2
    iteration_max = 200000
    time_limit = 18
    d_min = 1
    d_max = 50
    prob = 0.5
    penalty =  0.005
    # seed = 12345

    number_vertex = [200, 500, 1000, 2000]
    probability = [0.025, 0.05, 0.1, 0.2, 0.5, 0.8]
    number_graphs = 10
    instance_dir = '../instances/random_instances'

    seeds = [12345, 68531]

    batches = ceil(len(seeds)/paralellism)

    for k in [1]:

        file_name_res = '../results/VNS_random/random_k_' + str(k) + '.txt'

        for i in range(number_graphs):
            for pro in probability:
                for n in number_vertex:
                    instance = "NEW-V"+str(n)+"-P"+str(pro)+"-G"+str(i)+".txt"
                 
                    graph_open = instance_dir+'/'+instance
                    print("Reading graph!")
                    g = read_graph(graph_open)
                    print("-------", instance, k, "-------")

                    times = []
                    results = []
                    manager = Manager()
                    return_dict = manager.dict()
                    procs = []

                    for seed in seeds:
                        print("Creating process: ", seed)

                        p = Process(target=task, args=(instance, g, k, d_min, d_max, time_limit, iteration_max, prob, penalty, seed, return_dict, seed))
                        procs.append(p)

                    for b in range(batches):
                        print("Doing batch "+str(b))
                        for i in range(len(procs)):
                            if i%batches==b:
                                print("Starting process "+str(i) +". seed: "+str(seeds[i]))
                                procs[i].start()
                                
                        for i in range(len(procs)):
                            if i%batches==b:
                                procs[i].join()
                                print("Process "+str(i)+" finished")

                        print("Printing batch "+str(b)+" results")
                        with open(file_name_res, 'a') as f:
                            for i in range(len(seeds)):
                                seed2 = seeds[i]
                                if i%batches!=b:
                                    continue
                                f.write('{}, {}, {}, {:.2f}, {}, {:.2f}\n'.format(instance, seed2, return_dict[seed2][0], return_dict[seed2][1], return_dict[seed2][2], return_dict[seed2][3]))

