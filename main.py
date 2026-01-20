import sys
import numpy as np

from flows import createMatrix, matrixElimination
from footprint import rrff

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
    print(f"M: {m}; N: {n}")
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <xml_file>")
        return
    
    global M, N
    # This is incident matrix
    C, M, N = createMatrix(sys.argv[1])

    # Augmented matrix to solve 
    aug = np.hstack((C,np.eye(M, dtype=int))).tolist()

    basis = matrixElimination(aug, M, N)
    new = rrff(basis)
 
    iRank = computeiRank(new)
    print(iRank)



if __name__ == "__main__":
    main()
    
    