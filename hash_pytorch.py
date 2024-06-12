import torch
import numpy as np

def row_collisions(matrix):
    return torch.matmul(matrix, matrix.T)


def hash_adjacency_matrix(matrix):
    matrix = hash_adjacency_matrix_helper(hash_adjacency_matrix_helper(matrix.T).T)
    matrix = sort_adjacency_matrix_by_scores_and_decimal(matrix.T).T
    matrix = sort_adjacency_matrix_by_scores_and_decimal(matrix)
    return matrix


def hash_adjacency_matrix_helper(matrix):
    r_collisions = row_collisions(matrix)
    r_diag = torch.diag(r_collisions).reshape(1, -1).repeat(r_collisions.shape[0], 1)
    stacked_matrices = torch.stack([r_diag, r_collisions], dim=2)

    stacked_matrices = torch.sort(stacked_matrices, dim=1)

    matrix = torch.FloatTensor([x for _, _, x in sorted(
        zip(stacked_matrices[:][:][0].tolist(), stacked_matrices[:][:][1].tolist(), matrix.tolist()))])

    return matrix


def new_hash_adjacency_matrix_helper(matrix):
    r_collisions = row_collisions(matrix)
    r_diag = torch.diag(r_collisions).reshape(1, -1).repeat(r_collisions.shape[0], 0)

    stacked_matrices = torch.stack([r_diag, torch.sort(r_collisions)], dim=2)

    # stacked_matrices = torch.sort(stacked_matrices, dim=1)

    return matrix[torch.argsort(stacked_matrices, dim=1)[0, :, 0]]


def get_score(adjacency_matrix):
    row_sum = torch.sum(adjacency_matrix, dim=0).long()
    col_score = torch.matmul(row_sum, adjacency_matrix.T.long())
    return col_score


def get_edge_distance_matrix(height, width):
    arr_1 = torch.arange(width)
    arr_2 = torch.arange(height).reshape(height, 1)

    repeated_arr_1 = torch.tile(arr_1, (height, 1))
    repeated_arr_2 = torch.tile(arr_2, (1, width))

    return torch.minimum(repeated_arr_1, repeated_arr_2)


def get_decimal_edge_distance(adjacency_matrix):
    return torch.sum(torch.matmul(
        adjacency_matrix.long(),
        2 ** get_edge_distance_matrix(adjacency_matrix.shape[0], adjacency_matrix.shape[1])).long(),
        dim=1)


def sort_zipped_lists(zipped_lists):
    return sorted(zipped_lists, key=lambda element: element[:-1])


def pytorch_zip_sort_and_unzip(combined_scores_and_binary, adjacency_matrix):
    indexes = combined_scores_and_binary.argsort(dim=0, descending=False, stable=False) # is stable neccessary?
    return adjacency_matrix[indexes]

'''
def sort_adjacency_matrix_by_scores_and_decimal(adjacency_matrix):
    scores = get_score(adjacency_matrix)
    binary = get_decimal_edge_distance(adjacency_matrix)
    max_num = 1 / 2 ** adjacency_matrix.shape[0] #Usually -1, but need to take that out to prevent 1.0 max_num
    combined_scores_and_binary = scores + binary*max_num

    return pytorch_zip_sort_and_unzip(combined_scores_and_binary, adjacency_matrix)
'''
#-----------------------------------

def zip_sort_and_unzip(scores, binary, adjacency_matrix):
    row_tuple = list(zip(scores, binary, adjacency_matrix))
    row_tuple = sort_zipped_lists(row_tuple)
    print(row_tuple)
    print(f'----')
    temp = row_tuple[:][2]
    print(temp)
    return temp


def sort_adjacency_matrix_by_scores_and_decimal(adjacency_matrix):
    scores = get_score(adjacency_matrix)
    binary = get_decimal_edge_distance(adjacency_matrix)

    return zip_sort_and_unzip(scores, binary, adjacency_matrix)
