from networkx import DiGraph, Graph


def is_acceptable_solution(graph: DiGraph or Graph, D: list, k: int) -> bool:
    for v in graph.nodes:
        if v not in D and number_same_elements(set(graph[v]), D) < k:
            return False
    return True


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

    return objective_sum, len(g) - counter - len(s)/4.0


def fitness(s: set, g: Graph or DiGraph, k: int) -> float:
    objective_function, violating = obj_voi(s, g, k)
    return violating + float(objective_function) / (k*len(g))


def fitness_rec_rem(s: list, v: int, fit: float, g: Graph or DiGraph, k: int) -> float:

    for u in g[v]:
        if u not in s:
            neighbors = set(g[u])
            nse = number_same_elements(neighbors, s)

            fit -= min(k, nse)/float(k*len(g))

            if nse < k:
                fit += 1

    srem = list(s)
    srem.remove(v)

    for u in g[v]:
        if u not in s:
            neighbors = set(g[u])
            nse = number_same_elements(neighbors, s)

            fit += min(k, nse)/float(k*len(g))

            if nse < k:
                fit -= 1

    neighbors = set(g[v])
    nse = number_same_elements(neighbors, s)
    fit += min(k, nse) / float(k * len(g))
    if nse < k:
        fit -= 1

    return fit
