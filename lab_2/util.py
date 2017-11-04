import os
import numpy as np
import random
import logging
import datetime as dt


# Ensure if dir does exist
def ensure_dir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)


'''
Start logger config
'''
LOGS_DIR = 'logs'
LOG_FILENAME = 'run_{}.log'.format(dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))

ensure_dir('logs')

# Logger formatter
log_formatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s')
logger = logging.getLogger()

# Logger file handler
file_handler = logging.FileHandler(os.path.join(LOGS_DIR, LOG_FILENAME))
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Logger console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

# Logger level
logger.setLevel(os.environ.get('LOG_LEVEL') or logging.INFO)
'''
End logger config
'''


# Read input data from file
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


'''
Problem related util functions
'''


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


def swap(a, i, j):
    a[i], a[j] = a[j], a[i]


# this function changes matrix, does not change clusters -> matrix, perm_row are renewed
def swap_rows(matrix, i, j, perm_row):
    matrix[i], matrix[j] = matrix[j], matrix[i].copy()
    swap(perm_row, i, j)
    return matrix


# this function changes matrix, does not change clusters -> matrix, perm_col are renewed
def swap_cols(matrix, i, j, perm_col):
    matrix[:, i], matrix[:, j] = matrix[:, j], matrix[:, i].copy()
    swap(perm_col, i, j)
    return matrix


# this function changes clusters, does not change matrix -> clusters_row, clusters_col are renewed
def split_clusters(clusters_row, clusters_col, current_number_of_clusters, number_of_cluster):
    if (current_number_of_clusters >= min(len(clusters_row), len(clusters_col))):
        return -1  # cannot split if all clusters are 1*1
    new_row = clusters_row.copy()
    new_col = clusters_col.copy()
    part_row = []
    part_col = []
    # find cluster to split, at least 2*2
    M = number_of_cluster  # number of cluster to split
    for i in range(len(new_row)):
        if (new_row[i] == M): part_row.append(i)
    for i in range(len(new_col)):
        if (new_col[i] == M): part_col.append(i)
    if ((len(part_row) < 2) | (len(part_col) < 2)):
        return -1  # cannot split this cluster
    # choose row and column to split
    a = part_row[0] + random.randint(1, len(part_row) - 1)
    b = part_col[0] + random.randint(1, len(part_col) - 1)
    for i in range(a, len(new_row)):
        new_row[i] += 1
    for i in range(b, len(new_col)):
        new_col[i] += 1
    return new_row, new_col


# this function changes clusters, does not change matrix -> clusters_row, clusters_col are renewed
def union_two_clusters(clusters_row, clusters_col, current_number_of_clusters, number_of_cluster):
    if (current_number_of_clusters == 1):
        return -1  # cannot union if there is only one cluster
    new_row = clusters_row.copy()
    new_col = clusters_col.copy()
    # find clusters to union
    M = number_of_cluster  # union M and M + 1 clusters
    part_row = []
    part_col = []
    for i in range(len(new_row)):
        if (new_row[i] >= M + 1): new_row[i] -= 1
    for i in range(len(new_col)):
        if (new_col[i] >= M + 1): new_col[i] -= 1
    return new_row, new_col
