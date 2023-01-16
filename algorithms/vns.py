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

    # TODO: maybe add_cnt should be bounded as well, which is not a practical problem when graphs are large enough
    add_cnt = div
    shuffle(nodes)
    shak.union(set(nodes[:add_cnt]))

    return shak
    
def shaking_new_not_so_good(s: set, div: int, nodes: list, g: Graph or DiGraph) -> set:
    sl = list(s)
    shuffle(sl)
    
    remove_cnt = div
    if remove_cnt> len(sl)//2:
        remove_cnt = len(sl)//2
        
    shak = set(sl[:len(sl)-remove_cnt])

    for i in range(len(sl)-remove_cnt, len(sl)):
        v = sl[i]
        neighb = list(g[v])
        if len(neighb)==0:
            continue
        shak.add(neighb[randrange(0,len(neighb))])

    return shak

def shaking_balanced(s: set, div: int, nodes: list, g: Graph or DiGraph) -> set:
    sl = list(s)
    shuffle(sl)
    
    remove_cnt = div
    if remove_cnt> len(sl)//2:
        remove_cnt = len(sl)//2
        
    shak = set(sl[:len(sl)-remove_cnt])

    # balanced add
    complement_size = len(g)-len(sl)
    dom_size = len(sl)
    if dom_size == 0:
        dom_size = 1
    add_cnt = int(complement_size * remove_cnt // dom_size)

    shuffle(nodes)
    shak.union(set(nodes[:add_cnt]))

    return shak

def shaking_smart(s: set, div: int, nodes: list, g: Graph or DiGraph) -> set:
    sl = list(s)
    shuffle(sl)
    
    remove_cnt = div
    if remove_cnt> len(sl)//2:
        remove_cnt = len(sl)//2
        
    shak = set(sl[:len(sl)-remove_cnt])

    # for each removed node v bring back one of the best candidates w.r.t. similar coverage 
    # the newly added node u should cover similar set of nodes as the removed node v did
    max_candidates_share = 1
    for i in range(len(sl)-remove_cnt, len(sl)):
        v = sl[i]
        v_neigh = set(g[v])
        intersect_size = {}
        for u in nodes:
            if u in s:
                continue
            intersect_size[u] = len(v_neigh.intersection(set(g[u])))
        max_candidates_cnt = int(max_candidates_share*len(intersect_size))
        sorted_candidates = sorted(intersect_size.items(), key=lambda item: item[1], reverse=True)[:max_candidates_cnt]
        shak.add(sorted_candidates[randrange(0, len(sorted_candidates))][0])


    return shak

def shaking_with_random_fix(s: set, div: int, nodes: list, g: Graph or DiGraph, k: int) -> set:
    sl = list(s)
    shuffle(sl)
    
    remove_cnt = div
    if remove_cnt> len(sl)//2:
        remove_cnt = len(sl)//2
        
    shak = set(sl[:len(sl)-remove_cnt])

    # randomly add new nodes until the solution becomes feasible
    while not is_acceptable_solution(g, shak, k):
        shak.add(nodes[randrange(0, len(nodes))])

    return shak



def random_nodes(g: Graph or DiGraph) -> set:
    s = set()

    for v in g.nodes:
        if random() < 0.1:
            s.add(v)

    return s


def local_search_first_impr(s: set, g: Graph or DiGraph, nodes: list,neighbors: dict, k: int):
    improved = True
    cache = {}
    curr_fit = fitness(s, g, k, cache)

    while improved:
        improved = False

        shuffle(nodes)
        for v in nodes:
            if v in s:
                new_fit = fitness_rec_rem(s, v, curr_fit, g, neighbors, k, cache)
                # s.remove(v)
                # new_fit = fitness(s, g, k)
                # s.add(v)
                if new_fit < curr_fit:
                    curr_fit = new_fit
                    s.remove(v)
                    improved = True
                    cache = {}
                    check_fit = fitness(s, g, k, cache)
                    if abs(check_fit-curr_fit) > 0.000001:
                        print("Error in incremental fitness true fitness is "+str(check_fit)+" and incremental is "+str(curr_fit))
                        exit(1)
                    break
            else:
                new_fit = fitness_rec_add(s, v, curr_fit, g, neighbors, k, cache)
                # s.add(v)
                # new_fit = fitness(s, g, k)
                # s.remove(v)
                if new_fit < curr_fit:
                    curr_fit = new_fit
                    s.add(v)
                    improved = True
                    cache = {}
                    check_fit =  fitness(s, g, k, cache)
                    if abs(check_fit-curr_fit)>0.000001:
                        print("Error in incremental fitness true fitness is "+str(check_fit)+" and incremental is "+str(curr_fit))
                        exit(1)
                    break

    return curr_fit
    
    
def local_search_best_impr(s: set, g: Graph or DiGraph, nodes: list, neighbors: dict, neighb_matrix: list, k: int):
    improved = True
    cache = {}
    curr_fit = fitness(s, g, k, cache)

    while improved:
        improved = False
        best_fit = curr_fit
        best_v = None
        best_rem = None

        for v in nodes:
            if v in s:
                new_fit = fitness_rec_rem(s, v, curr_fit, g, neighbors, neighb_matrix, k, cache)
                if new_fit < best_fit:
                    best_fit = new_fit
                    best_v = v
                    best_rem = True
                    improved = True
            else:
                new_fit = fitness_rec_add(s, v, curr_fit, g, neighbors, neighb_matrix, k, cache)
                if new_fit < best_fit:
                    best_fit = new_fit
                    best_v = v
                    best_rem = False
                    improved = True
        
        if improved:
            if best_rem:
                s.remove(best_v)
            elif not best_rem:
                s.add(best_v)
            else:
                raise Exception("Unexpected value for best_rem +"+str(best_rem))
            curr_fit = best_fit
            #if curr_fit<1:
            #print("Improved to "+str(curr_fit) + " with size "+str(len(s)) +" out of "+str(len(g)))
            cache = {}
            check_fit =  fitness(s, g, k, cache)
            if abs(check_fit-curr_fit)>0.000001:
                print("Error in incremental fitness true fitness is "+str(check_fit)+" and incremental is "+str(curr_fit))
                exit(1)

    return curr_fit


def vns(instance_name, graph: DiGraph or Graph, k: int, d_min: int, d_max: int, time_execution: int, iteration_max: int) -> list:
    # TODO: set this to be parameter 
    seed(12345)
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
        #s_new = shaking_balanced(s, div, nodes, graph)
        #s_new = shaking_smart(s, div, nodes, graph)
        #s_new = shaking_with_random_fix(s, div, nodes, graph, k)
        #s_new = shaking_new_not_so_good(s, div, nodes, graph)
        # print("Fit: ", fitness(s_new, g, k), "velicine ", len(s_new))
        # if(is_acceptable_solution(graph, s_new, k)):
        #     print("s_new je dopustivo")
        fit_new = local_search_best_impr(s_new, graph, nodes, neighbors, neighb_matrix, k)
        # print("Fit_New: ", fit_new, "velicine ", len(s_new))
        # if (is_acceptable_solution(graph, s_new, k)):
        #     print("s_new je dopustivo")

        if fit_new < fit or (fit_new == fit and random() < 0.5):
            #if fit_new==fit:
            #    print("Prelazim u isto kvalitetno")
            s = s_new
            div = divmin
            fit = fit_new

            #print("Fit: ", fit, "velicine ", len(s))
            if len(s_accept) > len(s) and is_acceptable_solution(graph, s, k):
                #print("Pronadjen!!!!!!!!! Vrijeme: ", time() - start_time)
                # print("++Fit: ", fit, "velicina dominacije ", len(s))
                #if len(s)==len(s_accept):
                #    print("Pronadjen iste dimenzije")
                s_accept = list(s)
                best_time = time() - start_time
                divmax = int(len(s_accept)/2)
        else:
            div += 1
            if div >= divmax:
                div = divmin

        iteration += 1
        if iteration%200 == 0:
            print("it={:4d}\tt={:2d}\td={:2d}\tdmin={}\tdmax={}\tsize={}\tfit={:.5f}\tk={}\tinst={}".format(iteration, int(time() - start_time),div,divmin, divmax,  len(s), fit, k, instance_name))
    return s_accept, best_time


if __name__ == '__main__':
    g = read_graph("cities_small_instances/glasgow.txt")

    print("The graph has been loaded!!!")

    curr = time()
    d1, bt = vns("oxford", g, k=1, d_min=1, d_max=20, time_execution=160, iteration_max=90000)
    time_execute = time() - curr

    print(len(d1), bt, time_execute)
