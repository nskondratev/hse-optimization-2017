import os
import numpy as np
import random


def read_from_file(filepath):
    with open(filepath, 'r') as f:
        first_line = f.readline().strip().split(' ')
        m = int(first_line[0])
        p = int(first_line[1])
        res = np.zeros((m, p))
        for i in range(m):
            line = f.readline().strip().split(' ')
            row = int(line[0]) - 1
            for j in range(1, len(line)):
                col = int(line[j]) - 1
                res[row, col] = 1
        return res, m, p, np.sum(res)


def objective_function(matrix, n1, clusters_row, clusters_col):
    n_zeros_in = 0
    n_ones_in = 0
    for i in range(len(clusters_row)):
        for j in range(len(clusters_col)):
            if clusters_row[i] == clusters_col[j]:
                if matrix[i, j] == 1:
                    n_ones_in += 1
                else:
                    n_zeros_in += 1

    return n_ones_in / (n1 + n_zeros_in)

def generate_initial_solution(m, p):
    a = random.randint(1, m - 1)
    b = random.randint(1, p - 1)
    clusters_row = np.ones(m)
    clusters_column = np.ones(p)
    for i in range(a, m):
        clusters_row[i] = 2
    for i in range(b, p):
        clusters_column[i] = 2
    return clusters_row, clusters_column
