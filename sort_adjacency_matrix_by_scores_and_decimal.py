import numpy as np
import torch

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
    #print(f'args: {args[0]}')
    #print(f'args: {args[1]}')
    #print(f'args: {args[2]}')
    row_tuple = list(zip(*args))
    #print(f'row tuple')
    #print(row_tuple)
    row_tuple = sort_zipped_lists(row_tuple)
    #print('sorted zippled lists: ')
    #print(row_tuple)
    return np.array(list(zip(*row_tuple))[-1])


def sort_adjacency_matrix_by_scores_and_decimal(adjacency_matrix):
    scores = get_score(adjacency_matrix)
    binary = get_decimal_edge_distance(adjacency_matrix)
    final = zip_sort_and_unzip(scores, binary, adjacency_matrix)
    #print(f'final: ')
    #print(final)
    return final

#--------------------------------------------------------------
def pytorch_get_score(adjacency_matrix):
    row_sum = torch.sum(adjacency_matrix, dim=0)
    col_score = torch.matmul(row_sum, adjacency_matrix.T)
    return col_score

def pytorch_get_edge_distance_matrix(height, width):
    arr_1 = torch.arange(width)
    arr_2 = torch.arange(height).reshape(height, 1)

    repeated_arr_1 = torch.tile(arr_1, (height, 1))
    repeated_arr_2 = torch.tile(arr_2, (1, width))

    return torch.minimum(repeated_arr_1, repeated_arr_2)


def pytorch_get_decimal_edge_distance(adjacency_matrix):
    return torch.sum(torch.matmul(
        adjacency_matrix.long(),
        2 ** pytorch_get_edge_distance_matrix(adjacency_matrix.shape[0], adjacency_matrix.shape[1])).long(),
        dim=1)


def pytorch_sort_zipped_lists(zipped_lists):
    return sorted(zipped_lists, key=lambda element: element[:-1])


def pytorch_zip_sort_and_unzip(combined_scores_and_binary, adjacency_matrix):
    #row_tuple = list(zip(*args))

    #sorted_combined_tensors, indexes = torch.sort(combined_tensors, dim=0)
    #print('sorted combined tensors: ')
    #print(sorted_combined_tensors)

    indexes = combined_scores_and_binary.argsort(dim=0, descending=False, stable=False) # is stable neccessary?
    #print(f'indexes')
    #print(indexes)

    adjacency_matrix = adjacency_matrix[indexes]

    #row_tuple = torch.cat((scores, binary), 1)[indexes]
    #row_tuple, indecis = torch.sort(row_tuple, dim=-1)
    #row_tuple = sort_zipped_lists(row_tuple)
    return adjacency_matrix
    #return torch.FloatTensor(list(zip(*row_tuple))[-1])  # int tensor?


def pytorch_sort_adjacency_matrix_by_scores_and_decimal(adjacency_matrix):
    scores = pytorch_get_score(adjacency_matrix)
    binary = pytorch_get_decimal_edge_distance(adjacency_matrix)
    max_num = 2 ** adjacency_matrix.shape[0] - 1
    combined_scores_and_binary = scores + binary/max_num

    return pytorch_zip_sort_and_unzip(combined_scores_and_binary, adjacency_matrix)

sizes = 4
matrix = np.random.randint(2, size=(sizes, sizes))

print(matrix)
print('-------------')
print(sort_adjacency_matrix_by_scores_and_decimal(matrix))
print('-------------')
print(pytorch_sort_adjacency_matrix_by_scores_and_decimal(torch.FloatTensor(matrix)))
