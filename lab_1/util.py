import numpy as np
import os
import re

TEST_INSTANCES_DIR = 'test_instances'


# Helper function to parse one matrix from file
def read_n_lines_as_matrix(f, n):
    res = ''
    all_indexes = []
    for i in range(n):
        row = f.readline().lstrip()
        res = res + row
        all_indexes.append(i)
    res = '; '.join(res.split("\n"))  # Replace newline character with semicolon
    res = re.sub(' +', ' ', res)  # Replace multiple spaces with the single one
    res = re.sub('; $', '', res)  # Replace semicolon from the end of string
    res = np.matrix(res, dtype=np.float)
    res[tuple(all_indexes), tuple(all_indexes)] = np.nan # Replace diagonal zeros with NaN
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


# 2-opt algorithm
def two_opt(n, d, f):
    # Step 1
    prev_best_solution = build_initial_solution(n)
    while True:
        # Step 2
        current_best_solution = prev_best_solution.copy()
        current_best_obj_value = calc_obj_fun_value(current_best_solution, n, d, f)
        current_solution = current_best_solution.copy()
        for i in range(n):
            for j in range(i + 1, n):
                # Change i facility with j
                temp = current_solution[i]
                current_solution[i] = current_solution[j]
                current_solution[j] = temp
                cur_obj_value = calc_obj_fun_value(current_solution, n, d, f)
                # Compare with current best result
                if cur_obj_value < current_best_obj_value:
                    current_best_solution = current_solution.copy()
                    current_best_obj_value = cur_obj_value
        # Step 3
        if np.array_equal(current_best_solution, prev_best_solution):
            break
        else:
            prev_best_solution = current_best_solution
    return prev_best_solution, calc_obj_fun_value(prev_best_solution, n, d, f)
