# coding: utf-8
# pylint: disable = C0103, C0200, R0902, R0912, R0913, C0301, W0102

"""Gene Pool - Actually do the algorithm"""

import copy
import random
import operator
import Gene as Gene

class GenePool(object):
    """Gene Pool class"""
    def __init__(self, poolsize=256, max_iter=256, pro_CS=0.5, rat_CS=0.5, pro_MU=0.5, rat_MU=0.5, bgl=[]):
        self.poolsize = poolsize
        self.max_iter = max_iter
        self.pro_CS = pro_CS
        self.rat_CS = rat_CS
        self.pro_MU = pro_MU
        self.rat_MU = rat_MU
        self.genepoolList = []
        self.genelist = []
        self.bestgenelist = []
        self.bestgenesize = int(self.poolsize / 10)
        self.hasiter = 1
        self.init(bgl)

    def init(self, bestGeneList):
        """initialize"""
        if not bestGeneList:
            for _ in range(self.bestgenesize):
                gene = Gene.Gene()
                gene.f = 1e9
                self.bestgenelist.append(gene)
            for _ in range(self.poolsize):
                gene = Gene.Gene()
                gene.generate()
                self.genelist.append(gene)
        else:
            self.bestgenelist = copy.deepcopy(bestGeneList)
            percent25 = int(self.poolsize / 4)
            for _ in range(percent25):
                x = random.sample(range(len(self.bestgenelist)), 1)[0]
                gene = self.bestgenelist[x].clone()
                self.genelist.append(gene)
            for _ in range(percent25, self.poolsize):
                gene = Gene.Gene()
                gene.generate()
                self.genelist.append(gene)

    def geneIteration(self, inputt, outputt):
        """Do the iteration"""
        for _ in range(0, self.max_iter):
            bestGeneList = self.performGene(inputt, outputt)
        return bestGeneList

    def performGene(self, inputt, outputt):
        """Actually do the thing"""
        for i in range(self.poolsize):
            self.genelist[i].calculateFitness(inputt, outputt)

        self.genelist.sort(key=operator.attrgetter('f'))

        self.genepoolList = []

        bestgenelist = []

        for i in range(self.bestgenesize):
            bestgenelist.append(self.genelist[i])
            bestgenelist.append(self.bestgenelist[i])

        bestgenelist.sort(key=operator.attrgetter('f'))

        for i in range(self.bestgenesize):
            self.bestgenelist[i] = bestgenelist[i].clone()

        #Print Status
        self.genelist[0].showDNA()
        print("f=", self.genelist[0].f)

        # check if last time
        if self.hasiter >= self.max_iter:
            return self.bestgenelist
        else:
            # Reproduct
            bestsize = int(self.poolsize / 10)
            for i in range(bestsize):
                gene = self.genelist[i].clone()
                self.genepoolList.append(gene)
            for i in range(bestsize, self.poolsize):
                pick = random.sample(range(self.poolsize), 2)
                gene = self.reproduct(self.genelist, pick)
                self.genepoolList.append(gene)

            # Crossover
            pick = random.sample(range(self.poolsize), self.poolsize)
            for i in range(0, self.poolsize, 2):
                if random.random() < self.pro_CS:
                    x = self.genepoolList[pick[i]]
                    y = self.genepoolList[pick[i+1]]
                    self.crossover(x, y)

            # Mutation
            for i in range(self.poolsize):
                if random.random() < self.pro_MU:
                    for j in range(0, self.genepoolList[0].DNALength):
                        self.genepoolList[i].DNA[j] = self.mutate(self.genepoolList[i].DNA[j])
                self.genepoolList[i].on()

            self.genelist = copy.deepcopy(self.genepoolList)
            self.hasiter += 1
            return 0

    def reproduct(self, genelist, pickedlist):
        """Do Gene Reproduction and use real type"""
        gene = Gene.Gene()
        gene.f = 1e9
        for i in pickedlist:
            if genelist[i].f < gene.f:
                gene = genelist[i].clone()
        return gene

    def mutate(self, dna_val):
        """Do Gene Mutation and use real type"""
        ratio = (random.random() - 0.5) * 2 * self.rat_MU
        ret = dna_val
        if random.random() < self.pro_MU:
            ret += dna_val * ratio
        return ret

    def crossover(self, x, y):
        """Do Gene Crossover and use real type"""
        ratio = (random.random() - 0.5) * 2 * self.rat_CS
        gx = Gene.Gene()
        gy = Gene.Gene()
        for i in range(len(x.DNA)):
            gx.DNA[i] = x.DNA[i] + ratio * (x.DNA[i] - y.DNA[i])
            gy.DNA[i] = y.DNA[i] - ratio * (x.DNA[i] - y.DNA[i])
        return gx, gy

    def showBestDNA(self):
        """Just show the item of BestGeneList"""
        for gene in self.bestgenelist:
            gene.showDNA()