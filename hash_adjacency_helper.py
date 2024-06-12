import torch
import numpy as np

def row_collisions(matrix):
    return np.matmul(matrix, matrix.T)

def hash_adjacency_matrix_helper(matrix):
    r_collisions = row_collisions(matrix)
    r_diag = np.diag(r_collisions).reshape(1, -1).repeat(r_collisions.shape[0], axis=0)
    # stacked_matrices = np.stack([r_collisions, r_diag], axis=2)
    stacked_matrices = np.stack([r_diag, r_collisions], axis=2)

    print(f'r_collisions')
    print(r_collisions)

    print('diag')
    print(r_diag)

    print(f'stacked matrix: ')
    print(stacked_matrices)

    stacked_matrices = np.sort(stacked_matrices, axis=1)

    #print(f'sorted stacked matrix')
    #print(stacked_matrices)

    temp_indexes = np.array([stacked_matrices[:, :, 0].tolist(), stacked_matrices[:, :, 1].tolist(), matrix.tolist()])
    #print(f'Temp indexes')
    #print(temp_indexes)
    #print('--')
    matrix = np.array([x for _, _, x in sorted(
        zip(stacked_matrices[:, :, 0].tolist(), stacked_matrices[:, :, 1].tolist(), matrix.tolist()))])

    return matrix

#-------------------------------------------------
def pytorch_row_collisions(matrix):
    return torch.matmul(matrix, matrix.T)


def pytorch_hash_adjacency_matrix_helper(matrix):
    r_collisions = pytorch_row_collisions(matrix)
    #print(f'r_collisions: {r_collisions.shape}')
    print(f'row collisions: ')
    print(r_collisions)
    r_diag = torch.diag(r_collisions)#.reshape(1, -1).repeat(r_collisions.shape[0], 1)
    max_num = 1 / (matrix.shape[0] + 1) #does this need to be +1 so that no collisions occur when edge is connected to every node?

    combined_r_collisions = r_collisions.float()*max_num + r_diag
    print(f'combined r collisions')
    print(combined_r_collisions)

    #temp = 10 ** torch.arange(start=matrix.shape[0]-1, end=-1, step=-1, dtype=torch.float).reshape(-1, 1)
    #temp = 10**torch.arange(matrix.shape[0]).float()
    #combined_r_collisions = r_collisions.float() * temp

    #print(f'combined r collisions:')
    #print(combined_r_collisions)

    #sorted_stacked_matrices, indices = torch.sort(stacked_matrices, dim=1)
    #sorted_stacked_matrix_indexes = combined_r_collisions.sort(dim=0, descending=False, stable=False) # is stable neccessary?
    values, sorted_stacked_matrix_indexes = torch.sort(combined_r_collisions, dim=1, descending=False, stable=True)
    print(f'sorted stacked: ')
    print(sorted_stacked_matrix_indexes)

    for i in range(sorted_stacked_matrix_indexes.shape[0]):
        matrix[i] = matrix[i, sorted_stacked_matrix_indexes[i]]
        combined_r_collisions[i] = combined_r_collisions[i, sorted_stacked_matrix_indexes[i]]

    print('matrix')
    print(matrix)

    combined_r_collisions = torch.t(combined_r_collisions)
    #matrix = matrix[sorted_stacked_matrix_indexes]

    values, sorted_stacked_matrix_indexes = torch.sort(combined_r_collisions, descending=True)

    for i in range(sorted_stacked_matrix_indexes.shape[0]):
        matrix[:, i] = matrix[i, sorted_stacked_matrix_indexes[i]]

    #matrix = matrix[:, sorted_stacked_matrix_indexes]

    return matrix

sizes = 4
matrix = np.random.randint(2, size=(sizes, sizes))

print(matrix)
print('-------------')
print(hash_adjacency_matrix_helper(matrix))
print('-------------')
print(pytorch_hash_adjacency_matrix_helper(torch.FloatTensor(matrix)))