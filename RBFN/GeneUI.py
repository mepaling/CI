# coding: utf-8
# pylint: disable = C0301, C0103, W0123, C0200

"""Gene UI - for decoding the THETA value"""

import Gene

class GeneUI(object):
    def __init__(self):
        pass
    def main(self, gene, sensorlist):
        if gene is not None:
            return gene.getTheta(sensorlist)
        else:
            return None
