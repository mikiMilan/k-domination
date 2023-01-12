from time import time
from greedy import greedy
from vns import vns
# from cplexKD import ILP
from BSH import beam_search_heuristic
from statistics import mean
from read_graph import read_graph
from multiprocessing import Process, Manager


def task(fun, g, k, b, r, i):
    curr = time()
    d = fun(g, k, b)
    time_execute = time() - curr

    # print(len(d), time_execute)
    r[i] = [len(d), time_execute]


if __name__ == '__main__':
    algs = [greedy, beam_search_heuristic, vns]
    # alg: int = int(input("Izaberite algoritam (0-greedy, 1-BS, 2-VNS, 3-ILP): "))
    # k: int = int(input("k-domination, k=: "))
    # n: int = int(input("Broj cvorova: "))
    # p: float = float(input("Gustina grana u procentima: "))

    city_instances = ['newcastle.txt', 'nottingham.txt', 'oxford.txt', 'plymouth.txt',
                      'sheffield.txt', 'southampton.txt', 'sunderland.txt', 'york.txt']

    for k in [4]:
        for instance in city_instances:
            for b in [4]:
                file_name_res = 'results/reimplBS/kk' + str(k) + '-bb' + str(b) + '.txt'

                graph_open = 'cities_small_instances/'+instance
                print("Reading graph!")
                g = read_graph(graph_open)
                print("Start: ", graph_open)
                times = []
                results = []
                manager = Manager()
                return_dict = manager.dict()
                procs = []
                for j in range(5):
                    for i in range(2):
                        print("Start procesing ", i)
                        p = Process(target=task, args=(algs[1], g, k, b, return_dict, j*2+i))
                        procs.append(p)
                        p.start()

                    for p in procs:
                        p.join()

                # print(return_dict)

                for i in range(10):
                    results.append(return_dict[i][0])
                    times.append(return_dict[i][1])

                with open(file_name_res, 'a') as f:
                    f.write(instance + "\n")
                    f.write('{}, {:.2f}, {}, {}\n'.format(min(results), mean(results), str(results), str(times)))
                    print(instance, k, b)
                    print('{}, {:.2f}, {}\n'.format(min(results), mean(results), str(times)))
