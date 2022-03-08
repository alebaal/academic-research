#!/usr/bin/env python

from __future__ import division
from scipy import stats
import sys
import csv
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import os
import glob
import numpy as np
import math

from matplotlib import rc
font = {'family' : 'Arial', 'size'   : 28}
rc('font', **font)

rc('axes', linewidth=2)

from matplotlib.ticker import MultipleLocator, FormatStrFormatter
majorLocatorX = MultipleLocator(0.01)
majorFormatterX = FormatStrFormatter('%.2f')
minorLocatorX = MultipleLocator(0.002)
majorLocatorY = MultipleLocator(0.2)
majorFormatterY = FormatStrFormatter('%.1f')
minorLocatorY = MultipleLocator(0.05)

colX    = []
colY    = []
colYerr = []

dicColorsPol = {'0.0':(0, 0, 0, 1), '0.1':(1, 0, 0, 1), '0.2':(0, 0, 1, 1), '0.3':(0, 0.54509, 0, 1), '0.346':(0, 1, 0, 1), '0.4':(0.25099, 0.87843, 0.81568, 1), '0.5':(0.40392, 0.02745, 0.28235, 1), '0.6':(0.44706, 0.12941, 0.73725, 1), '0.65':(1, 0.64706, 0, 1), '0.66':(0.73725, 0.56078, 0.56078 ,1), '0.67':(0, 1, 0, 1) }

print("Creating graphic cosThetaXinvRadius.pdf")
fig, ax = plt.subplots(figsize=(10,7.5))
for readFileMoviment in sorted(glob.glob("./analysis/8pk0.*/MeasurementsXheight/parameters-ASbridge-fitting-AllHeight.dat")):
    polarity =  readFileMoviment[readFileMoviment.index('8pk')+3:readFileMoviment.index('/MeasurementsXheight/')]
    with open(readFileMoviment,"r") as fileref:
        reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
        next (reader_file)
        for line in reader_file:
            colX.append(1.0/float(line[1])) #1/rb
            colY.append(math.cos(math.radians(float(line[3]))))
            colYerr.append(math.sin(math.radians(float(line[4])))*float(line[4]))
        plt.errorbar(colX, colY, yerr = colYerr, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor='None', color= dicColorsPol[polarity], label = 'k = %s' % (polarity))
        slope, intercept, r_value, p_value, std_err = stats.linregress(colX, colY)
        xfit = np.arange(min(colX), max(colX), 0.0001)
        yfit = xfit*slope + intercept
        plt.plot(xfit, yfit, linewidth = 2, color = dicColorsPol[polarity])

        colY    = []
        colYerr = []
        colX    = []
plt.axis([0.02,0.045,-0.6,0.5])
plt.ylabel(r'$\cos (\theta_{\rm C})$')
plt.xlabel(r'$1/r_{\rm b}$')
ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, length = 12.0, width = 2.0)
ax.tick_params(axis='both', which='minor', direction='in', right=True, top=True, length = 6.0, width = 2.0)
ax.xaxis.set_major_locator(majorLocatorX)
ax.xaxis.set_major_formatter(majorFormatterX)
ax.xaxis.set_minor_locator(minorLocatorX)
ax.yaxis.set_major_locator(majorLocatorY)
ax.yaxis.set_major_formatter(majorFormatterY)
ax.yaxis.set_minor_locator(minorLocatorY)
ax.text(0.04,-0.5, "(a)", fontsize = 40)
ax.legend(loc='upper right', markerscale=0.8, borderpad = 0.2,labelspacing=0.3, handlelength=0.5 )
plt.tight_layout()
plt.savefig("./analysis/graphicsGeometry/cosThetaXinvRadius.pdf")
plt.close()
