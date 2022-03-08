#!/usr/bin/env python

from __future__ import division
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
#majorLocatorX = MultipleLocator(2)
#majorFormatterX = FormatStrFormatter('%d')
#minorLocatorX = MultipleLocator(1)
majorLocatorY = MultipleLocator(50)
majorFormatterY = FormatStrFormatter('%d')
minorLocatorY = MultipleLocator(25)

dicMovHeight = {'0':'50', '1':'40', '2':'30', '3':'25', '4':'20', '5':'19', '6':'18', '7':'17', '8':'16'}
dicColorsPol = {'0.0':{'0':(0, 0, 0, 1), '3':(0, 0, 1, 1),'4':'magenta', '5':(0,1,0,1), '6':(1,0,0,1), '7':(0.73725, 0.56078, 0.56078 ,1)}, '0.5':{'0':(1, 0, 0, 1), '3':(0.25099, 0.87843, 0.81568, 1), '4':(0.447058824, 0.129411765, 0.737254902 ,1) , '5':(0.40392, 0.02745, 0.28235, 1), '6':(0, 0.54509, 0, 1 )}}

files = {'0.0': {'0':[], '3':[], '4':[], '5':[], '6':[],'7':[]}, '0.5': {'0':[], '3':[], '4':[], '5':[], '6':[]}}

if (len(sys.argv) == 2):
    for readFileMoviment in sorted(glob.glob("./analysis/checkSlab/8pk0.?/moviment-?/fitting/parameters-ASbridge-fitting-k0.?-moviment?-2000000-0-*-rm%s.dat" % (sys.argv[1]))):
        pol =  readFileMoviment[readFileMoviment.index('/8pk')+4:readFileMoviment.index('/moviment-')]
        mov = readFileMoviment[readFileMoviment.index('/moviment-')+10:readFileMoviment.index('/fitting/')]
        Npoints = readFileMoviment[readFileMoviment.index('0-0-')+4:readFileMoviment.index('.dat')-4]
        files[pol][mov].append(Npoints)
    
    fig, ax = plt.subplots(figsize=(10,7.5))
    print("Creating graphic ThetaXslab-rm%s.pdf" % (sys.argv[1]))
    for keyPol, keyMov in files.iteritems():
        for keyMov2, Npoints in keyMov.iteritems():
            if not Npoints:
                continue
            else:
                colTheta = []
                colThetaErr = []
                #for i in slabs.sort(key=lambda x:float(x)):
                for i in Npoints:
                     readFileMoviment = ("./analysis/checkSlab/8pk%s/moviment-%s/fitting/parameters-ASbridge-fitting-k%s-moviment%s-2000000-0-%s-rm%s.dat" % (keyPol, keyMov2, keyPol, keyMov2, i, sys.argv[1]))
                     with open(readFileMoviment,"r") as fileref:
                         reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
                         next(reader_file)
                         line = next(reader_file)
                         colTheta.append(float(line[3]))
                         colThetaErr.append(float(line[4]))
            slabs = [float(dicMovHeight[keyMov2])/float(j) for j in Npoints]
            plt.errorbar(slabs, colTheta, yerr = colThetaErr, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor='None', color= dicColorsPol[keyPol][keyMov2], label = 'k = %s, h = %s $\mathsf{\AA}$' % (keyPol, dicMovHeight[keyMov2]))

    ax.set_xscale('log')
    plt.axis([0.9,15,50,175])
    plt.ylabel('%s  %s%s%s' % ("Contact Angle  ","[","$^\mathsf{\circ}$","]"))
    plt.xlabel('%s  %s%s%s' % ("Slab thickness ","[","$\mathsf{\AA}$","]"))
    ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, length = 12.0, width = 2.0)
    ax.tick_params(axis='both', which='minor', direction='in', right=True, top=True, length = 6.0, width = 2.0)
    ax.yaxis.set_major_locator(majorLocatorY)
    ax.yaxis.set_major_formatter(majorFormatterY)
    ax.yaxis.set_minor_locator(minorLocatorY)

    ax.text(10,125, "(a)", fontsize = 40)
    ax.legend(loc='upper center', markerscale=0.8, borderpad = 0.3,labelspacing=0.2, columnspacing = 0.5, handlelength= 0.6, handletextpad = 0.1, ncol = 2)
    plt.tight_layout()
    plt.savefig("./analysis/checkSlab/ThetaXslab-rm%s.pdf" % (sys.argv[1]))
    plt.close()

else:
    print "\nArguments Error"
    print  str(sys.argv)
    print "\n"
    print  "arg1 N missing points close the interface"

