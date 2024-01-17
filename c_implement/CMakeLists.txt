cmake_minimum_required(VERSION 3.26)
project(kdom C)

set(CMAKE_C_STANDARD 11)

add_executable(kdom main.c
        kdomination.h
        kdomination.c
        graph.h
        graph.c
        unit.h
        unit.c)
