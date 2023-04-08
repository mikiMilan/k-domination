from test import VNS
from read_graph import read_graph
from math import inf


class grid_search():
    def __init__(self, vns, param_space):
        self.vns = vns
        self.space = param_space

    def run(self):
        best_space = None
        best_fitness = inf
        # print("Inst:", self.vns.instance_name)

        for curr_space in self.space:
            self.vns.d_min = curr_space[0]
            self.vns.d_max_init = curr_space[1]
            self.vns.d_max = curr_space[1]
            self.vns.prob = curr_space[2]
            self.vns.penalty = curr_space[3]

            value, best_time, feasible = self.vns.run()

            if not feasible:
                best_space = None

            fitness = len(value) + best_time/100000

            if fitness < best_fitness:
                best_space = curr_space
                best_fitness = fitness
                print("Inst:", self.vns.instance_name, "\t Len_Sol: ", len(value), "\t Space", best_space)

        return best_space, best_fitness


if __name__ == '__main__':
    instance_dir = 'cities_small_instances'
    instance = 'bath.txt'
    time_limit = 3000
    iteration_max = 1000

    graph_open = instance_dir + '/' + instance
    print("Reading graph!")
    g = read_graph(graph_open)
    print("Creating process: ", graph_open)

    vns = VNS(instance, g, k=4, d_min=1, d_max_init=100, time_limit=time_limit, iteration_max=iteration_max, prob=0.5, penalty=0.01, rseed=12345)

    # define grid parameters
    d_min_space = {1, 4, 16}
    d_max_init_space = {25, 50, 75, 100}
    prob_space = {0, 0.25, 0.5, 0.75, 1}
    penalty_space = {0.005, 0.01, 0.015, 0.02}
    space = []
    for dmn in d_min_space:
        for dmx in d_max_init_space:
            for prob in prob_space:
                for penalty in penalty_space:
                    space.append((dmn, dmx, prob, penalty))

    print("length grid space: ", len(space))
    print(space)

    gr = grid_search(vns=vns, param_space=space)
    res = gr.run()

    # print(res)
