#!/usr/bin/env python
from __future__ import division
import sys
import csv
import numpy as np
import os

numWallsAtoms = 93184
numWaterAtoms = 10125

if (len(sys.argv) == ):
    step = int(sys.argv[1]) 
    deltaStep = int(sys.argv[3]) 
    while(step <= int(sys.argv[2])):
         fileDump = dump("./%d.pos" % (step))
         fileDump.map(1,'id',2,'type',3,'x',4,'y',5,'z')
         for patternsFiles in sorted(glob.glob("%s.%d.pos.Water.*" % (sys.argv[4], step)):   
             if (os.stat(patternsFiles).st_size == 0):
                continue
             else:
                waterPatterns = np.loadtxt(patternsFiles, dtype=int, delimiter = ' ')*3 -2 + numWallsAtoms # changing nodes 1,2,3... to atom id 
             xpos = fileDump.atom(atom,'x')
             
         step += deltaStep
      
   



else:
        print "\nArguments Error"
        print  str(sys.argv)
        print "\n"
        print ("USAGE:", sys.argv[0], "k")
        print "arg1  first step"
        print "arg2  last  step"
        print "arg3  time step interval"
        print "arg4  Input ChemNetwork"

