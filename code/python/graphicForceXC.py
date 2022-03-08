#!/usr/bin/env python

from __future__ import division
import sys
import csv
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
import os
import glob

from scipy.optimize import curve_fit

from matplotlib import rc
font = {'family' : 'Arial', 'size'   : 28}
rc('font', **font)

rc('axes', linewidth=2)


from matplotlib.ticker import MultipleLocator, FormatStrFormatter
majorLocatorX = MultipleLocator(10)
majorFormatterX = FormatStrFormatter('%d')
minorLocatorX = MultipleLocator(5)
majorLocatorY = MultipleLocator(0.25)
majorFormatterY = FormatStrFormatter('%.2f')
minorLocatorY = MultipleLocator(0.125)

dicColorsPol = {'0.0':(0, 0, 0, 1), '0.1':(1, 0, 0, 1), '0.2':(0, 0, 1, 1), '0.3':(0, 0.54509, 0, 1),'0.346':(0, 1, 0, 1) ,'0.4':(0.25099, 0.87843, 0.81568, 1), '0.5':(0.40392, 0.02745, 0.28235, 1), '0.6':(0.44706, 0.12941, 0.73725, 1), '0.65':(1, 0.64706, 0, 1), '0.66':(0.73725, 0.56078, 0.56078 ,1), '0.67':(0, 1, 0, 1) }

def linearFitting(x, a):
    return x*a

colX = []
colY = []
colYerr = []
colXerr = []
colXtot = []
colYtot = []
colYtotErr = []
colXtotErr = []



print("Creating graphic ForceXC.pdf")
fig, ax = plt.subplots(figsize=(10,7.5))
for readFileMoviment in sorted(glob.glob("./analysis/8pk0.*/MeasurementsXheight/")):
    polarity =  readFileMoviment[readFileMoviment.index('8pk')+3:readFileMoviment.index('/MeasurementsXheight/')]
    with open( "%s/parameters-ASbridge-fitting-AllHeight.dat" % (readFileMoviment),"r") as fileC:
        reader_file_C = csv.reader(fileC, delimiter='\t')   #fitting file has to skip one line
        next (reader_file_C)
        for line in reader_file_C:
           colX.append(float(line[17])/2/np.pi) 
           colXerr.append(float(line[18])/2/np.pi)
    with open( "%s/AveForceLammps-AllHeight.dat" % (readFileMoviment),"r") as fileForce:
        reader_file_Force = csv.reader(fileForce, delimiter='\t')   #fitting file has to skip one line
        next (reader_file_Force)
        for line in reader_file_Force:
           colY.append(float(line[1])) 
           colYerr.append(float(line[2]))
    colXtot.extend(colX)        
    colXtotErr.extend(colXerr)        
    colYtot.extend(colY)        
    colYtotErr.extend(colYerr)        
    plt.errorbar(colX, colY, xerr = colXerr, yerr = colYerr, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor='None', color= dicColorsPol[polarity], label = 'k = %s' % (polarity))
    colX = []    
    colY = []    
    colXerr = []    
    colYerr = []

#Surface Tension calculation    
parameters, cov_matrix = curve_fit(linearFitting, np.asarray(colXtot), np.asarray(colYtot), sigma = colYtotErr)
print("gamma = %f +/- %f N/m" % (10.0*parameters/2.0/np.pi, 10.0*np.sqrt(cov_matrix)/2.0/np.pi))
xfitting = np.linspace(-30, max(colXtot)*1.5, 1000)
yfitting = linearFitting(xfitting, *parameters)
plt.plot(xfitting, yfitting, '--', color = 'k', linewidth=2.0)

writeFile = open("./analysis/surfaceTension.dat", 'w')
writeFile.write("#gamma\tErrGamma [N/m]\n")
writeFile.write("%.8g\t%.8g\n" % (10.0*parameters/2.0/np.pi, 10.0*np.sqrt(cov_matrix)/2.0/np.pi))
writeFile.close()
#############

plt.axis([-10,48,-0.25,1.75])
plt.ylabel('%s  %s%s%s' % ("Force  ","[","nN","]"))
plt.xlabel('%s  %s%s%s' % ("C  ","[","$\mathsf{\AA}$","]"))
ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, length = 12.0, width = 2.0)
ax.tick_params(axis='both', which='minor', direction='in', right=True, top=True, length = 6.0, width = 2.0)
ax.xaxis.set_major_locator(majorLocatorX)
ax.xaxis.set_major_formatter(majorFormatterX)
ax.xaxis.set_minor_locator(minorLocatorX)
ax.yaxis.set_major_locator(majorLocatorY)
ax.yaxis.set_major_formatter(majorFormatterY)
ax.yaxis.set_minor_locator(minorLocatorY)
ax.text(30,1.5, "(a)", fontsize = 40)
ax.legend(loc='lower right', markerscale=0.8, borderpad = 0.2,labelspacing=0.3, handlelength=0.5 )
plt.tight_layout()
plt.savefig("./analysis/graphicsThermodynamic/ForceXC.pdf")
plt.close()  
