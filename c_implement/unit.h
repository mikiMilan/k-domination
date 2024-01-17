//
// Created by pc on 11/30/2023.
//

#ifndef KDOM_UNIT_H
#define KDOM_UNIT_H

void shuffle(int arr[], int size);

void shuffle_sort(int arr[], int size, const int num_add[]);

int number_same_elements(const int dom_cache[], const int* adj, int adj_len);

int random(int max);

void copy(int* arr1, const int* arr2, int len);

void copy_string(char* arr1, const char* arr2, int len);

double fit(int viol, int len, double penalty);

#endif //KDOM_UNIT_H
