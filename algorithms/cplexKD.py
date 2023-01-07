from time import time
from networkx import DiGraph, Graph, gnp_random_graph as rand_graph
from pulp import LpProblem, lpSum, LpVariable, LpMinimize, LpBinary, PULP_CBC_CMD, LpStatus, value
from read_graph import read_graph
import pulp as pl 
import orloge # pip install orloge
from os import remove
from math import ceil 

# define cplex path 
cplex_path = r'/home/marko/Desktop/CPLEX_Studio127/cplex/bin/x86-64_linux/cplex'
    
    
    
def ILP(graph: Graph or DiGraph, k: int, timelimit: float):

    model = LpProblem("k-domination", LpMinimize)
    y = LpVariable.dicts("x", list(graph.nodes),  0, 1, LpBinary)

    # objective function:
    model += lpSum([y[i] for i in list(graph.nodes)])
    # constraints for each vertex i in V:
    for i in list(graph.nodes):
        model += (k * y[i] + lpSum([y[j] for j in list(g[i])]) >= k)

    # run model:
    solver = pl.CPLEX_CMD(path=cplex_path, timelimit=timelimit, logPath="log_info.log")
    model.solve(solver)   #PULP_CBC_CMD(maxSeconds=timelimit, msg=True, fracGap=0))
    # stats:
    print("Status solving: ", LpStatus[model.status])
    # print("Vars:")
    # for v in model.variables():
    # 	print(v.name, "===> ", v.varValue)

    print("Obj value: ", value(model.objective))
    
    # retrieve gap: 
    logs_dict = orloge.get_info_solver("log_info.log", "CPLEX" ) # Orloge returns a dict with all logs info
    best_bound, best_solution = logs_dict["best_bound"], logs_dict["best_solution"]

    print("Best bound: ", best_bound) 
    remove("log_info.log")
    return best_solution, ceil(best_bound) 


if __name__ == '__main__':
    size: int = 200
    timelimit: float = 10
    #g = read_graph("cities_small_instances/bath.txt")
    g = read_graph("random_instances/NEW-V1000-P0.5-G1.txt")
    curr = time()
    primal, dual = ILP(g, 3, timelimit)
    time_execute = time() - curr
    print(time_execute, primal, dual)
