#!/usr/bin/env python

import sys
import math
import matplotlib.pyplot as plt
import functools as ft
import time

ARR_LEN = 1000000


class Random:
    def __init__(self, r0=108431, a=5689, m=1048496):
        self.r0 = r0
        self.a = a
        self.m = m

    def seed(self, value):
        self.r0 = value

    def random(self):
        self.seed((self.a * self.r0) % self.m)
        return self.r0 / self.m


def print_hist(lst):
    plt.hist(lst, bins=20)
    plt.grid(True)
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


def gamma_distr(eta=4, hl=1):
    random = Random()
    random.seed((time.time()))
    lst = list()
    for i in range(0, eta):
        lst.append(random.random())
    return (-1 / hl) * math.log((ft.reduce((lambda x, y: x * y), lst)), 10)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Using: " + sys.argv[0] + " eta lambda")
        exit(0)
    eta = int(sys.argv[1])
    hl = float(sys.argv[2])
    lst = list()
    for i in range(0, ARR_LEN):
        lst.append(gamma_distr(eta, hl))
    calc_params(lst)
    print_hist(lst)
