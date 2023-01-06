from networkx import Graph


def read_graph(file_name: str) -> Graph:
    graph = Graph()
    with open(file_name, 'r') as f:
        line = f.readline()
        line = line.strip()
        line = line.split(" ")
        graph.add_nodes_from(range(int(line[0])))

        eggs = []
        for line in f.readlines():
            line = line.strip()
            line = line.split(" ")
            eggs.append((int(line[0]), int(line[1])))
        graph.add_edges_from(eggs)
    return graph


if __name__ == '__main__':
    g = read_graph("random_instances/NEW-V200-P0.2-G0.txt")
    print(g)

