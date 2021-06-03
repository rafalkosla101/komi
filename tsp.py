# import operator
import numpy as np
from copy import deepcopy
INF = np.inf


def komi(m, path=None, LB_wynik=0):
    if path is None:
        path = []
    m, LB = redukcja(m)
    LB += LB_wynik
    choosed_v = choose(m)
    if choosed_v is None:
        return path, LB_wynik
    m_c = deepcopy(m)
    path_c = deepcopy(path)
    LB_c = deepcopy(LB)

    path.append((choosed_v[0], choosed_v[1]))
    if len(path) < len(m):
        m = update_matrix(m, choosed_v, path)
    else:
        m[choosed_v[0], choosed_v[1]] = INF

    path_l, LB_l = komi(m, path, LB)
    if LB_c + choosed_v[2] < LB_l:
        m_c[choosed_v[0], choosed_v[1]] = INF
        path_r, LB_r = komi(m_c, path_c, LB_c+choosed_v[2])
        if LB_l < LB_r:
            return path_l, LB_l
        else:
            return path_r, LB_r
    else:
        return path_l, LB_l


def sort_path(path):
    start_e = path[0][0]
    wynik = []
    for i in range(0, len(path)):
        for pair in path:
            if pair[0] == start_e:
                wynik.append((start_e, pair[1]))
                start_e = pair[1]
                break
    return wynik


def redukcja(m1):
    m = deepcopy(m1)
    lb = 0
    for wiersz in range(len(m)):
        mw = min(m[wiersz, :])
        if mw < INF-500:
            lb += mw
            m[wiersz, :] = m[wiersz, :] - mw

    for kol in range(len(m[0])):
        mk = min(m[:, kol])
        if mk < INF - 500:
            lb += mk
            m[:, kol] = m[:, kol] - mk
    return m, lb


def mincol(m, i, j):
    mi = np.inf
    for k in range(len(m)):
        if mi > m[k, j] and k != i:
            mi = m[k, j]
    return mi


def minrow(m, i, j):
    mi = np.inf
    for k in range(len(m)):
        if mi > m[i, k] and k != j:
            mi = m[i, k]
    return mi


def choose(m):
    # global path
    tab = []
    costs = []
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] == 0:
                cost = 0
                mk = mincol(m, i, j)
                mw = minrow(m, i, j)
                if mk < INF and mw < INF:
                    cost = mk + mw
                tab.append((i, j, cost))
                costs.append(cost)
                # path.append((i, j))
    if len(tab) == 0:
        return None
    max_c = max(costs)
    for roz in tab:
        if roz[2] == max_c:
            return roz
    # tab.sort(key=operator.itemgetter(2),reverse=True)
    # return tab[0]


def update_matrix(m, data, path):
    # global path
    x, y, cost = data
    m[x, :] = np.inf
    m[:, y] = np.inf
    m[y, x] = INF

    exit_tab = []
    enter_tab = []
    przejscie = []
    # visited = 0
    # exforb = -1
    # enforb = -1

    for i in path:
        exit_tab.append(i[0])
        enter_tab.append(i[1])
    for i in exit_tab:
        for j in enter_tab:
            if i == j:
                przejscie.append(i)
    for pair in path:
        start_ext = pair[0]
        start_ent = pair[1]
        connection_counter = 0
        is_connection = True
        while is_connection:
            is_connection = False
            for trans_vert in przejscie:
                if start_ent == trans_vert:
                    is_connection = True
                    break

            if is_connection:
                for pair2 in path:
                    if pair2[0] == start_ent:
                        start_ent = pair2[1]
                        connection_counter += 1
        if 0 < connection_counter < len(m)-2:
            m[start_ent][start_ext] = INF
    return m
    # if len(przejscie) <len(m) - 2:
    #     for ex in exit:
    #         visited = 0
    #         for tr in przejscie:
    #             if ex == tr:
    #                 visited = 1
    #         if visited == 0:
    #             exforb = ex
    #
    #     for ent in enter:
    #         visited = 0
    #         for tr in przejscie:
    #             if ent == tr:
    #                 visited = 1
    #         if visited == 0:
    #             enforb = ent
    #     m[enforb][exforb] = np.inf


def main():
    # m = [[np.inf,5,3],
    #      [5,np.inf,6],
    #      [6,4,np.inf]]
    # m = np.array(m)
    # m2 = redukcja(m)
    # print(m2[0])
    # print(choose(m2[0]))

    # m2 = [[INF, 1, 2, 1],
    #       [1, INF, 1, 2],
    #       [2, 1, INF, 1],
    #       [1, 2, 1, INF]]
    # m2 = np.array(m2)
    # print(komi(m2))

    m3 = [[INF, 10,  8,   19,  12],
          [10,  INF, 20,  6,   3],
          [8,   20,  INF, 4,   2],
          [19,  6,   4,   INF, 7],
          [12,  3,   2,   7,   INF]]
    m3 = np.array(m3)
    wyniki_m3 = komi(m3)
    print(sort_path(wyniki_m3[0]))
    print("LB = ", wyniki_m3[1])

    m4 = [[10 for i in range(0, 10)] for i in range(0, 10)]
    for i in range(0, 10):
        m4[i][i] = INF
        if i < 9:
            m4[i+1][i] = 1
            m4[i][i+1] = 1
    m4[9][0] = 1
    m4[0][9] = 1
    m4 = np.array(m4)
    print(m4)
    wyniki_m4 = komi(m4)
    print(sort_path(wyniki_m4[0]))
    print("LB = ", wyniki_m4[1])


main()
