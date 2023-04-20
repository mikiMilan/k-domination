from time import time
from random import sample, randint, shuffle
from test import VNS

class Test:
    def __init__(self, num_nodes) -> None:
        self.nodes = list(range(num_nodes))

    def shaking(self, s: set, d: int) -> set:
        s_len = len(s)

        x_prim = list(s)
        shuffle(x_prim)
        x_prim_len = s_len

        i = 0
        while i<d:
            del x_prim[randint(0, x_prim_len-i-1)]
            i += 1

        i = 0
        y_prim = set()
        shuffle(self.nodes)
        while i<d:
            if self.nodes[i] not in s:
                y_prim.add(self.nodes[i])
            i += 1

        return set(x_prim), y_prim
    
    def shaking2(self, s: set, d: int) -> set:
        sl = list(s)
        shuffle(sl)
            
        shak = set(sl[:len(sl)-d])

        shuffle(self.nodes)
        shak.union(set(self.nodes[:d]))

        return shak
    

if __name__ == '__main__':
    len_nodes = (1000, 10000, 100000)
    len_s = (100,200,500)
    for n, s in zip(len_nodes, len_s):
        t = Test(n)
        s = set(sample(range(0, n), s))
        for d in range(5,15,3):
            curr_time = time()
            t.shaking(s, d)
            print("new", time()-curr_time)
            curr_time = time()
            t.shaking2(s, d)
            print("old", time()-curr_time)

    t = dict()
    t[(1,2)] = '45'
    print(t)

    