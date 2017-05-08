"""Particle Swarm Optimization Machine - Run the PSO Algo"""
# coding: utf-8
# pylint: disable = C0301, C0103, C0200, W0403, W0612

import os
import sys
import time
import ast
import PSOSandbox

def setinfo(debugg, para):
    """Get the needed infomation for PSO Sandbox"""
    if debugg is True:
        if para is None:
            ret = {'itertimes':int(10), 'poolsize':int(10),
                   'ratio_phi1':float(0.5), 'ratio_phi2':float(0.5)}
        else:
            ret = {'itertimes':int(10), 'poolsize':int(10),
                   'ratio_phi1':float(para.get('phi1')), 'ratio_phi2':float(para.get('phi2'))}
    else:
        print "Please set the information of PSO Sandbox."
        print "Default value with nothing input!"
        poolsize = raw_input("Gene Pool Size (10):") or 10
        itertimes = raw_input("Iteration Times (10):") or 10
        ratio_phi1 = raw_input("Ratio of learning from INDIVIDUAL'S PREVIOUS best (0.5):") or 0.5
        ratio_phi2 = raw_input("Ratio of learning from NEIGHBORHOOD's best (0.5):") or 0.5
        ret = {'itertimes':int(itertimes), 'poolsize':int(poolsize),
               'ratio_phi1':float(ratio_phi1), 'ratio_phi2':float(ratio_phi2)}

    print "\n---\nYour Input:\n" + "PoolSize: " + str(ret.get('poolsize')) + \
          "\nIterating Times: " + str(ret.get('itertimes')) + \
          "\nRatio of learning from INDIVIDUAL'S PREVIOUS best: " + str(ret.get('ratio_phi1')) + \
          "\nRatio of learning from NEIGHBORHOOD's best: " + str(ret.get('ratio_phi2')) + "\n---\n"
    return ret

def main(debugg, para):
    """Run PSO Machine to find best parameter of RBF Network"""
    configs = setinfo(debugg, para)
    inputt = []
    outputt = []
    nowpath = os.path.dirname(os.path.abspath(__file__))
    print nowpath
    path = nowpath + '/data/no_pos/'

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
    #print "input list = " + str(inputt)
    #print "output list = " + str(outputt)
    start = time.time()
    for i in range(len(outputt)):
        outputt[i] = (outputt[i] + 40) / 80.0

    sandbox = PSOSandbox.PSOSandbox(configs.get('poolsize'), configs.get('itertimes'), \
                                    configs.get('ratio_phi1'), configs.get('ratio_phi2'))
    bestPSOList = sandbox.PSOIteration(inputt, outputt)
    PSOList = bestPSOList.getPSOList()

    if para is None:
        fileName = os.path.abspath("..") + "/bestPSO.txt"
    else:
        fileName = os.path.abspath("..") + "/bestPSO" + para.get('fName') + ".txt"
    print "\n--------------------------------------------------"
    print "fileName:" + fileName
    print "PSOList:"
    print PSOList

    fw = open(fileName, 'w')
    s = " ".join(str(ele) for ele in PSOList) + "\n"
    fw.write(s)
    fw.close()
    end = time.time()
    print "\nCost Time: " + str(end-start) + " sec."
    print "\nRBF Network trained complete!"
    print "--------------------------------------------------\n"

if __name__ == '__main__':
    print "-----------------\nWelcome to the PSO training Machine!\n"
    debug = False
    if len(sys.argv) < 2:
        main(debug, None)
    else:
        #['RBFN/PSOMachine.py', 'apple']
        phi1_Z = int(sys.argv[1])
        times = int(sys.argv[2])
        paraa = {'phi1':float(phi1_Z) / 10.0,
                 'phi2':1.0 - float(phi1_Z)/10.0,
                 'fName':str(phi1_Z) + "vs" + str(10-phi1_Z) + "-" + str(times)}
        print paraa
        main(debug, paraa)

    if not debug:
        raw_input("\nPress Enter to close the window")
    else:
        pass
