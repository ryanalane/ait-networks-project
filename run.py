import networkx as nx
import math
import lib
import dev
from collections import defaultdict
dev = reload(dev)

G = lib.test_ring(10)
k = 3
N = 100 # Number of randomized network samples

# Generate real_frequencies
motif_instances = dev.enumerate_motif_instances(G, k)
motif_types = dev.group_motif_types(motif_instances)

real_frequencies = dev.calculate_motif_frequencies(motif_instances, motif_types)

# Generate random_frequencies
randomized_networks = dev.randomized_networks(G, N)

random_frequencies = []
for rand_network in randomized_networks:
	random_motif_instances = dev.enumerate_motif_instances(rand_network, k)

	single_random_frequencies = dev.calculate_motif_frequencies(random_motif_instances, motif_types)

	random_frequencies.append(single_random_frequencies)

# Sum frequencies for each motif_type over all random_frequencies
aggregate_frequencies = defaultdict(int) 
for frequency_set in random_frequencies:
	for motif_type_index in frequency_set:
		aggregate_frequencies[motif_type_index] += frequency_set[motif_type_index]

# Calculate mean_frequencies
mean_frequencies = {}
for (motif_type_index, sum) in aggregate_frequencies.items():
	mean_frequencies[motif_type_index] = float(sum) / N

# Calculate standard deviations among random_frequencies
sum_of_squares = defaultdict(int) 

for frequency_set in random_frequencies:
	for motif_type_index in frequency_set:
		sum_of_squares[motif_type_index] += float((frequency_set[motif_type_index] - mean_frequencies[motif_type_index]))**2

standard_deviations = {} 
for motif_type_index, sum in sum_of_squares.items():
	standard_deviations[motif_type_index] = math.sqrt(float(sum) / float(N))

# Calculate the z-scores for each motif
z_scores = {}
for motif_type_index in mean_frequencies:
	z_scores[motif_type_index] = float(real_frequencies[motif_type_index] - mean_frequencies[motif_type_index]) / float(standard_deviations[motif_type_index])