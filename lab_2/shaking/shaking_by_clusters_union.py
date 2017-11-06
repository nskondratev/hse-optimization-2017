from .abstract_shaking import AbstractShaking
from lab_2.util import union_clusters
from lab_2.solution import Solution
from typing import Optional
import numpy as np


class ShakingByClustersUnion(AbstractShaking):
    @staticmethod
    def shake_solution(solution_to_shake: Solution) -> Optional[Solution]:
        shaken_solution = solution_to_shake.copy()
        clusters_count = len(np.unique(shaken_solution.clusters_row))
        clusters_union_range = np.arange(1, clusters_count)
        np.random.shuffle(clusters_union_range)
        for cluster_to_union in clusters_union_range:
            if union_clusters(shaken_solution.clusters_row, shaken_solution.clusters_col, clusters_count,
                              cluster_to_union):
                return shaken_solution
        return None
