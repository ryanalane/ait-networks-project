import networkx as nx
import random

def enumerate_motif_instances( G, k ):

	def extend_subgraph( vertex_subgraph, vertex_extension, vertex ):

		if len(vertex_subgraph) == k:
			motif_instances.append(G.subgraph(vertex_subgraph))
			return

		while len(vertex_extension) != 0:
			node = vertex_extension.pop()
			node_neighbors = G.neighbors(node)
			# To prevent set.pop() from popping nodes in order
			random.shuffle(node_neighbors)

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
		# To prevent set.pop() from popping nodes in order
		random.shuffle(vertex_neighbors)

		vertex_extension = set([n for n in vertex_neighbors if n > vertex])

		extend_subgraph( set([vertex]), vertex_extension, vertex )

	return motif_instances