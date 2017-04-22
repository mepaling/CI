"""Real type of Gene Algorithm"""
# coding: utf-8
# pylint: disable = C0103, C0200
import random
import RBFN

class Gene(object):
    """RGA class"""
    def __init__(self):
        self.J = 3
        self.xDim = 3
        self.DNALength = 1 + self.J + self.J * self.xDim + self.J +  self.J
        self.rbf = RBFN.RBFN(self.J, self.xDim)
        self.DNA = [0] * self.DNALength

    def getDNAName(self):
        """Get DNA string"""
        ret = [""]*self.DNALength
        for i in range(self.J):
            ret[i] = "w" + str(i)
        j = 0
        for i in range(1+self.J, 1+self.J+self.J*self.xDim):
            ret[i] = "m" + (j / self.xDim + 1) + "," + (j % self.xDim + 1)
            j += 1
        j = 0
        for i in range(1 + self.J + self.J*self.xDim, 1 + self.J + self.J*self.xDim + self.J):
            ret[i] = "σ" + (j + 1)
            j += 1
        return ret

    def clone(self):
        """Reproduction"""
        g = Gene()
        for i in range(len(self.DNA)):
            g.DNA[i] = self.DNA[i]
        g.on()
        return g

    def on(self):
        """Start iteration"""
        self.rbf.theta = self.DNA[0]
        for i in range(self.J):
            self.rbf.W[i] = self.DNA[i+1]
        j = 0
        for i in range(1+self.J, 1 + self.J + self.J*self.xDim):
            self.rbf.M[j / self.xDim][j % self.xDim] = self.DNA[i]
        j = 0
        for i in range(1 + self.J + self.J*self.xDim, 1 + self.J + self.J*self.xDim + self.J):
            self.rbf.sigma[j] = min(max(self.DNA[i], 1e-6), 10)
            self.DNA[i] = self.rbf.sigma[j]

    def randomBuild(self):
        """Random build Gene"""
        for i in range(1):
            self.DNA[i] = random.random()
        for i in range(1, 1+self.J):
            self.DNA[i] = random.random()
        for i in range(1 + self.J, 1 + self.J + self.J*self.xDim):
            self.DNA[i] = random.random() * 30
        for i in range(1+self.J + self.J*self.xDim, 1 + self.J + self.J*self.xDim + self.J):
            self.DNA[i] = random.random() * 10
        self.on()

    def calculateFitness(self, correct, x):
        """Calculate the stop condition"""
        ret = 0.0
        for i in range(len(correct)):
            f = self.rbf.calculate(x[i])
            ret += pow(correct[i]-f, 2)
        ret /= 2.0
        return ret
