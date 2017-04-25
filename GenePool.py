# coding: utf-8
# pylint: disable = C0103, C0200, R0902, R0912, R0913

"""Gene Pool - Actually do the algorithm"""

import random
import Gene
import GenePair

class GenePool(object):
    """Gene Pool class"""
    def __init__(self, gm, poolsize=512, pro_CS=0.5, rat_CS=0.5, pro_MU=0.5, rat_MU=0.5):
        self.poolsize = poolsize
        self.pro_CS = pro_CS
        self.rat_CS = rat_CS
        self.pro_MU = pro_MU
        self.rat_MU = rat_MU
        self.gene = [0]*poolsize
        self.newgene = [0]*poolsize
        for i in range(len(self.gene)):
            self.gene[i] = Gene.Gene()
        self.geneMachine = gm
        self.init(None)

    def init(self, prevBest):
        """initialize the genes"""
        if prevBest is None or len(prevBest) is 0:
            for i in range(len(self.gene)):
                self.gene[i].randomBuild()
        else:
            percent25 = int(len(self.gene) / 4)
            for i in range(percent25):
                x = int(random.random() * len(prevBest))
                self.gene[i] = prevBest[x]
            for i in range(percent25, len(self.gene)):
                self.gene[i].randomBuild()
        for i in range(len(self.gene)):
            self.gene[i].on()

    def geneCrossover(self, x, y, xg, yg):
        """Do Gene Crossover and use real type"""
        ratio = (random.random() - 0.5) * 2 * self.rat_CS
        nx = Gene.Gene()
        ny = Gene.Gene()
        for i in range(len(xg.DNA)):
            nx.DNA[i] = xg.DNA[i] + ratio * (xg.DNA[i] - yg.DNA[i])
            ny.DNA[i] = yg.DNA[i] + ratio * (xg.DNA[i] - yg.DNA[i])
        self.newgene[x] = nx
        self.newgene[y] = ny

    def geneMutation(self, g):
        """Do Gene Mutation and use real type"""
        ratio = (random.random() - 0.5) * 2 * self.rat_MU
        for i in range(len(g.DNA)):
            if random.random() < self.pro_MU:
                g.DNA[i] = g.DNA[i] + ratio * random.random() * g.DNA[i]

    def crossover(self, dataInput, dataOutput):
        """Do Gene Crossover and use real type"""
        A = [0] * len(self.gene)
        for i in range(self.gene):
            f = self.gene[i].calculateFitness(dataOutput, dataInput)
            A[i] = GenePair.GenePair(f, self.gene[i])
        A = sorted(A)
        bestF = A[0].f
        copyP = [0] * len(A)
        sumF = 0

        for i in range(len(A)):
            sumF += 1.0 / A[i].f

        for i in range(len(A)):
            copyP[i] = (1.0 / A[i].f) / sumF

        bestClone = int(self.poolsize / 10)

        for i in range(bestClone):
            self.newgene[i] = A[0].gene.clone()

        i = 0
        j = bestClone
        while j < len(A):
            p = random.random() * 10
            if copyP[i] > p:
                self.newgene[j] = A[i].gene.clone()
                j += 1
            i = (i + 1) % len(A)
        for i in range(len(A)):
            self.gene[i] = self.newgene[i]
        reserve = 0
        for i in range(len(A)):
            if random.random() < self.pro_CS:
                x = random.randint(0, 2**31-1) % (len(A) - reserve) + reserve
                self.geneCrossover(i, x, self.gene[i], self.gene[x])

        for i in range(len(A)):
            self.gene[i] = self.newgene[i]
        for i in range(reserve, len(A)):
            p = random.random()
            if p < self.pro_MU:
                self.geneMutation(self.gene[i])

        for i in range(len(A)):
            self.gene[i].on()

        return bestF
