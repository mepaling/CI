# coding: utf-8
# pylint: disable = C0301

"""Gene Machine - the UI and base setting of Gene Algo"""

import GenePool

class GeneMachine(object):
    """Gene Machine - the UI and base setting of Gene Algo"""
    def __init__(self):
        ret = self.setinfo()
        self.genepool = GenePool.GenePool(self, ret.get("ps"), ret.get("pro_CS"), ret.get("rat_CS"), ret.get("pro_MU"), ret.get("rat_MU"))

    def setinfo(self):
        """Get the needed infomation of gene pool"""
        print "\nSet the information of Gene Pool."
        print "If you don't type anything, remain default value!"
        poolsize = raw_input("Gene Pool Size (256):") or 256
        itertimes = raw_input("Iteration Times (256):") or 256
        pro_crossover = raw_input("Probability of Crossover (0.5):") or 0.5
        ratio_crossover = raw_input("Ratio of Crossover (0.5):") or 0.5
        pro_mutation = raw_input("Probability of Mutation (0.5):") or 0.5
        ratio_mutation = raw_input("Ratio of Mutation (0.5):") or 0.5
        return {'it':int(itertimes), 'ps':int(poolsize),
                'pro_CS':float(pro_crossover), 'rat_CS':float(ratio_crossover),
                'pro_MU':float(pro_mutation), 'rat_MU':float(ratio_mutation)}

    def main(self, sensorx, sensory, sensorz):
        """get the theta value by sensors"""

