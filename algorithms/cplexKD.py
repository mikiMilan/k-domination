from time import time
from networkx import DiGraph, Graph, gnp_random_graph as rand_graph
from pulp import LpProblem, lpSum, LpVariable, LpMinimize, LpBinary, PULP_CBC_CMD, LpStatus, value


def ILP(graph: Graph or DiGraph, k: int, timelimit: float):

    model = LpProblem("k-domination", LpMinimize)
    y = LpVariable.dicts("x", list(graph.nodes),  0, 1, LpBinary)

    # objective function:
    model += lpSum([y[i] for i in list(graph.nodes)])
    # constraints for each vertex i in V:
    for i in list(graph.nodes):
        model += (k * y[i] + lpSum([y[j] for j in list(g[i])]) >= k)

    # run model:
    model.solve(PULP_CBC_CMD(maxSeconds=timelimit, msg=True, fracGap=0))
    # stats:
    print("Status solving: ", LpStatus[model.status])
    # print("Vars:")
    # for v in model.variables():
    # 	print(v.name, "===> ", v.varValue)

    print("Obj value: ", value(model.objective))
    return value(model.objective)


if __name__ == '__main__':
    size: int = 200
    timelimit: float = 30
    g = rand_graph(size, 0.5, seed=1)
    curr = time()
    d1 = ILP(g, 3, timelimit)
    time_execute = time() - curr
    print(time_execute, d1)