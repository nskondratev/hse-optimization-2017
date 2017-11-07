import os
import numpy as np
import logging
import datetime as dt
from .solution import Solution


# Ensure if dir exists
def ensure_dir(path_to_dir):
    if not os.path.exists(path_to_dir):
        os.mkdir(path_to_dir)


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
# returns:
# - res - matrix
# - m - number of machines
# - p - number of parts
# - n1 - sum of ones in matrix
def read_from_file(path_to_file: str) -> np.ndarray:
    """
    Parse file and return matrix
    :param path_to_file: str -- Path to input file
    :return: np.ndarray
    """
    with open(path_to_file, 'r') as f:
        first_line = f.readline().strip().split(' ')
        m, p = int(first_line[0]), int(first_line[1])
        res = np.zeros((m, p))
        for i in range(m):
            line = f.readline().strip().split(' ')
            row = int(line[0]) - 1
            for j in range(1, len(line)):
                col = int(line[j]) - 1
                res[row, col] = 1
        return res


'''
Problem related util functions
'''


def swap(a, i, j):
    a[i], a[j] = a[j], a[i]


# this function changes matrix, does not change clusters -> matrix, perm_row are renewed
def swap_rows(matrix, i, j, perm_row):
    matrix[i], matrix[j] = matrix[j], matrix[i].copy()
    swap(perm_row, i, j)


# this function changes matrix, does not change clusters -> matrix, perm_col are renewed
def swap_cols(matrix, i, j, perm_col):
    matrix[:, i], matrix[:, j] = matrix[:, j], matrix[:, i].copy()
    swap(perm_col, i, j)


def increment_from_index(arr: np.array, i: int):
    """
    Increment values in array starting from provided index
    :param arr: np.array -- Array to change
    :param i: int -- Index to start with
    :return: void
    """
    arr[i:] = arr[i:] + 1


def split_clusters(clusters_row: np.array, clusters_col: np.array, clusters_count: int, cluster_to_split: int) -> bool:
    """
    Split requested cluster
    :param clusters_row: np.array -- Clusters by row
    :param clusters_col: np.array -- Clusters by columns
    :param clusters_count: int -- Clusters count
    :param cluster_to_split: int -- Cluster to split number
    :return: bool
    """
    # Check if we can split provided cluster
    cluster_to_split_row_indexes = np.where(clusters_row == cluster_to_split)[0]
    cluster_to_split_col_indexes = np.where(clusters_col == cluster_to_split)[0]
    if len(cluster_to_split_row_indexes) == 1 or len(cluster_to_split_col_indexes) == 1:
        return False
    # Pick random point for splitting
    split_row_index = np.random.choice(cluster_to_split_row_indexes[1:])
    split_col_index = np.random.choice(cluster_to_split_col_indexes[1:])
    # Split by row
    increment_from_index(clusters_row, split_row_index)
    increment_from_index(clusters_col, split_col_index)
    return True


def union_clusters(clusters_row: np.array, clusters_col: np.array, clusters_count: int, cluster_to_union: int) -> bool:
    """
    Union provided cluster with the next one
    :param clusters_row: np.array -- Clusters row
    :param clusters_col: np.array -- Clusters col
    :param clusters_count: int -- Clusters count
    :param cluster_to_union: int -- Cluster number to union
    :return: bool
    """
    if clusters_count == 1:
        return False
    clusters_row[clusters_row > cluster_to_union] = clusters_row[clusters_row > cluster_to_union] - 1
    clusters_col[clusters_col > cluster_to_union] = clusters_col[clusters_col > cluster_to_union] - 1
    return True


def write_result_to_file(path_to_file: str, solution: Solution):
    with open(path_to_file, 'w') as f:
        f.write(solution.format())
