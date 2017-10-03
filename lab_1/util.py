import numpy as np
import os
import re
import random
from random import shuffle
from lab_1.constants import TEST_INSTANCES_DIR, SOLUTIONS_DIR


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
    res[tuple(all_indexes), tuple(all_indexes)] = np.nan  # Replace diagonal zeros with NaN
    return res


# Read file and return number of facilities and locations, flows and distance matrices
def read_from_file(filename):
    with open(os.path.join(TEST_INSTANCES_DIR, filename)) as f:
        n = int(f.readline().strip())
        dm = read_n_lines_as_matrix(f, n)
        f.readline()
        fm = read_n_lines_as_matrix(f, n)
        return n, dm, fm


# Write solution to file
def write_solution_to_file(filename, solution, dir = SOLUTIONS_DIR):
    # Ensure that directory exists
    if not os.path.exists(dir):
        os.mkdir(dir)

    with open(os.path.join(dir, '{}.sol'.format(filename)), 'w') as f:
        f.write(solution.join(' '))


# Return objective function value based on provided solution, n, distance and flows matrices
def calc_obj_fun_value(solution, n, d, f):
    res = 0.0
    for i in range(n - 1):
        for j in range(i + 1, n):
            res = res + f[i, j] * d[solution[i], solution[j]]
    return res


def penalized_objective(solution, n, d, f, alpha, penalty_vec):
    res = 0.0
    for i in range(n - 1):
        for j in range(i + 1, n):
            res = res + f[i, j] * d[solution[i], solution[j]] + alpha * penalty_vec[i, j, solution[i], solution[j]]
    return res


# Build random initial solution
def build_random_solution(n):
    return np.random.permutation(n)


# Perturbation, k components
def perturbation(k0, solution):
    new_solution = solution.copy()
    n = len(solution)
    k = np.minimum(k0, n)
    part_solution = random.sample(list(new_solution), k)
    positions = []
    for i in range(len(new_solution)):
        for j in range(len(part_solution)):
            if (new_solution[i] == part_solution[j]):
                positions.append(i)
    shuffle(part_solution)
    for i in range(len(positions)):
        new_solution[positions[i]] = part_solution[i]
    return new_solution


def get_max_unchanged_iterations_number(n):
    return 5 * n
