import numpy as np
from classEllipse import Ellipse
from scipy.spatial import ConvexHull

class Slab(Ellipse):
    def __init__(self, slab, nmol):
        self.slab = slab
        self.nmol = nmol
        self.hull = ConvexHull(self.slab, qhull_options='Qi')
        self.hullPoints = self.slab[self.hull.vertices]
        Ellipse.__init__(self, self.hullPoints[:,0], self.hullPoints[:,1])
  