from hash import *
import numpy as np
import matplotlib.pyplot as plt
import time

sizes = 500
bipartite_adjacency_matrix = np.random.randint(2, size=(sizes, sizes))
#bipartite_adjacency_matrix = np.ones((sizes, sizes))
print(bipartite_adjacency_matrix)

#a = time.time()
#hashed_bipartite_adjacency_matrix = old_hash_adjacency_matrix(bipartite_adjacency_matrix)
#b = time.time()
#old_time = b-a

print(bipartite_adjacency_matrix)
a = time.time()
old_hashed_bipartite_adjacency_matrix = hash_adjacency_matrix(bipartite_adjacency_matrix)
b = time.time()
new_time = b-a

print(f"old time: {old_time} new time: {new_time}")


#print(hashed_bipartite_adjacency_matrix)

'''
start_graphs = 10
end_graphs = 1000
increment = 50
y = []
for i in range(start_graphs, end_graphs, increment):
    print(f"size: {i}")
    bipartite_adjacency_matrix = np.random.randint(2, size=(i, i))

    a = time.time()
    hashed_bipartite_adjacency_matrix = hash_adjacency_matrix(bipartite_adjacency_matrix)
    b = time.time()
    y.append(b - a)

x = [i for i in range(start_graphs, end_graphs, increment)]

plt.xlabel('size of hash', fontsize=20)
plt.ylabel('Time (ms)', fontsize=20)
plt.plot(x, y, 'bo')
plt.show()
'''