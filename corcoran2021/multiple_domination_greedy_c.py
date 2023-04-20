# This is the proposed greedy algotithm based on optimizing the C objective function.
import tarfile

import utilities
import numpy
import networkx
import warnings
import matplotlib.pyplot as plt
import random
from street_network_env import street_network_env
import pickle
import time
from statistics import mean

def reset(al):
	utilities.valid_undirected_adjacency_list(al)
	global num_vertex, ver_domination, ver_domination_val
	num_vertex = len(al)
	ver_domination = numpy.zeros(num_vertex, dtype=int) # Indicator function if each vertex is in dominating set
	ver_domination_val = numpy.zeros(num_vertex, dtype=int) # The number of times each vertex is dominated; value in range [0,k].

def add_vertex_domination(v):
	assert ver_domination[v] == 0
	ver_domination[v] = 1
	ver_domination_val[v] = k

	for av in al[v]:
		ver_domination_val[av] = min(ver_domination_val[av] + 1, k)

	count_dominated = numpy.count_nonzero(ver_domination_val >= k)
	done = (count_dominated == num_vertex)
	return done

def greedy_random_step_fast():
	l = list(range(num_vertex))
	random.shuffle(l)

	max_val = -float('inf')
	max_i = -1

	for i in l:
		if(ver_domination[i] == 0):
			count = -ver_domination_val[i]
			for av in al[i]:
				if(ver_domination_val[av] < k and ver_domination[av] == 0):
					count += 1.0
			if(count > max_val):
				max_val = count
				max_i = i
	return max_i

def greedy_random():
	done = False
	while(not done):
		v = greedy_random_step_fast()
		done = add_vertex_domination(v)


# random.seed(246)
# numpy.random.seed(4812)


file_name_res = 'results.txt'
instances = ['belgrade_pickle', 'berlin_pickle', 'boston_pickle', 'dublin_pickle', 'minsk_pickle']

for instance in instances:
	f = open("big_instances/"+instance, "rb")
	env_obj_t = pickle.load(f)

	print("sn.number_of_nodes(): ", env_obj_t.sn.number_of_nodes())
	print("sn.number_of_edges(): ", env_obj_t.sn.number_of_edges())
	print("rn.number_of_nodes(): ", env_obj_t.rn.number_of_nodes())
	print("rn.number_of_edges(): ", env_obj_t.rn.number_of_edges())

	al = env_obj_t.al
	for k in [1, 2, 4]:
		dresult = []
		tresult = []

		for i in range(10):
			print("Racunam ", i, " k=", k)
			reset(al)
			print("Start!!! ", i)
			tic = time.perf_counter()
			greedy_random()
			toc = time.perf_counter()
			print("End ", i)
			dresult.append(numpy.count_nonzero(ver_domination))
			print("Dominating size: ", numpy.count_nonzero(ver_domination))
			tresult.append(toc - tic)
			print(f"Time {toc - tic:0.4f} seconds")

		with open(file_name_res, 'a') as f:
			f.write(instance + "k=" + str(k) + "\n")
			f.write('{}, {:.2f}, {}, {}\n'.format(min(dresult), mean(dresult), str(dresult), str(tresult)))
			print(instance, k)
			print('{}, {:.2f}\n'.format(min(dresult), mean(dresult)))
