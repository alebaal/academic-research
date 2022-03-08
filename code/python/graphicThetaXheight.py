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
majorLocatorY = MultipleLocator(20)
majorFormatterY = FormatStrFormatter('%d')
minorLocatorY = MultipleLocator(10)
dicColorsPol = {'0.0':(0, 0, 0, 1), '0.1':(1, 0, 0, 1), '0.2':(0, 0, 1, 1), '0.3':(0, 0.54509, 0, 1),'0.346':(0, 1, 0, 1), '0.4':(0.25099, 0.87843, 0.81568, 1), '0.5':(0.40392, 0.02745, 0.28235, 1), '0.6':(0.44706, 0.12941, 0.73725, 1), '0.65':(1, 0.64706, 0, 1), '0.66':(0.73725, 0.56078, 0.56078 ,1), '0.67':(0, 1, 0, 1) }
#dicMovHeight = {'0':50.0,'1':40.0,'2':30.0,'3':25.0,'4':20.0,'5':19.0,'6':18.0,'7':17.0,'8':16.0,'9':15.0} #old colors
dicMovHeight = {'0':50.0,'1':45.0,'2':40.0,'3':35.0,'4':30.0,'5':25.0,'6':20.0,'7':19.0,'8':18.0,'9':17.0,'10':16.0,'11':15.0}

def main():
    if (len(sys.argv) == 3):
        colX = []
        colY = []
        colYerr = []
        print("Creating graphic ThetaXheightMov%sto%s.pdf" % (sys.argv[1], sys.argv[2]))
        fig, ax = plt.subplots(figsize=(10,7.5))
        for readFileMoviment in sorted(glob.glob("./analysis/8pk0.*/MeasurementsXheight/parameters-ASbridge-fitting-AllHeight.dat")):
            polarity =  readFileMoviment[readFileMoviment.index('8pk')+3:readFileMoviment.index('/MeasurementsXheight/')]
            with open(readFileMoviment,"r") as fileref:
                reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
                next (reader_file)
                aveTheta = []
                for line in reader_file:
                    height = round(float(line[0]))*2
                    if((height >= dicMovHeight[sys.argv[2]]) and (height <= dicMovHeight[sys.argv[1]])):
                      colX.append(float(line[0])*2) #h/2 -> h
                      colY.append(float(line[3]))
                      colYerr.append(float(line[4]))
                      if(height >= 35.0):
                        aveTheta.append(float(line[3])) 
                    else: 
                        continue 
                plt.plot([10,50], [np.mean(aveTheta), np.mean(aveTheta)], '--', linewidth=2, color = dicColorsPol[polarity])        
                plt.errorbar(colX, colY, yerr = colYerr, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor='None', color= dicColorsPol[polarity], label = 'k = %s' % (polarity))
        #        aveTheta = np.average(colY)
        #        plt.plot([10,55], [aveTheta, aveTheta],'--' , linewidth=2, color = dicColorsPol[polarity])        
                colY    = []
                colYerr = []
                colX    = []
        plt.axis([10,55,30,135])
        plt.ylabel('%s  %s%s%s' % ("Contact Angle  ","[","$^\mathsf{\circ}$","]"))
        plt.xlabel('%s  %s%s%s' % ("Height  ","[","$\mathsf{\AA}$","]"))
        ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, length = 12.0, width = 2.0)
        ax.tick_params(axis='both', which='minor', direction='in', right=True, top=True, length = 6.0, width = 2.0)
        ax.xaxis.set_major_locator(majorLocatorX)
        ax.xaxis.set_major_formatter(majorFormatterX)
        ax.xaxis.set_minor_locator(minorLocatorX)
        ax.yaxis.set_major_locator(majorLocatorY)
        ax.yaxis.set_major_formatter(majorFormatterY)
        ax.yaxis.set_minor_locator(minorLocatorY)
        ax.text(50,45, "(a)", fontsize = 40)
        ax.legend(loc='lower left', markerscale=0.8, borderpad = 0.3,labelspacing=0.2, columnspacing = 0.5, handlelength= 0.6, handletextpad = 0.1, ncol= 3)
        plt.tight_layout()
        plt.savefig("./analysis/graphicsGeometry/ThetaXheightMov%sto%s.pdf" % (sys.argv[1], sys.argv[2]))
        plt.close()
    else:
        print "Total force calculation\n"
        print "Parameters:"
        print "First height"
        print "Last  height"

if __name__ == "__main__": main()

