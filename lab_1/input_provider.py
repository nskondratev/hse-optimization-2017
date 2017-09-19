import numpy as np
import os
import re

TEST_INSTANCES_DIR = 'test_instances'


def read_n_lines_as_matrix(f, n):
    res = ''
    for i in range(n):
        row = f.readline().lstrip()
        res = res + row
    res = '; '.join(res.split("\n"))  # Replace newline character with semicolon
    res = re.sub(' +', ' ', res)  # Replace multiple spaces with the single one
    res = re.sub('; $', '', res)  # Replace semicolon from the end of string
    return np.matrix(res, dtype=np.uint8)


def read_from_file(filename):
    with open(os.path.join(TEST_INSTANCES_DIR, filename)) as f:
        n = int(f.readline().strip())
        dm = read_n_lines_as_matrix(f, n)
        f.readline()
        fm = read_n_lines_as_matrix(f, n)
        return n, dm, fm
