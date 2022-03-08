#!/usr/bin/env python

from __future__ import division
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
height = []
neck   = []
base = []

dicLetterFig = {'0.0':'(a)', '0.1':'(b)', '0.2':'(c)', '0.3':'(d)', '0.346':'(e)', '0.4':'(f)', '0.5':'(g)', '0.6':'(h)'}
dicColorsHeight = {0:(0, 0, 0, 1), 1:(1, 0, 0, 1), 2:(0, 0, 1, 1), 3:(0, 0.54509, 0, 1), 4:(0.403921, 0.027450, 0.2823529, 1), 5:(0.250980392,0.878431373,0.815686275,1), 6:(0.447058824, 0.129411765, 0.737254902 ,1), 7:('magenta')}
maxHeight = []

def findCurvature(r0, theta, rB): 
    if (theta < 90):  
       a = np.tan(np.radians(theta))
    else:
       a = np.tan(np.radians(180 - theta))
    b = rB**2 - r0**2
    roots = list(np.roots([(1+a**2)*b**2, 2*b*r0*(1+a**2), r0**2 - b*a**2 ]))
    roots2 = map(abs, roots) 
    return roots[roots2.index(min(roots2))]

def intProfile(r0, maxHeight, theta, rB):
    DeltaRho = 0.001 
    aveH = findCurvature(r0, theta, rB) 
    if (theta < 90):
       Rho = [r0]
       Z   = [0]
       for i in range(1, int(rB/0.001)):
           Rho.append(r0 + (DeltaRho*i))
           XXX =  abs(aveH*(Rho[-1]**2 - r0**2) + r0)
           DeltaZ = (XXX/np.sqrt(Rho[-1]**2 - XXX**2))*DeltaRho
           Z.append(Z[-1] + DeltaZ)
           if (Z[-1] > maxHeight):
              break
    else:
       Rho = [r0]
       Z   = [0]
       for i in range(1, int(rB/0.001)):
           Rho.append(r0 - (DeltaRho*i))
           XXX =  abs(aveH*(Rho[-1]**2 - r0**2) + r0)
           DeltaZ = (XXX/np.sqrt(Rho[-1]**2 - XXX**2))*DeltaRho
           Z.append(Z[-1] + DeltaZ)
           if (Z[-1] > maxHeight):
              break
    return Rho, Z

if (len(sys.argv) == 5):
#All fitting and profile for the same contact angle
    print("profileDMandFittingk%smov%sto%s.pdf" % (sys.argv[1], sys.argv[2], sys.argv[3]))
    fig, ax = plt.subplots(figsize=(10,7.5))
    for x in range( int(sys.argv[2]), int(sys.argv[3]) + 1):
        file1 = ("./analysis/8pk%s/moviment-%d/fitting/ASbridge-fitting-k%s-moviment%d-%s-0.dat" % (sys.argv[1], x, sys.argv[1], x, sys.argv[4]))
        file2 = ("./analysis/8pk%s/moviment-%d/profile/AS-bridge-profileDM-%s-0.dat" % (sys.argv[1], x, sys.argv[4]))
        with open(file1,"r") as fileref:
            reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
            next (reader_file)
            for line in reader_file:
                colX.append(float(line[1]))
                colY.append(float(line[0]))
            height.append(colY[-1])
            base.append(colX[-1])
            neck.append(colX[0])
            plt.plot(colX, colY, linewidth=2, color = dicColorsHeight[x], label = 'h = %.1f $\mathsf{\AA}$' % (round(2*colY[-1])))
        with open(file2,"r") as fileref:
            reader_file = csv.reader(fileref, delimiter=' ')
            for line in reader_file:
                colX2.append(float(line[1]))
                colY2.append(float(line[0]))
            plt.plot(colX2, colY2, 'o', markersize = 10,markeredgewidth=2,  markerfacecolor='None', color = dicColorsHeight[x])
        colY  = []
        colX  = []
        colY2 = []
        colX2 = []

    #Comparison with JPCC2018 paper: only for k different of 0.346
    if (sys.argv[1] != '0.346'):
       with open("./analysis/dataJPCC2018/ThetaXk-new.dat", "r") as fileProfile:
            reader_file = csv.reader(fileProfile, delimiter='\t')
            next(reader_file)
            next(reader_file)
            for line in reader_file:
                colk.append(line[0])
                colTheta.append(float(line[1]))
       theta = colTheta[colk.index(sys.argv[1])]
    
       colY = []
       colX = []
       for i in range(len(neck)-1):
           colX, colY =  intProfile(neck[i], height[i], theta, base[i])
           plt.plot(colX, colY, '--', linewidth=2, color = 'gray')
           colY = []
           colX = []
       colX, colY =  intProfile(neck[len(neck)-1], height[len(neck)-1], theta, base[len(neck)-1])
       plt.plot(colX, colY, '--', linewidth=2, color = 'gray', label = 'JPCC2018')


    plt.axis([0,70,0, 25])
    plt.ylabel('%s  %s%s%s' % ("Height","[","$\mathsf{\AA}$","]"))
    plt.xlabel('%s  %s%s%s' % ("r","[","$\mathsf{\AA}$","]"))
    ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, length = 12.0, width = 2.0)
    ax.tick_params(axis='both', which='minor', direction='in', right=True, top=True, length = 6.0, width = 2.0)
    ax.text(60,20, dicLetterFig[sys.argv[1]], fontsize = 40)
    ax.xaxis.set_major_locator(majorLocatorX)
    ax.xaxis.set_major_formatter(majorFormatterX)
    ax.xaxis.set_minor_locator(minorLocatorX)
    ax.yaxis.set_major_locator(majorLocatorY)
    ax.yaxis.set_major_formatter(majorFormatterY)
    ax.yaxis.set_minor_locator(minorLocatorY)
    if(sys.argv[1]=='0.0'):
       ax.legend(loc='upper left',markerscale=0.8, borderpad = 0.3, labelspacing=0.2, columnspacing = 0.5, handlelength= 0.6, handletextpad = 0.1)
    ax.set_title('k = %s' % (sys.argv[1]))
    plt.tight_layout()
    plt.savefig("./analysis/8pk%s/profileDMandFittingk%smov%sto%s.pdf" % (sys.argv[1], sys.argv[1], sys.argv[2], sys.argv[3]))
    plt.close()
else:
	print "\nArguments Error"
	print  str(sys.argv)
	print "\n"
	print  ("USAGE:", sys.argv[0], "model, caParameters, numSimulations, lH, hH")
	print  "arg1  polarization"
	print  "arg2  first moviment"
	print  "arg3  last  moviment"
	print  "arg4  taveInterval"
