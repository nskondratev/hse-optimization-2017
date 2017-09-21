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
    prev_best_solution = initial_solution.copy()
    while True:
        # Step 2
        current_best_solution = prev_best_solution.copy()
        current_best_obj_value = util.calc_obj_fun_value(current_best_solution, n, d, f)
        current_solution = current_best_solution.copy()
        for i in range(n):
            for j in range(i + 1, n):
                # Change i facility with j
                temp = current_solution[i]
                current_solution[i] = current_solution[j]
                current_solution[j] = temp
                cur_obj_value = util.calc_obj_fun_value(current_solution, n, d, f)
                # Compare with current best result
                if cur_obj_value < current_best_obj_value:
                    current_best_solution = current_solution.copy()
                    current_best_obj_value = cur_obj_value
        # Step 3
        if np.array_equal(current_best_solution, prev_best_solution):
            break
        else:
            prev_best_solution = current_best_solution
    return prev_best_solution


def iterated_local_search(n, d, f):
    MAX_UNCHANGED_ITERATIONS = n**3
    initial_solution = util.build_random_solution(n)
    best_solution = local_search(initial_solution, n, d, f)
    best_obj = util.calc_obj_fun_value(best_solution, n, d, f)
    print('Initial best objective function value: {}'.format(best_obj))
    no_change = 0
    while True:
        new_initial_solution = util.build_random_solution(n)
        current_solution = local_search(new_initial_solution, n, d, f)
        current_obj = util.calc_obj_fun_value(current_solution, n, d, f)
        if current_obj < best_obj:
            best_obj = current_obj
            best_solution = current_solution.copy()
            print('Improved best objective function value: {}'.format(best_obj))
            no_change = 0
        else:
            no_change = no_change + 1
        if no_change == MAX_UNCHANGED_ITERATIONS:
            break
    return best_solution, best_obj
