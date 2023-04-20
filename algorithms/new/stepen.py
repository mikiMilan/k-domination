from read_graph import read_graph


# city_instances = ['bath.txt', 'belfast.txt', 'brighton.txt', 'bristol.txt',
#                       'cardiff.txt', 'coventry.txt', 'exeter.txt', 'glasgow.txt',
#                       'leeds.txt', 'leicester.txt', 'liverpool.txt', 'manchester.txt',
#                       'newcastle.txt', 'nottingham.txt', 'oxford.txt', 'plymouth.txt',
#                       'sheffield.txt', 'southampton.txt', 'sunderland.txt', 'york.txt']
# critical = set()
# for city in city_instances:
#     g = read_graph("cities_small_instances/"+city)
#
#     for v in g.nodes:
#         if len(g[v])<4:
#             print("City: ", city, ", cvor: ", v, "stepen: ", len(g[v]))
#             critical.add(city)
#
# print(critical)

graph = read_graph("cities_small_instances/oxford.txt")
oxford_optk4 = [0, 6, 8, 11, 15, 26, 28, 37, 42, 44, 45, 46, 47, 49, 50, 56, 58, 60, 62, 63, 68, 69, 93, 100, 107, 108,
                109, 111, 115, 116, 132, 137, 140, 147, 152, 164, 169, 175, 202, 207, 210, 211, 212, 215, 219, 230, 232,
                233, 235, 237, 242, 248, 264, 268, 286, 298, 307, 309, 312, 315, 316, 322, 327, 328, 330, 336, 337, 341,
                349, 352, 353, 354, 356, 364, 374, 385, 387, 388, 392, 396, 405, 414, 420, 421, 427, 465, 467, 468, 469]


max_stepen = 0
for v in graph.nodes:
    if len(graph[v])>max_stepen:
        max_stepen = len(graph[v])

print(max_stepen)

for v in oxford_optk4:
    if len(graph[v]) < 5: # len(graph[v]) > max_stepen-10
        print("Cvor: ", v, " - stepen: ", len(graph[v]))