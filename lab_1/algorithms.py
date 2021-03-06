import lab_1.util as util
import numpy as np

'''
2-opt algorithm
Idea is taken from:
"Effective heuristics and meta-heuristics for the quadratic assignment problem
with tuned parameters and analytical comparisons", page 3
'''


def local_search(initial_solution, n, d, f):
    # Step 1
    best_solution = initial_solution.copy()
    best_obj = util.calc_obj_fun_value(initial_solution, n, d, f)
    while True:
        # Step 2
        change = False  # indicator that checks if objective value decreases
        current_solution = best_solution.copy()
        i = 0
        j = 1
        while not change and i < n - 1:
            # Change i facility with j
            new_solution = current_solution.copy()
            temp = new_solution[i]
            new_solution[i] = new_solution[j]
            new_solution[j] = temp
            new_obj = util.calc_obj_fun_value(new_solution, n, d, f)
            # Compare with current best result
            if new_obj < best_obj:
                change = True
                current_solution = new_solution.copy()
                best_solution = new_solution.copy()
                best_obj = new_obj
            if j < n - 1:
                j = j + 1
            else:
                i = i + 1
                j = i + 1
        # Step 3
        if not change:
            break
    return best_solution, best_obj


def local_search_penalized_obj(initial_solution, n, d, f, alpha, penalty_vec):
    # Step 1
    best_solution = initial_solution.copy()
    best_obj = util.penalized_objective(initial_solution, n, d, f, alpha, penalty_vec)
    while True:
        # Step 2
        change = False  # indicator that checks if objective value decreases
        current_solution = best_solution.copy()
        i = 0
        j = 1
        while not change and i < n - 1:
            # Change i facility with j
            new_solution = current_solution.copy()
            temp = new_solution[i]
            new_solution[i] = new_solution[j]
            new_solution[j] = temp
            new_obj = util.penalized_objective(new_solution, n, d, f, alpha, penalty_vec)
            # Compare with current best result
            if new_obj < best_obj:
                change = True
                current_solution = new_solution.copy()
                best_solution = new_solution.copy()
                best_obj = new_obj
            if j < n - 1:
                j = j + 1
            else:
                i = i + 1
                j = i + 1
        # Step 3
        if not change:
            break
    return best_solution, best_obj


def repeated_local_search(initial_solution, n, d, f):
    MAX_UNCHANGED_ITERATIONS = util.get_max_unchanged_iterations_number(n)
    best_solution, best_obj = local_search(initial_solution, n, d, f)
    no_change = 0
    while True:
        new_initial_solution = util.build_random_solution(n)
        current_solution, current_obj = local_search(new_initial_solution, n, d, f)
        if current_obj < best_obj:
            best_obj = current_obj
            best_solution = current_solution.copy()
            no_change = 0
        else:
            no_change = no_change + 1
        if no_change == MAX_UNCHANGED_ITERATIONS:
            break
    return best_solution, best_obj


def iterated_local_search(initial_solution, k, n, d, f):
    MAX_UNCHANGED_ITERATIONS = util.get_max_unchanged_iterations_number(n)
    best_solution, best_obj = local_search(initial_solution, n, d, f)
    ls_solution = best_solution.copy()  # found by LS
    no_change = 0
    while True:
        new_initial_solution = util.perturbation(k, ls_solution)
        current_solution, current_obj = local_search(new_initial_solution, n, d, f)
        if current_obj < best_obj:
            best_obj = current_obj
            best_solution = current_solution.copy()
            no_change = 0
        else:
            no_change = no_change + 1
        if no_change == MAX_UNCHANGED_ITERATIONS:
            break
    return best_solution, best_obj


def guided_local_search(initial_solution, alpha, n, d, f):
    MAX_UNCHANGED_ITERATIONS = util.get_max_unchanged_iterations_number(n)
    c = np.zeros((n, n, n, n))
    p = np.zeros((n, n, n, n))
    utility = np.zeros((n, n, n, n))
    no_change = 0
    best_solution = initial_solution.copy()
    best_obj = util.calc_obj_fun_value(initial_solution, n, d, f)
    while True:
        new_initial_solution = best_solution.copy()
        current_solution, penalyzed_obj = local_search_penalized_obj(new_initial_solution, n, d, f, alpha, p)
        current_obj = util.calc_obj_fun_value(current_solution, n, d, f)
        max = 0
        # cost of feature (i,j), i and j are facilities, n(n-1)/2 features
        for i1 in range(n - 1):
            for i2 in range(i1 + 1, n):
                c[i1, i2, current_solution[i1], current_solution[i2]] = f[i1, i2] * d[
                    current_solution[i1], current_solution[i2]]
                # find utility
                utility[i1, i2, current_solution[i1], current_solution[i2]] = c[i1, i2, current_solution[i1],
                                                                                current_solution[i2]] / (1 + p[
                    i1, i2, current_solution[i1], current_solution[i2]])
                if (utility[i1, i2, current_solution[i1], current_solution[i2]] > max):
                    max = utility[i1, i2, current_solution[i1], current_solution[i2]]
                    k1, k2, l1, l2 = i1, i2, current_solution[i1], current_solution[i2]
        # penalty with maximum utility
        p[k1, k2, l1, l2] = p[k1, k2, l1, l2] + 1
        if current_obj < best_obj:
            best_obj = current_obj
            best_solution = current_solution.copy()
            no_change = 0
        else:
            no_change = no_change + 1
        if no_change == MAX_UNCHANGED_ITERATIONS:
            break
    return best_solution, best_obj
