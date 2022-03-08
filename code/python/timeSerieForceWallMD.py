#!/usr/bin/env python

from __future__ import division
import sys
import csv
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np

axisLabelY = [r'$F_x$[nN]', r'$F_y$[nN]', r'$F_z$[nN]']
nameParSave = ['Fx_x_time_wall','Fy_x_time_wall','Fz_x_time_wall']

colTime = []
colF = []
if (len(sys.argv) == 3):
   for wall in range(1, 2 + 1):                                 
       teste = ("./analysis/8pk%s/moviment-%s/forceWallMD/forceASbridgeLargeWall%dk%s-mov%s.dat" % (sys.argv[1], sys.argv[2], wall, sys.argv[1], sys.argv[2]))
       for column in range(0, 2 + 1): #number of columns   CHANGE TO 2
           print("Creating graphic %s-%d-k%s.png ... " % (nameParSave[column], wall, sys.argv[1] ))
           fig = plt.figure( )
           axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
           axes.spines['right'].set_color('none')
           axes.spines['top'].set_color('none')
           axes.yaxis.tick_left()
           axes.xaxis.tick_bottom()
           axes.set_ylabel(axisLabelY[column], fontsize=10)
           axes.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
           axes.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
           axes.set_xlabel(r'time', fontsize=10)
           with open(teste,"r") as fileref:
              reader_file = csv.reader(fileref, delimiter=' ')
              next(reader_file)
              next(reader_file)
              for line in reader_file:
                  colTime.append(float(line[0]))
                  colF.append(float(line[column + 1])*0.06952) #CONVERTING kcal/mol/A -> nN
              axes.plot(colTime, colF, linewidth=0.50)
              mean = np.mean(colF)
              standDev = np.std(colF)
              axes.set_title('Force %s on  wall %d and k = %s : %.3f %s %.3f nN ' % (axisLabelY[column] ,wall, sys.argv[1] , mean, r'$\mp$' ,standDev))
              fig.savefig('./analysis/8pk%s/moviment-%s/forceWallMD/%s-%d-%s-moviment%s.png' % (sys.argv[1], sys.argv[2], nameParSave[column], wall, sys.argv[1], sys.argv[2]))
              plt.close(fig)
              mean = []
              stanDev = []
              colTime = []
              colF = []
else:                    
	print "\nArguments Error"
        print  str(sys.argv)
        print "\n"
        print  ("USAGE:", sys.argv[0], "k")
        print  "arg1  k"
        print  "arg2  moviment"
