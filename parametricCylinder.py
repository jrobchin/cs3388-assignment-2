from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricCylinder(parametricObject):

    def __init__(self,
                 T=matrix(np.identity(4)),
                 height=1.0,
                 radius=1.0,
                 color=(0,0,0),
                 reflectance=(0.0,0.0,0.0),
                 uRange=(0.0,0.0),
                 vRange=(0.0,0.0),
                 uvDelta=(0.0,0.0)):
        super().__init__(T,color,reflectance,uRange,vRange,uvDelta)
        
        self.__height = height
        self.__radius = radius

    def getPoint(self,u,v):
        __P = matrix(np.array([
            [self.__radius*cos(v)],
            [self.__radius*sin(v)],
            [self.__height*u],
            [1]
        ]))
        return __P
    
    def getRadius(self):
        return self.__radius
    
    def getHeight(self):
        return self.__height