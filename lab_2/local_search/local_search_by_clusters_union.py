from .abstract_local_search import AbstractLocalSearch
from lab_2.util import union_clusters
import numpy as np


class LocalSearchByClustersUnion(AbstractLocalSearch):
    def get_improved_solution(self):
        clusters_count = len(np.unique(self.initial_solution.clusters_row))
        clusters_union_range = np.arange(1, clusters_count)
        np.random.shuffle(clusters_union_range)
        for cluster_to_union in clusters_union_range:
            tmp_solution = self.initial_solution.copy()
            if union_clusters(tmp_solution.clusters_row, tmp_solution.clusters_col, clusters_count,
                              cluster_to_union) and tmp_solution.is_better(self.initial_solution):
                return tmp_solution
        return None
