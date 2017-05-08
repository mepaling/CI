"""Particle"""
# coding: utf-8
# pylint: disable = C0103, C0111, W0403

import random
import copy
import RBFN

class Particle(object):
    """Particle - a particle's status"""
    def __init__(self):
        self.J = 3
        self.xDim = 3
        self.xLength = 1 + self.J + self.J * self.xDim + self.J
        self.f = 0.0
        self.bestf = 0.0
        self.rbf = RBFN.RBFN(self.J, self.xDim)
        self.v = [0.0]*self.xLength
        self.x = [0.0]*self.xLength
        self.best = [0.0]*self.xLength

    def generate(self):
        """Random Generate"""
        for i in range(1):
            self.x[i] = self.best[i] = random.random()
            self.v[i] = random.random()
        for i in range(1, 1+self.J):
            self.x[i] = self.best[i] = random.random()
            self.v[i] = random.random()
        for i in range(1 + self.J, 1 + self.J + self.J*self.xDim):
            self.x[i] = self.best[i] = random.uniform(0, 30)
            self.v[i] = random.uniform(0, 30)
        for i in range(1+self.J + self.J*self.xDim, 1 + self.J + self.J*self.xDim + self.J):
            self.x[i] = self.best[i] = random.uniform(0, 10)
            self.v[i] = random.uniform(0, 10)

    def on(self):
        """Set the RBF Network"""
        for i in range(0, 1):
            self.rbf.bias = min(max(self.x[i], 0), 1)
            self.x[i] = self.rbf.bias

        j = 0
        for i in range(1, 1+self.J):
            self.rbf.W[j] = min(max(self.x[i], 0), 1)
            self.x[i] = self.rbf.W[j]
            j += 1

        j = 0
        for i in range(1+self.J, 1 + self.J + self.J*self.xDim):
            self.rbf.M[j / self.xDim][j % self.xDim] = min(max(self.x[i], 0), 30)
            self.x[i] = self.rbf.M[int(j / self.xDim)][j % self.xDim]
            j += 1

        j = 0
        for i in range(1 + self.J + self.J*self.xDim, 1 + self.J + self.J*self.xDim + self.J):
            self.rbf.sigma[j] = min(max(self.x[i], 1e-6), 10)
            self.x[i] = self.rbf.sigma[j]
            j += 1

    def calculateFitness(self, inputt, outputt):
        """Calculate the stop condition"""
        self.on()
        ret = 0.0
        for i in range(0, len(outputt)):
            ret += (outputt[i] - self.rbf.calculateOutput(inputt[i]))**2
        ret /= 2.0
        self.f = ret
        if self.f < self.bestf:
            self.best = copy.deepcopy(self.x)
            self.bestf = self.f

    def getPSOList(self):
        psolist = []
        for i in range(0, self.xLength):
            psolist.append(self.x[i])
        return psolist
