# pylint: disable=C0103, C0111
import random

filee = open("bestGene.txt", "w")
x = []

for _ in range(20):
    for _ in range(16):
        filee.write(str(random.uniform(0.0, 20.0)) + " ")
    filee.write("\n")
filee.close()
