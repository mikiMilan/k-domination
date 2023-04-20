from read_graph import read_graph
from networkx import shortest_path_length

graph = read_graph("cities_small_instances/oxford.txt")

# sp = dict(all_pairs_shortest_path_length(graph))
# print(sp)

oxford_optk4 = [0, 6, 8, 11, 15, 26, 28, 37, 42, 44, 45, 46, 47, 49, 50, 56, 58, 60, 62, 63, 68, 69, 93, 100, 107, 108,
                109, 111, 115, 116, 132, 137, 140, 147, 152, 164, 169, 175, 202, 207, 210, 211, 212, 215, 219, 230, 232,
                233, 235, 237, 242, 248, 264, 268, 286, 298, 307, 309, 312, 315, 316, 322, 327, 328, 330, 336, 337, 341,
                349, 352, 353, 354, 356, 364, 374, 385, 387, 388, 392, 396, 405, 414, 420, 421, 427, 465, 467, 468, 469]

for vs in oxford_optk4:
    if len(graph[vs]) >= 4:
        dists = []
        for u in oxford_optk4:
            try:
                dist = shortest_path_length(graph, source=vs, target=u)
            except:
                # print("nema puta:", vs, u)
                dist = 1000
            dists.append(dist)

        dists.sort()
        print("Cvoru ", vs, "udaljenosti", dists)