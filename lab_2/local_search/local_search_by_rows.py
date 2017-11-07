from .abstract_local_search import AbstractLocalSearch
from ..util import swap_rows
from ..solution import Solution
import numpy as np
from typing import Optional


class LocalSearchByRows(AbstractLocalSearch):
    @staticmethod
    def improve_solution(solution_to_improve: Solution) -> Optional[Solution]:
        initial_solution = solution_to_improve.copy()
        range_i = np.arange(0, initial_solution.m - 1)
        np.random.shuffle(range_i)
        for i in range_i:
            range_j = np.arange(i + 1, initial_solution.m)
            np.random.shuffle(range_j)
            for j in range_j:
                tmp_solution = initial_solution.copy()
                swap_rows(tmp_solution.matrix, i, j, tmp_solution.perm_row)
                if tmp_solution.is_better(initial_solution):
                    return tmp_solution
        return None
