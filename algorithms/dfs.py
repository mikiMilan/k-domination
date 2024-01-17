import networkx as nx

G = nx.barbell_graph(5, 1)

communities_generator = nx.community.girvan_newman(G)

top_level_communities = next(communities_generator)

print(top_level_communities)
next_level_communities = next(communities_generator)
print(next_level_communities)

sorted(map(sorted, next_level_communities))

print(next_level_communities)