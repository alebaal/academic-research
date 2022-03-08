#!/usr/bin/env python
from __future__ import division
import sys
import csv
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import os
import glob
import numpy as np
import math
from scipy.optimize import curve_fit


from matplotlib import rc
font = {'family' : 'Arial', 'size'   : 28}
rc('font', **font)

rc('axes', linewidth=2)


from matplotlib.ticker import MultipleLocator, FormatStrFormatter
majorLocatorX = MultipleLocator(10)
majorFormatterX = FormatStrFormatter('%d')
minorLocatorX = MultipleLocator(5)
majorLocatorY = MultipleLocator(0.2)
majorFormatterY = FormatStrFormatter('%.1f')
minorLocatorY = MultipleLocator(0.1)


def fitting(x, a, b, c):
    return a/x**b + c


dicColorsPol = {'0.0':(0, 0, 0, 1), '0.1':(1, 0, 0, 1), '0.2':(0, 0, 1, 1), '0.3':(0, 0.54509, 0, 1), '0.346':(0, 1, 0, 1), '0.4':(0.25099, 0.87843, 0.81568, 1), '0.5':(0.40392, 0.02745, 0.28235, 1), '0.6':(0.44706, 0.12941, 0.73725, 1), '0.65':(1, 0.64706, 0, 1), '0.66':(0.73725, 0.56078, 0.56078 ,1), '0.67':(0, 1, 0, 1) }
readFileMovimentsJPCC2018 = glob.glob("./analysis/dataJPCC2018/parameters/k*/parameters-ASbridge-fitting*.dat")
dicMovHeight = {'0':50.0,'1':40.0,'2':30.0,'3':25.0,'4':20.0,'5':19.0,'6':18.0,'7':17.0,'8':16.0,'9':15.0}

allTheta = {'0.0':[], '0.1':[], '0.2':[], '0.3':[], '0.346':[],'0.4':[], '0.5':[]}

def main():
    if (len(sys.argv) == 3):
       colX1    = []
       colY1    = []
       colX2    = []
       colY2    = []
       colYerr2 = []
       colXall  = []
       colYall  = []
       print("Creating graphic cosThetaXheightMov%sto%s.pdf" % (sys.argv[1],  sys.argv[2]))
       fig, ax = plt.subplots(figsize=(10,7.5))
       for readFileMoviment in sorted(glob.glob("./analysis/8pk0.*/MeasurementsXheight/parameters-ASbridge-fitting-AllHeight.dat")):
           polarity =  readFileMoviment[readFileMoviment.index('8pk')+3:readFileMoviment.index('/MeasurementsXheight/')]
           if (polarity != '0.346'):
              readFileJPCC2018 = [s for s in readFileMovimentsJPCC2018 if polarity in s][0]
              with open(readFileJPCC2018,"r") as fileref:
                   reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
                   next (reader_file)
                   for line in reader_file:
                       colX1.append(float(line[0])*2) #h/2 -> h
                       colY1.append(math.cos(math.radians(180 - float(line[3]))))
                   colX1.remove(colX1[0])  
                   colY1.remove(colY1[0])  
                   plt.errorbar(colX1, colY1, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor='None', color= 'gray')
           with open(readFileMoviment,"r") as fileref:
                reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
                next (reader_file)
                for line in reader_file:
                    height = round(float(line[0]))*2
                    if((height >= dicMovHeight[sys.argv[2]]) and (height <= dicMovHeight[sys.argv[1]])):
                      colX2.append(float(line[0])*2) #h/2 -> h
                      colY2.append(math.cos(math.radians(float(line[3]))))
                      colYerr2.append(math.sin(math.radians(float(line[3])))*math.radians(float(line[4])))
                    else:
                        continue
                plt.errorbar(colX2, colY2, yerr = colYerr2, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor='None', color= dicColorsPol[polarity], label = 'k = %s' % (polarity))
   
           allTheta[polarity].append(colX2+colX1)
           allTheta[polarity].append(colY2+colY1)
           colY1    =  []
           colX1    =  []
           colY2    =  []
           colX2    =  []
           colYerr2 =  []
       
       writeFile = open("./analysis/cosThetaXheightFitting.dat", 'w') 
       writeFile.write("#k\ta\tb\tc [y(x)=a/x^b + c]\n") 
#       for polarity , values in allTheta.iteritems():
#           print len(values[0])
#           print len(values[1]) 
#           parameters, cov_matrix = curve_fit(fitting, np.asarray(values[0]), np.asarray(values[1]))
#           xfitting = np.linspace(10, 80, 3000)
#           yfitting = fitting(xfitting, *parameters)
#           plt.plot(xfitting, yfitting, '--', color =dicColorsPol[polarity] , linewidth=2.0)
#           writeFile.write("%s\t%.8g\t%.8g\t%.8g\n" % (polarity, parameters[0], parameters[1], parameters[2])) 
#       writeFile.close()
       
       plt.axis([10, 80,-0.8,0.8])
       plt.ylabel('%s' % (r"$\cos\theta$"))
       plt.xlabel('%s  %s%s%s' % ("Height  ","[","$\mathsf{\AA}$","]"))
       ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, length = 12.0, width = 2.0)
       ax.tick_params(axis='both', which='minor', direction='in', right=True, top=True, length = 6.0, width = 2.0)
       ax.xaxis.set_major_locator(majorLocatorX)
       ax.xaxis.set_major_formatter(majorFormatterX)
       ax.xaxis.set_minor_locator(minorLocatorX)
       ax.yaxis.set_major_locator(majorLocatorY)
       ax.yaxis.set_major_formatter(majorFormatterY)
       ax.yaxis.set_minor_locator(minorLocatorY)
       ax.text(70,-0.6, "(b)", fontsize = 40)
       #ax.legend(loc='upper center', markerscale=0.8, borderpad = 0.1,labelspacing=0.2, columnspacing = 0.5, handlelength= 0.6, handletextpad = 0.1, ncol= 3)
       #ax.legend(loc='lower right', markerscale=0.8, borderpad = 0.2,labelspacing=0.3, handlelength=0.5 )
       plt.tight_layout()
       plt.savefig("./analysis/graphicsGeometry/cosThetaXheightMov%sto%s.pdf" % (sys.argv[1],  sys.argv[2]))
       plt.close()
    else:
        print "Total force calculation\n"
        print "Parameters:"
        print "First height"
        print "Last  height"

if __name__ == "__main__": main()

