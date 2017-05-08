"""Particle Swarm Optimization Machine - Run the PSO Algo"""
# coding: utf-8
# pylint: disable = C0301, C0103, C0200, W0403, W0612

import os
import ast
import PSOSandbox

def setinfo(debugg):
    """Get the needed infomation for PSO Sandbox"""
    if debugg is True:
        ret = {'itertimes':int(10), 'poolsize':int(64),
               'ratio_phi1':float(0.5), 'ratio_phi2':float(0.5)}
    else:
        print "Set the information of PSO Sandbox."
        print "Default value with nothing input!"
        poolsize = raw_input("Gene Pool Size (128):") or 128
        itertimes = raw_input("Iteration Times (50):") or 50
        ratio_phi1 = raw_input("Ratio of learning from INDIVIDUAL'S PREVIOUS best (0.5):") or 0.5
        ratio_phi2 = raw_input("Ratio of learning from NEIGHBORHOOD's best (0.5):") or 0.5
        ret = {'itertimes':int(itertimes), 'poolsize':int(poolsize),
               'ratio_phi1':float(ratio_phi1), 'ratio_phi2':float(ratio_phi2)}

    print "\n---\nYour Input:\n" + "PoolSize: " + str(ret.get('poolsize')) + \
          "\nIterating Times: " + str(ret.get('itertimes')) + \
          "\nRatio of learning from INDIVIDUAL'S PREVIOUS best: " + str(ret.get('ratio_phi1')) + \
          "\nRatio of learning from NEIGHBORHOOD's best: " + str(ret.get('ratio_phi2')) + "\n---\n"
    return ret

def main(debugg):
    """Run PSO Machine to find best parameter of RBF Network"""
    configs = setinfo(debugg)
    path = './data/no_pos/'
    inputt = []
    outputt = []

    for dirPath, dirNames, fileNames in os.walk(path):
        for filee in fileNames:
            filee = os.path.join(dirPath, filee)
            f = open(filee, "r")
            for line in f.readlines():
                tp = line.split()
                listt = []
                if isinstance(ast.literal_eval(tp[0]), float):
                    listt.append(ast.literal_eval(tp[0]))
                    listt.append(ast.literal_eval(tp[1]))
                    listt.append(ast.literal_eval(tp[2]))
                    inputt.append(listt)
                    outputt.append(ast.literal_eval(tp[3]))
                else:
                    print tp
    print "N = " + str(len(inputt))
    print "input list = " + str(inputt)
    print "output list = " + str(outputt)

    for i in  range(len(outputt)):
        outputt[i] = (outputt[i] + 40) / 80.0

    sandbox = PSOSandbox.PSOSandbox(configs.get('poolsize'), configs.get('itertimes'), \
                                    configs.get('ratio_phi1'), configs.get('ratio_phi2'))
    bestPSOList = sandbox.PSOIteration(inputt, outputt)
    PSOList = bestPSOList.getPSOList()
    fw = open("./bestPSO.txt", 'w')
    print PSOList
    s = " ".join(str(ele) for ele in PSOList) + "\n"
    fw.write(s)
    fw.close()
    print "RBF Network has been trained by PSO!"

if __name__ == '__main__':
    debug = True
    main(debug)
    raw_input("\nPress Enter to close the window")
