"""
一个m*n的矩阵，从左到右从上到下都是递增的，给一个数x，判断x是否在矩阵中。
"""
import numpy as np


def find(matrix: np.array, x):
    m, n = matrix.shape
    a = matrix[0][n - 1]
    if a == x:
        return True
    if m == 1 and n == 1 and a != x:
        return False
    if a > x:
        matrix = matrix[:, :-1]
        return find(matrix, x)
    if a < x:
        matrix = matrix[1:]
        return find(matrix, x)


def test_find():
    test_matrix = np.array([[1, 2, 3], [7, 10, 14], [13, 16, 20]])
    # to_find = 13
    # assert find(test_matrix, to_find)
    to_find = 15
    assert find(test_matrix, to_find) is False
