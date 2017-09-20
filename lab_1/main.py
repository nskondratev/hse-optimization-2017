import lab_1.util as util

if __name__ == '__main__':
    test_filename = 'test3'
    n, d, f = util.read_from_file(test_filename)
    print('Read from file: n = {}, d.shape = {}, f.shape = {}'.format(n, d.shape, f.shape))
    sol = util.build_initial_solution(n)
    sol_obj = util.calc_obj_fun_value(sol, n, d, f)
    print('Find initial solution: {}, objective func value = {}'.format(sol, sol_obj))

