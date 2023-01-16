from random import random
from time import time
from networkx import DiGraph, Graph


def is_acceptable_solution(graph: DiGraph or Graph, D: list, k: int) -> bool:
    for v in graph.nodes:
        if v not in D and number_same_elements(set(graph[v]), D) < k:
            return False
    return True


# TODO: use either library intersection method or check which set is smaller and set it to outer loop
def number_same_elements(nv: set, d: set) -> int:
    counter = 0
    for element in d:
        if element in nv:
            counter += 1
    return counter

def number_same_elements_at_least_k(nv: set, d: set, k: int) -> bool:
    if k==1:
        return number_same_elements_at_least_1(nv, d)
    else:
        return number_same_elements(nv, d)>=k

def number_same_elements_at_least_1(nv: set, d: set) -> bool:
    for element in d:
        if element in nv:
            return True


def objective_function(s: list, g: Graph or DiGraph, k: int) -> int:
    objective_sum: int = 0

    for v in g.nodes:
        if v not in s:
            neighbors = set(g[v])
            objective_sum += min(k, number_same_elements(neighbors, s))

    return objective_sum


def violating(s: list, g: Graph or DiGraph, k: int) -> float:
    counter: int = 0

    for v in g.nodes:
        if v not in s:
            neighbors = set(g[v])
            counter += 1 if number_same_elements(neighbors, s) < k else 0

    return len(g) - counter #- len(s)/2.0 - bolje radi bez ovog


def obj_voi(s: set, g: Graph or DiGraph, k: int) -> (int, int):
    objective_sum: int = 0
    counter: int = 0

    for v in g.nodes:
        if v not in s:
            neighbors = set(g[v])
            nse = number_same_elements(neighbors, s)

            objective_sum += min(k, nse)

            if nse < k:
                counter += 1

    return objective_sum, len(g) - counter #- len(s)/4.0


def fitness(s: set, g: Graph or DiGraph, k: int, cache={}) -> float:
    viol = 0
    for v in g.nodes:
        if v not in s:
            neighbors = set(g[v])
            nse = number_same_elements(neighbors, s)
            if nse < k:
                viol += k-nse
            cache[v] = nse

    return viol + float(len(s))/len(g)

def fitness_rec_rem(s: set, v: int, fit: float, g: Graph or DiGraph, all_neighbors: dict, neighb_matrix: list, k: int, cache: dict) -> float:

    srem = set(s)
    srem.remove(v)

    start = time()
    for u in g[v]:
        if u not in s: # then s not in 'srem' <== s intersect srem = s, srem / s = {v}, v not in g[v]
            #neighbors = all_neighbors[u] # set(g[u])
            #nse_s = number_same_elements(neighbors, s) # TODO: optimisation
            nse_s = cache[u]
            if nse_s < k:
                fit -= k-nse_s
            #if not number_same_elements_at_least_k(neighbors, s, k):
            #    fit-=1

            #nse_srem = number_same_elements(neighbors, srem) # TODO: optimisation
            nse_srem = nse_s
            if neighb_matrix[v][u]:
                nse_srem -= 1 # we removed the neighbor of u, se nse_srem is decreased
            if nse_srem < k:
                fit += k-nse_srem
            #if not number_same_elements_at_least_k(neighbors, srem, k):
            #    fit+=1

    nse_srem = number_same_elements(all_neighbors[v], srem)

    if nse_srem < k:
        fit += k-nse_srem

    return fit - 1.0/len(g)


def fitness_rec_add(s: set, v: int, fit: float, g: Graph or DiGraph, all_neighbors: dict, neighb_matrix: list, k: int, cache) -> float:
    #sadd = set(s)
    #sadd.add(v)

    for u in g[v]:
        if u not in s:  # then s not in 'srem' <== s intersect srem = s, srem / s = {v}, v not in g[v]
            #neighbors = all_neighbors[u] # set(g[u])
            #nse_s = number_same_elements(neighbors, s)  # TODO: optimisation
            nse_s = cache[u]
            if nse_s < k:
                fit -= k-nse_s
            #if not number_same_elements_at_least_k(neighbors, s, k):
            #    fit-=1

            #nse_sadd = number_same_elements(neighbors, sadd)  # TODO: optimisation
            nse_sadd = nse_s
            if neighb_matrix[v][u]:
                nse_sadd+=1
            if nse_sadd < k:
                fit += k-nse_sadd
            #if not number_same_elements_at_least_k(neighbors, sadd, k):
            #    fit+=1

    nse_s = cache[v] #number_same_elements(all_neighbors[v], s)

    if nse_s < k:
        fit -= k-nse_s

    return fit + 1.0/len(g)
