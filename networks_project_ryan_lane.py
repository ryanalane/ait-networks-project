import networkx as nx
import random
from collections import defaultdict

def randomize_networks(G, N):
	randomized_networks = []

	for n in range(N):

		randomized = G.copy()

		existing_edges = set(randomized.edges())

		# Sorted to ensure that nx.graph handles tuple appendage correctly (for undirected networks only)
		swap_edges = lambda edge_1, edge_2: [tuple(sorted([edge_1[0], edge_2[1]])), tuple(sorted([edge_2[0], edge_1[1]]))] 

		sample_mixing_factor = 100 # Sample Mixing factor

		for i in range( sample_mixing_factor * len(randomized.edges()) ):

			random_edges = random.sample(existing_edges, 2)
			potential_edges = swap_edges(random_edges[0], random_edges[1]) 

			edge_1 = potential_edges[0]
			edge_2 = potential_edges[1]	

			valid_swap = (edge_1[0] != edge_1[1] and edge_2[0] != edge_2[1] and edge_1 not in existing_edges and edge_2 not in existing_edges)

			if valid_swap:
				existing_edges.remove(random_edges[0])
				existing_edges.remove(random_edges[1])
				existing_edges.add(edge_1)
				existing_edges.add(edge_2)

		randomized.remove_edges_from(randomized.edges())
		randomized.add_edges_from(existing_edges)

		randomized_networks.append(randomized)

	return randomized_networks

def enumerate_motif_instances( G, k ):

	def extend_subgraph( vertex_subgraph, vertex_extension, vertex ):

		if len(vertex_subgraph) == k:
			motif_instances.append(G.subgraph(vertex_subgraph))
			return

		while len(vertex_extension) != 0:
			node = vertex_extension.pop()
			node_neighbors = G.neighbors(node)

			exclusive_neighborhood = set([neighbor for neighbor in node_neighbors if neighbor > vertex])

			subgraph_neighbors = set()
			for n in vertex_subgraph: 
				[subgraph_neighbors.add(neighbor) for neighbor in G.neighbors(n)]

			exclusive_neighborhood -= vertex_subgraph.union(subgraph_neighbors)

			new_vertex_extension = vertex_extension.union(exclusive_neighborhood)

			extend_subgraph(vertex_subgraph.union(set([node])), new_vertex_extension, vertex)

		return

	vertexes = G.nodes()
	motif_instances = []

	for vertex in vertexes:

		vertex_neighbors = G.neighbors(vertex)

		vertex_extension = set([n for n in vertex_neighbors if n > vertex])

		extend_subgraph( set([vertex]), vertex_extension, vertex )

	return motif_instances

def group_motif_types(motif_instances):

	motif_types = []
	for instance in motif_instances:

		type_already_exists = False	
		for type in motif_types:
			if nx.is_isomorphic(type, instance):
				type_already_exists = True
				break

		if type_already_exists == False:
			motif_types.append(instance)

	return motif_types

def calculate_motif_concentrations(motif_instances, motif_types):

	# Calculate motif frequencies
	motif_type_frequencies = defaultdict(int) 

	for instance in motif_instances:
		for index, type in enumerate(motif_types):

			if nx.is_isomorphic(type, instance):
				motif_type_frequencies[index] += 1

	# Calculating motif concentrations for each motif_type
	total_motif_frequencies = len(motif_instances)		

	motif_type_concentrations = {}
	for motif_type_index, frequency in motif_type_frequencies.items():
		motif_type_concentrations[motif_type_index] = float(frequency) / float(total_motif_frequencies)

	return motif_type_concentrations