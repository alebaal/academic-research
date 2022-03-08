#!/usr/bin/env python
 
from __future__ import division
import sys
import csv
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
import glob
from scipy import stats

AveFxWall1    = []
AveFyWall1    = []
AveFzWall1    = []
AveFxWall2    = []
AveFyWall2    = []
AveFzWall2    = []

if (len(sys.argv) == 3):
    for readFileMoviment in sorted(glob.glob("./forceWallsCalculation/8pk%s/moviment-%s/forceWall*k%smov%sstep*.out" % (sys.argv[1], sys.argv[2], sys.argv[1], sys.argv[2]))):
        with open(readFileMoviment,"r") as fileref:
             reader_file = csv.reader(fileref, delimiter=' ')
             next(reader_file)
             next(reader_file)
             next(reader_file)
             line = next(reader_file)
             Fx = float(line[1])*0.06952 #converting to Newton
             Fy = float(line[2])*0.06952 
             Fz = float(line[3])*0.06952 
             wallIndexP = len("./forceWallsCalculation/8pk%s/moviment-%s/forceWall" % (sys.argv[1], sys.argv[2]))
             wall = int(readFileMoviment[wallIndexP])
             if (wall == 1): 
                AveFxWall1.append(Fx)
                AveFyWall1.append(Fy)
                AveFzWall1.append(Fz)
             else: 
                AveFxWall2.append(Fx)
                AveFyWall2.append(Fy)
                AveFzWall2.append(Fz)
    fileName = ("./forceWallsCalculation/8pk%s/moviment-%s/AveForceWallk%smov%s.dat" % (sys.argv[1], sys.argv[2], sys.argv[1], sys.argv[2]))
    fileAveForce = open(fileName, "w")
    fileAveForce.write("#<Fx>\tSEM[Fx]\t<Fy>\tSEM[Fy]\t<Fz>\tSEM[Fz] (nN);\n")
    #fileAveForce.write("%f\t%f\t%f\t%f\t%f\t%f\n" % ( np.mean(AveFxWall1) , np.std(AveFxWall1), np.mean(AveFyWall1) , stats.sem(AveFyWall1) ,np.mean(AveFzWall1) , stats.sem(AveFzWall1))) 
    fileAveForce.write("%f\t%f\t%f\t%f\t%f\t%f\n" % ( np.mean(AveFxWall1) , np.std(AveFxWall1), np.mean(AveFyWall1) , np.std(AveFyWall1) ,np.mean(AveFzWall1) , np.std(AveFzWall1))) 
    fileAveForce.close()

else:
	print "\nArguments Error"
        print  str(sys.argv)
        print "\n"
        print  ("USAGE:", sys.argv[0], "k")
        print  "arg1  k"
        print  "arg2  moviment"
