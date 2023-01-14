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


def objective_function(s: list, g: Graph or DiGraph, k: int) -> int:
    objective_sum: int = 0

    for v in g.nodes:
        if v not in s:
            neighbors = set(g[v])
            objective_sum += min(k, number_same_elements(neighbors, s))

    return objective_sum


def violating(s: list, g: Graph or DiGraph, k: int) -> float:
    counter: int = 0

    for v in g.nodes:
        if v not in s:
            neighbors = set(g[v])
            counter += 1 if number_same_elements(neighbors, s) < k else 0

    return len(g) - counter #- len(s)/2.0 - bolje radi bez ovog


def obj_voi(s: set, g: Graph or DiGraph, k: int) -> (int, int):
    objective_sum: int = 0
    counter: int = 0

    for v in g.nodes:
        if v not in s:
            neighbors = set(g[v])
            nse = number_same_elements(neighbors, s)

            objective_sum += min(k, nse)

            if nse < k:
                counter += 1

    return objective_sum, len(g) - counter #- len(s)/4.0


def fitness(s: set, g: Graph or DiGraph, k: int) -> float:
    viol = 0
    for v in g.nodes:
        if v not in s:
            neighbors = set(g[v])
            nse = number_same_elements(neighbors, s)
            if nse < k:
                viol += 1

    return viol + float(len(s))/len(g)


def fitness_rec_rem(s: set, v: int, fit: float, g: Graph or DiGraph, all_neighbors: dict, k: int) -> float:
    srem = set(s)
    srem.remove(v)

    for u in g[v]:
        if u not in s: # then s not in 'srem' <== s intersect srem = s, srem / s = {v}, v not in g[v]
            neighbors = all_neighbors[u] # set(g[u])
            nse_s = number_same_elements(neighbors, s) # TODO: optimisation
            if nse_s < k:
                fit -= 1

            nse_srem = number_same_elements(neighbors, srem) # TODO: optimisation
            if nse_srem < k:
                fit += 1

    nse_srem = number_same_elements(set(g[v]), srem)
    if nse_srem < k:
        fit += 1

    return fit - 1.0/len(g)


def fitness_rec_add(s: set, v: int, fit: float, g: Graph or DiGraph, all_neighbors: dict, k: int) -> float:
    sadd = set(s)
    sadd.add(v)

    for u in g[v]:
        if u not in s:  # then s not in 'srem' <== s intersect srem = s, srem / s = {v}, v not in g[v]
            neighbors = all_neighbors[u] # set(g[u])
            nse_s = number_same_elements(neighbors, s)  # TODO: optimisation
            if nse_s < k:
                fit -= 1

            nse_sadd = number_same_elements(neighbors, sadd)  # TODO: optimisation
            if nse_sadd < k:
                fit += 1

    nse_s = number_same_elements(set(g[v]), s)
    if nse_s < k:
        fit -= 1

    return fit + 1.0/len(g)
