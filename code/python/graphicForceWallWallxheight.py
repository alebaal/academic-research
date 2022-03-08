#!/usr/bin/env python

from __future__ import division
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
majorLocatorY = MultipleLocator(0.5)
majorFormatterY = FormatStrFormatter('%.2f')
minorLocatorY = MultipleLocator(0.25)

def main():
        colX = []
        colY = []
        colYerr = []
        dicColorsPol = {'0.0':(0, 0, 0, 1), '0.1':(1, 0, 0, 1), '0.2':(0, 0, 1, 1), '0.3':(0, 0.54509, 0, 1), '0.346':(0, 1, 0, 1) ,'0.4':(0.25099, 0.87843, 0.81568, 1), '0.5':(0.40392, 0.02745, 0.28235, 1), '0.6':(0.44706, 0.12941, 0.73725, 1), '0.65':(1, 0.64706, 0, 1), '0.66':(0.73725, 0.56078, 0.56078 ,1), '0.67':(0, 1, 0, 1) }
        dicPolTheta  = {'0.0':105.57462, '0.1':104.75958, '0.2':100.78243, '0.3':94.336977, '0.4':84.445479, '0.5':70.818446, '0.6':50.382360, '0.65':32.786379, '0.66':28.323013, '0.67':25.793658}
#           dicHeight = {'0':50,  '1':40,  '2':30,  '3':25,  '4':20,  '5':19,  '6':18,  '7':17}  #old
        dicMovHeight = {'0':50.0,'1':45.0,'2':40.0,'3':35.0,'4':30.0,'5':25.0,'6':20.0,'9':17.0,'11':15.0}

        print("Creating graphic ForceWallWallXheight.pdf")
        fig, ax = plt.subplots(figsize=(10,7.5))

        #for k = 0.0
        colX2    = dicMovHeight.values() 
        colY2    = np.full(len(colX2), 0)
        colY2err = np.full(len(colX2), 0)
        plt.errorbar(colX2, colY2, yerr = colY2err, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor='None', color= dicColorsPol['0.0'])           

        colX2    = [50, 45, 40, 35, 30]
        colY2    = np.full(len(colX2), 0)
        colY2err = np.full(len(colX2), 0)
        plt.errorbar(colX2, colY2, yerr = colY2err, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor=dicColorsPol['0.0'], color= dicColorsPol['0.0'])           

        #second runs
        for readFileTheoretical in sorted(glob.glob("./analysis/forceFiles/forceASbridgeLargeWall1k*.dat")):
            polarity =  readFileTheoretical[readFileTheoretical.index('ASbridgeLargeWall1k')+19:readFileTheoretical.index('.dat')]
            colX2 = []
            colY2 = []
            colY2err = []
            if((polarity == '0.5') or (polarity == '0.3')):
               for readFileAveForce in sorted(glob.glob("./analysis-V10-V11-V12/check-simulations/forceWallsCalculation/8pk%s/moviment-*/AveForceWallk%smov*.dat"
                                              % (polarity, polarity)), key = lambda x: x[x.index("moviment-")+len("moviment-")]):
                   mov = readFileAveForce[readFileAveForce.index("moviment-")+len("moviment-"):readFileAveForce.index("/AveForceWall")]
                   if (mov in dicMovHeight.keys()):
                       with open(readFileAveForce,"r") as fileref:
                           reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
                           next(reader_file)
                           line = next(reader_file)
                           colY2.append(float(line[0]))
                           colY2err.append(float(line[1]))
                       colX2.append(float(dicMovHeight[mov]))
               plt.errorbar(colX2, colY2, yerr = colY2err, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor=dicColorsPol[polarity], color= dicColorsPol[polarity]) 

	#first runs
        for readFileTheoretical in sorted(glob.glob("./analysis/forceFiles/forceASbridgeLargeWall1k*.dat")):
            polarity =  readFileTheoretical[readFileTheoretical.index('ASbridgeLargeWall1k')+19:readFileTheoretical.index('.dat')]
            colX2 = []
            colY2 = []
            colY2err = []
            for readFileAveForce in sorted(glob.glob("./forceWallsCalculation/8pk%s/moviment-*/AveForceWallk%smov*.dat" % (polarity, polarity)), key = lambda x: x[x.index("moviment-")+len("moviment-")]):
                mov = readFileAveForce[readFileAveForce.index("moviment-")+len("moviment-"):readFileAveForce.index("/AveForceWall")]
                if (mov in dicMovHeight.keys()):
                    with open(readFileAveForce,"r") as fileref:
                        reader_file = csv.reader(fileref, delimiter='\t')   #fitting file has to skip one line
                        next(reader_file)
                        line = next(reader_file)
                        colY2.append(float(line[0]))
                        colY2err.append(float(line[1]))
                    colX2.append(float(dicMovHeight[mov]))
            plt.errorbar(colX2, colY2, yerr = colY2err, fmt='o', markersize = 14, markeredgewidth = 2, capsize = 4 ,markerfacecolor='None', color= dicColorsPol[polarity])           

            with open(readFileTheoretical,"r") as fileref:
                reader_file = csv.reader(fileref, delimiter=' ')   #fitting file has to skip one line
                next(reader_file)
                next(reader_file)
                for line in reader_file:
                    colX.append(50.0 - float(line[0])*2*0.01)
                    colY.append(float(line[1])*0.06952) 
                plt.plot(colX, colY, linewidth=2, color = dicColorsPol[polarity], label =  'k = %s' % (polarity))
               
                writeFile = open("./analysis/forceFiles/forcePlottedASbridgeLargeWall1k%s.dat" % (polarity), 'w')
                writeFile.write("#height\tForce Wall-Wall (nN)\n")
                for i in range(len(colY)):
                    writeFile.write("%.8g\t%.8g\n" % (colX[i], colY[i]))
                writeFile.close()
                colX = []
                colY = []

        plt.axis([10,55,-1.5,1.75])
        plt.ylabel('%s  %s%s%s' % ("Wall-Wall Force ","[","nN","]"))
        plt.xlabel('%s  %s%s%s' % ("Height  ","[","$\mathsf{\AA}$","]"))
        ax.tick_params(axis='both', which='major', direction='in', right=True, top=True, length = 12.0, width = 2.0)
        ax.tick_params(axis='both', which='minor', direction='in', right=True, top=True, length = 6.0, width = 2.0)
        ax.xaxis.set_major_locator(majorLocatorX)
        ax.xaxis.set_major_formatter(majorFormatterX)
        ax.xaxis.set_minor_locator(minorLocatorX)
        ax.yaxis.set_major_locator(majorLocatorY)
        ax.yaxis.set_major_formatter(majorFormatterY)
        ax.yaxis.set_minor_locator(minorLocatorY)
        ax.legend(loc='upper center', markerscale=0.8, borderpad = 0.1,labelspacing=0.2, columnspacing = 0.5,  handlelength=0.6, ncol =3 )

#       ax.text(50,4.8, "(b)", fontsize = 40)
        plt.tight_layout()
        plt.savefig("./analysis/ForceWallWallXheight.pdf")
        plt.close()

if __name__ == "__main__": main()

