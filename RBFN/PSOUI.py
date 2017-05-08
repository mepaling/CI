# coding: utf-8
# pylint: disable = C0301, C0103, W0123, C0200, C0111

"""PSO UI - for decoding the THETA value"""

class PSOUI(object):
    def __init__(self):
        pass
    def main(self, pso, sensorlist):
        if pso is not None:
            return pso.getTheta(sensorlist)
        else:
            return None
