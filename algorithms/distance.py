from time import time
from vns import VNS
from statistics import mean
from read_graph import read_graph
from multiprocessing import Process, Manager
from math import ceil
from networkx import all_pairs_shortest_path_length


instance_dir = 'instances/cities_small_instances'
instance = "manchester.txt"
                 
graph_open = instance_dir+'/'+instance
print("Reading graph!")
g = read_graph(graph_open)
print("end read")

d = {4:-1, 2:-9}
t = set(d)
print(t[0])

# path = dict(all_pairs_shortest_path_length(g)) # This is a generator)
# print("end find distance")
# n = len(g)
# l = []
# for i in range(n):
#     for j in range(i+1, n):
#         if path[i][j]==11:
#             if i not in l:
#                 l.append(i)

