import numpy as np
import os
import re

TEST_INSTANCES_DIR = 'test_instances'


def read_n_lines_as_matrix(f, n):
    res = ''
    for i in range(n):
        row = f.readline().lstrip()
        res = res + row
    res = '; '.join(res.split("\n")) # Replace newline character with semicolon
    res = re.sub(' +', ' ', res) # Replace multiple spaces with the single one
    res = re.sub('; $', '', res) # Replace semicolon from the end of string
    return np.matrix(res, dtype=np.uint8)


def read_from_file(filename):
    with open(os.path.join(TEST_INSTANCES_DIR, filename)) as f:
        n = int(f.readline().strip())
        # print('N = {}'.format(n))
        # print('Read distances matrix...')
        dm = read_n_lines_as_matrix(f, n)
        # print('Distances matrix is read.\n', dm.shape)
        f.readline()
        # print('Read flows matrix...')
        fm = read_n_lines_as_matrix(f, n)
        # print('Flows matrix is read.\n', fm.shape)
        return n, dm, fm


if __name__ == '__main__':
    test_filename = 'tai20a'
    n, d, f = read_from_file(test_filename)
    print('Read from file: n = {}, d.shape = {}, f.shape = {}'.format(n, d.shape, f.shape))
