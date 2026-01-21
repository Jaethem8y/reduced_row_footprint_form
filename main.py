import sys
import numpy as np
from pathlib import Path

from flows import createMatrix, matrixElimination
from footprint import rrff


Cpfinal = None
Cmfinal = None

M = None
N = None

def test(basis, C):
    for base in basis:
        res = base @ C
        for i in range(res.shape[0]):
            if res[i] != 0:
                print("Test Failed")
                print(base)
                break


def computeiRank(mat):
    iRank = 0
    m,n = mat.shape

    # print("shape of matrix: m:", m, "n:", n)
    for i in range(m):
        first = -1
        prev = 0
        for j in range(n):
            if prev == 0 and mat[i][j] != 0:
                first = j
                break
            prev = mat[i][j]

        if first == -1:
            print("Error lambda is -1")
            sys.exit(1)

        last = -1
        prev = 0
        for j in range(M-1, -1, -1):
            if prev == 0 and mat[i][j] != 0:
                last = j
                break
            prev = mat[i][j]

        if last == -1:
            print("Error tau is -1")
            print(mat[i])

            sys.exit(1)

        iRank += last - first
    return iRank

def getRRFF(mat):
    # Augmented matrix to solve 
    aug = np.hstack((mat,np.eye(M, dtype=int))).tolist()

    basis = matrixElimination(aug, M, N)
    test(basis, mat)
    # print("basis shape: ", basis.shape)
    
    new = rrff(basis)
    test(new, mat)
    # print("new shape: ", new.shape)

    return new

def randomPermMatrix():
    perm = np.random.permutation(N)
    P = np.eye(N, dtype=int)[perm]
    return P

def simmulatedAnnealing(cp0, cm0, p0):
    cp1 = (p0@cp0)
    cm1 = (p0@cm0)

    T = computeiRank(getRRFF(cp1 + cm1))
    
    mincp = cp1
    mincm = cm1

    currMIN = T
    print(f"initial irank: {T}")
    origT = T
    while True:
        thresh = 0
        deltaT = 0
        while True:
            # swap two variables
            i,j = np.random.choice(M, size=2, replace=False) 

            cp2 = cp1.copy()      
            cm2 = cm1.copy()
            cp2[[i,j]] = cp2[[j,i]]
            cm2[[i,j]] = cm2[[j,i]]

            E1 = computeiRank(getRRFF(cp1 + cm1))
            E2 = computeiRank(getRRFF(cp2 + cm2))

            # print(f"rref equal? : {np.array_equal(getRRFF(cp1 + cm1), getRRFF(cp2 + cm2))}")

            delta = E2 - E1

            prob = np.exp(-delta / (T))

            if delta < 0:
                cp1 = cp2
                cm1 = cm2
                thresh += 1
                if currMIN > E2:
                    currMIN = E2
                    mincp = cp1
                    mincm = cm1
                    print("currMin:", currMIN)

            # elif np.random.rand() < prob:
            #     cp1 = cp2
            #     cm1 = cm2
            #     thresh += 1
                
            if (thresh > 100): 
                break
        T -= T * (1/100)
        
        print(f"min: {currMIN}; T: {T}")
        # print(f"min: {check}; T: {T}")

        if (T < 1): break
    return mincp, mincm

def createFile(filename, cp, cm, marking):
    out = Path(filename).stem

    with open(f"txt/{out}.txt", "w") as f:
        f.write("initial-marking\n")
        for i in range(len(marking)):
            f.write(f"{marking[i]} ")
        f.write("\n")
        cp_t = cp.T
        cm_t = cm.T

        m,n = cp_t.shape
        for i in range(m):
            f.write("transition\n")
            # this is input
            for j in range(n):
                if cm_t[i][j] != 0:
                    f.write("1 ")
                else:
                    f.write("0 ")
            f.write("\n")
            # this is output
            for j in range(n):
                if cp_t[i][j] != 0:
                    f.write("1 ")
                else:
                    f.write("0 ")
            f.write("\n")
        f.write("done")
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <xml_file>")
        return
    
    global M, N
    # This is incident matrix
    # Cp and Cm are M x N matrices M = |P|, N = |T|
    Cp, Cm, M, N, initialMarking = createMatrix(sys.argv[1])

    # print(M, N)
    # getRRFF(Cp + Cm)
    # computeiRank(getRRFF(Cp + Cm))

    perm = np.random.permutation(M)
    I = np.eye(M, dtype=int)
    P = I[perm]

    # print(computeiRank(getRRFF(Cp+Cm)))

    # simmulatedAnnealing(Cp, Cm, P)
    # cp_o, cm_o = simmulatedAnnealing(Cp, Cm, I)

    # createFile(sys.argv[1], cp_o, cm_o, initialMarking)
    print(M, N)
    createFile(sys.argv[1], Cp, Cm, initialMarking)
    
    # rrff = getRRFF(Cp + Cm)

    # iRank = computeiRank(rrff)
    # print(iRank)
    # print(M, N)


if __name__ == "__main__":
    main()
    
    