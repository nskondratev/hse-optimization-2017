import lab_2.util as util
import random


# perm_row and perm_col save information about permutations with matrix;
# perm_row and perm_col are passed by reference


def swap(a, i, j):
    a[i], a[j] = a[j], a[i]


# this function changes matrix, does not change clusters -> matrix, perm_row are renewed
def move_row(matrix, i, j, perm_row):
    res = matrix.copy()
    res[i] = res[j]
    res[j] = matrix[i]
    swap(perm_row, i, j)
    return res


# this function changes matrix, does not change clusters -> matrix, perm_col are renewed
def move_col(matrix, i, j, perm_col):
    res = matrix.copy()
    res[:, i] = res[:, j]
    res[:, j] = matrix[:, i]
    swap(perm_col, i, j)
    return res


# this function changes clusters, does not change matrix -> clusters_row, clusters_col are renewed
def split_cluster(clusters_row, clusters_col, current_number_of_clusters, number_of_cluster):
    if (current_number_of_clusters >= min(len(clusters_row), len(clusters_col))):
        return -1  # cannot split if all clusters are 1*1
    new_row = clusters_row.copy()
    new_col = clusters_col.copy()
    part_row = []
    part_col = []
    # find cluster to split, at least 2*2
    M = number_of_cluster  # number of cluster to split
    for i in range(len(new_row)):
        if (new_row[i] == M): part_row.append(i)
    for i in range(len(new_col)):
        if (new_col[i] == M): part_col.append(i)
    if ((len(part_row) < 2) | (len(part_col) < 2)):
        return -1  # cannot split this cluster
    # choose row and column to split
    a = part_row[0] + random.randint(1, len(part_row) - 1)
    b = part_col[0] + random.randint(1, len(part_col) - 1)
    for i in range(a, len(new_row)):
        new_row[i] += 1
    for i in range(b, len(new_col)):
        new_col[i] += 1
    return new_row, new_col


# this function changes clusters, does not change matrix -> clusters_row, clusters_col are renewed
def union_two_clusters(clusters_row, clusters_col, current_number_of_clusters, number_of_cluster):
    if (current_number_of_clusters == 1):
        return -1  # cannot union if there is only one cluster
    new_row = clusters_row.copy()
    new_col = clusters_col.copy()
    # find clusters to union
    M = number_of_cluster  # union M and M + 1 clusters
    part_row = []
    part_col = []
    for i in range(len(new_row)):
        if (new_row[i] >= M + 1): new_row[i] -= 1
    for i in range(len(new_col)):
        if (new_col[i] >= M + 1): new_col[i] -= 1
    return new_row, new_col


# this function changes matrix, does not change clusters -> matrix, perm_row are renewed
# clusters are constant and used only to find objective function
def local_search_move_row(matrix, n1, m, p, clusters_row, clusters_col, perm_row):
    curr_obj = util.objective_function(matrix, n1, clusters_row, clusters_col)
    for i in range(m - 1):
        for j in range(i + 1, m):
            new_matrix = move_row(matrix, i, j, perm_row)
            new_obj = util.objective_function(new_matrix, n1, clusters_row, clusters_col)
            if (new_obj > curr_obj): return new_matrix, new_obj, clusters_row, clusters_col
    return -1


# this function changes matrix, does not change clusters -> matrix, perm_col are renewed
# clusters are constant and used only to find objective function
def local_search_move_col(matrix, n1, m, p, clusters_row, clusters_col, perm_col):
    curr_obj = util.objective_function(matrix, n1, clusters_row, clusters_col)
    for i in range(p - 1):
        for j in range(i + 1, p):
            new_matrix = move_col(matrix, i, j, perm_col)
            new_obj = util.objective_function(new_matrix, n1, clusters_row, clusters_col)
            if (new_obj > curr_obj): return new_matrix, new_obj, clusters_row, clusters_col
    return -1


# this function changes clusters, does not change matrix -> clusters_row, clusters_col are renewed
# matrix is constant and used only to find objective
def local_search_split_cluster(matrix, n1, m, p, clusters_row, clusters_col, current_number_of_clusters):
    curr_obj = util.objective_function(matrix, n1, clusters_row, clusters_col)
    N = current_number_of_clusters
    for i in range(1, N + 1):
        res = split_cluster(clusters_row, clusters_col, N, i)
        if (res != -1):
            new_row, new_col = res
            new_obj = util.objective_function(matrix, n1, new_row, new_col)
            if (new_obj > curr_obj): return matrix, new_obj, new_row, new_col
    return -1


# this function changes clusters, does not change matrix -> clusters_row, clusters_col are renewed
# matrix is constant and used only to find objective
def local_search_union_clusters(matrix, n1, m, p, clusters_row, clusters_col, current_number_of_clusters):
    curr_obj = util.objective_function(matrix, n1, clusters_row, clusters_col)
    new_row = clusters_row.copy()
    new_col = clusters_col.copy()
    N = current_number_of_clusters
    for i in range(1, N):
        res = split_cluster(clusters_row, clusters_col, N, i)
        if (res != -1):
            new_row, new_col = res
            new_obj = util.objective_function(matrix, n1, new_row, new_col)
            if (new_obj > curr_obj): return matrix, new_obj, new_row, new_col
    return -1


# this function changes matrix, does not change clusters -> matrix, perm_row are renewed
def shaking_row(matrix, m, p, perm_row):
    a1 = random.randint(0, m - 1)
    a2 = a1
    while (a2 == a1): a2 = random.randint(0, m - 1)
    return move_row(matrix, a1, a2, perm_row)


# this function changes matrix, does not change clusters -> matrix, perm_col are renewed
def shaking_col(matrix, m, p, perm_col):
    b1 = random.randint(0, p - 1)
    b2 = b1
    while (b2 == b1): b2 = random.randint(0, p - 1)
    return move_col(matrix, b1, b2, perm_col)


# this function changes clusters, does not change matrix -> clusters_row, clusters_col are renewed
def shaking_split(clusters_row, clusters_col, current_number_of_clusters):
    res = -1
    if (current_number_of_clusters == min(len(clusters_row), len(clusters_col))):
        return -1  # no shaking is possible
    while (res == -1):
        res = split_cluster(clusters_row, clusters_col, current_number_of_clusters,
                            random.randint(1, current_number_of_clusters))
    return res


# this function changes clusters, does not change matrix -> clusters_row, clusters_col are renewed
def shaking_union(clusters_row, clusters_col, current_number_of_clusters):
    res = -1
    if (current_number_of_clusters == 1):
        return -1  # no shaking is possible
    while (res == -1):
        res = union_two_clusters(clusters_row, clusters_col, current_number_of_clusters,
                                 random.randint(1, current_number_of_clusters - 1))
    return res
