from networkx import gnp_random_graph as rand_graph


number_vertex = [200, 500, 1000, 2000]
probability = [0.2, 0.5, 0.8]
number_graphs = 10

for i in range(number_graphs):
    for p in probability:
        for n in number_vertex:
            file_name = "instances/NEW-V"+str(n)+"-P"+str(p)+"-G"+str(i)+".txt"
            g = rand_graph(n, p, seed=i)

            with open(file_name, 'w') as f:
                f.write(str(n) + " " + str(g.number_of_edges()))
                for v in g.nodes:
                    for u in g[v]:
                        f.write("\n" + str(v) + " " + str(u))

            print("Created instance: ", g)