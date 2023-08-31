import numpy as np


def row_collisions(matrix):
    return np.matmul(matrix, matrix.T)


def hash_adjacency_matrix(matrix):
    matrix = hash_adjacency_matrix_helper(hash_adjacency_matrix_helper(matrix.T).T)
    matrix = sort_adjacency_matrix_by_scores_and_decimal(matrix.T).T
    matrix = sort_adjacency_matrix_by_scores_and_decimal(matrix)
    return matrix


def hash_adjacency_matrix_helper(matrix):
    r_collisions = row_collisions(matrix)
    r_diag = np.diag(r_collisions).reshape(1, -1).repeat(r_collisions.shape[0], axis=0)
    stacked_matrices = np.stack([r_collisions, r_diag], axis=2)

    #for row_index in range(stacked_matrices.shape[0]):
    #    stacked_matrices[row_index] = np.sort(stacked_matrices[row_index], axis=0)

    stacked_matrices = np.sort(stacked_matrices, axis=1)

    matrix = np.array([x for _, _, x in sorted(
        zip(stacked_matrices[:, :, 0].tolist(), stacked_matrices[:, :, 1].tolist(), matrix.tolist()))])

    return matrix

def new_hash_adjacency_matrix_helper(matrix):

    r_collisions = row_collisions(matrix)
    r_diag = np.diag(r_collisions).reshape(1, -1).repeat(r_collisions.shape[0], axis=0)

    stacked_matrices = np.stack([r_diag, np.sort(r_collisions)], axis=2)

    #stacked_matrices = np.sort(stacked_matrices, axis=1)

    return matrix[np.argsort(stacked_matrices, axis=1)[0, :, 0]]


def get_score(adjacency_matrix):
    row_sum = np.sum(adjacency_matrix, axis=0)
    col_score = np.matmul(row_sum, adjacency_matrix.T)
    return col_score


def get_edge_distance_matrix(height, width):
    arr_1 = np.arange(width)
    arr_2 = np.arange(height).reshape(height, 1)

    repeated_arr_1 = np.tile(arr_1, (height, 1))
    repeated_arr_2 = np.tile(arr_2, (1, width))

    return np.minimum(repeated_arr_1, repeated_arr_2)


def get_decimal_edge_distance(adjacency_matrix):
    return np.sum(np.matmul(
        adjacency_matrix,
        2 ** get_edge_distance_matrix(adjacency_matrix.shape[0], adjacency_matrix.shape[1])),
        axis=1)


def sort_zipped_lists(zipped_lists):
    return sorted(zipped_lists, key=lambda element: element[:-1])


def zip_sort_and_unzip(*args):
    row_tuple = list(zip(*args))
    row_tuple = sort_zipped_lists(row_tuple)
    return np.array(list(zip(*row_tuple))[-1])


def sort_adjacency_matrix_by_scores_and_decimal(adjacency_matrix):
    scores = get_score(adjacency_matrix)
    binary = get_decimal_edge_distance(adjacency_matrix)

    return zip_sort_and_unzip(scores, binary, adjacency_matrix)