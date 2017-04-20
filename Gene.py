"""Real type of Gene Algorithm"""

import RBFN

class Gene(object):
    """RGA class"""
    def __init__(self):
        self.J = 3
        self.xDim = 3
        self.DNALength = 1 + self.J + self.J * self.xDim + self.J +  self.J
        self.rbf = RBFN.RBFN(self.J, self.xDim)
        self.DNA = self.setDNA([0] * self.DNALength)

    def setDNA(self, dna):
        """set DNA variable"""
        self.DNA = dna

    def getDNALength(self):
        """Get DNA length"""
        return self.DNALength

    def getDNAName(self):
        """Get DNA string"""
        ret = ""