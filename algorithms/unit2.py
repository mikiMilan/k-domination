from random import random
from time import time
from networkx import DiGraph, Graph


def is_acceptable_solution(graph: DiGraph or Graph, D: list, k: int) -> bool:
    for v in graph.nodes:
        if v not in D and number_same_elements(set(graph[v]), D) < k:
            return False
    return True


def number_same_elements(nv: set, d: set) -> int:
    counter = 0

    outer, internal = d, nv
    if len(d)>len(nv):
        outer, internal = nv, d

    for element in outer:
        if element in internal:
            counter += 1

    return counter

# TODO: speed up this because of intensive usage in swap
def fitness(s: set, g: Graph or DiGraph, k: int, cache={}) -> float:
    viol = 0
    ineff =0
    max_ineff = 0
    for v in g.nodes:
        if v not in s:
            neighbors = set(g[v])
            nse = number_same_elements(neighbors, s)
            if nse < k:
                viol +=(k-nse)
            if nse > k+1:
                ineff+= 1#nse-k
            if nse>max_ineff:
                max_ineff = nse
            cache[v] = nse

    return (viol, len(s), ineff, max_ineff, len(g)-len(s))

def fitness_rec_rem(s: set, v: int, fit: tuple, g: Graph or DiGraph, all_neighbors: dict, neighb_matrix: list, k: int, cache: dict) -> float:

    viol = fit[0]
    size = fit[1]-1
    ineff = fit[2]
    max_ineff = fit[3]

    srem = set(s)
    srem.remove(v)

    for u in g[v]:
        if u not in s: # then s not in 'srem' <== s intersect srem = s, srem / s = {v}, v not in g[v]
            nse_s = cache[u]
            if nse_s < k:
                viol -= k-nse_s
            if nse_s>k+1:
                ineff-= 1#nse_s-k
            nse_srem = nse_s

            if neighb_matrix[v][u]:
                nse_srem -= 1 # we removed the neighbor of u, se nse_srem is decreased
            if nse_srem < k:
                viol += k-nse_srem
            if nse_srem>k+1:
                ineff+=1#nse_srem-k
            if nse_srem>max_ineff:
                max_ineff = nse_srem

    nse_srem = number_same_elements(all_neighbors[v], srem)

    if nse_srem < k:
        viol += k-nse_srem
    if nse_srem>k+1:
        ineff+=1#nse_srem-k
    if nse_srem>max_ineff:
        max_ineff = nse_srem

    return (viol, size, ineff, max_ineff, len(g)-size)


def fitness_rec_add(s: set, v: int, fit: tuple, g: Graph or DiGraph, all_neighbors: dict, neighb_matrix: list, k: int, cache) -> float:
    viol = fit[0]
    size = fit[1]+1
    ineff = fit[2]
    max_ineff = fit[3]

    for u in g[v]:
        if u not in s:  # then s not in 'srem' <== s intersect srem = s, srem / s = {v}, v not in g[v]
            nse_s = cache[u]
            if nse_s < k:
                viol -= k-nse_s
            if nse_s>k+1:
                ineff-=1#nse_s-k
            nse_sadd = nse_s
            if neighb_matrix[v][u]:
                nse_sadd+=1
            if nse_sadd < k:
                viol += k-nse_sadd
            if nse_sadd>k+1:
                ineff+=1#nse_sadd-k
            if nse_sadd > max_ineff:
                max_ineff = nse_sadd

    nse_s = cache[v] 

    if nse_s < k:
        viol -= k-nse_s
    if nse_s>k+1:
        ineff-=1#nse_s-k

    return (viol, size, ineff, max_ineff, len(g)-size)


def cache_rec_add(s: set, v: int, fit: tuple, g: Graph or DiGraph, all_neighbors: dict, neighb_matrix: list, k: int, cache) -> float:
    viol = fit[0]
    size = fit[1]+1
    ineff = fit[2]
    max_ineff = fit[3]

    for u in g[v]:
        if u not in s:  # then s not in 'srem' <== s intersect srem = s, srem / s = {v}, v not in g[v]
            nse_s = cache[u]
            if nse_s < k:
                viol -= k-nse_s
            if nse_s>k+1:
                ineff-=1#nse_s-k
            nse_sadd = nse_s
            if neighb_matrix[v][u]:
                nse_sadd+=1
            if nse_sadd < k:
                viol += k-nse_sadd
            if nse_sadd>k+1:
                ineff+=1#nse_sadd-k
            if nse_sadd > max_ineff:
                max_ineff = nse_sadd
            cache[u] = nse_sadd

    nse_s = cache[v] 

    if nse_s < k:
        viol -= k-nse_s
    if nse_s>k+1:
        ineff-=1#nse_s-k

    del cache[v]

    return (viol, size, ineff, max_ineff, len(g)-size)

def cache_rec_rem(s: set, v: int, fit: tuple, g: Graph or DiGraph, all_neighbors: dict, neighb_matrix: list, k: int, cache: dict) -> float:

    viol = fit[0]
    size = fit[1]-1
    ineff = fit[2]
    max_ineff = fit[3]

    srem = set(s)
    srem.remove(v)

    for u in g[v]:
        if u not in s: # then s not in 'srem' <== s intersect srem = s, srem / s = {v}, v not in g[v]
            nse_s = cache[u]
            if nse_s < k:
                viol -= k-nse_s
            if nse_s>k+1:
                ineff-= 1#nse_s-k
            nse_srem = nse_s

            if neighb_matrix[v][u]:
                nse_srem -= 1 # we removed the neighbor of u, se nse_srem is decreased
            if nse_srem < k:
                viol += k-nse_srem
            if nse_srem>k+1:
                ineff+=1#nse_srem-k
            if nse_srem>max_ineff:
                max_ineff = nse_srem

            cache[u] = nse_srem

    nse_srem = number_same_elements(all_neighbors[v], srem)
    cache[v] = nse_srem

    if nse_srem < k:
        viol += k-nse_srem
    if nse_srem>k+1:
        ineff+=1#nse_srem-k
    if nse_srem>max_ineff:
        max_ineff = nse_srem

    return (viol, size, ineff, max_ineff, len(g)-size)