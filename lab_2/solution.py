import numpy as np
from hashlib import sha256


def generate_random_clusters(size: int, clusters_count: int) -> np.array:
    """
    Generate random clusters
    :param size: int -- The output array size
    :param clusters_count: int -- Desirable clusters count
    :return: np.array
    """
    # Generate clusters array of needed size
    clusters = np.resize(np.array(list(range(1, clusters_count + 1))), size)
    # Replace repeated cluster numbers with zeros
    clusters[clusters_count:] = 0
    # Replace zeros with random clusters
    clusters[clusters == 0] = np.random.randint(1, clusters_count + 1, size=size - clusters_count)
    return np.sort(clusters)


def decode_clusters(range_ub: int, perm: np.array, clusters: np.array) -> list:
    """
    Decode clusters with permutations
    :param range_ub: int -- Range upper bound
    :param perm: np.array -- Permutations array
    :param clusters: np.array -- Clusters array
    :return: list -- Decoded clusters
    """
    res = []
    for i in range(range_ub):
        real_index = np.where(perm == i)[0][0]
        res.append(str(clusters[real_index]))
    return res


class Solution:
    def __init__(self, matrix: np.ndarray, clusters_row: np.array, clusters_col: np.array, perm_row: np.array = None,
                 perm_col: np.array = None):
        """
        Create new Solution instance
        :param matrix: np.array -- Input matrix
        :param clusters_row: np.array -- Clusters by rows
        :param clusters_col: np.array -- Clusters by columns
        :param perm_row: np.array -- Matrix permutations by rows
        :param perm_col: np.array -- Matrix permutations by columns
        """
        self.matrix = matrix.copy()
        self.clusters_row = clusters_row.copy()
        self.clusters_col = clusters_col.copy()
        self.perm_row = np.array(range(matrix.shape[0])) if perm_row is None else perm_row.copy()
        self.perm_col = np.array(range(matrix.shape[1])) if perm_col is None else perm_col.copy()
        self.__obj_val = None

    def __copy__(self):
        return Solution(self.matrix, self.clusters_row, self.clusters_col, self.perm_row, self.perm_col)

    def copy(self):
        """
        Copy the current solution
        :return: Solution -- new Solution instance with the same properties
        """
        return self.__copy__()

    @property
    def m(self) -> int:
        """
        The number if machines
        :return: int
        """
        return self.matrix.shape[0]

    @property
    def p(self) -> int:
        """
        The number of parts
        :return:
        """
        return self.matrix.shape[1]

    @property
    def obj_val(self) -> float:
        """
        The objective function value
        :return: float -- Objective function value
        """
        if self.__obj_val is None:
            self.__obj_val = Solution.calc_obj_val(self.matrix, self.clusters_row, self.clusters_col)
        return self.__obj_val

    @obj_val.setter
    def obj_val(self, new_obj_val):
        self.__obj_val = new_obj_val

    @staticmethod
    def get_random_solution(matrix: np.ndarray, clusters_count: int = 2):
        """
        Generate random solution
        :param matrix: np.array -- Input matrix
        :param clusters_count: int -- Desirable clusters count
        :return: Solution -- random solution
        """
        m, p = matrix.shape
        clusters_row = generate_random_clusters(m, clusters_count)
        clusters_col = generate_random_clusters(p, clusters_count)
        return Solution(matrix, clusters_row, clusters_col)

    @staticmethod
    def calc_obj_val(matrix: np.matrix, clusters_row: np.array, clusters_col: np.array) -> float:
        """
        Calculate the objective function value
        :param matrix: np.matrix -- Matrix
        :param clusters_row: np.array -- Clusters by rows
        :param clusters_col: np.array -- Clusters by columns
        :return: float -- The objective function value
        """
        n_zeros_in = 0
        n_ones_in = 0
        n1 = np.sum(matrix)
        for i in range(len(clusters_row)):
            for j in range(len(clusters_col)):
                if clusters_row[i] == clusters_col[j]:
                    if matrix[i, j] == 1:
                        n_ones_in += 1
                    else:
                        n_zeros_in += 1
        return n_ones_in / (n1 + n_zeros_in)

    def hash(self):
        h = sha256()
        h.update('{}_{}_{}_{}'.format(self.clusters_row, self.clusters_col, self.perm_row, self.perm_col).encode())
        return h.hexdigest()

    def __str__(self):
        return '<Solution>\nMatrix:\n{},\nclusters by rows: {}, by columns: {},\npermutations by rows: {}, by columns: {},\nobj_val={}'.format(
            self.matrix, self.clusters_row, self.clusters_col, self.perm_row, self.perm_col, self.obj_val)

    def is_better(self, other_solution) -> bool:
        """
        Checks if current solution is better than the other one
        :param other_solution:Solution -- the solution to compare with
        :return:Boolean -- is current solution better than the provided
        """
        if not isinstance(other_solution, Solution):
            raise TypeError('other_solution has to be the instance of Solution class')
        return self.obj_val > other_solution.obj_val

    def format(self) -> str:
        """
        Format solution to needed output format
        :return: str -- Formatted solution
        """
        res_m = decode_clusters(self.m, self.perm_row, self.clusters_row)
        res_p = decode_clusters(self.p, self.perm_col, self.clusters_col)
        return ' '.join(res_m) + '\n' + ' '.join(res_p)
