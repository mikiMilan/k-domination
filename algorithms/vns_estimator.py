from time import time
from random import shuffle, random, seed
from networkx import Graph
from sklearn.base import BaseEstimator
from sklearn.metrics import accuracy_score
from unit import fitness, fitness_rec_rem, fitness_rec_add


class VNS(BaseEstimator):
    def __init__(
            self,
            instance_name='test',
            graph=Graph(),
            k=1,
            d_min=1,
            d_max=100,
            time_limit=3600,
            iteration_max=999999,
            prob=0.5,
            penalty=0.01,
            rseed=12345
    ):
        self.instance_name = instance_name
        self.graph = graph
        self.k = k
        self.d_min = d_min
        self.d_max = d_max
        self.time_limit = time_limit
        self.iteration_max = iteration_max
        self.prob = prob
        self.penalty = penalty
        self.nodes = list(self.graph.nodes)  # kopiram cvorove zbog MJESANJA - necu da mjesam original
        self.rseed = rseed
        seed(self.rseed)
        # prepare neighbor matrices and sets
        self.neighbors = {}
        self.neighb_matrix = [[] for _ in range(len(self.graph.nodes))]
        for v in self.graph.nodes:
            self.neighbors[v] = set(self.graph[v])
            self.neighb_matrix[v] = [False] * len(self.graph.nodes)
            for u in self.graph[v]:
                self.neighb_matrix[v][u] = True

    def shaking(self, s: set, d: int) -> set:
        sl = list(s)
        shuffle(sl)

        shak = set(sl[:len(sl) - d])

        shuffle(self.nodes)
        shak.union(set(self.nodes[:d]))

        return shak

    def first_fitness_better(self, fit1, fit2):
        fit1Tot = (1 + fit1[0]) * (1 + fit1[1] * self.penalty)
        fit2Tot = (1 + fit2[0]) * (1 + fit2[1] * self.penalty)
        return fit1Tot < fit2Tot

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
                    new_fit = fitness_rec_add(s, v, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k,
                                              cache)
                    if self.first_fitness_better(new_fit, best_fit):
                        best_fit = new_fit
                        best_v = v
                        improved = True

            if improved:
                s.add(best_v)
                curr_fit = best_fit
                cache = {}
                check_fit = fitness(s, self.graph, self.k, cache)
                if not self.fitness_equal(curr_fit, check_fit):
                    print(
                        "Error in incremental fitness true fitness is " + str(check_fit) + " and incremental is " + str(
                            curr_fit))
                    exit(1)

        # now simple removal
        improved = True
        while improved:
            improved = False
            best_fit = curr_fit
            best_v = None

            for v in self.nodes:
                if v in s:
                    new_fit = fitness_rec_rem(s, v, curr_fit, self.graph, self.neighbors, self.neighb_matrix, self.k,
                                              cache)
                    if self.first_fitness_better(new_fit, best_fit):
                        best_fit = new_fit
                        best_v = v
                        improved = True

            if improved:
                s.remove(best_v)
                curr_fit = best_fit
                cache = {}
                check_fit = fitness(s, self.graph, self.k, cache)
                if not self.fitness_equal(curr_fit, check_fit):
                    print(
                        "Error in incremental fitness true fitness is " + str(check_fit) + " and incremental is " + str(
                            curr_fit))
                    exit(1)

        return curr_fit

    def run(self) -> list:
        start_time = time()
        best_time = 0

        s_accept = set([])
        for v in self.graph.nodes:
            if len(self.graph[v]) < self.k:
                s_accept.add(v)

        fixed_nodes = set(s_accept)

        fit = self.local_search_best(s_accept)
        best_time = time() - start_time

        iteration = 1
        d = self.d_min

        while iteration < self.iteration_max and time() - start_time < self.time_limit:
            s_new = self.shaking(s_accept, d)
            fit_new = self.local_search_best(s_new)

            if self.first_fitness_better(fit_new, fit) or (self.fitness_equal(fit,
                                                                              fit_new) and random() < self.prob):  # and len(s_new.intersection(s))!=len(s_new) and
                # if self.fitness_equal(fit_new, fit):
                #    print("Prelazim u isto kvalitetno sa drugacijom internom strukturom")
                if self.first_fitness_better(fit_new, fit):
                    best_time = time() - start_time
                s_accept = s_new
                d = self.d_min
                fit = fit_new
                self.d_max = int(len(s_accept) / 2)
            else:
                d += 1
                if d >= self.d_max:
                    d = self.d_min

            iteration += 1
            if iteration % 100 == 0:
                print("it={:4d}\tt={:2d}\td={:2d}\tdmin={}\tdmax={}\tbest={}\tnew={}\tk={}\tinst={}".format(iteration,
                                                                                                            int(time() - start_time),
                                                                                                            d,
                                                                                                            self.d_min,
                                                                                                            self.d_max,
                                                                                                            fit,
                                                                                                            fit_new,
                                                                                                            self.k,
                                                                                                            self.instance_name))
        return s_accept, best_time

    def fit(self, X, y):
        return self

    def score(self, X, y):
        return accuracy_score(y, self.predict(X))

    def predict(self, X):
        res = []
        for g in X:
            self.graph = g
            self.neighbors = {}
            self.neighb_matrix = [[] for _ in range(len(self.graph.nodes))]
            for v in self.graph.nodes:
                self.neighbors[v] = set(self.graph[v])
                self.neighb_matrix[v] = [False] * len(self.graph.nodes)
                for u in self.graph[v]:
                    self.neighb_matrix[v][u] = True
            s, t = self.run()
            res.append(len(s))

        return res


