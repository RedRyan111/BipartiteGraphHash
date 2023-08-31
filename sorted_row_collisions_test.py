import numpy as np
from sorted_row_collisions import *


def test_full_sorted_row_collisions():
    r_collisions = np.array([
        [1, 0, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 0],
        [1, 1, 0, 2]
    ])

    true_r_collisions = np.array([
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 1, 1, 2]
    ])

    pred_r_collisions = full_sorted_row_collisions(r_collisions)

    assert np.allclose(pred_r_collisions, true_r_collisions)


def test_matrix_2():
    a = np.zeros((4, 4))
    a[3, 3] = 1

    b = np.zeros((4, 4))
    b[3, 2] = 1

    c = np.zeros((4, 4))
    c[2, 3] = 1

    assert np.allclose(hash(a), hash(b))
    assert np.allclose(hash(b), hash(c))


def test_matrix_3(hash_matrix):
    a = np.array([[0, 0, 0, 0],
                  [0, 0, 0, 1],
                  [1, 1, 0, 0],
                  [0, 0, 1, 1]])

    b = np.array([[0, 0, 0, 0],
                  [0, 0, 0, 1],
                  [0, 1, 1, 0],
                  [1, 0, 0, 1]])

    assert np.allclose(hash_matrix(a), hash_matrix(b))


def test_unique_diags_list():
    matrix = np.array([[1, 0, 1, 1],
                       [0, 1, 0, 0],
                       [1, 0, 2, 2],
                       [1, 0, 2, 2]
                       ])

    expected_array = np.array([0, 2, 4])

    predicted_array = unique_diags_list(matrix)

    assert np.allclose(expected_array, predicted_array)


def test_order_of_rows():
    matrix = np.array([[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 2]])

    expected_array = [0, 0, 2, 3]

    predicted_array = new_order_of_rows(matrix)

    assert np.allclose(expected_array, predicted_array)


def test_order_of_rows_1():
    matrix = np.array([[0, 0, 0, 0],
                       [0, 1, 0, 1],
                       [0, 1, 0, 2],
                       [0, 0, 0, 2]])

    expected_array = [0, 1, 3, 2]

    predicted_array = new_order_of_rows(matrix)

    assert np.allclose(expected_array, predicted_array)


def test_order_of_rows_2():
    matrix = np.array([[0, 0, 1, 1],
                       [0, 1, 1, 0],
                       [0, 1, 1, 0],
                       [0, 0, 1, 2]])

    expected_array = [1, 1, 0, 3]

    predicted_array = new_order_of_rows(matrix)

    assert np.allclose(expected_array, predicted_array)


def test_matrix_row_and_col_collisions():
    matrix = format_array('[[0 0 0 1] [1 0 0 1] [0 1 1 0] [0 0 0 0]]')

    new_matrix, row_collisions, col_collisions = matrix_row_and_col_collisions(matrix)

    assert np.allclose(get_row_collisions(new_matrix), row_collisions)
    assert np.allclose(get_row_collisions(new_matrix.T), col_collisions)
