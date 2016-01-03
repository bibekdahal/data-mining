#!/usr/bin/env python3

import math
import numpy as np


# Make copy of a matrix
def copy(m):
    m1 = []
    for x in m:
        tmp = [y for y in x]
        m1.append(tmp)
    return m1


# Get identity matrix of m x n size
def identiy(m, n):
    m = []
    for x in range(m):
        tmp = []
        for y in range(n):
            if x == y:
                tmp.append(1)
            else:
                tmp.append(0)
        m.append(tmp)
    return m


# Get product of two matrices
def multiply(m1, m2):
    m = []
    r = len(m1)
    c = len(m2[0])
    c1 = len(m1[0])
    for x in range(r):
        tmp = []
        for y in range(c):
            s = 0
            for z in range(c1):
                s += m1[x][z] * m2[z][y]
            tmp.append(s)
        m.append(tmp)
    return m


# Get transpose of matrix
def transpose(m):
    m1 = []
    r = len(m)
    c = len(m[0])
    for x in range(c):
        tmp = []
        for y in range(r):
            tmp.append(m[y][x])
        m1.append(tmp)
    return m1


# Print a matrix
def mprint(m):
    for i in m:
        print(*i)


# Compute SVD of a matrix and print the result
def svd(x):
    xt = transpose(x)
    xxt = multiply(x, xt)
    e1, ev1 = np.linalg.eig(xxt)
    ev1, e1 = ev1.tolist(), e1.tolist()

    xtx = multiply(xt, x)
    e2, ev2 = np.linalg.eig(xtx)
    ev2, e2 = ev2.tolist(), e2.tolist()

    ec = []
    e2tmp = [int(t) for t in e2]
    for e in e1:
        if int(e) in e2tmp:
            ec.append(np.sqrt(e))

    A = []
    for i, e in enumerate(ec):
        tmp = []
        for j in range(len(ec)):
            if i != j:
                tmp.append(0)
            else:
                tmp.append(e)
        A.append(tmp)

    U = ev1
    VT = ev2

    print("X =")
    mprint(x)
    print("\nX = W * A * VT, where:")
    print("\nU =")
    mprint(U)
    print("\nA =")
    mprint(A)
    print("\nVT =")
    mprint(VT)


svd([[1, 1, 0, 2], [1, 1, 2, 0], [2, 0, 1, 1]])
