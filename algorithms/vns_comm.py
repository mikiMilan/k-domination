from time import time
from random import shuffle, random, seed
from read_graph import read_graph
from networkx import DiGraph, Graph
from unit import fitness, fitness_rec_rem, fitness_rec_add, cache_rec_add, cache_rec_rem
import sys
import networkx as nx


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
        curr_fit = fitness(s, self.graph, self.nodes, self.k, cache)

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
                cache_rec_add(s, best_v, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, cache)
                s.add(best_v)
                curr_fit = best_fit


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
                cache_rec_rem(s, best_v, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, cache)
                s.remove(best_v)
                curr_fit = best_fit

        return curr_fit


    def run(self) -> list:
        start_time = time()
        best_time = 0
        s_accept = set([])
        fit = self.local_search_best(s_accept)
        if fit[0]==0:
            best_time = time() - start_time
        iteration = 1
        d = self.d_min

        sum_time_shaking = 0
        sum_time_lsb = 0

        while iteration < self.iteration_max and time()-start_time < self.time_limit:

            start_time_shaking = time()
            s_new = self.shaking(s_accept, d)
            sum_time_shaking += time() - start_time_shaking
            start_time_lsb = time()
            fit_new = self.local_search_best(s_new)
            sum_time_lsb += time() - start_time_lsb
            

            if (self.first_fitness_better(fit_new, fit) or (self.fitness_equal(fit, fit_new) and random() < self.prob)) and fit_new[0]==0: #and len(s_new.intersection(s))!=len(s_new) and
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
            if iteration%10== 0:
                print("it={:4d}\tt={:2d}\tbest={}\tst={:.4f}\tlsbt={:.4f}".format(iteration, int(time() - start_time),fit, sum_time_shaking, sum_time_lsb))
        tot_time = time()-start_time
        
        return s_accept, best_time, fit[0]==0, tot_time


if __name__ == '__main__':

    k = 1
    instance_dir = '../instances/cities_small_instances'
    instance = 'manchester.txt'
    rseed = 12345
    d_min = 1
    d_max_init = 50
    prob = 0.5
    penalty = 0.005
  
    iteration_max = 200000
    time_limit = 30

    graph_open = instance_dir + '/' + instance
    print("Reading graph!")
    G = read_graph(graph_open)
    print("Graph loaded: ", graph_open)

    global_sol = set()

    S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    
    for g in S:
        if len(g)>200:
            comm = nx.algorithms.community.asyn_fluidc(g, 7, max_iter=100, seed=None)

            for gi in comm:
                vns = VNS(instance, G.subgraph(list(gi)).copy(), k=k, d_min=d_min, d_max_init=d_max_init, time_limit=time_limit, iteration_max=iteration_max, prob=prob, penalty=penalty, rseed=rseed)
                sol, time, feasible, tot_time = vns.run()
                global_sol.union(sol)

    print(global_sol)
