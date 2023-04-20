def valid_undirected_adjacency_list(al):
	num_vertex = len(al)
	for i in range(num_vertex):
		for j in range(len(al[i])):
			assert al[i][j] < num_vertex, "Adjacency list contains integers greater than number of vertices!"

	for i in range(num_vertex):
		for j in range(len(al[i])):
			assert i in al[al[i][j]], "Adjacency list missing edges in undirected case!"

	#for i in range(num_vertex):
	#	assert i in al[i], "Adjacency list missing edge self loops!"

	for i in range(num_vertex):
		assert len(al[i]) == len(set(al[i])), "Duplicates in adjacency list!"