from time import time
from vns import vns
from statistics import mean
from read_graph import read_graph
from multiprocessing import Process, Manager


def task(fun, g, k, r, i):
    d, time_execute = fun(g, k)
    # print(len(d), time_execute)
    r[i] = [len(d), time_execute]


if __name__ == '__main__':

    city_instances = ['bath.txt', 'belfast.txt', 'brighton.txt', 'bristol.txt',
                      'cardiff.txt', 'coventry.txt', 'exeter.txt', 'glasgow.txt',
                      'leeds.txt', 'leicester.txt', 'liverpool.txt', 'manchester.txt',
                      'newcastle.txt', 'nottingham.txt', 'oxford.txt', 'plymouth.txt',
                      'sheffield.txt', 'southampton.txt', 'sunderland.txt', 'york.txt']

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
            print("Start: ", graph_open)

            p = Process(target=task, args=(vns, g, k, return_dict, instance))
            procs.append(p)

        for i in range(10):
            procs[i].start()

        for p in procs:
            procs[i].join()

        for i in range(10, 20):
            procs[i].start()

        for p in procs:
            procs[i].join()

        with open(file_name_res, 'a') as f:
            for instance in city_instances:
                f.write(instance + "\n")
                f.write('{}, {:.2f}\n'.format(return_dict[instance][0], return_dict[instance][1]))

