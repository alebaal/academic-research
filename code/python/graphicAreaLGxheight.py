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
majorLocatorY = MultipleLocator(0.1)
majorFormatterY = FormatStrFormatter('%.1f')
minorLocatorY = MultipleLocator(0.05)

colX = []
colY = []
colYerr = []
colk = []
cola = []
colb = []
colc = []

dicColorsPol = {'0.0':(0, 0, 0, 1), '0.1':(1, 0, 0, 1), '0.2':(0, 0, 1, 1), '0.3':(0, 0.54509, 0, 1),'0.346':(0, 1, 0, 1) ,'0.4':(0.25099, 0.87843, 0.81568, 1), '0.5':(0.40392, 0.02745, 0.28235, 1), '0.6':(0.44706, 0.12941, 0.73725, 1), '0.65':(1, 0.64706, 0, 1), '0.66':(0.73725, 0.56078, 0.56078 ,1), '0.67':(0, 1, 0, 1) }
#dicPolTheta  = {'0.0':105.57462, '0.1':104.75958, '0.2':100.78243, '0.3':94.336977, '0.4':84.445479, '0.5':70.818446, '0.6':50.382360, '0.65':32.786379, '0.66':28.323013, '0.67':25.793658}

with open("./analysis/cosThetaXheightFitting.dat", "r") as fileProfile:
     reader_file = csv.reader(fileProfile, delimiter='\t')
     next(reader_file)
     for line in reader_file:
         colk.append(line[0])
         cola.append(float(line[1]))
         colb.append(float(line[2]))
         colc.append(float(line[3]))

print("Creating graphic AreaLGXheight.pdf")
fig, ax = plt.subplots(figsize=(10,7.5))
for readFileTheoretical in sorted(glob.glob("./analysis/theoreticalData/resultASbridgek*.dat")):
    polarity =  readFileTheoretical[readFileTheoretical.index('ASbridgek')+9:readFileTheoretical.index('.dat')]
    with open(readFileTheoretical,"r") as fileref:
        reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
        for line in reader_file:
            colX.append(float(line[0])*2) #h/2 -> h
    #        colY.append((float(line[2]) +  2*np.cos(np.radians(dicPolTheta[polarity]))*np.pi*float(line[3])**2)/10**4) #1) free energy - Base Area  2)figure scale
            indexPolarity = colk.index(polarity)
            colY.append((float(line[2]) +  2*(cola[indexPolarity]/colX[-1]**colb[indexPolarity] + colc[indexPolarity])*np.pi*float(line[3])**2)/10**4) #1) free energy - Base Area  2)figure scale
                
        plt.plot(colX, colY,'--', linewidth=2, color = dicColorsPol[polarity])
        colX = []
        colY = []

colX = []
colY = []
colYerr = []
for readFileMoviment in sorted(glob.glob("./analysis/8pk0.*/MeasurementsXheight/parameters-ASbridge-fitting-AllHeight.dat")):
    polarity =  readFileMoviment[readFileMoviment.index('8pk')+3:readFileMoviment.index('/MeasurementsXheight/')]
    with open(readFileMoviment,"r") as fileref:
        reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
        next (reader_file)
        for line in reader_file:
            colX.append(float(line[0])*2) #h/2 -> h
            colY.append(float(line[7])/10**4) #figure scale
            colYerr.append(float(line[8])/10**4)    #figure scale
        plt.errorbar(colX, colY, yerr = colYerr, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor='None', color= dicColorsPol[polarity], label = 'k = %s' % (polarity))
        colY    = []
        colYerr = []
        colX    = []
plt.axis([10,55,0.4,0.9])
#plt.axis([50,80,0.8,1.7])
plt.ylabel('%s  %s%s%s' % ("$\mathsf{A_{LG}}$  ","[","$\mathsf{10^4}$ $\mathsf{\AA^2}$","]"))
plt.xlabel('%s  %s%s%s' % ("Height  ","[","$\mathsf{\AA}$","]"))
ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, length = 12.0, width = 2.0)
ax.tick_params(axis='both', which='minor', direction='in', right=True, top=True, length = 6.0, width = 2.0)
ax.xaxis.set_major_locator(majorLocatorX)
ax.xaxis.set_major_formatter(majorFormatterX)
ax.xaxis.set_minor_locator(minorLocatorX)
ax.yaxis.set_major_locator(majorLocatorY)
ax.yaxis.set_major_formatter(majorFormatterY)
ax.yaxis.set_minor_locator(minorLocatorY)
ax.text(50,0.45, "(b)", fontsize = 40)
#ax.legend(loc='upper left', markerscale=0.8, borderpad = 0.2,labelspacing=0.3, handlelength=0.5 )
plt.tight_layout()
plt.savefig("./analysis/graphicsGeometry/AreaLGXheight.pdf")
plt.close()
