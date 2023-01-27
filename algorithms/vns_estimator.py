from numpy import int32, asarray
from time import time
from random import shuffle, random, seed
from networkx import Graph
from sklearn.base import BaseEstimator
from sklearn.metrics import accuracy_score
from unit import fitness, fitness_rec_rem, fitness_rec_add
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted


class VNS(BaseEstimator):
    def __init__(
            self,
            k=1,
            d_min=1,
            d_max=100,
            time_limit=3600,
            iteration_max=999999,
            prob=0.5,
            penalty=0.01
            # graph, instance_name and rseed are sample
    ):
        self.k = k
        self.d_min = d_min
        self.d_max = d_max
        self.time_limit = time_limit
        self.iteration_max = iteration_max
        self.prob = prob
        self.penalty = penalty

    def init_sample(self, graph: Graph, rseed: int, instance_name: str):
        self.instance_name = instance_name
        self.graph = graph
        self.nodes = list(graph.nodes)
        self.neighbors = {}
        self.neighb_matrix = [[] for _ in range(len(graph.nodes))]
        for v in graph.nodes:
            self.neighbors[v] = set(graph[v])
            self.neighb_matrix[v] = [False] * len(graph.nodes)
            for u in graph[v]:
                self.neighb_matrix[v][u] = True

        self.rseed = rseed
        seed(self.rseed)

    def destroy_sample(self):
        self.instance_name = None
        self.graph = None
        self.nodes = None
        self.neighbors = None
        self.neighb_matrix = None

        self.rseed = None
        seed(self.rseed)

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

    def run(self) -> int:
        start_time = time()

        s_accept = set([])
        for v in self.graph.nodes:
            if len(self.graph[v]) < self.k:
                s_accept.add(v)

        fit = self.local_search_best(s_accept)

        iteration = 1
        d = self.d_min

        while iteration < self.iteration_max and time() - start_time < self.time_limit:
            s_new = self.shaking(s_accept, d)
            fit_new = self.local_search_best(s_new)

            if self.first_fitness_better(fit_new, fit) or \
                    (self.fitness_equal(fit, fit_new) and random() < self.prob):
                s_accept = s_new
                d = self.d_min
                fit = fit_new
                # self.d_max = int(len(s_accept) / 2)
            else:
                d += 1
                if d >= self.d_max:
                    d = self.d_min

            iteration += 1
            if iteration % 10 == 0:
                print("it={:4d}\tt={:2d}\td={:2d}\tdmin={}\tdmax={}\tbest={}\tnew={}\tk={}\tinst={}".
                      format(iteration, int(time() - start_time), d, self.d_min, self.d_max, fit, fit_new, self.k,
                             self.instance_name))

        return len(s_accept)

    def fit(self, X, y):
        # X, y = check_X_y(X, y, accept_sparse=True)
        # self.is_fitted_ = True

        return self

    # def score(self, X, y):
    #     pass

    def predict(self, X):
        # X = check_array(X, accept_sparse=True)
        # check_is_fitted(self, 'is_fitted_')

        VNSX = []
        for x in X:
            print("Predict: ", x[1], " d_max: ", self.d_max)
            self.init_sample(x[0], x[1], x[2])
            s = self.run()
            self.destroy_sample()
            VNSX.append(s)

        return asarray(VNSX, dtype=int32)


if __name__ == '__main__':
    from sklearn.utils.estimator_checks import check_estimator

    check_estimator(VNS())
