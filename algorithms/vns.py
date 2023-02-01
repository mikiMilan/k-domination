from time import time
from random import shuffle, random, seed
from read_graph import read_graph
from networkx import DiGraph, Graph
from unit import fitness, fitness_rec_rem, fitness_rec_add


class VNS:
    def __init__(self, instance_name, graph: DiGraph or Graph, k: int, d_min: int, d_max_init: int, time_limit: int, iteration_max: int, prob: float, penalty: float, rseed : int):
        self.instance_name = instance_name
        self.graph = graph
        self.k = k
        self.d_min = d_min
        self.d_max_init = d_max_init
        self.d_max = self.d_max_init
        self.time_limit = time_limit
        self.iteration_max = iteration_max
        self.prob = prob
        self.penalty = penalty
        self.nodes = list(self.graph.nodes) # kopiram cvorove zbog MJESANJA - necu da mjesam original
        self.rseed = rseed
        seed(self.rseed)
        # prepare neighbor matrices and sets
        self.neighbors = {}
        self.neighb_matrix = [[] for _ in range(len(self.graph.nodes))]
        for v in self.graph.nodes:
            self.neighbors[v] = set(self.graph[v])
            self.neighb_matrix[v] = [False]*len(self.graph.nodes)
            for u in self.graph[v]:
                self.neighb_matrix[v][u] = True

    def shaking(self, s: set, d: int) -> set:
        sl = list(s)
        shuffle(sl)
            
        shak = set(sl[:len(sl)-d])

        shuffle(self.nodes)
        shak.union(set(self.nodes[:d]))

        return shak

    def first_fitness_better(self, fit1, fit2):
        fit1Tot = (1+fit1[0])*(1+fit1[1]*self.penalty)
        fit2Tot = (1+fit2[0])*(1+fit2[1]*self.penalty)
        return fit1Tot<fit2Tot
    
    def fitness_equal(self, fit1, fit2):
        return not self.first_fitness_better(fit1, fit2) and not self.first_fitness_better(fit2, fit1)

    def local_search_best(self, s: set):
        improved = True
        cache = {}
        curr_fit = fitness(s, self.graph, self.k, cache)

        # adding nodes to achieve feasibility
        while improved:
            improved = False
            best_fit = curr_fit
            best_v = None

            for v in self.nodes:
                if v not in s:
                    new_fit = fitness_rec_add(s, v, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, cache)
                    if self.first_fitness_better(new_fit, best_fit):
                        best_fit = new_fit
                        best_v = v
                        improved = True
            
            if improved:
                s.add(best_v)
                curr_fit = best_fit
                cache = {}
                check_fit =  fitness(s, self.graph, self.k, cache)
                if not self.fitness_equal(curr_fit, check_fit):
                    print("Error in incremental fitness true fitness is "+str(check_fit)+" and incremental is "+str(curr_fit))
                    exit(1)

        # now simple removal
        improved = True
        while improved:
            improved = False
            best_fit = curr_fit
            best_v = None

            for v in self.nodes:
                if v in s:
                    new_fit = fitness_rec_rem(s, v, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, cache)
                    if self.first_fitness_better(new_fit, best_fit):
                        best_fit = new_fit
                        best_v = v
                        improved = True
            
            if improved:
                s.remove(best_v)
                curr_fit = best_fit
                cache = {}
                check_fit =  fitness(s, self.graph, self.k, cache)
                if not self.fitness_equal(curr_fit, check_fit):
                    print("Error in incremental fitness true fitness is "+str(check_fit)+" and incremental is "+str(curr_fit))
                    exit(1)

        return curr_fit

    def run(self) -> list:
        start_time = time()
        best_time = 0
        s_accept = set([])
        fit = self.local_search_best(s_accept)
        iteration = 1
        d = self.d_min

        while iteration < self.iteration_max and time()-start_time < self.time_limit:
            s_new = self.shaking(s_accept, d)
            fit_new = self.local_search_best(s_new)

            if self.first_fitness_better(fit_new, fit) or (self.fitness_equal(fit, fit_new) and random() < self.prob): #and len(s_new.intersection(s))!=len(s_new) and
                #if self.fitness_equal(fit_new, fit):
                #    print("Prelazim u isto kvalitetno sa drugacijom internom strukturom")
                if self.first_fitness_better(fit_new, fit):
                    best_time = time() - start_time
                s_accept = s_new
                d = self.d_min
                fit = fit_new
                len_s_accept = int(len(s_accept)/2) if len(s_accept)>2 else self.d_max_init
                self.d_max = min(len_s_accept, self.d_max_init)
            else:
                d += 1
                if d >= self.d_max:
                    d = self.d_min

            iteration += 1
            if iteration%50== 0:
                print("it={:4d}\tt={:2d}\td={:2d}\tdmin={}\tdmax={}\tprob={:.2f}\tpen={:.4f}\tbest={}\tnew={}\tk={}\tinst={}".format(iteration, int(time() - start_time),d,self.d_min, self.d_max, self.prob, self.penalty, fit, fit_new, self.k, self.instance_name))
        return s_accept, best_time, fit[0]==0


if __name__ == '__main__':
    instance_dir = 'cities_small_instances'
    instance = 'bath.txt'
    graph_open = instance_dir + '/' + instance
    print("Reading graph!")
    g = read_graph(graph_open)
    print("Creating process: ", graph_open)

    vns = VNS(instance, g, k=4, d_min=5, d_max_init=39, time_limit=60, iteration_max=3900, prob=0.45, penalty=0.02, rseed=2)
    print(vns.run())

