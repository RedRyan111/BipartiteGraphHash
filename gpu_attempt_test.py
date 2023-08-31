import numpy as np


def test_matrix_1(hash_matrix):
    a = np.zeros((4, 4))
    a[2, 2] = 1
    a[3, 3] = 1

    b = np.zeros((4, 4))
    b[2, 3] = 1
    b[3, 2] = 1

    assert np.allclose(hash_matrix(a), hash_matrix(b))


def test_matrix_2(hash_matrix):
    a = np.zeros((4, 4))
    a[3, 3] = 1

    b = np.zeros((4, 4))
    b[3, 2] = 1

    c = np.zeros((4, 4))
    c[2, 3] = 1

    assert np.allclose(hash_matrix(a), hash_matrix(b))
    assert np.allclose(hash_matrix(b), hash_matrix(c))


def test_matrix_1(hash_matrix):
    a = np.array([[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 1, 1, 0],
                  [0, 0, 0, 1]])

    b = np.array([[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 1]])

    assert np.allclose(hash_matrix(a), hash_matrix(b))
    assert np.allclose(hash_matrix(b), hash_matrix(c))


def format_array(array_string):
    array_string = array_string.replace("\n", "")
    array_string = array_string.replace(" ", ",")
    return np.array(eval(array_string))


def fast_hash_testing(matrix, hash_matrix):
    hash_dict = set()

    m1 = np.fliplr(matrix)
    m2 = np.flipud(m1)
    m3 = np.flipud(matrix)

    sorted_edges_matrix = hash_matrix(matrix)
    sorted_edges_matrix = str(np.array(sorted_edges_matrix).flatten())

    sorted_edges_m1 = hash_matrix(m1)
    sorted_edges_m1 = str(np.array(sorted_edges_m1).flatten())

    sorted_edges_m2 = hash_matrix(m2)
    sorted_edges_m2 = str(np.array(sorted_edges_m2).flatten())

    sorted_edges_m3 = hash_matrix(m3)
    sorted_edges_m3 = str(np.array(sorted_edges_m3).flatten())

    hash_dict.add(sorted_edges_matrix)
    hash_dict.add(sorted_edges_m1)
    hash_dict.add(sorted_edges_m2)
    hash_dict.add(sorted_edges_m3)

    if len(hash_dict) > 1:
        for i in hash_dict:
            print(format_array(i).reshape((matrix.shape[0], matrix.shape[1])))
        # print(hash_dict)
    assert len(hash_dict) == 1


def gen(n, m):
    for i in range(2 ** (n * m)):
        yield np.array([int(k) for k in "{0:b}".format(i).zfill(n * m)]).reshape(n, m)


def test_matrix(hash_matrix):
    sizes = 4
    print(f"num of matrices: {int(2 ** (sizes * sizes))}")
    count = 0
    for mat in gen(sizes, sizes):
        if count % 1000 == 0:
            print(count)
        fast_hash_testing(mat, hash_matrix)
        count += 1
