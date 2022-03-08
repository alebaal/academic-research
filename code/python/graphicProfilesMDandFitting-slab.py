#!/usr/bin/env python
import sys
import csv
import glob
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')

from matplotlib import rc
font = {'family' : 'Arial', 'size'   : 28}
rc('font', **font)

rc('axes', linewidth=2)

from matplotlib.ticker import MultipleLocator, FormatStrFormatter
majorLocatorX = MultipleLocator(10)
majorFormatterX = FormatStrFormatter('%d')
minorLocatorX = MultipleLocator(1)
majorLocatorY = MultipleLocator(10)
majorFormatterY = FormatStrFormatter('%d')
minorLocatorY = MultipleLocator(1)

colX = []
colX2 = []
colY = []
colY2 = []
colk = []
colTheta = []

dicMovHeight = {'0':'50', '1':'40', '2':'30', '3':'25', '4':'20', '5':'19', '6':'18', '7':'17', '8':'16'}
dicColorsPol = {'0.0':{'0':(0, 0, 0, 1), '3':(0, 0, 1, 1),'4':'magenta','5':'magenta','6':'magenta', '7':(0.250980392,0.878431373,0.815686275,1)}, '0.5':{'0':(1, 0, 0, 1), '3':(0.25099, 0.87843, 0.81568, 1), '4':(0.447058824, 0.129411765, 0.737254902 ,1), '5':'magenta', '6':'magenta', '7':(0.250980392,0.878431373,0.815686275,1)}}

maxHeight = []

if (len(sys.argv) == 4):
    Npoints = []
    for readFileMoviment in sorted(glob.glob("./analysis/checkSlab/8pk%s/moviment-%s/fitting/parameters-ASbridge-fitting-k0.?-moviment?-2000000-0-*-rm%s.dat" % (sys.argv[1], sys.argv[2], sys.argv[3]))):
        Npoints.append(readFileMoviment[readFileMoviment.index('0-0-')+4:readFileMoviment.index('.dat')-4])
    for x in Npoints:
        file1 = ("./analysis/checkSlab/8pk%s/moviment-%s/fitting/ASbridge-fitting-k%s-moviment%s-2000000-0-%s-rm0.dat"  % (sys.argv[1], sys.argv[2], sys.argv[1], sys.argv[2], x))
        file2 = ("./analysis/checkSlab/8pk%s/moviment-%s/profile/AS-bridge-profileDM-2000000-0-%s.dat" % (sys.argv[1], sys.argv[2], x))
        print("Creating graphic profileDMandFittingk%smov%s-Npoints-%s.pdf" % (sys.argv[1], sys.argv[2], x))
        fig, ax = plt.subplots(figsize=(10,7.5))
        colY  = []
        colX  = []
        colY2 = []
        colX2 = []
        colY3 = []
        colX3 = []
        with open(file1,"r") as fileref:
            reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
            next (reader_file)
            for line in reader_file:
                colX.append(float(line[1]))
                colY.append(float(line[0]))
            plt.plot(colX, colY, '--', linewidth=2, color = dicColorsPol[sys.argv[1]][sys.argv[2]])
        with open(file2,"r") as fileref:
            reader_file = csv.reader(fileref, delimiter=' ')
            for line in reader_file:
                colX2.append(float(line[1]))
                colY2.append(float(line[0]))
            plt.plot(colX2, colY2, 'o', markersize = 10,markeredgewidth=2,  markerfacecolor='None', color = dicColorsPol[sys.argv[1]][sys.argv[2]])

        if (int(sys.argv[3]) > 0 ):
           file3 = ("./analysis/checkSlab/8pk%s/moviment-%s/fitting/ASbridge-fitting-k%s-moviment%s-2000000-0-%s-rm%s.dat" % (sys.argv[1], sys.argv[2], sys.argv[1], sys.argv[2], x, sys.argv[3]))
           with open(file3,"r") as fileref:                                                                  
                reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
                next (reader_file)
                for line in reader_file:
                    colX3.append(float(line[1]))
                    colY3.append(float(line[0]))
                plt.plot(colX3, colY3, linewidth=2, color = dicColorsPol[sys.argv[1]][sys.argv[2]])
            

        plt.axis([0,70,0,50])
        plt.ylabel('%s  %s%s%s' % ("Height","[","$\mathsf{\AA}$","]"))
        plt.xlabel('%s  %s%s%s' % ("r","[","$\mathsf{\AA}$","]"))
        ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, length = 12.0, width = 2.0)
        ax.tick_params(axis='both', which='minor', direction='in', right=True, top=True, length = 6.0, width = 2.0)
#       ax.text(60,20, dicLetterFig[x], fontsize = 40)
        ax.xaxis.set_major_locator(majorLocatorX)
        ax.xaxis.set_major_formatter(majorFormatterX)
        ax.xaxis.set_minor_locator(minorLocatorX)
        ax.yaxis.set_major_locator(majorLocatorY)
        ax.yaxis.set_major_formatter(majorFormatterY)
        ax.yaxis.set_minor_locator(minorLocatorY)
        ax.legend(loc='upper left',markerscale=0.8, borderpad = 0.3, labelspacing=0.2, columnspacing = 0.5, handlelength= 0.6, handletextpad = 0.1)
        ax.set_title('k = %s     slab $\simeq$ %.3f $\mathsf{\AA}$' % (sys.argv[1], float(dicMovHeight[sys.argv[2]])/float(x)))
        plt.tight_layout()
        plt.savefig("./analysis/checkSlab/8pk%s/moviment-%s/profileDMandFittingk%smov%s-Npoints-%s-rm%s.pdf" % (sys.argv[1], sys.argv[2], sys.argv[1], sys.argv[2], x, sys.argv[3]))
        plt.close()
else:
	print "\nArguments Error"
	print  str(sys.argv)
	print "\n"
	print  "arg1   polarization"
	print  "arg2   moviment"
	print  "arg3   n missing points close to the interface"
