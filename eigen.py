#!/usr/bin/env python3


import random
import math
import matplotlib.pyplot as plt


# 10 different points
def getPoints():
    return [(1, 1), (1, 5), (2, 3), (4, 5), (6, 6),
            (3, 7), (8, 9), (12, 23), (7, 8), (9, 10)]


# mean of list of points. Returns (x-mean, y-mean)
def mean(l):
    n = len(l)
    x, y = zip(*l)
    return (sum(x)/n, sum(y)/n)


# covariance from list of x's and y's and their means
def covar(x, y, m):
    n = len(x)
    s = 0
    for i in range(n):
        s += (x[i] - m[0]) * (y[i] - m[1])
    return s / (n-1)


# magnitude of a vector
def magnitude(v):
    nsq = 0
    n = len(v)
    for k in range(n):
        nsq += v[k] * v[k]
    return math.sqrt(nsq)


# covariance matrix of a list of points
def covar_matrix(l):
    f = list(zip(*l))
    n = len(f)
    m = mean(l)
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            v = covar(f[i], f[j], m)
            row.append(v)
        matrix.append(row)
    return matrix


# Calculate eigen vector and value for matrix m by power iteration method
def eigen(m):
    n = len(m)
    b = [0] * n
    b[0] = 1
    norm = 0

    for l in range(100):
        tmp = [0] * n
        for i in range(n):
            for j in range(n):
                tmp[i] += m[i][j] * b[j]

        norm = magnitude(tmp)

        for k in range(n):
            b[k] = tmp[k] / norm

    return b, norm


# Project a list of 2d-points along a unit 2d-vector
def project(l, v):
    n = len(v)
    res = []
    for p in l:
        dot = p[0]*v[0] + p[1]*v[1]
        res.append((dot * v[0], dot * v[1]))
    return res


# scatter plot a set of points
def plot(l, c='blue'):
    x, y = zip(*l)
    plt.scatter(x, y, color=c)


mypoints = getPoints()
plot(mypoints)

covarianceMatrix = covar_matrix(mypoints)
eigenVector, eigenValue = eigen(covarianceMatrix)
plt.arrow(0, 0, eigenVector[0]*eigenValue, eigenVector[1]*eigenValue)

projectedPoints = project(mypoints, eigenVector)
plot(projectedPoints, 'red')

plt.show()
plt.close()
