from time import time
from random import shuffle, random, randrange, seed
from math import sqrt
from networkx import DiGraph, Graph, gnp_random_graph as rand_graph
from unit import fitness, is_acceptable_solution, fitness_rec_rem, fitness_rec_add
from read_graph import read_graph


def shaking(s: set, div: int, nodes: list) -> set:
    sl = list(s)
    shuffle(sl)
    
    remove_cnt = div
    if remove_cnt> len(sl)//2:
        remove_cnt = len(sl)//2
        
    shak = set(sl[:len(sl)-remove_cnt])

    add_cnt = div
    shuffle(nodes)
    shak.union(set(nodes[:add_cnt]))

    return shak

def random_nodes(g: Graph or DiGraph) -> set:
    s = set()

    for v in g.nodes:
        if random() < 0.1:
            s.add(v)

    return s

def first_fitness_better(fit1, fit2):
    return fit1[0] < fit2[0] or (fit1[0]==fit2[0] and fit1[1]<fit2[1]) or (fit1[0]==fit2[0] and fit1[1]==fit2[1] and fit1[2]<fit2[2])

def fitness_equal(fit1, fit2):
    return not first_fitness_better(fit1, fit2) and not first_fitness_better(fit2, fit1)


adding_cnt = 0
removing_cnt = 0
ls3_tried = set()

def local_search_best_impr_phases(s: set, g: Graph or DiGraph, nodes: list, neighbors: dict, neighb_matrix: list, k: int, best_size_so_far: int, iteration: int):
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

    #print("Solution after simple additions and removals is "+str(curr_fit))
    # now swap nodes (in and out) to improve third element of fitness
    '''
    improved = False
    while improved:
        improved = False
        best_fit = curr_fit
        best_v1_rem = None
        best_v2_add = None

        for v1 in s:
            sp = s.copy()
            sp.remove(v1)
            cache = {}
            sp_fit = fitness(sp, g, k, cache)
            for v2 in nodes:
                if v2 in s:
                    continue
                new_sp_fit = fitness_rec_add(sp, v2, sp_fit, g, neighbors, neighb_matrix, k, cache)
                if new_sp_fit < best_fit:
                    best_fit = new_sp_fit
                    best_v1_rem = v1
                    best_v2_add = v2
                    improved = True
        
        if improved:
            print("LS2 improvement!")
            s.remove(best_v1_rem)
            s.add(best_v2_add)
            curr_fit = best_fit
            cache = {}
            check_fit =  fitness(s, g, k, cache)
            if not fitness_equal(curr_fit, check_fit):
                print("Error in incremental fitness true fitness is "+str(check_fit)+" and incremental is "+str(curr_fit))
                exit(1)

    # now fancy removal two nodes out and one new gets in (called LS3)
    # do it only if LS3 was not previously performed on this exact solution and if candidate solution has best size so far
    
    size_ok = curr_fit[1] == best_size_so_far
    s_list = list(s)
    s_list_sorted = sorted(s_list)
    s_sorted_string = "_".join([str(x) for x in s_list_sorted])
    tried_before = s_sorted_string in ls3_tried
    if size_ok and not tried_before and iteration%100==0 and iteration>0:
        improved = True
        ls3_tried.add(s_sorted_string)
        print("Doing LS3 for solution with fit "+str(curr_fit))
    else:
        improved = False
    while improved:
        improved = False
        best_fit = curr_fit
        best_v1_rem = None
        best_v2_rem = None
        best_v3_add = None

        for v1 in s:
            for v2 in s:
                if v1==v2:
                    continue
                sp = s.copy()
                sp.remove(v1)
                sp.remove(v2)
                cache = {}
                sp_fit = fitness(sp, g, k, cache)
                for v3 in nodes:
                    if v3 in s:
                        continue
                    new_sp_fit = fitness_rec_add(sp, v3, sp_fit, g, neighbors, neighb_matrix, k, cache)
                    if new_sp_fit < best_fit:
                        best_fit = new_sp_fit
                        best_v1_rem = v1
                        best_v2_rem = v2
                        best_v3_add = v3
                        improved = True
        
        if improved:
            print("LS3 improvement "+str(best_fit))
            s.remove(best_v1_rem)
            s.remove(best_v2_rem)
            s.add(best_v3_add)
            curr_fit = best_fit
            cache = {}
            check_fit =  fitness(s, g, k, cache)
            if not fitness_equal(curr_fit, check_fit):
                print("Error in incremental fitness true fitness is "+str(check_fit)+" and incremental is "+str(curr_fit))
                exit(1)'''

    return curr_fit


def vns(instance_name, graph: DiGraph or Graph, k: int, d_min: int, d_max: int, time_execution: int, iteration_max: int) -> list:
    # TODO: set this to be parameter 
    seed(12345)
    prob = 0.5
    divmin = d_min
    divmax = min(d_max, len(graph)/5)
    div = divmin
    iteration = 0
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

    s: set = ([]) # random_nodes(graph) # ACA: brze radi kad se instancira praznim resenjem
    fit = fitness(s, graph, k)
    s_accept = set(graph.nodes)
    
    while iteration < iteration_max and time()-start_time < time_execution:
        s_new = shaking(s, div, nodes)
        fit_new = local_search_best_impr_phases(s_new, graph, nodes, neighbors, neighb_matrix, k, len(s), iteration)

        if first_fitness_better(fit_new, fit) or (fitness_equal(fit, fit_new) and random() < prob): #and len(s_new.intersection(s))!=len(s_new) and
            #if fitness_equal(fit_new, fit):
            #    print("Prelazim u isto kvalitetno sa drugacijom internom strukturom")
            s = s_new
            div = divmin
            fit = fit_new

            if len(s_accept) > len(s) and is_acceptable_solution(graph, s, k):
                s_accept = list(s)
                best_time = time() - start_time
                divmax = int(len(s_accept)/2)
        else:
            div += 1
            if div >= divmax:
                div = divmin

        iteration += 1
        if iteration%100 == 0:
            print("it={:4d}\tt={:2d}\td={:2d}\tdmin={}\tdmax={}\tsize={}\tbest={}\tnew={}\tk={}\tinst={}".format(iteration, int(time() - start_time),div,divmin, divmax,  len(s), fit, fit_new, k, instance_name))
    return s_accept, best_time


if __name__ == '__main__':
    g = read_graph("cities_small_instances/glasgow.txt")

    print("The graph has been loaded!!!")

    curr = time()
    d1, bt = vns("oxford", g, k=1, d_min=1, d_max=20, time_execution=160, iteration_max=90000)
    time_execute = time() - curr

    print(len(d1), bt, time_execute)
