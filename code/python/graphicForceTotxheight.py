#!/usr/bin/env python
import sys
import csv
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import os
import glob
import numpy as np

from uncertainties import ufloat
from uncertainties import umath 

from matplotlib import rc
font = {'family' : 'Arial', 'size'   : 28}
rc('font', **font)

rc('axes', linewidth=2)


from matplotlib.ticker import MultipleLocator, FormatStrFormatter
majorLocatorX = MultipleLocator(5)
majorFormatterX = FormatStrFormatter('%d')
minorLocatorX = MultipleLocator(1)
majorLocatorY = MultipleLocator(0.8)
majorFormatterY = FormatStrFormatter('%.1f')
minorLocatorY = MultipleLocator(0.2)

def H(r0,r2):
    return 0.5*(1.0/r0 + 1.0/r2)

def forceGamma(gamma, rb, theta):
    return 2*np.pi*rb*gamma*umath.sin(np.pi*theta/180.0)*0.1 #0.1 comes from length conversion
    
def forcePressure(gamma, r0, r2, rb):
    return -2*0.1*np.pi*gamma*H(r0,r2)*rb**2 #0.1 comes from length conversion

def forceTotBase(gamma, r0, r2, rb, theta):
    return forcePressure(gamma, r0, r2, rb) + forceGamma(gamma, rb, theta)

def main():
    if (len(sys.argv) == 3):
        colX = []
        colY = []
        colYerr = []
        dicColorsPol = {'0.0':(0, 0, 0, 1), '0.1':(1, 0, 0, 1), '0.2':(0, 0, 1, 1), '0.3':(0, 0.54509, 0, 1),'0.346':(0, 1, 0, 1) ,'0.4':(0.25099, 0.87843, 0.81568, 1), '0.5':(0.40392, 0.02745, 0.28235, 1), '0.6':(0.44706, 0.12941, 0.73725, 1), '0.65':(1, 0.64706, 0, 1), '0.66':(0.73725, 0.56078, 0.56078 ,1), '0.67':(0, 1, 0, 1) }
        dicPolTheta  = {'0.0':105.57462, '0.1':104.75958, '0.2':100.78243, '0.3':94.336977, '0.4':84.445479, '0.5':70.818446, '0.6':50.382360, '0.65':32.786379, '0.66':28.323013, '0.67':25.793658}
        gamma = float(sys.argv[1])
        ErrGamma = float(sys.argv[2])
        print("Creating graphic ForceTotXheight.pdf")
        fig, ax = plt.subplots(figsize=(10,7.5))
        for readFileTheoretical in sorted(glob.glob("./analysis/theoreticalData/resultASbridgek*.dat")):
            polarity =  readFileTheoretical[readFileTheoretical.index('ASbridgek')+9:readFileTheoretical.index('.dat')]
            with open(readFileTheoretical,"r") as fileref:
                reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
                for line in reader_file:
                    colX.append(float(line[0])*2) #h/2 -> h
                    colY.append(float(line[1])*gamma/10.0) # factor 10.0: convertion from \AA no nm
                plt.plot(colX, colY,'--', linewidth=2, color = dicColorsPol[polarity])
                colX = []
                colY = []
        for readFileMoviment in sorted(glob.glob("./analysis/8pk0.*/MeasurementsXheight/parameters-ASbridge-fitting-AllHeight.dat")):
            polarity =  readFileMoviment[readFileMoviment.index('8pk')+3:readFileMoviment.index('/MeasurementsXheight/')]
            with open(readFileMoviment,"r") as fileref:
                reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
                next (reader_file)
                for line in reader_file:
                    colX.append(float(line[0])*2) #h/2 -> h
                    forceTot = forceTotBase(ufloat(gamma, ErrGamma), ufloat(float(line[11]), float(line[12])), ufloat(float(line[13]), float(line[14])), 
                                                                     ufloat(float(line[1]), float(line[2])), ufloat(float(line[3]), float(line[4])))
                    colY.append(forceTot.n) 
                    colYerr.append(forceTot.s)
                plt.errorbar(colX, colY, yerr = colYerr, fmt='s', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor='None', color= dicColorsPol[polarity])
                
                colY    = []
                colYerr = []
                colX    = []
        for readFileMoviment in sorted(glob.glob("./analysis/8pk0.*/MeasurementsXheight/AveForceLammps-AllHeight.dat")):
            polarity =  readFileMoviment[readFileMoviment.index('8pk')+3:readFileMoviment.index('/MeasurementsXheight/')]
            with open(readFileMoviment,"r") as fileref:
                reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
                next (reader_file)
                for line in reader_file:
                    colX.append(float(line[0])*2) #h/2 -> h
                    colY.append(float(line[1])) 
                    colYerr.append(float(line[2]))
                plt.errorbar(colX, colY, yerr = colYerr, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor='None', color= dicColorsPol[polarity], label = 'k = %s' % (polarity))
                colY    = []
                colYerr = []
                colX    = []
        plt.axis([10,55,-2.5,2.])
        plt.ylabel('%s  %s%s%s' % ("Force ","[","nN","]"))
        plt.xlabel('%s  %s%s%s' % ("Height  ","[","$\mathsf{\AA}$","]"))
        ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, length = 12.0, width = 2.0)
        ax.tick_params(axis='both', which='minor', direction='in', right=True, top=True, length = 6.0, width = 2.0)
        ax.xaxis.set_major_locator(majorLocatorX)
        ax.xaxis.set_major_formatter(majorFormatterX)
        ax.xaxis.set_minor_locator(minorLocatorX)
        ax.yaxis.set_major_locator(majorLocatorY)
        ax.yaxis.set_major_formatter(majorFormatterY)
        ax.yaxis.set_minor_locator(minorLocatorY)
        ax.text(50,4.8, "(b)", fontsize = 40)
#        ax.legend(loc='upper right', markerscale=0.8, borderpad = 0.2,labelspacing=0.3, handlelength=0.5 )
        plt.tight_layout()
        plt.savefig("./analysis/graphicsThermodynamic/ForceTotXheight.pdf")
        plt.close()
    else:
        print "Total force calculation\n"
        print "Parameters:"
        print "gamma"
        print "error gamma"

if __name__ == "__main__": main()


