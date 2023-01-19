from time import time
from random import shuffle, random, randrange, seed
from math import sqrt
from networkx import DiGraph, Graph, gnp_random_graph as rand_graph
from unit import fitness, is_acceptable_solution, fitness_rec_rem, fitness_rec_add
from read_graph import read_graph


def shaking(s: set, div: int, nodes: list, fixed_nodes: set) -> set:
    sl = []
    for e in s:
        if e not in fixed_nodes:
            sl.append(e)
    shuffle(sl)

    if len(sl)+len(fixed_nodes) != len(s): # TODO: fixed_nodes in s?
        print("Error: Fixed element not in s!!!")
        exit(1)

    if div < len(sl):
        shak = set(sl[:len(sl)-div])

        shuffle(nodes)
        shak.union(set(nodes[:div]))
        shak.union(fixed_nodes)

        return shak
    else:
        pass # TODO: if div>divmin then div-=1 else END_ALGORITHM

    return s


def random_nodes(g: Graph or DiGraph) -> set:
    s = set()

    for v in g.nodes:
        if random() < 0.1:
            s.add(v)

    return s

def first_fitness_better(fit1, fit2):
    fit1Tot = (1+fit1[0])*(1+fit1[1]*0.01)
    fit2Tot = (1+fit2[0])*(1+fit2[1]*0.01)
    return fit1Tot<fit2Tot
    #return fit1[0] < fit2[0] or (fit1[0]==fit2[0] and fit1[1]<fit2[1]) or (fit1[0]==fit2[0] and fit1[1]==fit2[1] and fit1[2]<fit2[2])

def fitness_equal(fit1, fit2):
    return not first_fitness_better(fit1, fit2) and not first_fitness_better(fit2, fit1)


adding_cnt = 0
removing_cnt = 0
ls3_tried = set()

def local_search_best(s: set, g: Graph or DiGraph, nodes: list, neighbors: dict, neighb_matrix: list, k: int, best_size_so_far: int, iteration: int):
    global adding_cnt, removing_cnt, ls3_tried
    
    improved = True
    cache = {}
    curr_fit = fitness(s, g, k, cache)

    # adding nodes to achieve feasibility
    while improved:
        improved = False
        best_fit = curr_fit
        best_v = None

        for v in nodes:
            if v not in s:
                new_fit = fitness_rec_add(s, v, curr_fit, g, neighbors, neighb_matrix, k, cache)
                if first_fitness_better(new_fit, best_fit):
                    best_fit = new_fit
                    best_v = v
                    improved = True
        
        if improved:
            s.add(best_v)
            adding_cnt+=1
            #if adding_cnt%1000==0:
            #    print("Removals "+str(removing_cnt)+" Additions "+str(adding_cnt))
            curr_fit = best_fit
            cache = {}
            check_fit =  fitness(s, g, k, cache)
            if not fitness_equal(curr_fit, check_fit):
                print("Error in incremental fitness true fitness is "+str(check_fit)+" and incremental is "+str(curr_fit))
                exit(1)

    # now simple removal
    improved = True
    while improved:
        improved = False
        best_fit = curr_fit
        best_v = None

        for v in nodes:
            if v in s:
                new_fit = fitness_rec_rem(s, v, curr_fit, g, neighbors, neighb_matrix, k, cache)
                if first_fitness_better(new_fit, best_fit):
                    best_fit = new_fit
                    best_v = v
                    improved = True
        
        if improved:
            s.remove(best_v)
            removing_cnt+=1
            if adding_cnt%1000==0:
                print("Removals "+str(removing_cnt)+" Additions "+str(adding_cnt))
            curr_fit = best_fit
            cache = {}
            check_fit =  fitness(s, g, k, cache)
            if not fitness_equal(curr_fit, check_fit):
                print("Error in incremental fitness true fitness is "+str(check_fit)+" and incremental is "+str(curr_fit))
                exit(1)

    # if solution is not good we do not want to execute this expensive remove+swap-based LS 
    #print("Best size so far is "+str(best_size_so_far))
    #if len(s)>best_size_so_far+2:
    #    return curr_fit
    #if iteration%100!=0:
    return curr_fit


def vns(instance_name, graph: DiGraph or Graph, k: int, d_min: int, d_max: int, time_execution: int, iteration_max: int) -> list:
    # TODO: set this to be parameter 
    seed(12345)
    prob = 0.5
    divmin = d_min
    divmax = min(d_max, len(graph)/5)
    div = divmin
    iteration = 1
    start_time = time()
    best_time = 0
    nodes = list(graph.nodes) # kopiram cvorove zbog MJESANJA - necu da mjesam original
    
    neighbors = {}
    neighb_matrix = [[] for _ in range(len(graph.nodes))]
    for v in graph.nodes:
        neighbors[v] = set(graph[v])
        neighb_matrix[v] = [False]*len(graph.nodes)
        for u in graph[v]:
            neighb_matrix[v][u] = True

    s_accept = set([])
    for v in graph.nodes:
        if len(graph[v]) < k:
            s_accept.add(v)

    fixed_nodes = set(s_accept)

    fit = local_search_best(s_accept, graph, nodes, neighbors, neighb_matrix, k, len(nodes), 0)
    best_time = time()-start_time
    
    while iteration < iteration_max and time()-start_time < time_execution:
        s_new = shaking(s_accept, div, nodes, fixed_nodes)
        fit_new = local_search_best(s_new, graph, nodes, neighbors, neighb_matrix, k, fit[1], iteration)

        if first_fitness_better(fit_new, fit) or (fitness_equal(fit, fit_new) and random() < prob): #and len(s_new.intersection(s))!=len(s_new) and
            #if fitness_equal(fit_new, fit):
            #    print("Prelazim u isto kvalitetno sa drugacijom internom strukturom")
            if first_fitness_better(fit_new, fit):
                best_time = time() - start_time
            s_accept = s_new
            div = divmin
            fit = fit_new
            divmax = int(len(s_accept)/4)
        else:
            div += 1
            if div >= divmax:
                div = divmin

        iteration += 1
        if iteration%100== 0:
            print("it={:4d}\tt={:2d}\td={:2d}\tdmin={}\tdmax={}\tbest={}\tnew={}\tk={}\tinst={}".format(iteration, int(time() - start_time),div,divmin, divmax, fit, fit_new, k, instance_name))
    return s_accept, best_time


if __name__ == '__main__':
    g = read_graph("cities_small_instances/glasgow.txt")

    print("The graph has been loaded!!!")

    curr = time()
    d1, bt = vns("oxford", g, k=1, d_min=1, d_max=20, time_execution=160, iteration_max=90000)
    time_execute = time() - curr

    print(len(d1), bt, time_execute)
