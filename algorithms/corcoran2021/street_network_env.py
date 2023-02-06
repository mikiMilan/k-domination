import osmnx
import networkx
import pickle
import copy
import utilities
import numpy
import random
import matplotlib.pyplot as plt
import warnings
import pickle

class street_network_env():
	def __init__(self, coord):
		# Compute street network
		# Belgrade: center_point=(44.8086, 20.4524)
		# Dublin: center_point=(53.3432, -6.2704)
		# Berlin :(52.51703, 13.38887)
		# Boston: (42.35546, -71.06052)
		# Minsk: (53.90252, 27.56194)
		self.cox = coord[0]
		self.coy = coord[1]

		sn_radius = 15000 # 1500
		print("+++++++++++++++++")
		self.sn = osmnx.graph_from_point(center_point=(self.cox, self.coy), dist=sn_radius, network_type='drive', dist_type='bbox')
		print("+++++++++++++++++---------------------")
		self.sn = self.sn.to_undirected()
		print("sn.number_of_nodes(): ", self.sn.number_of_nodes())
		print("sn.number_of_edges(): ", self.sn.number_of_edges())
		self.plot_sn()

		# Compute reachability network
		reachability_radius = 3000 # 500
		self.rn = networkx.Graph(copy.deepcopy(self.sn))
		self.rn.remove_edges_from(list(self.rn.edges))
		for i in self.sn.nodes:
			en = networkx.ego_graph(self.sn, i, distance='length', radius=reachability_radius)
			self.rn.add_edges_from([(i,j) for j in list(en.nodes())])
			self.rn.remove_edge(i,i)
			if(i%100==0):
				print("radim sa cvorom", i/100)
		print("rn.number_of_nodes(): ", self.rn.number_of_nodes())
		print("rn.number_of_edges(): ", self.rn.number_of_edges())

		# Adjacency and edge lists for reachability graph
		self.al = street_network_env.networkx_2_adj(self.rn)
		utilities.valid_undirected_adjacency_list(self.al)
		self.num_vertex = len(self.al)

	def plot_sn(self, nl=[]):
		''' use self.plot_sn(s.nodes) to plot a subgraph s '''
		nc = ['r' if node in nl else 'k' for node in self.sn.nodes()]
		osmnx.plot_graph(self.sn, node_size=5, bgcolor='white', node_color=nc)

	@staticmethod
	def networkx_2_adj(net):
		osmid_2_ind = dict()
		net_nodes = list(net.nodes)
		for i in range(len(net_nodes)):
			osmid_2_ind[net_nodes[i]] = i

		adj = [[] for i in range(len(net_nodes))]
		net_edges = list(net.edges)
		for e in net_edges:
			adj[osmid_2_ind[e[0]]].append(osmid_2_ind[e[1]])
			adj[osmid_2_ind[e[1]]].append(osmid_2_ind[e[0]])

		return(adj)

if __name__ == "__main__":
	random.seed(2)
	numpy.random.seed(2)

	cites = {# 'belgrade': (44.8086, 20.4524),
	'dublin': (53.3432, -6.2704),
	'berlin': (52.51703, 13.38887),
	'boston': (42.35546, -71.06052),
	'minsk': (53.90252, 27.56194)
	}

	for key in cites:
		print(key, cites[key])

		st_obj = street_network_env(cites[key])
		f = open(key + "_pickle", "wb")
		pickle.dump(st_obj, f)
		#
		# f = open("belgrade_pickle", "rb")
		# st_obj = pickle.load(f)
		# print(st_obj)

		print("sn.number_of_nodes(): ", st_obj.sn.number_of_nodes())
		print("sn.number_of_edges(): ", st_obj.sn.number_of_edges())
		print("rn.number_of_nodes(): ", st_obj.rn.number_of_nodes())
		print("rn.number_of_edges(): ", st_obj.rn.number_of_edges())

		al = st_obj.al

		file_name = key + ".txt"
		with open(file_name, 'w') as f:
			f.write(str(st_obj.rn.number_of_nodes()) + " " + str(st_obj.rn.number_of_edges()))
			for i in range(len(al)):
				for v in al[i]:
					f.write("\n" + str(i) + " " + str(v))

		print("Created instance: ", file_name)
