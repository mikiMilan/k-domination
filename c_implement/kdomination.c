#include "kdomination.h"
#include "unit.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void vns(struct Graph *g, struct Problem *p){
    clock_t start = clock();
    double best_time = 0.0, total_time;
    int dom[g->numVertices],
    new_dom[g->numVertices],
    dom_cache[g->numVertices],
    new_dom_cache[g->numVertices],
    fit_cache[g->numVertices],
    new_fit_cache[g->numVertices],
    number_additions[g->numVertices];
    int dom_len = 0,
    new_dom_len,
    viol,
    new_viol,
    iteration =1,
    d = p->d_min,
    d_max = p->d_max_init,
    new_d_max,
    condition1,
    condition2,
    condition3,
    indikator = 0;

    for (int i = 0; i < g->numVertices; ++i) {
        dom_cache[i] = 0; // vertex 'i' not in dom[]
        fit_cache[i] = 0; // fitness of vertex 'i' is unknown
    }

    viol = fitness(g, p, dom_cache, fit_cache);
    shuffle(g->vertex, g->numVertices);
    local_search_best(g, p, dom, &dom_len, dom_cache, fit_cache, &viol);
    printf("Fit: %.5f\n", fit(viol, dom_len, p->penalty));

    if (viol==0)
        best_time = ((double) (clock() - start)) / CLOCKS_PER_SEC;

    while (iteration < p->iteration_max &&  total_time < p->time_limit) {


        new_dom_len = dom_len;
        new_viol = viol;
        copy(new_dom, dom, dom_len);
        copy(new_dom_cache, dom_cache, g->numVertices);
        copy(new_fit_cache, fit_cache, g->numVertices);


//        if (iteration%10<8){
//            shaking(g, p, new_dom, &new_dom_len, new_dom_cache, new_fit_cache, g->numVertices, d, &new_viol);
            shaking_without_add(g, p, new_dom, &new_dom_len, new_dom_cache, new_fit_cache, d, &new_viol);
            shuffle(g->vertex, g->numVertices);
            local_search_bestADD_firstREM(g, p, new_dom, &new_dom_len, new_dom_cache, new_fit_cache, &new_viol, &indikator);
//        }else{
//            shaking(g, p, new_dom, &new_dom_len, new_dom_cache, new_fit_cache, g->numVertices, d, &new_viol);
//            shuffle(g->vertex, g->numVertices);
//            local_search_best(g, p, new_dom, &new_dom_len, new_dom_cache, new_fit_cache, &new_viol);
//        }

        condition1 = first_fitness_better(new_viol, new_dom_len, viol, dom_len, p->penalty);
        condition2 = fitness_equal_sol_dif(g,new_viol, new_dom_len, new_dom_cache, viol, dom_len, dom_cache) && ((double )rand()/RAND_MAX) < p->prob;
        condition3 = new_viol==0;

        if ((condition1 || condition2) && condition3){
            if (condition1)
                best_time = ((double) (clock() - start)) / CLOCKS_PER_SEC;

            dom_len = new_dom_len;
            viol = new_viol;
            copy(dom, new_dom, new_dom_len);
            copy(dom_cache,new_dom_cache,  g->numVertices);
            copy(fit_cache, new_fit_cache, g->numVertices);

            d = p->d_min;
/*izmjena*/            new_d_max = (dom_len > 4) ? dom_len / 2  : p->d_max_init;
            d_max = (new_d_max > p->d_max_init) ? p->d_max_init : new_d_max;
        } else {
            d += 1;
            if (d >= d_max)
                d = p->d_min;
        }

        iteration += 1;
        if (iteration%100 == 0) {
            printf("it=%5d t=%5.2f\tfit=%.5f\tlen=%d\tbest_time=%.4f\td=%d\n",
                   iteration,
                   ((double) (clock() - start)) / CLOCKS_PER_SEC,
                   fit(viol, dom_len, p->penalty),
                   dom_len,
                   best_time, d);
        }

        total_time = ((double) (clock() - start)) / CLOCKS_PER_SEC;
    }
    write_solve(g, p, dom_len, viol, best_time, total_time);
}

int verification(struct Graph *g, int* dom, int dom_len, int* dom_cache, int* fit_cache){


    for (int i = 0; i < dom_len; ++i) {
        if(dom_cache[dom[i]]!=1){
            printf("dom i dom_cath nisu usaglaseni>dom[%d]=%d\n", i, dom[i]);
            return 1;
        }
    }

    return 0;
}

// function will change: dom, dom_len, dom_cache, fit_cache, viol - not change 'g' and 'p'
void local_search_best(struct Graph *g, struct Problem *p, int dom[], int *dom_len, int dom_cache[], int fit_cache[], int *viol){
    int improved = 1,
            current_viol = *viol,
            current_len = *dom_len,
            best_viol,
            best_len,
            best_vertex,
            new_len,
            new_viol,
            index_best_vertex,
            i, // for loop
    u; // vertex

    //adding nodes to achieve feasibility
    while (improved) {
        improved = 0;
        best_viol = current_viol;
        best_len = current_len;

        for (i = 0; i < g->numVertices; ++i) {
            u = g->vertex[i];
            if (dom_cache[u] == 0) {
                new_len = current_len + 1;
                new_viol = fitness_rec_add(g, p, u, dom_cache, fit_cache, current_viol);
                if (first_fitness_better(new_viol, new_len, best_viol, best_len, p->penalty)) {
                    best_viol = new_viol;
                    best_len = new_len;
                    best_vertex = u;
                    improved = 1;
                }
            }
        }

        if (improved){
            // add best vertex
            dom[current_len] = best_vertex;
            dom_cache[best_vertex] = 1;
            current_len++;
            // fix fit_cache
            current_viol = fitness_rec_add_with_cache(g, p, best_vertex, dom_cache, fit_cache, current_viol);
        }
    }

    improved = 1;
    while (improved) {
        improved = 0;
        best_viol = current_viol;
        best_len = current_len;
        for (i = 0; i < g->numVertices; ++i) {
            u = g->vertex[i];
            if (dom_cache[u] == 1) {
                new_len = current_len - 1;
                new_viol = fitness_rec_remove(g, p, u, dom_cache, fit_cache, current_viol);
                if (first_fitness_better(new_viol, new_len, best_viol, best_len, p->penalty)) {
                    best_viol = new_viol;
                    best_len = new_len;
                    best_vertex = u;
                    improved = 1;
                }
            }
        }

        if (improved) {
            // remove element
            index_best_vertex = -1;
            for (i = 0; i < g->numVertices; ++i)
                if (dom[i] == best_vertex) {
                    index_best_vertex = i;
                    break;
                }
            dom[index_best_vertex] = dom[current_len - 1];
            dom_cache[best_vertex] = 0;
            current_len--;
            // fix fit_cache
            current_viol = fitness_rec_remove_with_cache(g, p, best_vertex, dom_cache, fit_cache, current_viol);
        }
    }

    *viol = current_viol;
    *dom_len = current_len;

}

// function will change: dom, dom_len, dom_cache, fit_cache, viol - not change 'g' and 'p'
void local_search_bestADD_firstREM(struct Graph *g, struct Problem *p, int dom[], int *dom_len, int dom_cache[], int fit_cache[], int *viol, int *indikator){

    int best_vertices[g->numVertices];

    int improved = 1,
    current_viol = *viol,
    current_len = *dom_len,
    best_viol,
    best_len,
    best_vertex,
    new_len,
    new_viol,
    best_vertices_len=0,
    i, // for loop
    u; // vertex

    //adding nodes to achieve feasibility
    while (improved) {
        improved = 0;
        best_viol = current_viol;
        best_len = current_len;

        for (i = 0; i < g->numVertices; ++i) {
            u = g->vertex[i];
            if (dom_cache[u] == 0) {
                new_len = current_len + 1;
                new_viol = fitness_rec_add(g, p, u, dom_cache, fit_cache, current_viol);
                if (first_fitness_better(new_viol, new_len, best_viol, best_len, p->penalty)) {
                    best_viol = new_viol;
                    best_len = new_len;
                    best_vertices_len=0;
                    best_vertices[best_vertices_len] = u;
                    best_vertices_len++;
                    improved = 1;
                }else if(fitness_equal(new_viol, new_len, best_viol, best_len)){
                    best_vertices[best_vertices_len] = u;
                    best_vertices_len++;
                }
            }
        }

        if (improved){
            shuffle(best_vertices, best_vertices_len);
//            shuffle_sort(best_vertices, best_vertices_len, num_add);
//            best_vertices_len = (best_vertices_len>4) ? 4 : best_vertices_len;
            for (int j = 0; j < best_vertices_len; ++j) {
                best_vertex = best_vertices[j];
                // add best vertex
                dom[current_len] = best_vertex;
                dom_cache[best_vertex] = 1;
                current_len++;
                // fix fit_cache
                current_viol = fitness_rec_add_with_cache(g, p, best_vertex, dom_cache, fit_cache, current_viol);
            }
        }
    }

//    shuffle(dom, current_len);
//    for (i = 0; i < current_len; ++i) {
//        u = dom[i];
//        new_len = current_len - 1;
//        new_viol = fitness_rec_remove(g, p, u, dom_cache, fit_cache, current_viol);
//        if (first_fitness_better(new_viol, new_len, current_viol, current_len, p->penalty)) {
//            // remove element
//            for (int j = i; j < current_len - 1; ++j)
//                dom[j] = dom[j + 1];
////                dom[i] = dom[current_len - 1];
//            dom_cache[u] = 0;
//            current_len--;
//            // fix fit_cache
//            current_viol = fitness_rec_remove_with_cache(g, p, u, dom_cache, fit_cache, current_viol);
//            i--;
//        }
//    }


    local_search_remove_more(g, p, dom, &current_len, dom_cache, fit_cache, &current_viol, indikator);

    *viol = current_viol;
    *dom_len = current_len;

}

void local_search_remove_more(struct Graph *g, struct Problem *p, int* dom, int *dom_len, int* dom_cache, int* fit_cache, int *viol, int *indikator){

    int best_viol = *viol,
    best_len = *dom_len,
    copy_viol,
    copy_dom_len,
    new_len,
    new_viol,
    i, // for loop
    u; // vertex

    int copy_dom[*dom_len],
    copy_dom_cache[g->numVertices],
    copy_fit_cache[g->numVertices],
    best_dom[*dom_len],
    best_dom_cache[g->numVertices],
    best_fit_cache[g->numVertices];

    copy(best_dom, dom, *dom_len);
    copy(best_dom_cache, dom_cache, g->numVertices);
    copy(best_fit_cache, fit_cache, g->numVertices);


    for (int j = 0; j < (*dom_len); ++j) {

//        int t= dom[0];
//        for (int k = 1; k < (*dom_len); ++k) {
//            dom[k-1] = dom[k];
//        }
//        dom[*dom_len-1] = t;

        copy(copy_dom, dom, *dom_len);
        copy(copy_dom_cache, dom_cache, g->numVertices);
        copy(copy_fit_cache, fit_cache, g->numVertices);
        copy_dom_len = *dom_len;
        copy_viol = *viol;

        shuffle(copy_dom, copy_dom_len);
        for (i = 0; i < copy_dom_len; ++i) {
            u = copy_dom[i];
            if(u>=g->numVertices || u<0) {
                printf("U=%d, len=%d, i=%d, indikator=%d\n", u, copy_dom_len, i, (*indikator));
                (*indikator)++;
            }
            new_len = copy_dom_len - 1;
            new_viol = fitness_rec_remove(g, p, u, copy_dom_cache, copy_fit_cache, copy_viol);
            if (first_fitness_better(new_viol, new_len, copy_viol, copy_dom_len, p->penalty)) {
                // remove element
//                for (int l = i; l < copy_dom_len - 1; ++l)
//                    copy_dom[l] = copy_dom[l + 1];
                copy_dom[i] = copy_dom[copy_dom_len - 1];
                copy_dom_cache[u] = 0;
                copy_dom_len--;
                // fix fit_cache
                copy_viol = fitness_rec_remove_with_cache(g, p, u, copy_dom_cache, copy_fit_cache, copy_viol);
                i--;
            }
        }

        if (first_fitness_better(copy_viol, copy_dom_len, best_viol, best_len, p->penalty)){
            best_len = copy_dom_len;
            best_viol = copy_viol;

            copy(best_dom, copy_dom, copy_dom_len);
            copy(best_dom_cache, copy_dom_cache, g->numVertices);
            copy(best_fit_cache, copy_fit_cache, g->numVertices);
        }
    }

//    printf("Best fit=%f\n", fit(best_viol, best_len, p->penalty));
    *viol = best_viol;
    *dom_len = best_len;

    copy(dom, best_dom, best_len);
    copy(dom_cache, best_dom_cache, g->numVertices);
    copy(fit_cache, best_fit_cache, g->numVertices);
}

void local_search_remove_one(struct Graph *g, struct Problem *p, int dom[], int *dom_len, int dom_cache[], int fit_cache[], int *viol){

    int copy_viol,
            copy_dom_len,
            new_len,
            new_viol,
            i, // for loop
    u; // vertex

    int copy_dom[*dom_len],
            copy_dom_cache[g->numVertices],
            copy_fit_cache[g->numVertices];

    copy(copy_dom, dom, *dom_len);
    copy(copy_dom_cache, dom_cache, g->numVertices);
    copy(copy_fit_cache, fit_cache, g->numVertices);
    copy_dom_len = *dom_len;
    copy_viol = *viol;

    shuffle(copy_dom, copy_dom_len);
    for (i = 0; i < copy_dom_len; ++i) {
        u = copy_dom[i];
        new_len = copy_dom_len - 1;
        new_viol = fitness_rec_remove(g, p, u, copy_dom_cache, copy_fit_cache, copy_viol);
        if (first_fitness_better(new_viol, new_len, copy_viol, copy_dom_len, p->penalty)) {
            // remove element
//                for (int l = i; l < copy_dom_len - 1; ++l)
//                    copy_dom[l] = copy_dom[l + 1];
            copy_dom[i] = copy_dom[copy_dom_len - 1];
            copy_dom_cache[u] = 0;
            copy_dom_len--;
            // fix fit_cache
            copy_viol = fitness_rec_remove_with_cache(g, p, u, copy_dom_cache, copy_fit_cache, copy_viol);
            i--;
        }

    }

    *viol = copy_viol;
    *dom_len = copy_dom_len;

    copy(dom, copy_dom, copy_dom_len);
    copy(dom_cache, copy_dom_cache, g->numVertices);
    copy(fit_cache, copy_fit_cache, g->numVertices);
}

int first_fitness_better(int viol1, int len1, int viol2, int len2, double penalty){
    return fit(viol1,len1, penalty)<fit(viol2,len2, penalty);
}

int fitness_equal(int viol1, int len1, int viol2, int len2){
    return viol1==viol2 & len1==len2;
}

int fitness_equal_sol_dif(struct Graph *g,int viol1, int len1, const int dom1_cache[], int viol2, int len2, const int dom2_cache[]){
    if (viol1!=viol2 || len1!=len2)
        return 0;

    for (int i = 0; i < g->numVertices; ++i)
        if (dom1_cache[i] != dom2_cache[i])
            return 1;

    return 0;
}

// function will change: fit_cache
int fitness(struct Graph *g, struct Problem *p, const int dom_cache[], int fit_cache[]){
    int viol = 0;

    for (int i = 0; i < g->numVertices; ++i)
        if (dom_cache[i] == 0) {  // vertex i not in dom
            int nse = number_same_elements(dom_cache, g->adj[i], g->degree[i]);
            if (nse < p->k)
                viol += p->k - nse;
            fit_cache[i] = nse;
        }

    return viol;
}

//----------------------------- Fitness  -  ADD  -------------------------------------------------------------------
int fitness_rec_add(struct Graph *g, struct Problem *p, int v, const int dom_cache[], const int fit_cache[], int viol){
    int new_viol = viol;

    // visit the neighbors of node V
    for (int i = 0; i < g->degree[v]; ++i){
        int u = g->adj[v][i];
        if (dom_cache[u]==0){ // u not in dom
            int nseS = fit_cache[u];
            if (nseS < p->k)
                new_viol -= (p->k) - nseS;

            int nseNewS = nseS;
            if (g->matrix[v][u])
                nseNewS+=1;
            if (nseNewS < p->k)
                new_viol += (p->k) - nseNewS;
        }
    }

    int nseS = fit_cache[v];
    if (nseS < p->k)
        new_viol -= (p->k) - nseS;

    return new_viol;
}

int fitness_rec_add_with_cache(struct Graph *g, struct Problem *p, int v, const int dom_cache[], int fit_cache[], int viol){
    int new_viol = viol;

    // visit the neighbors of node V
    for (int i = 0; i < g->degree[v]; ++i){
        int u = g->adj[v][i];
        if (dom_cache[u]==0){ // u not in dom
            int nseS = fit_cache[u];
            if (nseS < p->k)
                new_viol -= (p->k) - nseS;

            int nseNewS = nseS;
            if (g->matrix[v][u]==1)
                nseNewS+=1;
            if (nseNewS < p->k)
                new_viol += (p->k) - nseNewS;

            fit_cache[u] = nseNewS;
        }
    }

    int nseS = fit_cache[v];
    if (nseS < p->k)
        new_viol -= (p->k) - nseS;

    fit_cache[v] = 0;

    return new_viol;
}

//-----------------------------Fitness  -  REMOVE  ----------------------------------------------------------------
int fitness_rec_remove(struct Graph *g, struct Problem *p, int v, const int dom_cache[], const int fit_cache[], int viol){
    int new_viol = viol;

    // visit the neighbors of node V
    for (int i = 0; i < g->degree[v]; ++i){
        int u = g->adj[v][i];
        if (dom_cache[u]==0){ // u not in dom
            int nseS = fit_cache[u];
            if (nseS < p->k)
                new_viol -= (p->k) - nseS;

            int nseNewS = nseS;
            if (g->matrix[v][u])
                nseNewS -= 1;
            if (nseNewS < p->k)
                new_viol += (p->k) - nseNewS;
        }
    }


    int new_dom_cache[g->numVertices];
    for (int i = 0; i < g->numVertices; ++i)
        new_dom_cache[i] = dom_cache[i];
    new_dom_cache[v] = 0;
    int nseS = number_same_elements(new_dom_cache, g->adj[v], g->degree[v]);

    if (nseS < p->k)
        new_viol += (p->k) - nseS;

    return new_viol;
}

int fitness_rec_remove_with_cache(struct Graph *g, struct Problem *p, int v, int dom_cache[], int fit_cache[], int viol){
    int new_viol = viol;

    // visit the neighbors of node V
    for (int i = 0; i < g->degree[v]; ++i){
        int u = g->adj[v][i];
        if (dom_cache[u]==0){ // u not in dom
            int nseS = fit_cache[u];
            if (nseS < p->k)
                new_viol -= (p->k) - nseS;

            int nseNewS = nseS;
            if (g->matrix[v][u])
                nseNewS -= 1;
            if (nseNewS < p->k)
                new_viol += (p->k) - nseNewS;

            fit_cache[u] = nseNewS;
        }
    }

    int nseS = number_same_elements(dom_cache, g->adj[v], g->degree[v]);
    fit_cache[v] = nseS;

    if (nseS < p->k)
        new_viol += (p->k) - nseS;

    return new_viol;
}

void shaking(struct Graph *g, struct Problem *p, int dom[], int *dom_len, int dom_cache[], int fit_cache[], int numVertices, int d, int* viol){
    int index, element;
    // random delete
    for (int i = 0; i < d; ++i) {
        index = rand() % (*dom_len);
        element = dom[index];
        if (g->degree[element] < p->k){
            i--;
            continue;
        }
        dom_cache[element] = 0;
        dom[index] = dom[*dom_len-1];
        (*dom_len)--;

        *viol = fitness_rec_remove_with_cache(g, p, element, dom_cache, fit_cache, *viol);
    }

    // random add
    for (int i = 0; i < d; ++i) {
        element = random(numVertices - 1);
        if (dom_cache[element]==1)
            continue;
        dom_cache[element] = 1;
        dom[*dom_len] = element;
        (*dom_len)++;

        *viol = fitness_rec_add_with_cache(g, p, element, dom_cache, fit_cache, *viol);
    }

    shuffle(dom, *dom_len);
}

void shaking_without_add(struct Graph *g, struct Problem *p, int dom[], int *dom_len, int dom_cache[], int fit_cache[], int d, int* viol){
    int index, element;
    // random delete
    for (int i = 0; i < d; ++i) {
        index = rand() % (*dom_len);
        element = dom[index];
        if (g->degree[element] <= p->k){
            i--;
            continue;
        }
        dom_cache[element] = 0;
        dom[index] = dom[(*dom_len)-1];
        (*dom_len)--;

        *viol = fitness_rec_remove_with_cache(g, p, element, dom_cache, fit_cache, *viol);
    }


//    // random add
//    for (int i = 0; i < d; ++i) {
//        element = random(g->numVertices - 1);
//        if (dom_cache[element]==1)
//            continue;
//        dom_cache[element] = 1;
//        dom[*dom_len] = element;
//        (*dom_len)++;
//
//        *viol = fitness_rec_add_with_cache(g, p, element, dom_cache, fit_cache, *viol);
//    }
//
//    shuffle(dom, *dom_len);
//
//    if (iteration%100==0){
//        int num_min_add = 0, brojac=0;
//        for (int i = 0; i < g->numVertices; ++i) {
//            if(num_add[g->vertex[i]]== num_min_add && g->degree[g->vertex[i]]>p->k) {
//        //                        printf("v=%d,", g->vertex[i]);
//                brojac++;
//            }
//        }
//        printf("----broj nedaodanih:%d-----\n", brojac);
//
//        if(brojac < *dom_len){
//
//            for (int i = 0; i < g->numVertices; ++i) {
//                if(num_add[g->vertex[i]]== num_min_add && g->degree[g->vertex[i]]>p->k) {
//                    dom_cache[g->vertex[i]] = 1;
//                    dom[*dom_len] = g->vertex[i];
//                    (*dom_len)++;
//
//                    *viol = fitness_rec_add_with_cache(g, p, g->vertex[i], dom_cache, fit_cache, *viol);
//                }
//            }
//        }
//    }
}

void write_solve(struct Graph *g, struct Problem *p, int len_dom, int viol, double best_time, double total_time){
    printf("END");
}

