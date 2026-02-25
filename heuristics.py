#This is the file where I will put the  Gradient, FORCE, SLOAN, TOV/NOACK heuristic algorithms.
import numpy as np
import math
from metrics import PSF

def Gradient():

    return 0


def FORCE():

    return 0

def SLOAN():

    return 0

def ExpPSemiFlows(Cm, Cp):
    #So, if I am reading this right, I need to combine the two incidence matrices and then 
    #construct an identity matrix. From there I can repeat the operations from the algorithm and create
    #matrice T and P and derive the P-semiflows from there.

    #Iterate through the size of the incidence matrix
    IncMat = np.add(Cp, Cm)

    IdentityMat = np.identity(len(Cp))

    AMat = np.hstack((IncMat, IdentityMat))

    AMatPos = np.empty((0,13))

    AMatNeg = np.empty((0,13))

    for i in range(len(Cm[0])):
        j = 0

        #I think I need to reset the values for AMatPos and AMatNeg
        AMatPos = np.empty((0,13))

        AMatNeg = np.empty((0,13))

        while j < len(AMat):
            
            if AMat[j][i] > 0 and j > 0:
                #add row to 
                AMatPos = np.vstack((AMatPos, AMat[j]))
                #Now remove the row from AMat, I think this should actually not be (0), since this 
                # just deletes the first row in the matrix, but it might not be the first row.
                AMat = np.delete(AMat, j, axis=0)
                j -= 1
                
            elif AMat[j][i] > 0 and j == 0 :
                #add row to 
                AMatPos = np.vstack((AMatPos, AMat[j]))
                #Now remove the row from AMat
                AMat = np.delete(AMat, j, axis=0)
                j = 0
                continue

            if AMat[j][i] < 0  and j > 0:
                #add row to 
                AMatNeg = np.vstack((AMatNeg, AMat[j]))
                #Now remove the row from AMat
                AMat = np.delete(AMat, j, axis=0)
                j -= 1

            elif AMat[j][i] < 0 and j == 0:
                 #add row to 
                AMatNeg = np.vstack((AMatNeg, AMat[j]))
                #Now remove the row from AMat
                AMat = np.delete(AMat, j, axis=0)
                j = 0
                continue

            j += 1
        #This is where I want to then compare each pairing of rows from A_N and A_P
        for l in range(len(AMatNeg)):
            for k in range(len(AMatPos)):

                v = abs(int(AMatNeg[l][i]*AMatPos[k][i]))  // math.gcd(-int(AMatNeg[l][i]),int(AMatPos[k][i]))

                AddedRow = (-v/AMatNeg[l][i])*AMatNeg[l] + (v/AMatPos[k][i])*AMatPos[k]

                AMat = np.vstack((AMat, AddedRow))

    AMat  = AMat[:, len(IncMat[0]):]
    return AMat

def main():

    #Create the positive and negative flow matrices here, maybe test some stuff out and see what works.
    #These are based off of the example in Ciardo's paper, so they should return the P_final?
    Cm = [[0,-1,0,0,0,0],[0,0,-1,0,0,0],[-1,0,0,0,0,0],[0,0,0,0,-1,0],[0,0,0,0,0,-1],[0,0,0,-1,0,0],[-1,0,0,-1,0,0]]


    Cp = [[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1],[0,0,1,0,0,1]]

    print(PSF(ExpPSemiFlows(Cm, Cp)))


if __name__ == "__main__":
    main()