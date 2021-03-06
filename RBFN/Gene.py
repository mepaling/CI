# coding: utf-8
# pylint: disable = C0103, C0200, C0111

"""Real type of Gene Algorithm"""

import random
import numpy
import RBFN

class Gene(object):
    """Real type Gene Algorithm class"""
    def __init__(self):
        self.J = 3
        self.xDim = 3
        self.DNALength = 1 + self.J + self.J * self.xDim + self.J
        self.f = 0.0
        self.rbf = RBFN.RBFN(self.J, self.xDim)
        #self.DNA = [0.0] * self.DNALength
        self.DNA = numpy.zeros((self.DNALength), numpy.float32)

    def generate(self):
        """Random build Gene"""
        for i in range(1):
            self.DNA[i] = random.random()
        for i in range(1, 1+self.J):
            self.DNA[i] = random.random()
        for i in range(1 + self.J, 1 + self.J + self.J*self.xDim):
            self.DNA[i] = random.uniform(0, 30)
        for i in range(1+self.J + self.J*self.xDim, 1 + self.J + self.J*self.xDim + self.J):
            self.DNA[i] = random.uniform(0, 10)

    def clone(self):
        """Reproduction"""
        g = Gene()
        for i in range(0, self.DNALength):
            g.DNA[i] = self.DNA[i]
        g.f = self.f
        g.on()
        return g

    def calculateFitness(self, inputt, outputt):
        """Calculate the stop condition"""
        self.on()
        ret = 0.0
        for i in range(0, len(outputt)):
            ret += (outputt[i] - self.rbf.calculateOutput(inputt[i]))**2
        ret /= 2.0
        self.f = ret

    def on(self):
        """Set parameters for RBF Network"""
        for i in range(0, 1):
            self.rbf.bias = min(max(self.DNA[i], 0), 1)
            self.DNA[i] = self.rbf.bias

        j = 0
        for i in range(1, 1+self.J):
            self.rbf.W[j] = min(max(self.DNA[i], 0), 1)
            self.DNA[i] = self.rbf.W[j]
            j += 1

        j = 0
        for i in range(1+self.J, 1 + self.J + self.J*self.xDim):
            self.rbf.M[int(j / self.xDim)][j % self.xDim] = min(max(self.DNA[i], 0), 30)
            self.DNA[i] = self.rbf.M[int(j / self.xDim)][j % self.xDim]
            j += 1

        j = 0
        for i in range(1 + self.J + self.J*self.xDim, 1 + self.J + self.J*self.xDim + self.J):
            self.rbf.sigma[j] = min(max(self.DNA[i], 1e-6), 10)
            self.DNA[i] = self.rbf.sigma[j]
            j += 1

    def setGene(self, genestr):
        """Set Best Gene"""
        gene_list = genestr.split()
        for i in range(len(gene_list)):
            self.DNA[i] = gene_list[i]
        self.on()

    def getThetaList(self, inputt):
        ret = []
        for i in inputt:
            ret.append(self.rbf.calculateOutput(i))
        return ret

    def showrbf(self):
        ret = []
        ret.append(self.rbf.bias)
        for i in range(self.J):
            ret.append(self.rbf.W[i])
        for i in range(self.J*self.xDim):
            ret.append(self.rbf.M[int(i / self.xDim)][i % self.xDim])
        for i in range(self.J):
            ret.append(self.rbf.sigma[i])
        return ret

    def getDNAList(self):
        ret = []
        for i in range(self.DNALength):
            ret.append(self.DNA[i])
        return ret

    def showDNA(self):
        ret = self.getDNAList()
        print "DNA:", ret

    def getTheta(self, inputt):
        ret = self.rbf.calculateOutput(inputt)
        ret = ret * 80 - 40
        return ret
