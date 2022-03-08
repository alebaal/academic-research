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
colFx = []
colFy = []
colFz = []

invSign = lambda x: -x

if (len(sys.argv) == 5):
    #calculating the error
    colSerieFx     = []
    colSerieFy     = []
    colSerieFz     = []
    AveSampleFx    = []
    AveSampleFy    = []
    AveSampleFz    = []
    StdAveSampleFx = []
    StdAveSampleFy = []
    StdAveSampleFz = []
    ErrorForceXHeight = [0]*3
    ErrorForceYHeight = [0]*3
    ErrorForceZHeight = [0]*3
    for wall in range(1, 2 + 1): 
        teste = ("./analysis/8pk%s/moviment-%s/forceWallMD/forceASbridgeLargeWall%dk%s-mov%s.dat" % (sys.argv[1], sys.argv[2], wall, sys.argv[1], sys.argv[2]))
        sizeSample = 1
        while (sizeSample <= int(sys.argv[4])):
            with open(teste,"r") as fileref:
                reader_file = csv.reader(fileref, delimiter=' ')
                next(reader_file)
                next(reader_file)
                runningAverage = 0
                for i in range(0, int(sys.argv[3])): 
                    next(reader_file)
                for line in reader_file:
     	            colTime.append(float(line[0]))
                    colSerieFx.append(float(line[1])*0.06952) #CONVERTING kcal/mol/A -> nN
                    colSerieFy.append(float(line[2])*0.06952) 
                    colSerieFz.append(float(line[3])*0.06952) 
                    runningAverage+=1
                    if (runningAverage == sizeSample):
                        AveSampleFx.append(np.mean(colSerieFx))
                        AveSampleFy.append(np.mean(colSerieFy))
                        AveSampleFz.append(np.mean(colSerieFz))
                        runningAverage = 0
                        colSerieFx = []
                        colSerieFy = []	
                        colSerieFz = []
            StdAveSampleFx.append(np.std(AveSampleFx)/np.sqrt(len(AveSampleFx)))
            StdAveSampleFy.append(np.std(AveSampleFy)/np.sqrt(len(AveSampleFy)))
            StdAveSampleFz.append(np.std(AveSampleFz)/np.sqrt(len(AveSampleFz)))
            AveSampleFx = []
            AveSampleFy = []
            AveSampleFz = []
            sizeSample*=2		
        ErrorForceXHeight[wall] += max(StdAveSampleFx)**2 ##Equal here?
        ErrorForceYHeight[wall] += max(StdAveSampleFy)**2
        ErrorForceZHeight[wall] += max(StdAveSampleFz)**2
        
        print("Creating graphic MeanErrorFxyz-%d-%s-moviment%s.png ... " % ( wall, sys.argv[1], sys.argv[2]))
        fig = plt.figure( )
        axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        axes.spines['right'].set_color('none')
        axes.spines['top'].set_color('none')
        axes.yaxis.tick_left()
        axes.xaxis.tick_bottom()
        axes.set_ylabel( r'Error on Force [nN]' , fontsize=10)
        axes.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        axes.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        axes.set_xlabel(r'sample size: 2^x', fontsize=10)
        colX = np.arange(len(StdAveSampleFx))
        axes.plot( colX, StdAveSampleFx, linewidth=0.50, label ="Fx")
        axes.plot( colX, StdAveSampleFy, linewidth=0.50, label ="Fy")
        axes.plot( colX, StdAveSampleFz, linewidth=0.50, label ="Fz")
        axes.legend(loc='upper right');
        axes.set_title('Force: wall-%d, k-%s, moviment-%s' % (wall, sys.argv[1], sys.argv[2]))
        fig.savefig('./analysis/8pk%s/moviment-%s/forceWallMD/MeanErrorFxyz-Wall%d-k%s-moviment%s.png'    % (sys.argv[1], sys.argv[2], wall, sys.argv[1], sys.argv[2]))
        plt.close(fig)
        StdAveSampleFx = []
        StdAveSampleFy = []
        StdAveSampleFz = []
	
    #read the wall wall force to correct
    colFww = []
    fileName = ("./forceWallsCalculation/8pk%s/moviment-%s/AveForceWallk%smov%s.dat" % (sys.argv[1], sys.argv[2], sys.argv[1], sys.argv[2]))
    with open(fileName,"r") as fileref:
        reader_file = csv.reader(fileref, delimiter='\t')
        next(reader_file)
        colFww = next(reader_file)

    #calculating the mean	 
    meanForceHeight = [0]*3
    fileName = ("./analysis/8pk%s/moviment-%s/forceWallMD/AveForceMoviment%sWallk%s.dat" % (sys.argv[1], sys.argv[2], sys.argv[2], sys.argv[1]))
    fileAveForce = open(fileName, "w")
    for wall in range(1, 2 + 1): 
        teste = ("./analysis/8pk%s/moviment-%s/forceWallMD/forceASbridgeLargeWall%dk%s-mov%s.dat" % (sys.argv[1], sys.argv[2], wall, sys.argv[1], sys.argv[2]))
        with open(teste,"r") as fileref:
            reader_file = csv.reader(fileref, delimiter=' ')
            next(reader_file)
            next(reader_file)
            for i in range(0, int(sys.argv[3])): 
               next(reader_file)
            for line in reader_file:
                colFx.append([float(line[1])*0.06952])
                colFy.append([float(line[2])*0.06952])
                colFz.append([float(line[3])*0.06952]) #CONVERTING kcal/mol/A -> nN
            meanForceHeight[0] += abs(np.mean(colFx))
            meanForceHeight[1] += abs(np.mean(colFy))
            meanForceHeight[2] += abs(np.mean(colFz))
        colFx = [] 
        colFy = []
        colFz = []
    fileAveForce.write("#<Fx(nN)>\tSTD[Fx(nN)]\t<Fy(nN)>\tSTD[Fy(nN)]\t<Fz(nN)>\tSTD[Fz(nN)]; Fx is correted by Fww \n")
#   fileAveForce.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (meanForceHeight[0]/2, np.sqrt((np.sqrt(sum(ErrorForceXHeight))/1.414213562)**2) ,meanForceHeight[1]/2, np.sqrt(sum(ErrorForceYHeight))/1.414213562,meanForceHeight[2]/2, np.sqrt(sum(ErrorForceZHeight))/1.414213562))
    fileAveForce.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (meanForceHeight[0]/2 - invSign(float(colFww[0])), np.sqrt((np.sqrt(sum(ErrorForceXHeight))/1.414213562)**2) ,meanForceHeight[1]/2, np.sqrt(sum(ErrorForceYHeight))/1.414213562,meanForceHeight[2]/2, np.sqrt(sum(ErrorForceZHeight))/1.414213562))
    #fileAveForce.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (meanForceHeight[0]/2 - float(colFww[0]), np.sqrt((np.sqrt(sum(ErrorForceXHeight))/1.414213562)**2 + float(colFww[1])**2) , meanForceHeight[1]/2, np.sqrt(sum(ErrorForceYHeight))/1.414213562,meanForceHeight[2]/2, np.sqrt(sum(ErrorForceZHeight))/1.414213562))
    fileAveForce.close()

else:
	print "\nArguments Error"
        print  str(sys.argv)
        print "\n"
        print ("USAGE:", sys.argv[0], "k")
        print "arg1  k"
        print "arg2  moviment"
        print "arg3  skip lines average"
        print "arg4  biggest sample size"

