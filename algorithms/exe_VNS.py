from time import time
from vns import vns
from statistics import mean
from read_graph import read_graph
from multiprocessing import Process, Manager
from math import ceil


def task(fun, instance_name, g, k, time_limit, iteration_max, r, i):
    d, time_execute = fun(instance_name, g, k, time_limit, iteration_max)
    # print(len(d), time_execute)
    r[i] = [len(d), time_execute]


if __name__ == '__main__':

    paralellism = 10
    iteration_max = 1000000
    time_limit = 3600
    
    city_instances = ['bath.txt', 'belfast.txt', 'brighton.txt', 'bristol.txt',
                      'cardiff.txt', 'coventry.txt', 'exeter.txt', 'glasgow.txt',
                      'leeds.txt', 'leicester.txt', 'liverpool.txt', 'manchester.txt',
                      'newcastle.txt', 'nottingham.txt', 'oxford.txt', 'plymouth.txt',
                      'sheffield.txt', 'southampton.txt', 'sunderland.txt', 'york.txt']
    batches = ceil(len(city_instances)/paralellism)

    for k in [1, 2, 4]:
        file_name_res = 'results/VNS/k' + str(k) + '.txt'
        times = []
        results = []
        manager = Manager()
        return_dict = manager.dict()
        procs = []
        i = 0

        for instance in city_instances:
            graph_open = 'cities_small_instances/'+instance
            print("Reading graph!")
            g = read_graph(graph_open)
            print("Creating process: ", graph_open)

            p = Process(target=task, args=(vns, instance, g, k, time_limit, iteration_max, return_dict, instance))
            procs.append(p)

        for b in range(batches):
            print("Doing batch "+str(b))
            for i in range(len(procs)):
                if i%batches==b:
                    print("Starting process "+str(i) +". "+city_instances[i])
                    procs[i].start()
                    
            for i in range(len(procs)):
                if i%batches==b:
                    procs[i].join()
                    print("Process "+str(i)+" finished")

            print("Printing batch "+str(b)+" results")
            with open(file_name_res, 'a') as f:
                for i in range(len(city_instances)):
                    instance = city_instances[i]
                    if i%batches!=b:
                        continue
                    f.write('{}, {}, {:.2f}\n'.format(instance, return_dict[instance][0], return_dict[instance][1]))

