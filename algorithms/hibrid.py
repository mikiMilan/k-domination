from time import time
from random import shuffle, random, seed, randint
from read_graph import read_graph
from networkx import DiGraph, Graph
from unit import fitness, fitness_rec_rem, fitness_rec_add, cache_rec_add, cache_rec_rem
import sys
from cplexKH import ILP
from numpy import full


class VNS:
    def __init__(self, instance_name, graph_dict, k: int, d_min: int, d_max_init: int, time_limit: int, iteration_max: int, prob: float, penalty: float, rseed : int):
        self.instance_name = instance_name
        self.graphD = graph_dict
        self.k = k
        self.d_min = d_min
        self.d_max_init = d_max_init
        self.d_max = self.d_max_init
        self.time_limit = time_limit
        self.iteration_max = iteration_max
        self.prob = prob
        self.penalty = penalty
        self.rseed = rseed
        seed(self.rseed)
        # copy the graph in multiple shapes for efficiency
        self.graph_nodes = set(graph_dict)
        self.nodes = list(self.graph_nodes) # kopiram cvorove zbog funk shaking
        self.n = len(self.nodes)
        self.neighborsSET = {}
        self.neighborsLIST = {}
        self.graphM = full((self.n, self.n), False)
        for v in self.graphD:
            self.neighborsSET[v] = set(self.graph[v].values())
            self.neighborsLIST[v] = list(self.graph[v].values())
            for u in self.graph[v]:
                self.graphM[v][u] = True

    def shaking(self, s: set, d: int) -> set:
        sl = list(s)
        shuffle(sl)

        deleted = sl[len(sl)-d:]
            
        shak = set(sl[:len(sl)-d])

        shuffle(self.nodes)
        shak.union(set(self.nodes[:d]))

        for i in deleted:
            max_rand =len(self.neighborsSET[i])
            shak.add(self.neighborsSET[i][randint(0,max_rand)])

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
                    new_fit = fitness_rec_add(s, v, curr_fit, self.graph, self.neighborsSET, self.graphM, self.k, cache)
                    if self.first_fitness_better(new_fit, best_fit):
                        best_fit = new_fit
                        best_v = v
                        improved = True
            
            if improved:
                cache_rec_add(s, best_v, curr_fit, self.graph, self.neighborsSET, self.graphM, self.k, cache)
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
                    new_fit = fitness_rec_rem(s, v, curr_fit, self.graph, self.neighborsSET, self.graphM, self.k, cache)
                    if self.first_fitness_better(new_fit, best_fit):
                        best_fit = new_fit
                        best_v = v
                        improved = True
            
            if improved:
                cache_rec_rem(s, best_v, curr_fit, self.graph, self.neighborsSET, self.graphM, self.k, cache)
                s.remove(best_v)
                curr_fit = best_fit

        return curr_fit


    def run(self) -> list:
        start_time = time()
        best_time = 0
        print("ILP start")
        _, _, _, sol = ILP(self.graph, self.k, 30, 10)
        print("End ILP")
        print("ILP solve len: ", len(sol))
        s_accept = set(sol)
        fit = self.local_search_best(s_accept)
        if fit[0]==0:
            best_time = time() - start_time
        iteration = 1
        d = self.d_min

        while iteration < self.iteration_max and time()-start_time < self.time_limit:
            s_new = self.shaking(s_accept, d)
            fit_new = self.local_search_best(s_new)

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
            if iteration%20== 0:
                print("it={:4d}\tt={:2d}\td={:2d}\tdmin={}\tdmax={}\tprob={:.2f}\tpen={:.4f}\tbest={}\tnew={}\tk={}\tinst={}".format(iteration, int(time() - start_time),d,self.d_min, self.d_max, self.prob, self.penalty, fit, fit_new, self.k, self.instance_name))
        tot_time = time()-start_time
        
        return s_accept, best_time, fit[0]==0, tot_time


if __name__ == '__main__':

    k = 4
    instance_dir = 'instances/cities_small_instances'
    instance = 'manchester.txt'
    time_limit = 1800
    iteration_max = 20000
    rseed = 12345
    d_min = 1
    d_max_init = 50
    prob = 0.5
    penalty = 0.005

    graph_open = instance_dir + '/' + instance
    print("Reading graph!")
    g = read_graph(graph_open)
    graph_dict = {}
    for v in g:
        graph_dict[v] = {}
        i = 0
        for u in set(g[v]):
           graph_dict[v][i] = u
           i+=1 
            
    print("Graph loaded: ", graph_open)

    vns = VNS(instance, graph_dict, k=k, d_min=d_min, d_max_init=d_max_init, time_limit=time_limit, iteration_max=iteration_max, prob=prob, penalty=penalty, rseed=rseed)
    sol, time, feasible, tot_time = vns.run()
    
    # + '_dmin'+str(d_min)+'_dmax'+str(d_max_init)+'_prob'+str(prob)+'_pen'+str(penalty)
    # file_name_res = 'results/VNS/k' + str(k) +'_tl'+str(time_limit)+'_it'+str(iteration_max)+'_seed'+str(rseed)+'.txt'
    # with open(file_name_res, 'a') as f:
    #     f.write('{}, {}, {:.2f}, {}, {:.2f}\n'.format(instance, len(sol),  time, feasible, tot_time))

