#ifndef KDOM_KDOMINATION_H
#define KDOM_KDOMINATION_H

struct Graph{
    char name[60];
    int** matrix;
    int** adj;
    int numVertices;
    int* degree;
    int* vertex;
};

struct Problem{
    int k;
    int d_min;
    int d_max_init;
    double prob;
    double penalty;
    int iteration_max;
    double time_limit;
    int rand_seed;
};

int verification(struct Graph *g, int* dom, int dom_len, int* dom_cache, int* fit_cache);

int fitness_rec_add(struct Graph *g, struct Problem *p, int v, const int dom_cache[], const int fit_cache[], int viol);

int fitness_rec_add_with_cache(struct Graph *g, struct Problem *p, int v, const int dom_cache[], int fit_cache[], int viol);

int fitness_rec_remove(struct Graph *g, struct Problem *p, int v, const int dom_cache[], const int fit_cache[], int viol);

int fitness_rec_remove_with_cache(struct Graph *g, struct Problem *p, int v, int dom_cache[], int fit_cache[], int viol);

int fitness(struct Graph *g, struct Problem *p, const int dom_cache[], int fit_cache[]);

int first_fitness_better(int viol1, int len1, int viol2, int len2, double penalty);

int fitness_equal(int viol1, int len1, int viol2, int len2);

void local_search_best(struct Graph *g, struct Problem *p, int dom[], int *dom_len, int dom_cache[], int fit_cache[], int *viol);

void local_search_remove_more(struct Graph *g, struct Problem *p, int* dom, int *dom_len, int* dom_cache, int* fit_cache, int *viol, int *indikator);
void local_search_remove_one(struct Graph *g, struct Problem *p, int dom[], int *dom_len, int dom_cache[], int fit_cache[], int *viol);

void local_search_bestADD_firstREM(struct Graph *g, struct Problem *p, int dom[], int *dom_len, int dom_cache[], int fit_cache[], int *viol, int *indikator);

void shaking(struct Graph *g, struct Problem *p, int dom[], int *dom_len, int dom_cache[], int fit_cache[], int numVertices, int d, int* viol);

void shaking_without_add(struct Graph *g, struct Problem *p, int dom[], int *dom_len, int dom_cache[], int fit_cache[], int d, int* viol);

void write_solve(struct Graph *g, struct Problem *p, int len_dom, int viol, double best_time, double total_time);

int fitness_equal_sol_dif(struct Graph *g,int viol1, int len1, const int dom1_cache[], int viol2, int len2, const int dom2_cache[]);

void vns(struct Graph *g, struct Problem *p);

#endif //KDOM_KDOMINATION_H
