from collections import Counter
from itertools import permutations
import matplotlib.pyplot as plt
import time

from hash import *


class NoZeros(Exception):
    pass


def sum_of_rows(matrix):
    return np.sum(matrix, axis=1)


def sum_of_cols(matrix):
    return np.sum(matrix, axis=0)


def add_one_to_first_zero_in_matrix(matrix):
    for row_index, row in enumerate(matrix):
        for col_index, col in enumerate(row):
            if col == 0:
                matrix[row_index, col_index] = 1
                return matrix
    raise NoZeros


def get_wrong_counts(first_rows, rows):
    return len([k for k, v in (Counter(first_rows) - Counter(rows)).items() for _ in range(v)])


def permute_matrix_from_index(matrix, row_permutation, col_permutation):
    temp = matrix.copy()
    temp = zip_sort_and_unzip(row_permutation, temp)
    temp = zip_sort_and_unzip(col_permutation, temp.T).T
    return temp


def hash_test(matrix):
    num_rows, num_cols = matrix.shape
    row_permutations = list(permutations(range(num_rows)))
    col_permutations = list(permutations(range(num_cols)))
    hash_dict = set()

    first_rows = sum_of_rows(matrix)
    first_cols = sum_of_cols(matrix)

    wrong_count = 0

    for row_permutation in row_permutations:
        for col_permutation in col_permutations:
            permuted_matrix = permute_matrix_from_index(matrix, row_permutation, col_permutation)

            sorted_edges = hash_adjacency_matrix(permuted_matrix)

            rows = sum_of_rows(sorted_edges)
            cols = sum_of_cols(sorted_edges)

            wrong_count += get_wrong_counts(first_rows, rows)
            wrong_count += get_wrong_counts(first_cols, cols)

            sorted_edges = str(np.array(sorted_edges).flatten())

            hash_dict.add(sorted_edges)

    assert len(hash_dict) == 1
    assert wrong_count == 0
    return hash_dict

import networkx as nx

def networkx_hash_test(matrix):
    num_rows, num_cols = matrix.shape
    row_permutations = list(permutations(range(num_rows)))
    col_permutations = list(permutations(range(num_cols)))
    hash_dict = set()

    #first_rows = sum_of_rows(matrix)
    #first_cols = sum_of_cols(matrix)

    #wrong_count = 0

    for row_permutation in row_permutations:
        for col_permutation in col_permutations:
            permuted_matrix = permute_matrix_from_index(matrix, row_permutation, col_permutation)

            G = nx.from_numpy_array(permuted_matrix)
            hashed_string = nx.weisfeiler_lehman_graph_hash(G)

            #sorted_edges = hash_adjacency_matrix(permuted_matrix)

            #rows = sum_of_rows(sorted_edges)
            #cols = sum_of_cols(sorted_edges)

            #wrong_count += get_wrong_counts(first_rows, rows)
            #wrong_count += get_wrong_counts(first_cols, cols)

            #sorted_edges = str(np.array(sorted_edges).flatten())

            hash_dict.add(hashed_string)

    if len(hash_dict) != 1:
        print(hash_dict)
    assert len(hash_dict) == 1
    #assert wrong_count == 0
    return hash_dict

def fast_hash_testing(matrix):
    hash_dict = set()

    m1 = np.fliplr(matrix)
    m2 = np.flipud(m1)
    m3 = np.flipud(matrix)

    sorted_edges_matrix = hash_adjacency_matrix(matrix)
    sorted_edges_matrix = str(np.array(sorted_edges_matrix).flatten())

    sorted_edges_m1 = hash_adjacency_matrix(m1)
    sorted_edges_m1 = str(np.array(sorted_edges_m1).flatten())

    sorted_edges_m2 = hash_adjacency_matrix(m2)
    sorted_edges_m2 = str(np.array(sorted_edges_m2).flatten())

    sorted_edges_m3 = hash_adjacency_matrix(m3)
    sorted_edges_m3 = str(np.array(sorted_edges_m3).flatten())

    hash_dict.add(sorted_edges_matrix)
    hash_dict.add(sorted_edges_m1)
    hash_dict.add(sorted_edges_m2)
    hash_dict.add(sorted_edges_m3)

    assert len(hash_dict) == 1


def gen(n, m):
    for i in range(2 ** (n * m)):
        yield np.array([int(k) for k in "{0:b}".format(i).zfill(n * m)]).reshape(n, m)


def format_array(array_string):
    array_string = array_string.replace("\n", "")
    array_string = array_string.replace(" ", ",")
    return np.array(eval(array_string))


#---------------------------------------------------------

sizes = 4
matrix = np.random.randint(2, size=(sizes, sizes))
print(matrix)
print('--------------')
hash_dict = hash_test(matrix)
for i in hash_dict:
    print(format_array(i).reshape(sizes, sizes))


sizes = 4
matrix = np.random.randint(2, size=(sizes, sizes))
print(matrix)
print('--------------')
hash_dict = networkx_hash_test(matrix)
for i in hash_dict:
    print(format_array(i).reshape(sizes, sizes))

#---------------------------------------------------------


sizes = 4
print(f"num of matrices: {int(2 ** (sizes * sizes))}")
num_of_matrices = int(2 ** (sizes * sizes))
count = 0
for mat in gen(sizes, sizes):
    if count % 1000 == 0:
        print(f"{count}/{num_of_matrices}")
    fast_hash_testing(mat)
    count += 1


sizes = 50
for i in range(1000):
    if i % 50 == 0:
        print(i/1000)
    matrix = np.random.randint(2, size=(sizes, sizes))
    fast_hash_testing(matrix)

'''
sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 300, 400, 500]
trial_times = []
num_of_trys = 10
for size in sizes:
    trial_time = 0
    for _ in range(num_of_trys):
        matrix = np.random.randint(2, size=(size, size))

        a = time.time()
        hash_adjacency_matrix(matrix)
        b = time.time()
        time_difference = b - a
        trial_time += time_difference

    trial_times.append(trial_time / num_of_trys)

plt.plot(sizes, trial_times)
plt.show()
print(trial_times)
'''

print("DONE!!")