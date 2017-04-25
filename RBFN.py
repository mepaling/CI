# coding: utf-8
# pylint: disable = C0103, C0301, C0200

"""Radial Basis Function Network"""

import math

class RBFN(object):
    """RBFN Main Class"""
    def __init__(self, J, xDim):
        self.theta = 0
        self.sigma = [0 for _ in range(J)]
        self.W = [0 for _ in range(J)]
        self.M = [[0 for _ in range(xDim)] for _ in range(J)]
        self.J = J
        self.xDim = xDim

    def calculate(self, x):
        """Calculate the output of Gauss base function"""
        ret = self.theta
        for i in range(self.J):
            val = self.W[i] * math.exp(-self.__dist(x, self.M[i] / (2 * self.sigma[i] * self.sigma[i])))
            ret += val
        return ret

    def __dist(self, x, y):
        """Calculate vector's distance"""
        ret = 0
        for i in range(len(x)):
            ret += (x[i] - y[i]) * (x[i] - y[i])
        return ret
