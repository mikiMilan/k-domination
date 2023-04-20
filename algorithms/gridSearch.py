from time import time
from test import VNS
from statistics import mean
from read_graph import read_graph
from multiprocessing import Process, Manager
from math import ceil
from random import seed as rseed, shuffle

def myFunc(e):
  return e[1]


def create_space(d_min_space, d_max_init_space, prob_space, penalty_space):
    space = []
    for dmn in d_min_space:
        for dmx in d_max_init_space:
            for prob in prob_space:
                for penalty in penalty_space:
                    space.append((dmn, dmx, prob, penalty))

    return space

def task(instance_name, g, k, d_min, d_max, time_limit, iteration_max, prob, penalty, seed, r, i):
    vns  = VNS(instance_name, g, k, d_min, d_max, time_limit, iteration_max, prob, penalty, seed)
    d, time_execute, invalid_cnt, fit = vns.run()
    r[i] = [len(d), time_execute, invalid_cnt, fit]


if __name__ == '__main__':
    paralellism = 6
    iteration_max = 1000
    time_limit = 3600
    seed = 12345
    rseed(12345)
    
    
    instance_dir = 'cities_small_instances'
    instances = ['bath.txt', 'belfast.txt', 'brighton.txt', 'bristol.txt',
                      'cardiff.txt', 'coventry.txt', 'exeter.txt', 'glasgow.txt',
                      'leeds.txt', 'leicester.txt', 'liverpool.txt', 'manchester.txt',
                      'newcastle.txt', 'nottingham.txt', 'oxford.txt', 'plymouth.txt',
                      'sheffield.txt', 'southampton.txt', 'sunderland.txt', 'york.txt']
                  
    '''
    instance_dir = 'cities_big_instances'
    instances = ['belgrade.txt', 'berlin.txt', 'boston.txt', 'dublin.txt', 'minsk.txt']'''

    

    # define grid space
    d_min_space = [1]
    d_max_init_space = [5, 10, 15, 20, 25, 30, 40, 50, 100]
    prob_space = [0, 0.25, 0.5, 0.75, 1]
    penalty_space = [0.005, 0.01, 0.015, 0.02]

    grid_space = create_space(d_min_space, d_max_init_space, prob_space, penalty_space)

    new_insts = []
    for ins in instances:
        for k in [1, 2, 4]:
            new_insts.append((ins, k))
    
    shuffle(new_insts)
    new_insts = new_insts[:20]
    new_insts.sort(key=myFunc)

    batches = ceil(len(grid_space)/paralellism)

    for ins in new_insts[:20]:
        file_name_res = 'results/GS/' + str(ins[0]) + '_k'+str(ins[1])+'.txt'
        times = []
        results = []
        manager = Manager()
        return_dict = manager.dict()
        procs = []
        graph_open = instance_dir+'/'+ins[0]
        g = read_graph(graph_open)
        print("Creating process: ", graph_open)
        for conf in grid_space:
            p = Process(target=task, args=(ins[0], g, ins[1], conf[0], conf[1], time_limit, iteration_max, conf[2], conf[3], seed, return_dict, conf))
            procs.append(p)

        for b in range(batches):
            print("Doing batch "+str(b))
            for i in range(len(procs)):
                if i%batches==b:
                    print("Starting process "+str(i) +". "+str(grid_space[i]))
                    procs[i].start()
                    
            for i in range(len(procs)):
                if i%batches==b:
                    procs[i].join()
                    print("Process "+str(i)+" finished")

            print("Printing batch "+str(b)+" results")
            with open(file_name_res, 'a') as f:
                for i in range(len(grid_space)):
                    if i%batches==b:
                        config = grid_space[i]
                        f.write('{}, {}, {:.2f}, {}, {:.10f}\n'.format(config, return_dict[config][0], return_dict[config][1], return_dict[config][2], return_dict[config][3]))

