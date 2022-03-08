#!/usr/bin/env python

from __future__ import division
from uncertainties import ufloat
from uncertainties import umath 
import math
import csv
import numpy as np
import sys
import glob
import os
import time

#Global variables
R_PROF_MIN_HPHOBIC =  5.0    # minimal radius of the hydrophobic profile
R_PROF_MAX_HPHOBIC =  350.0  # maximal radius of the hydrophobic profile

dicR_PROF_MIN_HPHILIC = {0.4:-50 , 0.5:-20}#  minimal radius of the hydrophilic profile
dicR_PROF_MAX_HPHILIC = {0.4:-1000, 0.5:-100}# maximal radius of the hydrophilic profile


DELTA_R            =  0.1     #  increment along bridge radius (x) for fitting, Angstroms
DELTAFITTINGRHO    =  0.001

def AlgVol(colRho,colH):
    Volume = 0;
    AreaRev = 0;		    
    for i in range(len(colH)-1):
        angular = (colRho[i + 1] - colRho[i])/(colH[i + 1] - colH[i])
        linear =  ((colRho[i]*colH[i + 1]) - (colRho[i + 1]*colH[i]))/(colH[i + 1] - colH[i])
        Volume  += np.pi*((angular**2)*(colH[i + 1]**3 - colH[i]**3)/3.0 + angular*linear*(colH[i + 1]**2 - colH[i]**2) + (linear**2)*(colH[i + 1] - colH[i]))
        AreaRev += 2.0*np.pi*umath.sqrt( angular**2 + 1 )*(angular*(colH[i + 1]**2 - colH[i]**2)/2.0 + linear*(colH[i + 1] - colH[i]))
    Volume*=2
    AreaRev*=2    
    return Volume, AreaRev
    
def intProfile(R1, R2, ZMaxFit, polk):
    profile = []
    aveH = H(R1, R2)
    Z   = [0.0]
    Rho = [R1]
    if (polk > 0.35): #fitting for k>0.35   ###BE CAREFULL HERE, SEE THE FITTING FOR k < 0.35 FIRST!!!!!!!!
        R1MaxFit = np.sqrt(R1**2 + (1- (2*R1*aveH))/aveH**2)
        i = 1    
        while True:  #infinity loop; I do not have to define the array size
            Rho.append(R1 + (DELTAFITTINGRHO*i))
            if(Rho[-1] > R1MaxFit):
                break
            XXX =  abs(aveH*(Rho[-1]**2 - R1**2) + R1)
            DeltaZ = (XXX/np.sqrt(Rho[-1]**2 - XXX**2))*DELTAFITTINGRHO
            if(Z[-1] + DeltaZ > ZMaxFit):
                del Rho[-1]
                break
            Z.append(Z[-1] + DeltaZ)
            i += 1
    else:           #fitting for k<0.35
        if ((R1**2 + (1 - (2*R1*aveH))/aveH**2) > 0):
            R1MinFit = np.sqrt(R1**2 + ((1 - (2*R1*aveH))/aveH**2))
        else: 
            R1MinFit = 0    
        i = 1    
        while True:  #infinity loop; I do not have to define the array size
            Rho.append(R1 - (DELTAFITTINGRHO*i))
            if(Rho[-1] < R1MinFit):
                break
            XXX =  abs(aveH*(Rho[-1]**2 - R1**2) + R1)
            DeltaZ = (XXX/np.sqrt(Rho[-1]**2 - XXX**2))*DELTAFITTINGRHO
            if(Z[-1] + DeltaZ > ZMaxFit):
                del Rho[-1]
                break
            Z.append(Z[-1] + DeltaZ)
            i += 1
    profile.append(Rho)
    profile.append(Z)    
    return profile 
 
def compareProfiles(MDprofile, fitProfile):
    sumDiffTot = 0.0
    jNextFitProf = 0
    for i in range(len(MDprofile[1])):    
        d = 10000000000.0
        for j in range(jNextFitProf, len(fitProfile[1])):    
            distPoints = (fitProfile[0][j] - MDprofile[0][i])**2 + (fitProfile[1][j] - MDprofile[1][i])**2
            if (distPoints < d):
                d = distPoints
            else:
                jNextFitProf = j
                break
        sumDiffTot += d
    return np.sqrt(sumDiffTot)/len(MDprofile[0])

def H(r0,r2):
    return 0.5*(1.0/r0 + 1.0/r2)

def main():
    if (len(sys.argv) == 5):
        polk             = float(sys.argv[1])
        tave             = int(sys.argv[3])
        dSurface         = float(sys.argv[4])  		
        #Open the profile calculated from the density
        with open("./analysis/8pk%s/moviment-%s/profile/AS-bridge-profileDM-%s-0.dat" % ( sys.argv[1], sys.argv[2], sys.argv[3]), "r") as fileProfile:
            reader_file = csv.reader(fileProfile, delimiter=' ')
            colHeight, colRadius = [], []
            for line in reader_file:
                colHeight.append(float(line[0]))
                colRadius.append(float(line[1]))
        MDprofile = []
        MDprofile.append(colRadius)
        MDprofile.append(colHeight)
        #Fitting
        if(polk < 0.35):
            profRadiusIni = R_PROF_MIN_HPHOBIC
            profRadiusEnd = R_PROF_MAX_HPHOBIC
            neckRadiusIni = 0.95*colRadius[0]
            neckRadiusEnd = 1.05*colRadius[0]
            DeltaR0 = DELTA_R
            DeltaR2 = DELTA_R
        else:
            profRadiusIni = dicR_PROF_MIN_HPHILIC[polk]
            profRadiusEnd = dicR_PROF_MAX_HPHILIC[polk]
            neckRadiusIni = 1.05*colRadius[0]
            neckRadiusEnd = 0.95*colRadius[0]
            DeltaR0 = -1.0*DELTA_R
            DeltaR2 = -1.0*DELTA_R 
        fittingErrorMin = 10000000000000.0
        for neckRadius in np.arange(neckRadiusIni, neckRadiusEnd, DeltaR0): 
            goodProfileFound = False
            for profRadius in np.arange(profRadiusIni, profRadiusEnd, DeltaR2): 
                fitProfile = intProfile(neckRadius, profRadius, dSurface, polk)
                fittingError = compareProfiles(MDprofile, fitProfile) 
                if (fittingError < fittingErrorMin):
                    fittingErrorMin = fittingError
                    bestFitNeckRadius = neckRadius  
                    bestFitProfRadius = profRadius
                    bestFitProfile = fitProfile
                    goodProfileFound = True
                    print "Profile Found: R1 = %f, R2 = %f, Error = %f" % (neckRadius, profRadius, fittingError)
                else: 
                    if (goodProfileFound):
                        break
            if (goodProfileFound == False):
               break
        print "Best profile found: R1 = %f, R2 = %f, Error = %f" % (bestFitNeckRadius, bestFitProfRadius, fittingErrorMin)
        #Saving results       
        bestFitNeckRadius = ufloat(bestFitNeckRadius, fittingErrorMin) # IMPORTANT!! CHECK HERE IF THE ERROR IS CORRECT!!!
        bestFitProfRadius = ufloat(bestFitProfRadius, fittingErrorMin)   
        #Saving fitting profile
        with open("./analysis/8pk%s/moviment-%s/fitting/ASbridge-fitting-k%s-moviment%s-%s-0.dat" % 
                           ( sys.argv[1], sys.argv[2], sys.argv[1], sys.argv[2], sys.argv[3]), "w") as fileBestFit:
            fileBestFit.write("#Rho\t Z\n")
            for i in range(len(bestFitProfile[1])):
                fileBestFit.write("%f\t%f\n" % (bestFitProfile[1][i], bestFitProfile[0][i])) #I am printing ZxRho to be like the file AS-bridge-profileDM-2000000-0.dat
        fileBestFit.close()
        #Calculating and saving fitting parameters
        for i in range(len(bestFitProfile[0])):
            bestFitProfile[0][i] = ufloat(bestFitProfile[0][i], fittingErrorMin)
            bestFitProfile[1][i] = ufloat(bestFitProfile[1][i], fittingErrorMin)
        Volume, AreaRev = AlgVol(bestFitProfile[0], bestFitProfile[1])
        AreaBase = 2*np.pi*bestFitProfile[0][-1]**2
        bestFitH = H(bestFitNeckRadius, bestFitProfRadius)# IMPORTANT!! CHECK HERE IF THE ERROR IS CORRECT!!! Then, the error on the pressure should be constant
        if(polk > 0.35):
            XXX =  abs(bestFitH*(bestFitProfile[0][-1]**2 - bestFitNeckRadius**2) + bestFitNeckRadius)
            Theta = 180.0/math.pi*umath.atan(XXX/umath.sqrt(bestFitProfile[0][-1]**2 - XXX**2))
        else:
            XXX =  abs(bestFitH*(bestFitProfile[0][-1]**2 - bestFitNeckRadius**2) + bestFitNeckRadius)
            Theta = 180.0 - 180.0/math.pi*umath.atan(XXX/umath.sqrt(bestFitProfile[0][-1]**2 - XXX**2))
        forceOverGammaBase = ((bestFitProfile[0][-1]*umath.sin(umath.radians(Theta))) - bestFitH*bestFitProfile[0][-1]**2)*2*np.pi	
        forceOverGammaNeck = (bestFitNeckRadius - bestFitH*bestFitNeckRadius**2)*2*np.pi

        
        with open("./analysis/8pk%s/moviment-%s/fitting/parameters-ASbridge-fitting-k%s-moviment%s-%s-0.dat" % 
                   ( sys.argv[1], sys.argv[2], sys.argv[1], sys.argv[2], sys.argv[3]), "w") as fileBestFitParameters:
            fileBestFitParameters.write("#1-TouchHeight"                                    +
                                        "\t2-TouchtRho\t3-ErrTouchtRho"                     +
                                        "\t4-Theta\t5-ErrTheta"                             +
                                        "\t6-Volume\t7-ErrVolume"                           +
                                        "\t8-AreaRev\t9-ErrAreaRev"                         +
                                        "\t10-AreaBase\t11-ErrAreaBase"                     +
                                        "\t12-rhoNeck\t13-ErrrhoNeck"                       +
                                        "\t14-RadiusProfile\t15-ErrRadiusProfile"           +
                                        "\t16-H\t17-ErrH"                                   +
                                        "\t18-ForceNeckOverGamma\t19-ErrForceNeckOverGamma" +
                                        "\t20-ForceBaseOverGamma\t21-ErrForceBaseOverGamma" +
                                        "\t22-ErrorFitting\t((k=" + str(polk) + "\th/2=" + str(dSurface) +"))\n")
            fileBestFitParameters.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%f\n" %
                                       (bestFitProfile[1][-1].n,
                                        bestFitProfile[0][-1].n, bestFitProfile[1][-1].s,
                                        Theta.n, Theta.s,
                                        Volume.n, Volume.s,
                                        AreaRev.n, AreaRev.s,
                                        AreaBase.n, AreaBase.s,
                                        bestFitNeckRadius.n, bestFitNeckRadius.s,
                                        bestFitProfRadius.n, bestFitProfRadius.s,
                                        bestFitH.n, bestFitH.s,
                                        forceOverGammaNeck.n, forceOverGammaNeck.s,
                                        forceOverGammaBase.n, forceOverGammaBase.s,
                                        fittingErrorMin))
            fileBestFitParameters.close()
    else:    
        print "Fitting of liquid bridge profile z(rho) x rho\n"
        print "Parameters:"
        print "normalized polarization k (0.0, 0.1, ... 0.65):"
        print "moviment"
        print "tave"
        print "half height"

if __name__ == "__main__": main()

