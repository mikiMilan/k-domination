#include <stdio.h>
#include <stdlib.h>
#include "graph.h"

// Funkcija za učitavanje grafa iz datoteke u matricu susedstva
int** loadGraphFromFile(const char *filename, int *numVertices) {
    FILE *file = fopen(filename, "r");

    if (file == NULL) {
        fprintf(stderr, "Neuspešno otvaranje datoteke %s.\n", filename);
        return NULL; // Vratite NULL ako otvaranje nije uspelo
    }

    // Učitaj broj čvorova
    if (fscanf(file, "%d %*d", numVertices) != 1) {
        fprintf(stderr, "Nije moguće pročitati broj čvorova.\n");
        fclose(file);
        return NULL;
    }

    // Alociraj dinamički matricu na hipu
    int** graph = (int**)malloc(*numVertices * sizeof(int*));
    for (int i = 0; i < *numVertices; ++i) {
        graph[i] = (int*)malloc(*numVertices * sizeof(int));
    }

    // Inicijalizuj matricu na 0
    for (int i = 0; i < *numVertices; ++i) {
        for (int j = 0; j < *numVertices; ++j) {
            graph[i][j] = 0;
        }
    }

    // Učitaj ivice grafa i popuni matricu susedstva
    int vertex1, vertex2;
    while (fscanf(file, "%d %d", &vertex1, &vertex2) == 2) {
        // Dodajte ivicu u matricu susedstva
        graph[vertex1][vertex2] = 1;
        graph[vertex2][vertex1] = 1; // Budući da je graf neusmeren, dodajemo i za drugi smer
    }

    fclose(file);
    return graph; // Vrati pokazivač na dinamički alociranu matricu
}

// Funkcija za oslobađanje memorije zauzete za matricu
void freeGraph(int** graph, int numVertices) {
    for (int i = 0; i < numVertices; ++i) {
        free(graph[i]);
    }
    free(graph);
}

int* calculateDegree(int** adjacencyMatrix, int numVertices) {
    int* degree = (int*)malloc(numVertices * sizeof(int));

    for (int i = 0; i < numVertices; ++i) {
        degree[i] = 0;

        for (int j = 0; j < numVertices; ++j) {
            if (adjacencyMatrix[i][j] == 1) {
                degree[i]++;
            }
        }
    }

    return degree;
}

int** convertToAdjList(int** adjacencyMatrix, int numVertices, const int* degree) {
    int** adjList = (int**)malloc(numVertices * sizeof(int*));

    for (int i = 0; i < numVertices; ++i) {
        adjList[i] = (int*)malloc((degree[i]) * sizeof(int));
        int k=0;
        for (int j = 0; j <= numVertices; ++j)
            if (adjacencyMatrix[i][j]==1)
                adjList[i][k++] = j;
    }

    return adjList;
}