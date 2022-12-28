from networkx import \
    DiGraph, \
    gnp_random_graph as rand_graph, \
    is_connected, \
    draw_networkx


def f(l):
    del l[0]



if __name__ == '__main__':

    l = [1,2,3,4,5]

    print(l[:len(l)-2])
    print(l[2:])

#draw_networkx(g)
#plt.show()


