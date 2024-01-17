#ifndef KDOM_GRAPH_H
#define KDOM_GRAPH_H

int** loadGraphFromFile(const char *filename, int *numVertices);

void freeGraph(int** graph, int numVertices);

int* calculateDegree(int** adjacencyMatrix, int numVertices);

int** convertToAdjList(int** adjacencyMatrix, int numVertices, const int* degree);

#endif //KDOM_GRAPH_H
