from .abstract_local_search import AbstractLocalSearch
from ..util import union_clusters
from ..solution import Solution
import numpy as np
from typing import Optional


class LocalSearchByClustersUnion(AbstractLocalSearch):
    @staticmethod
    def improve_solution(solution_to_improve: Solution) -> Optional[Solution]:
        initial_solution = solution_to_improve.copy()
        clusters_count = len(np.unique(initial_solution.clusters_row))
        clusters_union_range = np.arange(1, clusters_count)
        np.random.shuffle(clusters_union_range)
        for cluster_to_union in clusters_union_range:
            tmp_solution = initial_solution.copy()
            if union_clusters(tmp_solution.clusters_row, tmp_solution.clusters_col, clusters_count,
                              cluster_to_union) and tmp_solution.is_better(initial_solution):
                return tmp_solution
        return None
