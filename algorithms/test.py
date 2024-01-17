
from read_graph import read_graph
from networkx import DiGraph, Graph
import networkx as nx

if __name__ == '__main__':

    k = 1
    instance_dir = 'instances/cities_small_instances'
    instance = 'bath.txt'
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

    S = [g.subgraph(c).copy() for c in nx.connected_components(g)]
    for G in S:
        print(len(G))

    g = S[0]

    t = nx.algorithms.community.asyn_fluidc(g, 5, max_iter=100, seed=None)

    for i in t:
        print(i)

    communities_generator = nx.community.girvan_newman(g)
    # print("prosao")
    #top_level_communities = next(communities_generator)
    # print(top_level_communities)

    # next_level_communities = next(communities_generator)
    # print(next_level_communities)