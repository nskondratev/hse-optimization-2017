from .abstract_local_search import AbstractLocalSearch
from lab_2.util import swap_cols
import numpy as np


class LocalSearchByColumns(AbstractLocalSearch):
    def get_improved_solution(self):
        range_i = np.arange(self.initial_solution.p - 1)
        np.random.shuffle(range_i)
        for i in range_i:
            range_j = np.arange(i + 1, self.initial_solution.p)
            np.random.shuffle(range_j)
            for j in range_j:
                tmp_solution = self.initial_solution.copy()
                swap_cols(tmp_solution.matrix, i, j, tmp_solution.perm_col)
                if tmp_solution.is_better(self.initial_solution): return tmp_solution
        return None
