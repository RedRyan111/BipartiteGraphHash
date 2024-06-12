import torch


# sort by row score # does the row score change when rows are changed? YES!!!
def collisions(matrix):  # O(n^2.73)
    return torch.matmul(matrix, matrix.T)

'''
def get_score(n, matrix, diagonal):  # O(n^2) on CPU or O(1) on GPU
    for i in range(n):
        for j in range(n):
            matrix[i][j] = (n+1) ** diagonal[i] * matrix[i][j] #this number blows up way too quickly
    return torch.sum(matrix, dim=0)
'''
def complex_score_sorting(n, matrix):
    new_collisions = collisions(matrix)
    new_matrix = []
    for i in range(n):
        row_diag = new_collisions[i][i]
        row_collisions_summed = []
        old_col_diag = row_diag
        current_sum = 0
        for j in range(n):
            col_diag = new_collisions[j][j]
            if old_col_diag != col_diag:
                col_diag = old_col_diag
                row_collisions_summed.append(current_sum)
            else:
                current_sum += col_diag
        new_matrix.append(row_collisions_summed)


def get_score(n, matrix, diagonal):  # O(n^2) on CPU or O(1) on GPU
    for i in range(n):
        for j in range(n):
            matrix[i][j] = diagonal[i] * matrix[i][j]

    return torch.sum(matrix, dim=1) #dim=1? #not sure this sum is good... shouldn't it be sorted by each diag then the diag area?

def get_binary_score(n, matrix):  # O(n^2) on CPU or O(1) on GPU
    binary_vector = (2 ** torch.arange(n)).reshape(-1, 1)#.to(torch.int32)
    #print(f'binary vector: {binary_vector} type: {binary_vector.type()}')
    return torch.matmul(matrix.float(), binary_vector.float())
    #for i in range(n):
    #    for j in range(n):
    #        matrix[i][j] = matrix[i][j] * 2 ** i
    #return torch.sum(matrix, dim=1) #dim=1?


def get_decimal_edge_distance(matrix):
    return torch.sum(torch.matmul(
        matrix.float(),
        2 ** get_edge_distance_matrix(matrix.shape[0], matrix.shape[1]).float()).float(),
        dim=1)


def get_edge_distance_matrix(height, width):
    arr_1 = torch.arange(width)
    arr_2 = torch.arange(height).reshape(height, 1)

    repeated_arr_1 = torch.tile(arr_1, (height, 1))
    repeated_arr_2 = torch.tile(arr_2, (1, width))

    return torch.minimum(repeated_arr_1, repeated_arr_2)

def sort_matrix_by_diag(matrix):
    row_diag = torch.sum(matrix, dim=1)#torch.diag(row_collisions) #dim=1? #could be faster to use collisions
    #sorted_row_indexes = torch.argsort(row_diag)
    row_diag, sorted_row_indexes = torch.sort(row_diag)
    matrix = matrix[sorted_row_indexes]
    #row_diag = row_diag[sorted_row_indexes]
    return matrix, row_diag, sorted_row_indexes

'''
def hash_adjacency_matrix(matrix):  # 2 * ( O(n^2.73) + O(n^2) + O(nlog(n)) )
    # sort by row score
    row_collisions = collisions(matrix)
    print(f'row collisions')
    print(row_collisions)
    row_score = get_score(matrix.shape[0], row_collisions, row_diag)
    row_score, row_collision_indexes = torch.sort(row_score)

    matrix = matrix[row_collision_indexes]

    new_row_diag = row_diag[row_collision_indexes]
    _, diag_row_indexes = torch.sort(new_row_diag)

    print(f'row score: {row_score}')
    print(f'row index: {row_collision_indexes}')

    matrix = matrix[diag_row_indexes]

    # sort by col score
    col_collisions = collisions(matrix.T)
    col_score = get_score(matrix.shape[0], col_collisions, row_diag)
    col_score, col_collision_indexes = torch.sort(col_score)

    #collision_col_diag = row_diag[col_collision_indexes]
    #_, diag_col_indexes = torch.sort(collision_col_diag)

    print(f'col score: {row_score}')
    print(f'col index: {col_collision_indexes}')

    matrix = matrix[:, col_collision_indexes]
    #matrix = matrix[:, diag_col_indexes]

    #sort by row diag
    matrix, row_diag, diag_row_indexes = sort_matrix_by_diag(matrix)
    print(f'row diag: {row_diag} indexes: {diag_row_indexes}')

    # sort by col diag
    matrix, col_diag, diag_col_indexes = sort_matrix_by_diag(matrix.T)
    matrix = matrix.T
    print(f'col diag: {col_diag} indexes: {diag_col_indexes}')



    # above is good

    #binary scores

    print('matrix before row')
    print(matrix)
    row_binary_score = get_binary_score(matrix.shape[0], matrix.clone()).reshape(-1)
    #row_binary_score = get_decimal_edge_distance(matrix)
    row_binary_indexes = torch.argsort(row_binary_score)

    print(f'row binary: {row_binary_score}')

    new_row_score = row_score[row_binary_indexes]
    new_row_diag = row_diag[row_binary_indexes]
    matrix = matrix[row_binary_indexes]

    new_row_score_indexes = torch.argsort(new_row_score)
    new_row_diag = new_row_diag[new_row_score_indexes]
    matrix = matrix[new_row_score_indexes]

    new_row_diag_indexes = torch.argsort(new_row_diag)
    matrix = matrix[new_row_diag_indexes]

    print('matrix after row ')
    print(matrix)

    col_binary_score = get_binary_score(matrix.shape[0], matrix.clone().T).reshape(-1)
    #col_binary_score = get_decimal_edge_distance(matrix.T)
    col_binary_indexes = torch.argsort(col_binary_score)

    new_col_score = col_score[col_binary_indexes]
    new_col_diag = col_diag[col_binary_indexes]
    matrix = matrix[:, col_binary_indexes]

    new_col_score_indexes = torch.argsort(new_col_score)
    new_col_diag = new_col_diag[new_col_score_indexes]
    matrix = matrix[:, new_col_score_indexes]

    new_col_diag_indexes = torch.argsort(new_col_diag)
    matrix = matrix[:, new_col_diag_indexes]

    print(f'after column binary')


    # last one???
    #rows
    row_edge_distance = get_binary_score(matrix.shape[0], matrix.clone()).reshape(-1)
    #row_edge_distance = get_decimal_edge_distance(matrix)
    row_edge_distance_indexes = torch.argsort(row_edge_distance)

    print(f'row binary: {row_edge_distance} indexes: {row_edge_distance_indexes}')

    new_binary_score = row_binary_score[row_edge_distance_indexes]
    new_row_score = row_score[row_edge_distance_indexes]
    new_row_diag = row_diag[row_edge_distance_indexes]
    matrix = matrix[row_edge_distance_indexes]

    #new_binary_score_indexes = torch.argsort(new_binary_score)
    #new_row_score = new_row_score[new_binary_score_indexes]
    #new_row_diag = new_row_diag[new_binary_score_indexes]
    #matrix = matrix[new_binary_score_indexes]

    new_row_score_indexes = torch.argsort(new_row_score)
    new_row_diag = new_row_diag[new_row_score_indexes]
    matrix = matrix[new_row_score_indexes]

    new_row_diag_indexes = torch.argsort(new_row_diag)
    matrix = matrix[new_row_diag_indexes]

    print('matrix after row ')
    print(matrix)
    

    # Columns

    col_edge_distance = get_binary_score(matrix.shape[0], matrix.clone()).reshape(-1)
    #col_edge_distance = get_decimal_edge_distance(matrix)
    col_edge_distance_indexes = torch.argsort(col_edge_distance)

    new_binary_score = col_binary_score[col_edge_distance_indexes]
    new_col_score = col_score[col_edge_distance_indexes]
    new_col_diag = col_diag[col_edge_distance_indexes]
    matrix = matrix[:, col_edge_distance_indexes]

    #new_binary_score_indexes = torch.argsort(new_binary_score)
    #new_col_score = new_col_score[new_binary_score_indexes]
    #new_col_diag = new_col_diag[new_binary_score_indexes]
    #matrix = matrix[:, new_binary_score_indexes]

    new_col_score_indexes = torch.argsort(new_col_score)
    new_col_diag = new_col_diag[new_col_score_indexes]
    matrix = matrix[:, new_col_score_indexes]

    new_col_diag_indexes = torch.argsort(new_col_diag)
    matrix = matrix[:, new_col_diag_indexes]
    
    return matrix  # , row_score, col_score
'''

sizes = 4
matrix = torch.randint(2, size=(sizes, sizes))
print(f'matrix')
print(matrix)
new_matrix = hash_adjacency_matrix(matrix)
print('new matrix:')
print(new_matrix)
#colum diag is getting fucked
