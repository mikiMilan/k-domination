from time import time
from networkx import DiGraph, Graph
from pulp import LpProblem, lpSum, LpVariable, LpMinimize, LpBinary, PULP_CBC_CMD, LpStatus, value, LpSolution
from read_graph import read_graph
import pulp as pl 
import orloge # pip install orloge
from os import remove
from math import ceil 

# define cplex path 
#cplex_path = r'C:\Program Files\IBM\ILOG\CPLEX_Studio221\cplex\bin\x64_win64\cplex.exe'
cplex_path= r'/home/marko/Desktop/CPLEX_Studio127/cplex/bin/x86-64_linux/cplex'   

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
    
    #print("Problem status: ", LpStatus[model.status])
    #print("Solution status: ", LpSolution[model.sol_status])
    
    # retrieve gap: 
    logs_dict = orloge.get_info_solver("log_info.log", "CPLEX" ) # Orloge returns a dict with all logs info
    best_bound, best_solution, status = logs_dict["best_bound"], logs_dict["best_solution"], logs_dict["status"]
    #print("Best bound: ", best_bound) 
    #print(logs_dict["status"])
    remove("log_info.log")
    
    return best_solution, ceil(best_bound), int(status == "MIP - Integer optimal")#"MIP - Time limit exceeded" --if not optimal


if __name__ == '__main__':
    size: int = 200
    timelimit: float = 10
    g = read_graph("cities_small_instances/manchester.txt")
    # g = read_graph("random_instances/NEW-V1000-P0.2-G0.txt")
    curr = time()
    primal, dual, status = ILP(g, 2, timelimit)
    time_execute = time() - curr
    print(time_execute, primal, dual, status)
    
    
