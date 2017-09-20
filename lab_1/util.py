import numpy as np
import os
import re

TEST_INSTANCES_DIR = 'test_instances'

# Helper function to parse one matrix from file
def read_n_lines_as_matrix(f, n):
    res = ''
    for i in range(n):
        row = f.readline().lstrip()
        res = res + row
    res = '; '.join(res.split("\n"))  # Replace newline character with semicolon
    res = re.sub(' +', ' ', res)  # Replace multiple spaces with the single one
    res = re.sub('; $', '', res)  # Replace semicolon from the end of string
    res = np.matrix(res, dtype=np.float)
    res[res == 0] = np.nan
    return res

# Read file and return number of facilities and locations, flows and distance matrices
def read_from_file(filename):
    with open(os.path.join(TEST_INSTANCES_DIR, filename)) as f:
        n = int(f.readline().strip())
        dm = read_n_lines_as_matrix(f, n)
        f.readline()
        fm = read_n_lines_as_matrix(f, n)
        return n, dm, fm

# Return objective function value based on provided solution, n, distance and flows matrices
def calc_obj_fun_value(solution, n, d, f):
    res = 0.0
    for i in range(n - 1):
        for j in range(i + 1, n):
            res = res + f[i, j] * d[solution[i], solution[j]]
    return res


# Build random initial solution
def build_initial_solution(n):
    return np.random.permutation(n)
