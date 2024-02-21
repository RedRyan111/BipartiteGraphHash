import numpy as np


def format_array(array_string):
    array_string = array_string.replace("\n", "")
    array_string = array_string.replace(" ", ",")
    return np.array(eval(array_string))


def get_row_collisions(matrix):
    return np.matmul(matrix, matrix.T)


def manual_sorted_r_collisions(matrix):
    r_collisions = row_collisions(matrix)
    diags = np.diag(r_collisions).argsort()
    return reorder_diag(r_collisions, diags)


def reorder_diag(matrix, reorder_list):
    num_rows = matrix.shape[0]
    num_cols = matrix.shape[0]
    result = [[0] * num_cols for _ in range(num_rows)]  # Create an empty matrix of the same size

    for i, new_row in enumerate(reorder_list):
        for j, new_col in enumerate(reorder_list):
            result[i][j] = matrix[new_row][new_col]  # Rearrange rows and columns

    return np.array(result)


def argsort_matrix_by_diagonals(matrix):  # fastest one on cpu
    return np.diag(matrix).argsort()


# this is WRONG!!!! #this must be provided with sorted r_collisions i think...
def sort_chunked_row_collisions(r_collisions):
    diags = unique_diags_list(r_collisions)
    r_collisions = split_r_collisions(r_collisions, diags)

    return r_collisions


def unique_diags_list(r_collisions):
    diags = np.diag(r_collisions)
    prev_element = diags[0]
    new_list = [0]
    for index, element in enumerate(diags):
        if element != prev_element:
            new_list.append(index)
            prev_element = element

    new_list.append(r_collisions.shape[0])

    return new_list


def split_r_collisions(r_collisions, diags):
    # maybe do a sort on the matrix rows here to save time?
    for i in range(len(diags) - 1):
        r_start = diags[i]
        r_end = diags[i + 1]

        for j in range(len(diags) - 1):
            c_start = diags[j]
            c_end = diags[j + 1]

            #split_collisions = r_collisions[r_start:r_end, c_start:c_end]
            #sorted_split_collisions = np.sort(split_collisions)
            #r_collisions[r_start:r_end, c_start:c_end] = sorted_split_collisions
            # np.sort(r_collisions[r_start:r_end, c_start:c_end])
            if i <= j:
                r_collisions[r_start:r_end, c_start:c_end] = np.sort(r_collisions[r_start:r_end, c_start:c_end])
            else:
                r_collisions[r_start:r_end, c_start:c_end] = np.zeros((r_end-r_start, c_end-c_start))
            #    #np.sort(r_collisions[r_start:r_end, c_start:c_end], axis=1)

    return r_collisions


def get_row_bit_scores(matrix):
    return np.matmul(matrix, (2 ** np.arange(matrix.shape[1])).reshape(-1, 1))

'''
def order_of_rows(matrix):
    flipped_matrix = np.flip(matrix, axis=1)
    _, indices, counts = np.unique(flipped_matrix, axis=0, return_index=True, return_counts=True)
    sorted_indices = np.argsort(indices)
    result = np.repeat(sorted_indices, counts[sorted_indices])
    return result
'''


def order_of_rows(matrix):
    flipped_matrix = np.flip(matrix, axis=1)
    _, unique_indices, counts = np.unique(flipped_matrix, axis=0, return_index=True, return_counts=True)
    sorted_indices = unique_indices[np.argsort(counts)]

    unique_row_counts = np.bincount(counts)
    unique_row_indices = np.repeat(np.arange(len(unique_row_counts)), unique_row_counts)

    final_result = unique_row_indices[np.searchsorted(unique_row_counts.cumsum(), sorted_indices, side='right')]

    return final_result


# this is good i think...
def matrix_row_and_col_collisions(matrix):
    matrix, row_collisions = get_matrix_and_row_collisions_sorted_by_row_collision_diagonals(matrix)
    matrix, col_collisions = get_matrix_and_row_collisions_sorted_by_row_collision_diagonals(matrix.T)
    matrix = matrix.T
    return matrix, row_collisions, col_collisions


def get_matrix_and_row_collisions_sorted_by_row_collision_diagonals(matrix):
    row_collisions = get_row_collisions(matrix)
    argsorted_row_diags = argsort_matrix_by_diagonals(row_collisions)

    row_collisions = row_collisions[argsorted_row_diags][:, argsorted_row_diags]
    new_matrix = matrix[argsorted_row_diags]#matrix[argsorted_row_diags] #this swaps rows and columns and isn't equivalent to the original matrix anymore: matrix.T[argsorted_row_diags][:, argsorted_row_diags]
    return new_matrix, row_collisions


def new_order_of_rows(collision_matrix):
    prev_order = np.lexsort(collision_matrix.T)
    #print(f"previous index: {prev_order}")
    prev_row = collision_matrix[prev_order][0]
    prev_index = 0
    for index, row in enumerate(collision_matrix[prev_order]):
        #print(row)
        if not np.allclose(prev_row, row):
            prev_index = index
            prev_row = row
        prev_order[index] = prev_order[prev_index]
    return prev_order

'''
#this is good i think...
def matrix_row_and_col_collisions(matrix):
    matrix, row_collisions = get_matrix_and_row_collisions_sorted_by_row_collision_diagonals(matrix)
    print("matrix after row collisions sorted")
    print(matrix)
    print("row collisions")
    print(row_collisions)
    #sorting columns isn't correct
    #column collisions messes up the row collisions!!
    matrix, col_collisions = get_matrix_and_row_collisions_sorted_by_row_collision_diagonals(matrix.T)
    matrix = matrix.T
    print("matrix after col collisions sorted")
    print(matrix)
    print("col collisions")
    print(col_collisions)
    print(get_row_collisions(matrix))
    return matrix, row_collisions, col_collisions


#this is incorrect!!!!
#the error is coming from the sorted_indecis
def order_rows(matrix):
    unique_rows, inverse_indices = np.unique(matrix, axis=0, return_inverse=True)
    #sorted_indices = np.lexsort(sorted_chunked_row_collisions.T)
    #sorted_indices = arg_sort_rows(unique_rows)
    result = sorted_indices[inverse_indices]

    return result


def row_collisions_sorted_by_diag_row_collisions(matrix):  # fastest on cpu when matrix has less than 400 rows
    r_collisions = row_collisions(matrix)
    diags = np.diag(r_collisions)
    sorted_matrix = matrix[diags.argsort()]
    new_r_collisions = row_collisions(sorted_matrix)
    return new_r_collisions

#maybe sort by decimal last?
def matrix_row_collisions_split_then_sorted(matrix):
    row_collisions = get_row_collisions(matrix)
    argsorted_rows_indecis = argsort_matrix_by_diagonals(row_collisions)

    #sort row collisions and matrix
    row_collisions = row_collisions[argsorted_rows_indecis][:, argsorted_rows_indecis]
    matrix = matrix[argsorted_rows_indecis]
    
    row_diags = np.diag(row_collisions).reshape(-1,1)

    #get row collision order
    row_collisions = sort_chunked_row_collisions(row_collisions)
    row_collision_order = order_of_rows(row_collisions).reshape(-1,1)

    #get decimal values of matrix
    decimal_matrix = get_row_bit_scores(matrix)

    row_collisions = np.concatenate([summed_row_collisions, row_collision_order, decimal_matrix],axis=1)

    #print(f"r: {r_collisions.shape} dec: {decimal_matrix.shape}")
    #print(f"decimal: {decimal_matrix}")

    #

    #print(f"r_col: {r_collisions}")
    #print(f"diags sorted: {diags_sorted} r_col sorted: {np.lexsort(r_collisions.T)}")

    return matrix, arg_sort_rows(row_collisions) #arg_sort_rows(r_collisions)#

    #get row sorts and column sorts and then use matrix[row_sort][:, col_sort] at the very end

    #return matrix
    
def full_hash(matrix):
    matrix, row_sort_1 = matrix_row_collisions_split_then_sorted(matrix)
    matrix = matrix[row_sort_1]
    matrix, col_sort_1 = matrix_row_collisions_split_then_sorted(matrix.T)
    matrix = matrix[:, col_sort_1]


    return matrix

def new_order_hash(matrix):
    matrix, row_order_2 = matrix_row_collisions_split_then_sorted(matrix)
    print(f"matrix after row collision diag sort")
    print(matrix)
    matrix, col_order_2 = matrix_row_collisions_split_then_sorted(matrix.T)
    matrix = matrix.T
    print(f"matrix after col collision diag sort")
    print(matrix)

    #rows order sorts
    decimal_matrix = get_row_bit_scores(matrix)
    row_sorts = np.concatenate([row_order_2.reshape(-1, 1), decimal_matrix], axis=1)
    print("concatenated row sorts")
    print(row_sorts)
    #row_sorts = np.lexsort(row_sorts.T)
    row_sorts = arg_sort_rows(row_sorts)

    print("row sorts")
    print(row_sorts)
    matrix = matrix[row_sorts]
    print(f"matrix after row sorts:")
    print(matrix)

    #cols order sorts
    decimal_matrix = get_row_bit_scores(matrix.T)
    print(f"col shape {col_order_2.reshape(-1, 1).shape} decimal columns: {decimal_matrix.shape}")
    col_sorts = np.concatenate([col_order_2.reshape(-1, 1), decimal_matrix], axis=1)
    print("concatenated col sorts")
    print(col_sorts)
    #col_sorts = np.lexsort(col_sorts.T)
    col_sorts = arg_sort_rows(col_sorts)
    print("col sorts")
    print(col_sorts)
    matrix = matrix[:, col_sorts]
    print(f"matrix after col sorts:")
    print(matrix)

    return matrix

def new_hash(matrix):
    matrix, row_sort_1 = matrix_row_collisions_split_then_sorted(matrix)
    matrix = matrix[row_sort_1]
    matrix, col_sort_1 = matrix_row_collisions_split_then_sorted(matrix.T)
    matrix = matrix[:, col_sort_1]

    #need rank instead of sorted rows [0,0,1,1] instead of [0,1,2,3]
    #rows
    decimal_matrix = get_row_bit_scores(matrix)
    #print(f"col shape {row_sort_1.shape} decimal columns: {decimal_matrix.shape}")
    r_collisions = np.concatenate([row_sort_1.reshape(-1, 1), decimal_matrix],axis=1)

    row_sort_2 = arg_sort_rows(r_collisions)
    matrix = matrix[row_sort_2]

    #columns
    decimal_matrix = get_row_bit_scores(matrix.T)
    #print(f"col shape {col_sort_1.reshape(-1, 1).shape} decimal columns: {decimal_matrix.shape}")
    r_collisions = np.concatenate([col_sort_1.reshape(-1, 1), decimal_matrix],axis=1)

    col_sort_2 = arg_sort_rows(r_collisions)
    matrix = matrix[:, col_sort_2]

    #print(f"r: {r_collisions.shape} dec: {decimal_matrix.shape}")
    #print(f"decimal: {decimal_matrix}")

    #r_collisions = np.concatenate([r_collisions, decimal_matrix],axis=1)

    #print(f"row sort: {row_sort} col_sort: {col_sort}")

    #matrix = matrix[row_sort_2][:, col_sort_1][:, col_sort_2]
    #matrix = matrix[row_sort_2][:, col_sort_2]
    #matrix = matrix[:, col_sort_1][:, col_sort_2]

    return matrix

'''
