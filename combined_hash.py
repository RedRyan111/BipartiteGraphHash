import torch

def sort_by_diags(matrix):
    row_diags = torch.sum(matrix, dim=1)
    col_diags = torch.sum(matrix.T, dim=1)

    row_diag_indexes = torch.argsort(row_diags)
    col_diag_indexes = torch.argsort(col_diags)

    matrix = matrix[row_diag_indexes]
    matrix = matrix[:, col_diag_indexes]

    return matrix

# sort by row score # does the row score change when rows are changed? YES!!!
def collisions(matrix):  # O(n^2.73)
    return torch.matmul(matrix, matrix.T)

def complex_score(n, matrix):
    new_collisions = collisions(matrix)
    print(f'collisions')
    print(new_collisions)
    new_matrix = []
    for i in range(n):
        old_col_diag = new_collisions[0][0]
        row_collisions_summed = []

        current_sum = 0
        for j in range(n):
            col_diag = new_collisions[j][j]
            if old_col_diag != col_diag:
                old_col_diag = col_diag
                row_collisions_summed.append(current_sum)
                current_sum = 0
            current_sum += int(new_collisions[i][j])

        row_collisions_summed.append(current_sum)
        new_matrix.append(row_collisions_summed)
    return new_matrix, matrix

def sort_rows_by_complex_ordering(new_collisions, matrix, collisions_size):
    new_collisions = torch.FloatTensor(new_collisions)

    for i in range(collisions_size):
        index = i#collisions_size - i - 1
        print(f'currently sorting by: {new_collisions[:, index]}')

        indexes = torch.argsort(new_collisions[:, index])
        print(f'indexes: {indexes}')
        new_collisions = new_collisions[indexes]
        matrix = matrix[indexes]

    return matrix

def sort_by_complex_sort_ordering(matrix):
    new_collisions, matrix = complex_score(matrix.shape[0], matrix)
    num_of_collision_cols = len(new_collisions[0])
    print(f'pre rows matrix')
    print(matrix)
    print(f'pre rows collisions')
    print(new_collisions)
    matrix = sort_rows_by_complex_ordering(new_collisions, matrix, num_of_collision_cols)

    print(f'pre cols matrix')
    print(matrix)
    print(f'pre cols collisions')
    print(new_collisions)
    new_collisions, matrix = complex_score(matrix.shape[0], matrix.T)
    num_of_collision_cols = len(new_collisions[0])
    matrix = sort_rows_by_complex_ordering(new_collisions, matrix, num_of_collision_cols)

    return matrix.T

def hash_adjacency_matrix(matrix):
    matrix = sort_by_diags(matrix)

    matrix = sort_by_complex_sort_ordering(matrix)

    return matrix

sizes = 4
matrix = torch.randint(2, size=(sizes, sizes))
print(f'original matrix')
print(matrix)
matrix = hash_adjacency_matrix(matrix)
print('new matrix:')
print(matrix)
# colum diag is getting fucked


'''
    print('new_collisions tensor')
    print(new_collisions)
    new_collisions = torch.FloatTensor(new_collisions)
    #matrix = torch.FloatTensor(matrix)

    for i in range(new_matrix_size):
        index = new_matrix_size - i - 1
        print(f'currently sorting by: {new_collisions[:, index]}')

        indexes = torch.argsort(new_collisions[:, index])
        print(f'indexes: {indexes}')
        matrix = matrix[indexes]
'''