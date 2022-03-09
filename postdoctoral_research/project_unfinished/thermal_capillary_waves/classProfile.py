import numpy as np
from classSlab import Slab

class Profiles():
    def __init__(self, N, h, L, S):
        #total Water molecules
        self.N = N
        #height        
        self.h = h
        #Simulation Box
        self.L = L
        #Slab thickness
        self.S = S
        #water density box        
#        self.rho = np.zeros((int(self.h/self.S), int(self.L/self.S), int(self.L/self.S))) Not in use, check
        self.listProfiles = []
        self.Oatoms = None
        
    def addProfile(self, path):
        self.getOxygenPos(path) 
        self.correctBoardEffect()
        self.removeOutMolecules()
        self.listProfiles.append(self.findProfile()) 
         
    def getOxygenPos(self, file): 
        '''
        sets the Oxigen positions
        '''
        rawData = np.genfromtxt(file,dtype="float",skip_header=9)
        self.Oatoms = rawData[np.where(rawData[:,1]==2)][:,2:] 

    def getsCM(self, mols):
        '''
        Calculates the Center of Mass
        '''
        return np.sum(mols, axis=0)/self.N

    def correctBoardEffect(self):
        '''
        Fix the boarder problem and calculate the CM
        '''
        
        OatomsFix = self.Oatoms
        CM = self.getsCM(OatomsFix)
        OatomsFix[:,1:] -= CM[1:]
      
        Oatoms_out_index  = np.where(abs(OatomsFix[:,1]) > self.L/2)
        Oatoms_out_index2 = np.where(OatomsFix[Oatoms_out_index][:,1] > 0)      
        OatomsFix[Oatoms_out_index[0][Oatoms_out_index2],1] -= self.L 
        Oatoms_out_index  = np.where(abs(OatomsFix[:,1]) > 140/2)
        Oatoms_out_index3 = np.where(OatomsFix[Oatoms_out_index][:,1] < 0)
        OatomsFix[Oatoms_out_index[0][Oatoms_out_index3],1] += self.L 

        Oatoms_out_index  = np.where(abs(OatomsFix[:,2]) > self.L/2)
        Oatoms_out_index2 = np.where(OatomsFix[Oatoms_out_index][:,2] > 0)      
        OatomsFix[Oatoms_out_index[0][Oatoms_out_index2],2] -= self.L 
        Oatoms_out_index  = np.where(abs(OatomsFix[:,2]) > 140/2)
        Oatoms_out_index3 = np.where(OatomsFix[Oatoms_out_index][:,1] < 0)
        OatomsFix[Oatoms_out_index[0][Oatoms_out_index3],2] += self.L 
        
        OatomsFix[:,1:] += CM[1:]
        CM = self.getsCM(OatomsFix)
        OatomsFix[:,1:] -= CM[1:]

        #CM = self.getsCM() #Check this line. Maybe it is before Oatoms
        self.Oatoms = OatomsFix


    def removeOutMolecules(self):
        '''
        Remove water molecules out from bridge
        '''
        mask = np.sqrt(np.sum(self.Oatoms[:, 1:]**2, axis=1)) > 30.0
        self.Oatoms = self.Oatoms[~mask]


    def findProfile(self):
        '''
        Fitting a ellipse for each profile
        '''
        #get atoms position from histogram
        hist_count, bins_edges = np.histogramdd(self.Oatoms, bins =(int(self.h/self.S), int(self.L/self.S), int(self.L/self.S)), range = ((-self.h/2,self.h/2), (-self.L/2,self.L/2), (-self.L/2,self.L/2)))
        bins_posY = (bins_edges[1][1:] - bins_edges[1][:-1])/2 + bins_edges[1][:-1]
        bins_posZ = (bins_edges[2][1:] - bins_edges[2][:-1])/2 + bins_edges[2][:-1]
        grid = []
        for y in bins_posY:
            temp = []
            for z in bins_posZ:
                temp.append([y,z])
            grid.append(temp)
        grid = np.array(grid)    

        pointsProfile = []
        nSlabs = 5
    #Loop: 1) Colappse the O atoms inside 5A slabes into a plane, which is a cross section of the bridge

        for i in range(0,len(hist_count), nSlabs):

            #here I am collapsing five slabs into one
            points_cross_section = np.sum(hist_count[i:i+nSlabs], axis=0)

            #here I am finding the filled cells
            mask = points_cross_section > 0    

            #finding the cells positions and creating points coordinates
            px, py =  np.split(grid[mask], 2, axis = 1)
            px = px.flatten()
            py = py.flatten()
            pointsCH = np.stack((px,py), axis=-1)
            pointsProfile.append(Slab(pointsCH, points_cross_section.sum()))
        return pointsProfile
