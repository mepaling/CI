# coding: utf-8
# pylint: disable = C0301, C0103, W0123, C0200, C0111

"""Gene UI - for decoding the THETA value"""

class GeneUI(object):
    def __init__(self):
        pass
    def main(self, gene, sensorlist):
        if gene is not None:
            return gene.getTheta(sensorlist)
        else:
            return None
