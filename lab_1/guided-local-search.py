import numpy as np
import lab_1.util as util
import lab_1.algorithms as alg

if __name__ == '__main__':
    test_filename = 'tai12a'
    n, d, f = util.read_from_file(test_filename)
    print('Read from file: n = {}, d.shape = {}, f.shape = {}'.format(n, d.shape, f.shape))

    # Build random solution
    random_solution = util.build_random_solution(n)

    # Calc objective function value for some solution
    obj_fun_value = util.calc_obj_fun_value(random_solution, n, d, f)

    # Use local search (2-opt algorithm)
    improved_solution = alg.local_search(random_solution, n, d, f)
