from vns import VNS
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
    d_min_space = (1, 10, 2)
    d_max_init_space = (10, 101, 10)
    prob_space = (0, 1, 0.2)
    penalty_space = (0.001, 0.02, 0.004)
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

    print("length grid space: ", len(space))
    # print(space)

    gr = grid_search(vns=vns, param_space=space)
    # res = gr.run()

    # print(res)
