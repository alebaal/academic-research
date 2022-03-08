#!/usr/bin/env python
from __future__ import division
import sys
import csv
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
import os
import glob

from matplotlib import rc
font = {'family' : 'Arial', 'size'   : 28}
rc('font', **font)

rc('axes', linewidth=2)


from matplotlib.ticker import MultipleLocator, FormatStrFormatter
majorLocatorX = MultipleLocator(5)
majorFormatterX = FormatStrFormatter('%d')
minorLocatorX = MultipleLocator(2.5)
majorLocatorY = MultipleLocator(0.4)
majorFormatterY = FormatStrFormatter('%.1f')
minorLocatorY = MultipleLocator(0.2)

dicColorsPol = {'0.0':(0, 0, 0, 1), '0.1':(1, 0, 0, 1), '0.2':(0, 0, 1, 1), '0.3':(0, 0.54509, 0, 1), '0.346':(0, 1, 0, 1), '0.4':(0.25099, 0.87843, 0.81568, 1), '0.5':(0.40392, 0.02745, 0.28235, 1), '0.6':(0.44706, 0.12941, 0.73725, 1), '0.65':(1, 0.64706, 0, 1), '0.66':(0.73725, 0.56078, 0.56078 ,1), '0.67':(0, 1, 0, 1) }
dicMovHeight = {0:'50', 1:'40', 2:'30', 3:'25', 4:'20', 5:'19', 6:'18', 7:'17'}
dicLetterFig = {0:'(a)', 1:'(b)', 2:'(c)', 3:'(d)',4:'(e)', 5:'(f)', 6:'(g)', 7:'(h)'}

colZ = []
colRho = []

for mov in range(8):
    print("Creating graphic graphicRhoZavemov%d.pdf" % (mov))
    fig, ax = plt.subplots(figsize=(10,7.5))
    for readFile in sorted(glob.glob("./analysis/8pk*/moviment-%d/zdfave/AS-bridge-zdf-ave-2000000-0.dat" % (mov)), key = lambda i: float(i[i.index('8pk')+3:i.index('/moviment-')])):
        pol = readFile[readFile.index('8pk')+3:readFile.index('/moviment-')]       
        with open("./analysis/8pk%s/moviment-%s/fitting/parameters-ASbridge-fitting-k%s-moviment%d-2000000-0.dat" % (pol,mov,pol,mov), "r") as readFileCSV:
            reader_file = csv.reader(readFileCSV, delimiter='\t')
            next (reader_file)
            for line in reader_file:
                if (float(pol) > 0.3469):
                    maxRadius = float(line[11]) - 5.0
                else:
                    maxRadius = float(line[1]) - 5.0
        with open(readFile, "r") as readFileCSV:
            reader_file = csv.reader(readFileCSV, delimiter='\t')   #fitting file has to skip one line
            header =  next (reader_file)
            header.remove('#')
            header.remove('')
            header = [float(i) for i in header]
            for i in header:
                if(i < maxRadius):
                    continue
                else:
                    column = header.index(i)
                    break 
            for line in reader_file:
                colZ.append(float(line[0])) 
                colRho.append(float(line[column]))
#        colRhoAve = []
#        colZave = []
#        Nave = 3
#        for i in range(len(colRho)-int(Nave/2)):
#            colRhoAve.append(sum(colRho[i:i+Nave])/Nave)
#            colZave.append(colZ[i+int(Nave/2)])
        plt.plot(colZ, colRho, linewidth=2.0, color = dicColorsPol[pol], label = 'k = %s' % (pol))
        colZ = []
        colRho = []
    plt.axis([0, 25, 0, 2.25])
    plt.ylabel('%s  %s%s%s' % ("Density  ","[","g/cm$^3$","]"))
    plt.xlabel('%s  %s%s%s' % ("Height ","[","$\mathsf{\AA}$","]"))
    ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, length = 12.0, width = 2.0)
    ax.tick_params(axis='both', which='minor', direction='in', right=True, top=True, length = 6.0, width = 2.0)
    ax.text(22.5,1.8, dicLetterFig[mov], fontsize = 40)
    ax.xaxis.set_major_locator(majorLocatorX)
    ax.xaxis.set_major_formatter(majorFormatterX)
    ax.xaxis.set_minor_locator(minorLocatorX)
    ax.yaxis.set_major_locator(majorLocatorY)
    ax.yaxis.set_major_formatter(majorFormatterY)
    ax.yaxis.set_minor_locator(minorLocatorY)
    ax.set_title('h = %s' % (dicMovHeight[mov]))
    if (mov ==0):
       ax.legend(loc='upper center', markerscale=0.8, borderpad = 0.1,labelspacing=0.2, columnspacing = 0.5, handlelength= 0.6, handletextpad = 0.1, ncol= 3)
    plt.tight_layout()
    plt.savefig("./analysis/graphicsThermodynamic/graphicRhoZavemov%d.pdf" % (mov))
    plt.close()  
