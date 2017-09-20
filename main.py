#!/usr/bin/env python


import sys
import math
import matplotlib.pyplot as plt

ARRAY_LEN = 1000000


def my_random(a, r0, m):
    rn_1 = r0
    lst = list()
    lst.append(r0)
    for i in range(1, ARRAY_LEN):
        arn_1 = a * rn_1
        rn_1 = arn_1 % m
        lst.append(rn_1 / m)
    return lst


def print_hist(lst):
    plt.hist(lst, bins=20)
    plt.show()


def calc_params(lst):
    mx = (1 / len(lst)) * sum(lst)
    sumsqr = 0
    for xi in lst:
        sumsqr += (xi - mx) ** 2
    dx = (1 / (len(lst) - 1)) * sumsqr
    sigma = math.sqrt(dx)
    print("~Mx = %f" % mx)
    print("~Dx = %f" % dx)
    print("~Sigma = %f" % sigma)
    return (mx, dx, sigma)


def uniformity_test(lst):
    k = 0
    for i in range(0, len(lst) // 2):
        if (lst[2 * i] ** 2) + (lst[(2 * i) + 1] ** 2) < 1:
            k += 1
    print("%f -> %f" % ((2 * k / len(lst)), (math.pi / 4)))


def aperiodic_test(a, r0, m):
    lst1 = my_random(a, r0, m)
    xv = lst1[-1]

    lst2 = my_random(a, r0, m)
    i1 = -1
    i2 = -1
    for i in range(0, ARRAY_LEN):
        if (lst1[i] == xv) and (lst2[i] == xv) and (i1 == -1):
            i1 = i
            continue
        if (lst1[i] == xv) and (lst2[i] == xv) and (i2 == -1):
            i2 = i
            break
    p = i2 - i1

    lst1 = my_random(a, r0, m)
    lst2 = my_random(a, r0, m)
    i3 = -1
    for i in range(0, ARRAY_LEN):
        if (lst1[i] == lst1[i + p]) and (lst2[i] == lst2[i + p]):
            i3 = i
            break
    l = i3 + p
    print("P = %d" % p)
    print("L = %d" % l)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Using: " + sys.argv[0] + " a R0 m")
        exit(0)
    a = int(sys.argv[1])
    r0 = int(sys.argv[2])
    m = int(sys.argv[3])
    lst = my_random(a, r0, m)
    calc_params(lst)
    uniformity_test(lst)
    aperiodic_test(a, r0, m)
    #  print_hist(lst)
