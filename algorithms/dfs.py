from time import time
from random import shuffle, random, seed
from read_graph import read_graph
from networkx import DiGraph, Graph
from unit import fitness, fitness_rec_rem, fitness_rec_add, cache_rec_add, cache_rec_rem
import sys


def dfs(visited, graph, node):  #function for dfs 
    if node not in visited:
        if len(visited)%100==0:
            print(len(visited))
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

graph_open = "instances/cities_big_instances/belgrade.txt"
print("Reading graph!")
g = read_graph(graph_open)
print("Graph loaded: ", graph_open)

visited = set()
dfs(visited, g, 0)