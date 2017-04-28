"""Particle"""
# coding: utf-8
# pylint: disable =

import RBFN

class Particle(object):
    """Particle - a particle's status"""
    def __init__(self, p, v):
        self.J = 3
        self.xDim = 3
        self.xLength = 1 + self.J + self.J * self.xDim + self.J
        self.rbf = RBFN.RBFN(self.J, self.xDim)
        self.velocity = v
        self.position = p
        self.pbest = None # Best position of itself
        self.gbest = None # Best position of whole group

    def generate(self):
        
