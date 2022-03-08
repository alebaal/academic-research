#!/usr/bin/env python
import sys
import csv
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import os
import glob
import numpy as np
from uncertainties import ufloat 

from matplotlib import rc
font = {'family' : 'Arial', 'size'   : 28}
rc('font', **font)

rc('axes', linewidth=2)


from matplotlib.ticker import MultipleLocator, FormatStrFormatter
majorLocatorX = MultipleLocator(0.1)
majorFormatterX = FormatStrFormatter('%.1f')
minorLocatorX = MultipleLocator(0.05)
majorLocatorY = MultipleLocator(20)
majorFormatterY = FormatStrFormatter('%d')
minorLocatorY = MultipleLocator(10)

colX = []
colY = []
colYerr = []
colAveTheta = []
colTemp = []

colXjpcc = []
colYjpcc = []

print("Creating graphic ThetaXk.pdf")

readDataJPCC2018 = ("./analysis/dataJPCC2018/ThetaXk-new.dat")
with open(readDataJPCC2018,"r") as fileref:
     reader_file = csv.reader(fileref, delimiter='\t')  
     next (reader_file)
     next (reader_file)
     for line in reader_file:
         colXjpcc.append(float(line[0]))
         colYjpcc.append(float(line[1]))

fig, ax = plt.subplots(figsize=(10,7.5))
for readFileMoviment in sorted(glob.glob("./analysis/8pk0.*/MeasurementsXheight/parameters-ASbridge-fitting-AllHeight.dat")):
    polarity =  readFileMoviment[readFileMoviment.index('8pk')+3:readFileMoviment.index('/MeasurementsXheight/')]
    colX.append(float(polarity))
    with open(readFileMoviment,"r") as fileref:
        reader_file = csv.reader(fileref, delimiter='\t')  
        next(reader_file)
        for line in reader_file:
            if (float(line[0]) > 18.0): # calculate the average only for h < 35\AA
                colTemp.append(ufloat(float(line[3]), float(line[4])))
            else:                        
                continue                 
    colAveTheta.append(np.mean(colTemp)) 
    colTemp = []                         
for i in colAveTheta:                    
    colY.append(i.n)                       
    colYerr.append(i.s)                  
plt.errorbar(colX, colY, yerr = colYerr, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor='None', color= 'k', label = "AS bridge")
plt.plot(colXjpcc, colYjpcc, 'o', markersize = 14, markeredgewidth = 2, markerfacecolor='None', color= 'r', label = "ref [JPCC2018]")
plt.axis([0.0,1.0,0,120])
plt.ylabel('%s  %s%s%s' % ("Contact Angle  ","[","$^\mathsf{\circ}$","]"))
plt.xlabel('%s' % ("k"))
ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, length = 12.0, width = 2.0)
ax.tick_params(axis='both', which='minor', direction='in', right=True, top=True, length = 6.0, width = 2.0)
ax.xaxis.set_major_locator(majorLocatorX)
ax.xaxis.set_major_formatter(majorFormatterX)
ax.xaxis.set_minor_locator(minorLocatorX)
ax.yaxis.set_major_locator(majorLocatorY)
ax.yaxis.set_major_formatter(majorFormatterY)
ax.yaxis.set_minor_locator(minorLocatorY)
ax.text(0.85,10, "(c)", fontsize = 40)
ax.legend(loc='upper right', markerscale=0.8, borderpad = 0.2,labelspacing=0.3, handlelength=0.5 )
plt.tight_layout()
plt.savefig("./analysis/graphicsGeometry/ThetaXk.pdf")
plt.close()
