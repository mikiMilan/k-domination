from time import time
from random import shuffle, random, seed, randint
from read_graph import read_graph
from networkx import DiGraph, Graph
from unit import fitness, fitness_rec_rem, fitness_rec_add, cache_rec_add, cache_rec_rem, fitness_rec_add_cache_change, fitness_rec_rem_cache_change
import sys


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

    def shaking2(self, s: set, d: int) -> set:
        sl = list(s)
        shuffle(sl)
            
        shak = set(sl[:len(sl)-d])

        # 
        # shak.union(set(self.nodes[:d+5]))

        return shak
    
    def shaking(self, s: set, d: int, curr_fit, cache) -> set:
        ls = list(s)
        shuffle(ls)

        shak_cache = dict(cache)
        new_fit = curr_fit

        for i in range(d):
            v = ls.pop()
            new_fit = fitness_rec_rem_cache_change(s, v, new_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, shak_cache)
             
        shuffle(self.nodes)

        return set(ls), new_fit, shak_cache

    def first_fitness_better(self, fit1, fit2):
        fit1Tot = (1+fit1[0])*(1+fit1[1]*self.penalty)
        fit2Tot = (1+fit2[0])*(1+fit2[1]*self.penalty)
        return fit1Tot<fit2Tot
    
    def first_fitness_better_or_equal(self, fit1, fit2):
        fit1Tot = (1+fit1[0])*(1+fit1[1]*self.penalty)
        fit2Tot = (1+fit2[0])*(1+fit2[1]*self.penalty)
        return fit1Tot<=fit2Tot
    
    def fitness_equal(self, fit1, fit2):
        return not self.first_fitness_better(fit1, fit2) and not self.first_fitness_better(fit2, fit1)

    def local_search_best(self, s: set,  curr_fit, cache):
        improved = True
        
        # adding nodes to achieve feasibility
        while improved:
            improved = False
            best_fit = curr_fit
            list_best = []

            for v in self.nodes:
                if v not in s:
                    new_fit = fitness_rec_add(s, v, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, cache)
                    if self.first_fitness_better(new_fit, best_fit):
                        best_fit = new_fit
                        improved = True
                        list_best = [v]
                    elif self.fitness_equal(new_fit, best_fit):
                        list_best.append(v)

            if improved:
                shuffle(list_best)
                for inter in range(0, randint(1,len(list_best))):
                    curr_fit = fitness_rec_add_cache_change(s, list_best[inter], curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, cache)
                    s.add(list_best[inter])

                # for u in list_best:
                #     curr_fit = fitness_rec_add_cache_change(s, u, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, cache)
                #     s.add(u)

        # now simple removal
        improved = True
        while improved:
            improved = False
            for v in self.nodes:
                if v in s:
                    new_fit = fitness_rec_rem(s, v, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, cache)
                    if self.first_fitness_better(new_fit, curr_fit):
                        curr_fit = fitness_rec_rem_cache_change(s, v, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, cache)
                        improved = True
                        s.remove(v)

        return curr_fit
    

    def local_search_first(self, s: set):
        improved = True
        cache = {}
        curr_fit = fitness(s, self.graph, self.k, cache)

        while improved:
            improved = False
            for v in self.nodes:
                if v not in s:
                    new_fit = fitness_rec_add(s, v, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, cache)
                    if self.first_fitness_better(new_fit, curr_fit):
                        curr_fit = fitness_rec_add_cache_change(s, v, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, cache)
                        improved = True
                        s.add(v)
            ls = list(s)
            shuffle(ls)
            improved = False
            for v in ls:
                if v in s:
                    new_fit = fitness_rec_rem(s, v, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, cache)
                    if self.first_fitness_better_or_equal(new_fit, curr_fit):
                        curr_fit = fitness_rec_rem_cache_change(s, v, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k, cache)
                        improved = True
                        s.remove(v)

        return curr_fit


    def run(self) -> list:
        start_time = time()
        best_time = 0
        s_accept = set([])
        cache = {}
        fit = fitness(s_accept, self.graph, self.k, cache)
        fit = self.local_search_best(s_accept, fit, cache)
        
        if fit[0]==0:
            best_time = time() - start_time

        iteration = 1
        d = self.d_min

        sum_sh = 0
        sum_ls = 0

        while iteration < self.iteration_max and time()-start_time < self.time_limit:
            start_sh = time()
            s_new, shak_fit, shak_cache = self.shaking(s_accept, d, fit, cache)
            sum_sh += time()-start_sh
            start_ls = time()
            fit_new = self.local_search_best(s_new, shak_fit, shak_cache)
            sum_ls += time() - start_ls
            
            if (self.first_fitness_better(fit_new, fit) or (self.fitness_equal(fit, fit_new) and random() < self.prob)) and fit_new[0]==0: #and len(s_new.intersection(s))!=len(s_new) and
                if self.first_fitness_better(fit_new, fit):
                    best_time = time() - start_time
                s_accept = s_new
                d = self.d_min
                fit = fit_new
                cache = shak_cache
                len_s_accept = int(len(s_accept)/2) if len(s_accept)>2 else self.d_max_init
                self.d_max = min(len_s_accept, self.d_max_init)
            else:
                d += 1
                if d >= self.d_max:
                    d = self.d_min

            iteration += 1
            if iteration%10== 0:
                print("it={:4d}\tt={:2d}\tbest={}\tshak={:.4f}\tls={:.4f}".format(iteration, int(time() - start_time),fit, sum_sh, sum_ls))
        tot_time = time()-start_time
        
        return s_accept, best_time, fit[0]==0, tot_time


if __name__ == '__main__':

    k = 4
    instance_dir = '../instances/cities_small_instances'
    instance = 'manchester.txt'
    rseed = 12345
    d_min = 1
    d_max_init = 50
    prob = 0.5
    penalty = 0.005
  
    iteration_max = 200000
    time_limit = 1800

    graph_open = instance_dir + '/' + instance
    print("Reading graph!")
    g = read_graph(graph_open)
    print("Graph loaded: ", graph_open)

    vns = VNS(instance, g, k=k, d_min=d_min, d_max_init=d_max_init, time_limit=time_limit, iteration_max=iteration_max, prob=prob, penalty=penalty, rseed=rseed)
    sol, time, feasible, tot_time = vns.run()
    
    # + '_dmin'+str(d_min)+'_dmax'+str(d_max_init)+'_prob'+str(prob)+'_pen'+str(penalty)
    file_name_res = 'results/VNS/k' + str(k) +'_tl'+str(time_limit)+'_it'+str(iteration_max)+'_seed'+str(rseed)+'.txt'
    with open(file_name_res, 'a') as f:
        f.write('{}, {}, {:.2f}, {}, {:.2f}\n'.format(instance, len(sol),  time, feasible, tot_time))

