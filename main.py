from hash import *
import numpy as np

sizes = 10
bipartite_adjacency_matrix = np.random.randint(2, size=(sizes, sizes))

hashed_bipartite_adjacency_matrix = hash_adjacency_matrix(bipartite_adjacency_matrix)

print(hashed_bipartite_adjacency_matrix)

