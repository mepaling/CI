"""Particle Swarm Optimization SandBox -
   the simulation environment"""
# coding: utf-8
# pylint: disable = C0103, C0111, C0301, W0403

import operator
import time
import copy
import Particle

class PSOSandbox(object):
    """Particle Swarm Optimization SandBox"""
    def __init__(self, poolSize=128, maxIter=50, phi1=0.5, phi2=0.5):
        self.poolSize = poolSize
        self.maxIteration = maxIter
        self.phi1 = phi1
        self.phi2 = phi2
        self.PSOList = []
        self.bestPSOList = []
        self.hasiter = 1
        self.bestPSO = Particle.Particle()
        for _ in range(poolSize):
            p = Particle.Particle()
            p.generate()
            self.PSOList.append(p)

    def PSOIteration(self, inputt, outputt):
        for _ in range(self.maxIteration):
            bestPSOList = self.performPSO(inputt, outputt)
        return bestPSOList

    def performPSO(self, inputt, outputt):
        start = time.time()
        for i in range(self.poolSize):
            self.PSOList[i].calculateFitness(inputt, outputt)

        self.PSOList.sort(key=operator.attrgetter('f'))

        self.bestPSO = copy.deepcopy(self.PSOList[0])

        print "Iter Round #" + str(self.hasiter) + " start"

        for i in range(0, self.poolSize):
            for j in range(self.bestPSO.xLength):
                self.PSOList[i].v[j] += self.phi1 * (self.PSOList[i].best[j] - self.PSOList[i].x[j]) + \
                                        self.phi2 * (self.bestPSO.x[j] - self.PSOList[i].x[j])
                self.PSOList[i].x[j] += self.PSOList[i].v[j]
                self.PSOList[i].calculateFitness(inputt, outputt)
                if self.PSOList[i].f < self.bestPSO.f:
                    self.bestPSO = copy.deepcopy(self.PSOList[i])
        end = time.time()
        print "Round #" + str(self.hasiter) + " cost: " + str(end-start) + " sec.\n"
        self.hasiter += 1
        return self.bestPSO
