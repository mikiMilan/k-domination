#include <stdlib.h>
#include "unit.h"
#include <stdio.h>

void shuffle(int arr[], int size) {
    if (size <= 1)
        return;

    int i, j, temp;
    for (i = size - 1; i > 0; --i) {
        j = random(size-1) % (i + 1);

        temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

void shuffle_sort(int arr[], int size,const int num_add[]) {
    if (size <= 4)
        return;

    int i, temp;
    for (i = 0; i < size; ++i)
        if(num_add[arr[1]]>num_add[arr[i]]){
            temp = arr[1];
            arr[1] = arr[i];
            arr[i] = temp;
        }
}

int number_same_elements(const int dom_cache[], const int* adj, int adj_len){
    int counter = 0;

    for (int i = 0; i < adj_len; ++i)
        if( dom_cache[adj[i]]==1 ) //
            counter++;

    return counter;
}

// max incude
int random(int max){
    if (RAND_MAX < max){
        int block = max / RAND_MAX;
        int smal_block = max % RAND_MAX;

        // first choice block
        int rand_block = rand() % (block+1);

        if(rand_block != block)
            return rand_block*RAND_MAX + rand();
        else {
            if (smal_block != 0)
                return rand_block * RAND_MAX + rand() % (smal_block+1);
            else
                return (rand_block-1) * RAND_MAX + rand();
        }
    }
    return rand()%(max+1);
}

void copy(int* arr1, const int* arr2, int len){
    for (int i = 0; i < len; ++i) {
        arr1[i] = arr2[i];
    }
}

void copy_string(char* arr1, const char* arr2, int len){
    for (int i = 0; i < len; ++i) {
        arr1[i] = arr2[i];
    }
}

double fit(int viol, int len, double penalty){
    return (1+viol) * (1+len*penalty);
}