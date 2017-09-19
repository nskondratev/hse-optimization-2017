import lab_1.input_provider as ip

if __name__ == '__main__':
    test_filename = 'tai20a'
    n, d, f = ip.read_from_file(test_filename)
    print('Read from ip file: n = {}, d.shape = {}, f.shape = {}'.format(n, d.shape, f.shape))
