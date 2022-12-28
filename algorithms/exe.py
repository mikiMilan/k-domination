from time import time
from networkx import gnp_random_graph as rand_graph
from greedy import greedy
from vns3 import vns
from vns2 import vns as myvns
from beamSearchHeuristic import beam_search_heuristic

if __name__ == '__main__':
    alg: int = int(input("Izaberite algoritam (0-greedy, 1-vns, 2-myvns, 3-beamS): "))
    k: int = int(input("k-domination, k=: "))
    n: int = int(input("Broj cvorova: "))
    # p: float = float(input("Gustina grana u procentima: "))

    for p in [0.2, 0.5, 0.8]:
        file_name = 'result/alg-'+str(alg)+' '+str(k)+'-dom num_ver-'+str(n)+' p-'+str(p)+'.txt'

        with open(file_name, 'w') as f:
            for i in range(15):
                print("Graph ", i)
                g = rand_graph(n, p, seed=i)
                algs = [greedy, vns, myvns, beam_search_heuristic]
                curr = time()
                d = algs[alg](g, k)
                time_execute = time() - curr
                print("KRAJ!! ---- " + str(time_execute) + " - " + str(len(d)))
                f.write(str(i) + " - " + str(time_execute) + " - " + str(len(d)) + "\n")