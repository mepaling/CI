# coding: utf-8
# pylint: disable = C0103, C0301, C0200

"""Radial Basis Function Network"""

import math
import numpy

class RBFN(object):
    """RBFN Main Class"""
    def __init__(self, J, xDim):
        #self.sigma = [0.0 for _ in range(J)]
        self.sigma = numpy.zeros((J), numpy.float32)
        #self.W = [0.0 for _ in range(J)]
        self.W = numpy.zeros((J), numpy.float32)
        #self.M = [[0.0 for _ in range(xDim)] for _ in range(J)]
        self.M = numpy.zeros((J, xDim), numpy.float32)
        self.J = J
        self.xDim = xDim
        self.bias = 0

    def calculateOutput(self, x):
        """Calculate the output of Gauss base function"""
        ret = 0.0
        for i in range(self.J):
            val = self.W[i] * math.exp(- self.dist(x, self.M[i]) / (2 * self.sigma[i] * self.sigma[i]))
            ret += val
        return ret

    def dist(self, x, y):
        """Calculate vector's distance"""
        ret = 0.0
        for i in range(len(x)):
            ret += (x[i] - y[i]) * (x[i] - y[i])
        return ret
