#!/usr/bin/env python
import sys
import csv
import os
import glob
import numpy as np
import pandas as pd

for readFileMoviment in sorted(glob.glob("./analysis/8pk0.*/MeasurementsXheight/parameters-ASbridge-fitting-AllHeight.dat")):
    polarity =  readFileMoviment[readFileMoviment.index('8pk')+3:readFileMoviment.index('/MeasurementsXheight/')]
    print("Creating tablek%s.tex" % (polarity))
    df = pd.read_table(readFileMoviment, sep = '\t', header = 0, usecols = [0, 11, 13, 15, 3, 21]) 
    df.loc[:,'#1-TouchHeight']*=2
    df = df.round({'#1-TouchHeight':1, '4-Theta':1, '12-rhoNeck':1, '14-RadiusProfile':1, '16-H':4, '22-ErrorFitting':2})
    df = df.set_index('#1-TouchHeight')
    df = df[['12-rhoNeck', '14-RadiusProfile', '16-H', '4-Theta', '22-ErrorFitting']]
    with open('./analysis/tables/tablek%s.tex' % (polarity), 'w') as tf:
         tf.write(df.to_latex())
    tf.close()

readFileMoviment = ("./analysis/cosThetaXheightFitting.dat")
print("Creating tableCosThetaFitting.tex")
df = pd.read_table(readFileMoviment, sep = '\t', header = 0) 
df = df.round({'#k':1, 'a':2, 'b':2, 'c [y(x)=a/x^b + c]':4})
df = df.set_index('#k')
with open('./analysis/tables/cosThetaXheightFitting.tex', 'w') as tf:
     tf.write(df.to_latex())
tf.close()




