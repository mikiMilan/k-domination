from vns import VNS
from read_graph import read_graph
from multiprocessing import Process, Manager
from math import ceil
from grid_search import grid_search


def create_space(d_min_space, d_max_init_space, prob_space, penalty_space):
    space = []
    for dmn in range(d_min_space[0], d_min_space[1], d_min_space[2]):
        for dmx in range(d_max_init_space[0], d_max_init_space[1], d_max_init_space[2]):
            prob = prob_space[0]
            while prob < prob_space[1]:
                penalty = penalty_space[0]
                while penalty < penalty_space[1]:
                    space.append((dmn, dmx, prob, penalty))
                    penalty += penalty_space[2]
                prob += prob_space[2]

    return space


def task(vns, grid_space, r, i):
    gs = grid_search(vns, grid_space)
    res, res_time = gs.run()
    r[i] = [res, res_time]


if __name__ == '__main__':
    paralellism = 3
    iteration_max = 100
    time_limit = 3600
    seed = 12345

    # define grid space
    d_min_space = (1, 10, 2)
    d_max_init_space = (10, 101, 10)
    prob_space = (0, 1, 0.2)
    penalty_space = (0.001, 0.02, 0.004)
    grid_space = create_space(d_min_space, d_max_init_space, prob_space, penalty_space)
    print("length grid space: ", len(grid_space))
    # print(space)

    instance_dir = 'cities_small_instances'
    instances = ['bath.txt', 'belfast.txt', 'brighton.txt', 'bristol.txt',
                      'cardiff.txt', 'coventry.txt', 'exeter.txt', 'glasgow.txt',
                      'leeds.txt', 'leicester.txt', 'liverpool.txt', 'manchester.txt',
                      'newcastle.txt', 'nottingham.txt', 'oxford.txt', 'plymouth.txt',
                      'sheffield.txt', 'southampton.txt', 'sunderland.txt', 'york.txt']
                  
    '''
    instance_dir = 'cities_big_instances'
    instances = ['belgrade.txt', 'berlin.txt', 'boston.txt', 'dublin.txt', 'minsk.txt']'''

    batches = ceil(len(instances)/paralellism)

    for k in [1, 2, 4]:
        file_name_res = 'results/grid_serach/all_k' + str(k) + '_it'+str(iteration_max)+'.txt'
        times = []
        results = []
        manager = Manager()
        return_dict = manager.dict()
        procs = []
        i = 0

        for instance in instances:
            graph_open = instance_dir+'/'+instance
            print("Reading graph!")
            g = read_graph(graph_open)
            print("Creating process: ", graph_open)
            vns = VNS(instance, g, k, 1, 100, time_limit, iteration_max, 0.5, 0.01, seed)
            p = Process(target=task, args=(vns, grid_space, return_dict, instance))
            procs.append(p)

        for b in range(batches):
            print("Doing batch "+str(b))
            for i in range(len(procs)):
                if i%batches==b:
                    print("Starting process "+str(i) +". "+instances[i])
                    procs[i].start()
                    
            for i in range(len(procs)):
                if i%batches==b:
                    procs[i].join()
                    print("Process "+str(i)+" finished")

            print("Printing batch "+str(b)+" results")
            with open(file_name_res, 'a') as f:
                for i in range(len(instances)):
                    instance = instances[i]
                    if i%batches!=b:
                        continue
                    f.write('inst={}\t k={}\t it_max={}\t vns_seed={}\t params={}\t fit={}\n'.format(instance, k, iteration_max, seed, return_dict[instance][0], return_dict[instance][1]))

