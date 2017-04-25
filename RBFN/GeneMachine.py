# coding: utf-8
# pylint: disable = C0301, C0103, W0123, C0200

"""Gene Machine - the UI and base setting of Gene Algo"""

import os
import GenePool
import Gene

def setinfo():
    """Get the needed infomation of gene pool"""
    print "\nSet the information of Gene Pool."
    print "If you don't type anything, remain default value!"
    poolsize = raw_input("Gene Pool Size (256):") or 256
    itertimes = raw_input("Iteration Times (256):") or 256
    pro_crossover = raw_input("Probability of Crossover (0.5):") or 0.5
    ratio_crossover = raw_input("Ratio of Crossover (0.5):") or 0.5
    pro_mutation = raw_input("Probability of Mutation (0.5):") or 0.5
    ratio_mutation = raw_input("Ratio of Mutation (0.5):") or 0.5
    return {'itertimes':int(itertimes), 'poolsize':int(poolsize),
            'pro_CS':float(pro_crossover), 'rat_CS':float(ratio_crossover),
            'pro_MU':float(pro_mutation), 'rat_MU':float(ratio_mutation)}

def main():
    """Start Gene Machine"""
    ret = setinfo()
    path = "./data/no_pos/"
    datalist = []
    inputt = []
    outputt = []

    for dirPath, dirNames, fileNames in os.walk(path):
        for filee in fileNames:
            filee = os.path.join(dirPath, filee)
            f = open(filee, "r")
            for line in f.readlines():
                tp = line.split()
                listt = []
                if isinstance(eval(tp[0]), float):
                    listt.append(eval(tp[0]))
                    listt.append(eval(tp[1]))
                    listt.append(eval(tp[2]))
                    inputt.append(listt)
                    outputt.append(eval(tp[3]))
                else:
                    print tp
    print "N = " + str(len(inputt))
    print "input list = " + str(inputt)
    print "output list = " + str(outputt)

    # Normalize
    for i in range(len(outputt)):
        outputt[i] = (outputt[i] + 40.0) / 80.0

    fError_ori = 1e9
    fError_now = 1e9
    bestGeneSize = int(ret.get('poolsize') / 10)

    while fError_now > 5:
        if os.path.isfile("./best.txt"):
            readfile = open("./best.txt", "r")
            strlist = []
            for i in range(bestGeneSize):
                strlist.append(readfile.readline())
            readfile.close()

            genelist = []
            for i in range(bestGeneSize):
                gene = Gene.Gene()
                gene.setGene(strlist[i])
                gene.calculateFitness(inputt, outputt)
                genelist.append(gene)
            fError_ori = genelist[0].f
            print("before min function error = ", genelist[0].f)
            genepool = GenePool.GenePool(ret.get("poolsize"), ret.get('itertimes'),
                                        ret.get("pro_CS"), ret.get("rat_CS"),
                                        ret.get("pro_MU"), ret.get("rat_MU"), genelist)
        else:
            genepool = GenePool.GenePool(ret.get("poolsize"), ret.get('itertimes'),
                                         ret.get("pro_CS"), ret.get("rat_CS"),
                                         ret.get("pro_MU"), ret.get("rat_MU"), [])

        bestGeneList = genepool.geneIteration(inputt, outputt)

        print ("after min function error", bestGeneList[0].f)

        fError_now = bestGeneList[0].f

        if fError_now < fError_ori:
            fw = open("./best.txt", 'w')
            for i in range(genepool.bestgenesize):
                DNAList = bestGeneList[i].getDNAList()
                s = " ".join(str(ele) for ele in DNAList) + "\n"
                fw.write(s)
            fw.close()
            print "Training Complete!"

if __name__ == '__main__':
    main()
