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


def fitness(s: set, g: Graph or DiGraph, k: int, cache={}) -> float:
    viol = 0
    ineff = 0
    for v in g.nodes:
        if v not in s:
            neighbors = set(g[v])
            nse = number_same_elements(neighbors, s)
            if nse < k:
                viol +=(k-nse)
            if nse > k:
                ineff+= (nse-k)
            cache[v] = nse

    return (viol, len(s), ineff)

def fitness_rec_rem(s: set, v: int, fit: tuple, g: Graph or DiGraph, all_neighbors: dict, neighb_matrix: list, k: int, cache: dict) -> float:

    viol = fit[0]
    size = fit[1]-1
    ineff = fit[2]

    srem = set(s)
    srem.remove(v)

    start = time()
    for u in g[v]:
        if u not in s: # then s not in 'srem' <== s intersect srem = s, srem / s = {v}, v not in g[v]
            nse_s = cache[u]
            if nse_s < k:
                viol -= k-nse_s
            if nse_s>k:
                ineff-= nse_s-k
            nse_srem = nse_s

            if neighb_matrix[v][u]:
                nse_srem -= 1 # we removed the neighbor of u, se nse_srem is decreased
            if nse_srem < k:
                viol += k-nse_srem
            if nse_srem>k:
                ineff+=nse_srem-k

    nse_srem = number_same_elements(all_neighbors[v], srem)

    if nse_srem < k:
        viol += k-nse_srem
    if nse_srem>k:
        ineff+=nse_srem-k

    return (viol, size, ineff)


def fitness_rec_add(s: set, v: int, fit: tuple, g: Graph or DiGraph, all_neighbors: dict, neighb_matrix: list, k: int, cache) -> float:
    viol = fit[0]
    size = fit[1]+1
    ineff = fit[2]

    for u in g[v]:
        if u not in s:  # then s not in 'srem' <== s intersect srem = s, srem / s = {v}, v not in g[v]
            nse_s = cache[u]
            if nse_s < k:
                viol -= k-nse_s
            if nse_s>k:
                ineff-=nse_s-k
            nse_sadd = nse_s
            if neighb_matrix[v][u]:
                nse_sadd+=1
            if nse_sadd < k:
                viol += k-nse_sadd
            if nse_sadd>k:
                ineff+=nse_sadd-k

    nse_s = cache[v] 

    if nse_s < k:
        viol -= k-nse_s
    if nse_s>k:
        ineff-=nse_s-k

    return (viol, size, ineff)
