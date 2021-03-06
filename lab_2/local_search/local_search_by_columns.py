from .abstract_local_search import AbstractLocalSearch
from ..util import swap_cols
from ..solution import Solution
import numpy as np
from typing import Optional


class LocalSearchByColumns(AbstractLocalSearch):
    @staticmethod
    def improve_solution(solution_to_improve: Solution) -> Optional[Solution]:
        initial_solution = solution_to_improve.copy()
        range_i = np.arange(0, initial_solution.p - 1)
        np.random.shuffle(range_i)
        for i in range_i:
            range_j = np.arange(i + 1, initial_solution.p)
            np.random.shuffle(range_j)
            for j in range_j:
                # Skip columns if they are in the same cluster
                if initial_solution.clusters_col[i] == initial_solution.clusters_col[j]:
                    continue
                tmp_solution = initial_solution.copy()
                swap_cols(tmp_solution.matrix, i, j, tmp_solution.perm_col)
                if tmp_solution.is_better(initial_solution):
                    return tmp_solution
        return None
