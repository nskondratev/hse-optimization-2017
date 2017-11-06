from .abstract_shaking import AbstractShaking
from lab_2.solution import Solution
from lab_2.util import split_clusters
from typing import Optional
import numpy as np


class ShakingByClustersSplitting(AbstractShaking):
    @staticmethod
    def shake_solution(solution_to_shake: Solution) -> Optional[Solution]:
        shaken_solution = solution_to_shake.copy()
        clusters_count = len(np.unique(shaken_solution.clusters_row))
        clusters_to_split = np.arange(1, clusters_count + 1)
        np.random.shuffle(clusters_to_split)
        for cluster_to_split in clusters_to_split:
            if split_clusters(shaken_solution.clusters_row, shaken_solution.clusters_col, clusters_count,
                              cluster_to_split):
                return shaken_solution
        return None
