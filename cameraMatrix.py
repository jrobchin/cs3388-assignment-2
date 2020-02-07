from math import *
import numpy as np
from matrix import matrix

class cameraMatrix:

    def __init__(self,UP,E,G,nearPlane=10.0,farPlane=50.0,width=640,height=480,theta=90.0):
        __Mp = self.__setMp(nearPlane,farPlane)
        __T1 = self.__setT1(nearPlane,theta,width/height)
        __S1 = self.__setS1(nearPlane,theta,width/height)
        __T2 = self.__setT2()
        __S2 = self.__setS2(width,height)
        __W2 = self.__setW2(height)

        self.__UP = UP.normalize()
        self.__N = (E - G).removeRow(3).normalize()
        self.__U = self.__UP.removeRow(3).transpose().crossProduct(self.__N.transpose()).normalize().transpose()
        self.__V = self.__N.transpose().crossProduct(self.__U.transpose()).transpose()
        self.__Mv = self.__setMv(self.__U,self.__V,self.__N,E)
        self.__C = __W2*__S2*__T2*__S1*__T1*__Mp
        self.__M = self.__C*self.__Mv

    def __setMv(self,U,V,N,E):

        R_inv = matrix(np.array([
            U.transpose().getArray()[0],
            V.transpose().getArray()[0],
            N.transpose().getArray()[0],
            np.array([0, 0, 0]),
        ]))
        R_inv = R_inv.insertColumn(3, [0, 0, 0, 1])

        T_inv = matrix(np.array(np.identity(3)))
        T_inv = T_inv.insertRow(3, np.array([0, 0, 0]))
        T_inv = T_inv.insertColumn(3, -E.getArray().T)
        T_inv.set(3, 3, 1)

        __Mv = R_inv * T_inv

        return __Mv

    def __setMp(self,nearPlane,farPlane):

        N = nearPlane
        F = farPlane

        b = (-2*F*N) / (F-N)
        a = (N+b) / N

        __Mp = np.array([
            [N, 0, 0, 0],
            [0, N, 0, 0],
            [0, 0, a, b],
            [0, 0, -1, 0],
        ])
   
        return matrix(__Mp)

    def __setT1(self,nearPlane,theta,aspect):
        N = nearPlane

        t = N * tan((pi / 180) * (theta / 2))
        b = -t
        r = aspect * t
        l = -r

        __T1 = matrix(np.identity(3))
        __T1 = __T1.insertRow(3, np.zeros((1, 3)))
        __T1 = __T1.insertColumn(3, np.array([
            -(r+l)/2, -(t+b)/2, 0, 1
        ]))

        return __T1

    def __setS1(self,nearPlane,theta,aspect):
        
        N = nearPlane

        t = N * tan((pi / 180) * (theta / 2))
        b = -t
        r = aspect * t
        l = -r

        __S1 = np.array([
            [2/(r-l), 0, 0, 0],
            [0, 2/(t-b), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        return matrix(__S1)

    def __setT2(self):

        __T2 = matrix(np.identity(4))
        __T2.set(0, 3, 1)
        __T2.set(1, 3, 1)

        return __T2

    def __setS2(self,width,height):

        __S2 = matrix(np.identity(4))
        __S2.set(0, 0, width/2)
        __S2.set(1, 1, height/2)

        return __S2

    def __setW2(self,height):
        
        __W2 = matrix(np.identity(4))
        __W2.set(1, 1, -1)
        __W2.set(1, 3, height)
 
        return __W2

    def worldToViewingCoordinates(self,P):
        return self.__Mv*P

    def viewingToImageCoordinates(self,P):
        return self.__C*P

    def imageToPixelCoordinates(self,P):
        return P.scalarMultiply(1.0/P.get(3,0))

    def worldToImageCoordinates(self,P):
        return self.__M*P

    def worldToPixelCoordinates(self,P):
        return self.__M*P.scalarMultiply(1.0/(self.__M*P).get(3,0))

    def getUP(self):
        return self.__UP

    def getU(self):
        return self.__U

    def getV(self):
        return self.__V

    def getN(self):
        return self.__N

    def getMv(self):
        return self.__Mv

    def getC(self):
        return self.__C

    def getM(self):
        return self.__M
