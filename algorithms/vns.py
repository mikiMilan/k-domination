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


def random_nodes(g: Graph or DiGraph) -> set:
    s = set()

    for v in g.nodes:
        if random() < 0.1:
            s.add(v)

    return s


def local_search_first_impr(s: set, g: Graph or DiGraph, nodes: list,neighbors: dict, k: int):
    improved = True
    curr_fit = fitness(s, g, k)

    while improved:
        improved = False

        shuffle(nodes)
        for v in nodes:
            if v in s:
                new_fit = fitness_rec_rem(s, v, curr_fit, g, neighbors, k)
                # s.remove(v)
                # new_fit = fitness(s, g, k)
                # s.add(v)
                if new_fit < curr_fit:
                    curr_fit = new_fit
                    s.remove(v)
                    improved = True
                    check_fit =  fitness(s, g, k)
                    if abs(check_fit-curr_fit)>0.000001:
                        print("Error in incremental fitness true fitness is "+str(check_fit)+" and incremental is "+str(curr_fit))
                        exit(1)
                    break
            else:
                new_fit = fitness_rec_add(s, v, curr_fit, g, neighbors, k)
                # s.add(v)
                # new_fit = fitness(s, g, k)
                # s.remove(v)
                if new_fit < curr_fit:
                    curr_fit = new_fit
                    s.add(v)
                    improved = True
                    check_fit =  fitness(s, g, k)
                    if abs(check_fit-curr_fit)>0.000001:
                        print("Error in incremental fitness true fitness is "+str(check_fit)+" and incremental is "+str(curr_fit))
                        exit(1)
                    break

    return curr_fit
    
    
def local_search_best_impr(s: set, g: Graph or DiGraph, nodes: list, neighbors: dict, k: int):
    improved = True
    curr_fit = fitness(s, g, k)

    while improved:
        improved = False
        best_fit = curr_fit
        best_v = None
        best_rem = None

        for v in nodes:
            if v in s:
                new_fit = fitness_rec_rem(s, v, curr_fit, g, neighbors, k)
                if new_fit < best_fit:
                    best_fit = new_fit
                    best_v = v
                    best_rem = True
                    improved = True
            else:
                new_fit = fitness_rec_add(s, v, curr_fit, g, neighbors, k)
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
            check_fit =  fitness(s, g, k)
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
    for v in graph.nodes:
        neighbors[v] = set(graph[v])

    s: set = ([]) # random_nodes(graph) # ACA: brze radi kad se instancira praznim resenjem
    fit = fitness(s, graph, k)
    s_accept = set(graph.nodes)
    
    while iteration < iteration_max and time()-start_time < time_execution:
        s_new = shaking(s, div, nodes)
        #s_new = shaking_new_not_so_good(s_accept, div, nodes, graph)
        # print("Fit: ", fitness(s_new, g, k), "velicine ", len(s_new))
        # if(is_acceptable_solution(graph, s_new, k)):
        #     print("s_new je dopustivo")
        fit_new = local_search_best_impr(s_new, graph, nodes, neighbors, k)
        # print("Fit_New: ", fit_new, "velicine ", len(s_new))
        # if (is_acceptable_solution(graph, s_new, k)):
        #     print("s_new je dopustivo")

        if fit_new < fit or (fit_new==fit and random()<0.5):
            #if fit_new==fit:
            #    print("Prelazim u isto kvalitetno")
            s = s_new
            div = divmin
            fit = fit_new

            #print("Fit: ", fit, "velicine ", len(s))
            if len(s_accept) > len(s) and is_acceptable_solution(graph, s, k):
                #print("Pronadjen!!!!!!!!! Vrijeme: ", time() - start_time)
                #print("++Fit: ", fit, "velicina dominacije ", len(s))
                #if len(s)==len(s_accept):
                #    print("Pronadjen iste dimenzije")
                s_accept = list(s)
                best_time = time() - start_time
        else:
            div += 1
            if div >= divmax:
                div = divmin

        iteration += 1
        if iteration%50 == 0:
            print("it={}\tt={}\td={}\tsize={}\tfit={:.5f}\tk={}\tinst={}".format(iteration, int(time() - start_time),div,  len(s), fit, k, instance_name))
    return s_accept, best_time


if __name__ == '__main__':
    g = read_graph("cities_small_instances/oxford.txt")

    print("The graph has been loaded!!!")

    curr = time()
    d1, bt = vns("oxford", g, k=8, d_min=1, d_max=20, time_execution=160, iteration_max=90000)
    time_execute = time() - curr

    print(len(d1), bt, time_execute)
