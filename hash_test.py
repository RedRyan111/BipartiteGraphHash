from collections import Counter
from itertools import permutations
import pytest
from hash import zip_sort_and_unzip
from hash import *


class NoZeros(Exception):
    pass


def sum_of_rows(adjacency_matrix):
    return np.sum(adjacency_matrix, axis=1)


def sum_of_cols(adjacency_matrix):
    return np.sum(adjacency_matrix, axis=0)


def create_1_by_1_adjacency_matrix():
    return np.zeros((1, 1))


def add_one_to_first_zero_in_matrix(adjacency_matrix):
    for row_index, row in enumerate(adjacency_matrix):
        for col_index, col in enumerate(row):
            if col == 0:
                adjacency_matrix[row_index, col_index] = 1
                return adjacency_matrix
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
            temp = permute_matrix_from_index(matrix, row_permutation, col_permutation)

            sorted_edges = hash_adjacency_matrix(temp)

            rows = sum_of_rows(sorted_edges)
            cols = sum_of_cols(sorted_edges)

            wrong_count += get_wrong_counts(first_rows, rows)
            wrong_count += get_wrong_counts(first_cols, cols)

            sorted_edges = str(np.array(sorted_edges).flatten())

            hash_dict.add(sorted_edges)

    assert len(hash_dict) == 1
    assert wrong_count == 0
    return hash_dict


matrix = create_1_by_1_adjacency_matrix()
full_dict = set()
for i in range(20):
    print(f"i: {i} matrix shape: {matrix.shape}")

    try:
        matrix = add_one_to_first_zero_in_matrix(matrix)
    except NoZeros:
        matrix = np.pad(matrix, ((0, 1), (0, 1)))

    new_hash_dict = hash_test(matrix)
    assert new_hash_dict not in full_dict
    full_dict.update(new_hash_dict)
