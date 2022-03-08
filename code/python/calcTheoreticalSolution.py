#!/usr/bin/env python

import numpy as np
import sys
import glob
import os
import time
import csv
from subprocess import call

colk = []
cola = []
colb = []
colc = []
colVol = []

def main():
    with open("./analysis/cosThetaXheightFitting.dat", "r") as fileProfile:
         reader_file = csv.reader(fileProfile, delimiter='\t')
         next(reader_file)
         for line in reader_file:
             colk.append(float(line[0]))
             cola.append(float(line[1]))
             colb.append(float(line[2]))
             colc.append(float(line[3]))

    with open("./analysis/averageVolumehGeq30.dat", "r") as fileProfile:
         reader_file = csv.reader(fileProfile, delimiter='\t')
         next(reader_file)
         for line in reader_file:
             colVol.append(float(line[1]))

    os.chdir("./analysis/theoreticalData/")
    for i in range(len(colk)):
#        print(["./theorticalProfilehleq50", str(colVol[i]), "8", "25.0", "0.001", "resultASbridgek" + str(colk[i]) + ".dat", str(cola[i]), str(colb[i]), str(colc[i])])
        call(["./theorticalProfilehleq50", str(colVol[i]), "12.5", "25.0", "0.001", "resultASbridgek" + str(colk[i]) + ".dat", str(cola[i]), str(colb[i]), str(colc[i])]);
if __name__ == "__main__": main()

