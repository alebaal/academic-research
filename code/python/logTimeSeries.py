#!/usr/bin/env python

import sys
import csv
import matplotlib
#matplotlib.use('cairo')
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np

#TO_DO: this script works, but I should set one different scale for each graphic


nameParSave = ['TotEng_X_Time','KinEng_X_Time','Temp_x_Time','waterTem_x_Time','wallHTem_x_Time','PotEng_X_Time','Ebond_x_Time', 'Eang_x_Time', 'Evdwl_x_Time', 'Ecoul_X_Time', 'Elong_x_Time', 'Press_x_Time','Volume_x_Time']
unitsY = [r'[$Kcal/mole$]', r'[$Kcal/mole$]', r'[Kelvin]', r'[Kelvin]',r'[Kelvin]',r'[$Kcal/mole$]', r'[$Kcal/mole$]', r'[$Kcal/mole$]', r'[$Kcal/mole$]', r'[$Kcal/mole$]', r'[$Kcal/mole$]', r'[atm] ',r'[$\AA^3$]']
Graphic = [r'TotEng', r'KinEng', r'Temp', r'waterTem',r'wallHTem',r'PotEng', r'Ebond', r'Eang', r'Evdwl', r'Ecoul', r'Elong', r'Press',r'Volume']

AllTable = []
AllMean  = []
AllStd   = []
if (len(sys.argv) == 3):
    teste = ("./analysis/8pk%s/moviment-%s/logAnalysis/logk%s.dat" % (sys.argv[1],sys.argv[2],sys.argv[1]))
    if (sys.argv[1]=="0.0"):
       del nameParSave[4]
       del unitsY[4]
       del Graphic[4]        
    with open(teste,"r") as fileref:
        reader_file = csv.reader(fileref,skipinitialspace=False ,delimiter=' ')
        for line in reader_file:
            AllTable.append(map(float,filter(None,line)))	
            AllTableNumpy = np.array(AllTable)
        for column in range(len(nameParSave)): #number of columns   CHANGE TO 2
            print("Creating graphic %s-k%s.png ... " % (nameParSave[column], sys.argv[1] ))
            fig = plt.figure( )
            axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
            axes.spines['right'].set_color('none')
            axes.spines['top'].set_color('none')
            axes.yaxis.tick_left()
            axes.xaxis.tick_bottom()
            axes.set_ylabel(unitsY[column - 1], fontsize=10)
            axes.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            axes.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
            axes.set_xlabel(r'time', fontsize=10)
            axes.plot(AllTableNumpy[:,0], AllTableNumpy[:,column + 1], linewidth=0.4)
            mean = AllTableNumpy[:,column + 1].mean()
            standDev = AllTableNumpy[:,column + 1].std()
            AllMean.append(mean)
            AllStd.append(standDev)
            axes.set_title('k%s   <%s> = %.3f %s %.3f ' % (sys.argv[1] ,Graphic[column - 1],  mean, r'$\mp$' ,standDev))
            fig.savefig('./analysis/8pk%s/moviment-%s/logAnalysis/%s-%s.png' % (sys.argv[1],sys.argv[2],nameParSave[column - 1], sys.argv[1]))
            plt.close(fig)
            mean = []
            stanDev = []
else:
	print "\nArguments Error"
        print  str(sys.argv)
        print "\n"
        print  ("USAGE:", sys.argv[0], "k")
        print  "arg1  k"
        print  "arg2  moviment"



