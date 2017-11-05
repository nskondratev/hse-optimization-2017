from .abstract_local_search import AbstractLocalSearch
from lab_2.util import split_clusters
import numpy as np


class LocalSearchByClustersSplitting(AbstractLocalSearch):
    def get_improved_solution(self):
        clusters_count = len(np.unique(self.initial_solution.clusters_row))
        clusters_to_split = np.arange(1, clusters_count + 1)
        np.random.shuffle(clusters_to_split)
        for cluster_to_split in clusters_to_split:
            tmp_solution = self.initial_solution.copy()
            if split_clusters(tmp_solution.clusters_row, tmp_solution.clusters_col, clusters_count,
                              cluster_to_split) and tmp_solution.is_better(self.initial_solution):
                return tmp_solution
        return None
