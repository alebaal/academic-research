from classProfile import Profiles
import matplotlib.pyplot as plt
import matplotlib
import glob
import numpy as np



class Analysis(Profiles):
    def __init__(self, N, h, L, S, path):
        self.path = path
        Profiles.__init__(self, N, h, L, S)
        self.filesPos = sorted(glob.glob(self.path), key = lambda x: int(filter(str.isdigit, x)) )
        #Analised Profiles
        
    def loop(self):        
        '''Loop to read configurations'''
        if not self.listProfiles:
            count = 0
            for fileConfig in self.filesPos:
                self.addProfile(fileConfig)
#                if(count%1000 == 0):
                print("Analysing " + fileConfig)    
 #               count+=1        
        else:
            print("The configuration files " + self.path + " have already been analysed.")
            
           
    def rotate(self, x, y, radians, origin):
        """Use numpy to build a rotation matrix and take the dot product."""
        offset_x, offset_y = origin
        adjusted_x = (x - offset_x)
        adjusted_y = (y - offset_y)
        cos_rad = np.cos(-radians)
        sin_rad = np.sin(-radians)
        qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
        qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
        return qx, qy
        
    def plotSlab(self, slab, pos, path = None):
        cmap = matplotlib.cm.get_cmap('hsv')
        plt.figure(figsize=(10,10))
        plt.ylim(-self.L/2,self.L/2)
        plt.xlim(-self.L/2,self.L/2)

        arc = 2
        R = np.arange(0,arc*np.pi, 0.01)
        center = self.listProfiles[pos][slab].center
        phi = self.listProfiles[pos][slab].rotation1
        axes = self.listProfiles[pos][slab].axis_length

        a, b = axes
        xx = center[0] + a*np.cos(R)*np.cos(phi) - b*np.sin(R)*np.sin(phi)
        yy = center[1] + a*np.cos(R)*np.sin(phi) + b*np.sin(R)*np.cos(phi)

        #all points
        plt.scatter(self.listProfiles[pos][slab].slab[:,0], self.listProfiles[pos][slab].slab[:,1],  color='grey', s=10, marker='o', label = 'All points from slab')
        #slab profile
        plt.scatter(self.listProfiles[pos][slab].x, self.listProfiles[pos][slab].y,  color='b', s=20, marker='o', label = 'Boarder from slab')
        #Center
        plt.scatter(center[0], center[1],  color='r', s=40, marker='o', label = 'Center Ellipse')
        
        ellipse_axis1x = np.arange(center[0], center[0] + axes[0], 0.0001)
        ellipse_axis1y = np.full((len(ellipse_axis1x)), center[1])    
        ellipse_axis1x, ellipse_axis1y =  self.rotate(ellipse_axis1x, ellipse_axis1y, phi, center)
        plt.plot(ellipse_axis1x, ellipse_axis1y, label = 'Smaller axis (%f)' % (axes[0]), color = 'navy', alpha = 0.5, linewidth=2.0)
        
        ellipse_axis2x = np.arange(center[0], center[0] + axes[1], 0.0001)
        ellipse_axis2y = np.full((len(ellipse_axis2x)), center[1])    
        ellipse_axis2x, ellipse_axis2y =  self.rotate(ellipse_axis2x, ellipse_axis2y, phi + np.pi/2, center)
        plt.plot(ellipse_axis2x, ellipse_axis2y, label = 'Larger axis (%f)' % (axes[1]) , color = 'navy', linewidth=2.0)
        
        #plt.plot(pointsCH[hull.vertices[0],0], pointsCH[hull.vertices[0],1], 'ro')
        plt.plot(xx,yy, color = 'r', label = 'Fitting')
        plt.title('Fitting of slab %d at the config %d000000.pos\n Slab area found: %f' % (slab, pos, self.listProfiles[pos][slab].area))
        plt.legend()    
        if path is None:
            plt.savefig('./find_ellipse_All_profile_s' + str(slab) + 'p' + str(pos) + '.png')
        else: 
            plt.savefig( path + 'find_ellipse_All_profile_s' + str(slab) + 'p' + str(pos) + '.png')
            
            
        plt.close()    
        
        
    def plotPar(self):        

        nMolsSlab = {'base':list(), 'top':list()}
        areaSlab = {'base':list(), 'top':list()}
        length_s = {'base':list(), 'top':list()}
        length_l = {'base':list(), 'top':list()}
        
        for i in self.listProfiles:
            nMolsSlab['base'].append(i[-1].nmol)
            areaSlab['base'].append(i[-1].area) 
            nMolsSlab['top'].append(i[0].nmol)
            areaSlab['top'].append(i[0].area) 
            length_s['base'].append(i[-1].axis_length[0])
            length_l['base'].append(i[-1].axis_length[1])
            length_s['top'].append(i[0].axis_length[0])
            length_l['top'].append(i[0].axis_length[1])
            
        
        f, ax = plt.subplots(2, 2,figsize=(20,20))
        ax[0][0].plot(range(len(nMolsSlab['base'])),nMolsSlab['base'], label = 'base', color = 'k')
        ax[0][0].plot(range(len(nMolsSlab['top'])),nMolsSlab['top'], label = 'top', color = 'r')
        ax[0][0].set_ylabel('nMolecules')
        ax[0][0].set_xlabel('time (1000 fs)')
        ax[0][0].legend(loc = 'upper right')
        
        ax[0][1].plot(range(len(areaSlab['base'])), areaSlab['base'], label = 'base', color = 'k')
        ax[0][1].plot(  range(len(areaSlab['top'])), areaSlab['top'], label = 'top', color = 'r')
        ax[0][1].set_ylabel('Area')
        ax[0][1].set_xlabel('time (1000 fs)')
        ax[0][1].legend(loc = 'upper right')        
        
        ax[1][0].plot(range(len(length_s['base'])),  length_s['base'],  label  ='Smallest radius', color = 'k')
        ax[1][0].plot(  range(len(length_l['base'])), length_l['base'], label  ='Largest  radius', color = 'r')
        ax[1][0].set_ylabel('Ellipse radii on base')
        ax[1][0].set_xlabel('time (1000 fs)')
        ax[1][0].legend(loc = 'upper right')        
        
        ax[1][1].plot(range(len(length_s['top'])),   length_s['top'], label  ='Smallest radius', color = 'k')
        ax[1][1].plot(range(len(length_l['top'])),   length_l['top'], label  ='Largest  radius', color = 'r')
        ax[1][1].set_ylabel('Ellipse radii on top')
        ax[1][1].set_xlabel('time (1000 fs)')
        ax[1][1].legend(loc = 'upper right')        
        
        plt.savefig('./analysisAreaAndNumWaterMolecules.png')
#         for i in range(len(fitEllipseProfile) ):
#         #for i in [0]:
#             arc = 2
#             R = np.arange(0,arc*np.pi, 0.01)
#             center = ellipse_center(fitEllipseProfile[i])
#             phi = ellipse_angle_of_rotation2(fitEllipseProfile[i])
#             axes = ellipse_axis_length(fitEllipseProfile[i])

#             a, b = axes
#             xx = center[0] + a*np.cos(R)*np.cos(phi) - b*np.sin(R)*np.sin(phi)
#             yy = center[1] + a*np.cos(R)*np.sin(phi) + b*np.sin(R)*np.cos(phi)

#             plt.scatter(pointsProfile[i][:, 0], pointsProfile[i][:, 1],  color='grey', s=10, marker='o')
#             plt.scatter(pointsProfile[i][hullData[i].vertices, 0], pointsProfile[i][hullData[i].vertices, 1],  color='b', s=20, marker='o')

#             #plt.plot(pointsCH[hull.vertices[0],0], pointsCH[hull.vertices[0],1], 'ro')
#             plt.plot(xx,yy, color = cmap(i/10), label = 'slab %d' % (i))
#         plt.legend()    
#         plt.savefig('./find_ellipse_All_profile2.png')


    def savePar(self):         
        writeFileArea         = open("./Area.dat", 'w')
        writeFileNumMol       = open("./Nmol.dat", 'w')
        count = 0
        for profile in self.listProfiles:
            writeFileArea.write("%d\t" % (count))
            writeFileNumMol.write("%d\t" % (count))
            for slab in profile:
                writeFileArea.write("%f\t" % (slab.area))
                writeFileNumMol.write("%f\t" % (slab.nmol))
            writeFileArea.write("\n")
            writeFileNumMol.write("\n")   
            count+=1
        writeFileArea.close()
        writeFileNumMol.close()
