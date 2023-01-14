from time import time
from random import shuffle, random
from math import sqrt
from networkx import DiGraph, Graph, gnp_random_graph as rand_graph
from unit import fitness, is_acceptable_solution, fitness_rec_rem, fitness_rec_add
from read_graph import read_graph


def shaking(s: set, div: int, nodes: list) -> set:
    sl = list(s)
    shuffle(sl)
    shak = set(sl[:len(sl)-div])

    shuffle(nodes)
    shak.union(set(nodes[:div]))

    return shak


def random_nodes(g: Graph or DiGraph) -> set:
    s = set()

    for v in g.nodes:
        if random() < 0.5:
            s.add(v)

    return s


def local_search_first_impr(s: set, g: Graph or DiGraph, nodes: list, k: int):
    improved = True
    curr_fit = fitness(s, g, k)

    while improved:
        improved = False

        shuffle(nodes)
        for v in nodes:
            if v in s:
                new_fit = fitness_rec_rem(s, v, curr_fit, g, k)
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
                new_fit = fitness_rec_add(s, v, curr_fit, g, k)
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
    
    
def local_search(s: set, g: Graph or DiGraph, nodes: list, k: int):
    improved = True
    curr_fit = fitness(s, g, k)

    while improved:
        improved = False
        best_fit = curr_fit
        best_v = None
        best_rem = None

        for v in nodes:
            if v in s:
                new_fit = fitness_rec_rem(s, v, curr_fit, g, k)
                if new_fit < best_fit:
                    best_fit = new_fit
                    best_v = v
                    best_rem = True
                    improved = True
            else:
                new_fit = fitness_rec_add(s, v, curr_fit, g, k)
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
            #    print("Improved to feasible "+str(curr_fit) + " with size "+str(len(s)))
            check_fit =  fitness(s, g, k)
            if abs(check_fit-curr_fit)>0.000001:
                print("Error in incremental fitness true fitness is "+str(check_fit)+" and incremental is "+str(curr_fit))
                exit(1)

    return curr_fit


def vns(instance_name, graph: DiGraph or Graph, k: int, d_min: int, d_max: int, time_execution: int, iteration_max: int) -> list:
    divmin = d_min
    divmax = min(d_max, len(graph)/5)
    div = divmin
    iteration = 0
    start_time = time()
    best_time = 0
    nodes = list(graph.nodes) # kopiram cvorove zbog MJESANJA - necu da mjesam original

    s: set = random_nodes(graph)
    fit = fitness(s, graph, k)

    s_accept = set(graph.nodes)
    while iteration < iteration_max and time()-start_time < time_execution:
        s_new = shaking(s, div, nodes)
        # print("Fit: ", fitness(s_new, g, k), "velicine ", len(s_new))
        # if(is_acceptable_solution(graph, s_new, k)):
        #     print("s_new je dopustivo")
        fit_new = local_search(s_new, graph, nodes, k)
        # print("Fit_New: ", fit_new, "velicine ", len(s_new))
        # if (is_acceptable_solution(graph, s_new, k)):
        #     print("s_new je dopustivo")

        if fit_new < fit:
            s = s_new
            div = divmin
            fit = fit_new

            #print("Fit: ", fit, "velicine ", len(s))
            if len(s_accept) > len(s) and is_acceptable_solution(graph, s, k):
                #print("Pronadjen!!!!!!!!! Vrijeme: ", time() - start_time)
                #print("++Fit: ", fit, "velicina dominacije ", len(s))
                s_accept = list(s)
                best_time = time() - start_time
        else:
            div += 1
            if div >= divmax:
                div = divmin

        iteration += 1
        #if iteration%1 == 0:
        print("it={}\tt={}\td={}\tinst={}\tk={}\tsize={}\tfit={:.5f}".format(iteration, int(time() - start_time),div, instance_name, k, len(s), fit))
    return s_accept, best_time


if __name__ == '__main__':
    g = read_graph("cities_small_instances/oxford.txt")

    print("The graph has been loaded!!!")

    curr = time()
    d1, bt = vns("oxford", g, k=8, d_min=1, d_max=20, time_execution=160, iteration_max=90000)
    time_execute = time() - curr

    print(len(d1), bt, time_execute)
