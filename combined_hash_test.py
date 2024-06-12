import torch
from combined_hash import complex_score, sort_by_diags

matrix_1 = torch.FloatTensor(
    [[1, 0, 1, 1],
     [0, 0, 0, 0],
     [1, 0, 0, 0],
     [1, 0, 1, 1]]
)

matrix = sort_by_diags(matrix_1).tolist()
print(matrix)
assert matrix == torch.FloatTensor(
    [[0, 0, 0, 0],
     [0, 0, 0, 1],
     [0, 1, 1, 1],
     [0, 1, 1, 1]]
).tolist()


collisions, matrix = complex_score(4, matrix)
print(collisions)
assert collisions == [[1, 1, 1], [1, 2, 2], [1, 1, 5], [0, 1, 5]]
