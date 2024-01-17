#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "kdomination.h"
#include "graph.h"
#include "unit.h"

int main() {

    struct Problem p;
    p.k=4;
    p.d_min = 4;
    p.d_max_init = 50;
    p.prob = 0.2;
    p.penalty = 0.005;
    p.time_limit = 7200;
    p.iteration_max = 1000000;
    p.rand_seed = 287311465;
    srand(p.rand_seed);
    //srand(time(NULL));

    struct Graph g;
    int numVertices;
    char location[] = "../cities_small_instances/manchester.txt";
//    char location[] = "../cities_big_instances/belgrade.txt";
    copy_string(g.name, location, 60);
    g.matrix = loadGraphFromFile(location, &numVertices);
    g.numVertices = numVertices;
    g.degree = calculateDegree(g.matrix, numVertices);
    g.adj = convertToAdjList(g.matrix, numVertices, g.degree);
    g.vertex = (int*)malloc(g.numVertices * sizeof(int));
    for (int i = 0; i < g.numVertices; ++i)
        g.vertex[i] = i;

    //---------------------------------------VNS-----------------------------------
    vns(&g, &p);
    //---------------------------------------VNS-----------------------------------

    //dealocation memori - mada i ne treba, ali nije odzgoreg
    if (g.matrix != NULL) {
        freeGraph(g.matrix, numVertices);
        free(g.degree);
        freeGraph(g.adj, numVertices);
    }

    return 0;
}
