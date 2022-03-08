#!/usr/bin/env python
import sys
import csv
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import os
import glob
import numpy as np

from matplotlib import rc
font = {'family' : 'Arial', 'size'   : 28}
rc('font', **font)

rc('axes', linewidth=2)


from matplotlib.ticker import MultipleLocator, FormatStrFormatter
majorLocatorX = MultipleLocator(5)
majorFormatterX = FormatStrFormatter('%d')
minorLocatorX = MultipleLocator(1)
majorLocatorY = MultipleLocator(0.04)
majorFormatterY = FormatStrFormatter('%.2f')
minorLocatorY = MultipleLocator(0.02)

colX = []
colY = []
colYerr = []

dicColorsPol = {'0.0':(0, 0, 0, 1), '0.1':(1, 0, 0, 1), '0.2':(0, 0, 1, 1), '0.3':(0, 0.54509, 0, 1),'0.346':(0, 1, 0, 1) ,'0.4':(0.25099, 0.87843, 0.81568, 1), '0.5':(0.40392, 0.02745, 0.28235, 1), '0.6':(0.44706, 0.12941, 0.73725, 1), '0.65':(1, 0.64706, 0, 1), '0.66':(0.73725, 0.56078, 0.56078 ,1), '0.67':(0, 1, 0, 1) }

aveVolumeGeq30 = []


writeFile = open("./analysis/averageVolumehGeq30.dat", 'w')
writeFile.write("#k\tVolume[\AA^3]\n")
print("Creating graphic VolumeXheight.pdf")
fig, ax = plt.subplots(figsize=(10,7.5))
for readFileMoviment in sorted(glob.glob("./analysis/8pk0.*/MeasurementsXheight/parameters-ASbridge-fitting-AllHeight.dat")):
    polarity =  readFileMoviment[readFileMoviment.index('8pk')+3:readFileMoviment.index('/MeasurementsXheight/')]
    with open(readFileMoviment,"r") as fileref:
        reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
        next (reader_file)
        for line in reader_file:
            colX.append(float(line[0])*2) #h/2 -> h
            colY.append(float(line[5])/10**5) #figure scale
            colYerr.append(float(line[6])/10**5)    #figure scale
            if (colX[-1] >= 29.9):
               aveVolumeGeq30.append(float(line[5]))
        writeFile.write("%s\t%f\n" % (polarity, np.mean(aveVolumeGeq30)))
        plt.errorbar(colX, colY, yerr = colYerr, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor='None', color= dicColorsPol[polarity], label = 'k = %s' % (polarity))
        plt.plot([30,50], [np.mean(aveVolumeGeq30)/10**5, np.mean(aveVolumeGeq30)/10**5],'--' , linewidth=2, color = dicColorsPol[polarity])
        colY    = []
        colYerr = []
        colX    = []
        aveVolumeGeq30 = []

writeFile.close()
plt.axis([10,55,1.1,1.26])
plt.ylabel('%s  %s%s%s' % ("$\mathsf{\Omega}$  ","[","$\mathsf{10^5}$ $\mathsf{\AA^3}$","]"))
plt.xlabel('%s  %s%s%s' % ("Height  ","[","$\mathsf{\AA}$","]"))
ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, length = 12.0, width = 2.0)
ax.tick_params(axis='both', which='minor', direction='in', right=True, top=True, length = 6.0, width = 2.0)
ax.xaxis.set_major_locator(majorLocatorX)
ax.xaxis.set_major_formatter(majorFormatterX)
ax.xaxis.set_minor_locator(minorLocatorX)
ax.yaxis.set_major_locator(majorLocatorY)
ax.yaxis.set_major_formatter(majorFormatterY)
ax.yaxis.set_minor_locator(minorLocatorY)
ax.text(50,1.12, "(c)", fontsize = 40)
#ax.legend(loc='upper left', markerscale=0.8, borderpad = 0.2,labelspacing=0.3, handlelength=0.5 )
plt.tight_layout()
plt.savefig("./analysis/graphicsGeometry/VolumeXheight.pdf")
plt.close()

