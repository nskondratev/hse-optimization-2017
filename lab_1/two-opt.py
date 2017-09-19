import numpy as np
import lab_1.input_provider as ip

def calc_obj_fun_value(solution, n, d, f):
    res = 0.0
    for i in range(n):
        print('Place #{} facility in location #{}'.format(i, solution[i]))
        res = res + d[]

if __name__ == '__main__':
    test_filename = 'tai12a'
    n, d, f = ip.read_from_file(test_filename)
    print('Read data from file: n = {}, d.shape = {}, f.shape = {}'.format(n, d.shape, f.shape))

