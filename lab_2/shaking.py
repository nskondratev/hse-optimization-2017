import lab_2.util as util
import random


# this function changes matrix, does not change clusters -> matrix, perm_row are renewed
def by_rows(matrix, m, p, perm_row):
    a1 = random.randint(0, m - 1)
    a2 = a1
    while (a2 == a1): a2 = random.randint(0, m - 1)
    return util.swap_rows(matrix, a1, a2, perm_row)


# this function changes matrix, does not change clusters -> matrix, perm_col are renewed
def by_columns(matrix, m, p, perm_col):
    b1 = random.randint(0, p - 1)
    b2 = b1
    while (b2 == b1): b2 = random.randint(0, p - 1)
    return util.swap_cols(matrix, b1, b2, perm_col)


# this function changes clusters, does not change matrix -> clusters_row, clusters_col are renewed
def by_clusters_splitting(clusters_row, clusters_col, current_number_of_clusters):
    res = -1
    if (current_number_of_clusters == min(len(clusters_row), len(clusters_col))):
        return -1  # no shaking is possible
    while (res == -1):
        res = util.split_clusters(clusters_row, clusters_col, current_number_of_clusters,
                                  random.randint(1, current_number_of_clusters))
    return res


# this function changes clusters, does not change matrix -> clusters_row, clusters_col are renewed
def by_clusters_union(clusters_row, clusters_col, current_number_of_clusters):
    res = -1
    if (current_number_of_clusters == 1):
        return -1  # no shaking is possible
    while (res == -1):
        res = util.union_two_clusters(clusters_row, clusters_col, current_number_of_clusters,
                                      random.randint(1, current_number_of_clusters - 1))
    return res
