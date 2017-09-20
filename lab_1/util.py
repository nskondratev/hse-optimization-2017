import numpy as np


def calc_obj_fun_value(solution, n, d, f):
    res = 0.0
    for i in range(n - 1):
        for j in range(i + 1, n):
            print('Place #{} facility in location #{}'.format(i, solution[i]))
            res = res + f[i, j] * d[solution[i], solution[j]]
    return res

def argextr(m, filter):
    for i in filter:
        print()

def find_initial_solution(n, d, f):
    rest_facilities = set()
    rest_locations = set()
    solution = []
    for i in range(n):
        rest_facilities.add(i)
        rest_locations.add(i)
        solution.append(np.nan)
    while len(rest_facilities) > 0:
        a = rest_facilities.pop()
        if len(rest_locations) == 1 and len(rest_facilities) == 0:
            solution[a] = rest_locations.pop()
            break
        # Find maximum flow facility
        wts = f[a, tuple(rest_facilities)]
        print('Facility #{}, flows to search: {}'.format(a, wts))
        b = np.nanargmax(wts)
        # Locate them in nearest locations
        rest_loc_m = d[:, tuple(rest_locations)][tuple(rest_locations), :]
        nearest_locations = np.where(rest_loc_m == np.nanmin(rest_loc_m))[0]
        solution[a] = nearest_locations[0]
        solution[b] = nearest_locations[1]
        # Remove processed facilities and locations from search
        rest_facilities.remove(b)
        rest_locations.remove(nearest_locations[0])
        rest_locations.remove(nearest_locations[1])
    return solution

