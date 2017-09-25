import lab_1.util as util
import lab_1.algorithms as alg

if __name__ == '__main__':
    test_filename = 'tai12a'
    n, d, f = util.read_from_file(test_filename)
    print('Read from file: n = {}, d.shape = {}, f.shape = {}'.format(n, d.shape, f.shape))
    sol, sol_obj = alg.repeated_local_search(n, d, f)
    print('Find solution: {}, objective func value = {}'.format(sol, sol_obj))

