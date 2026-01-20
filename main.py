import sys
import numpy as np

from flows import createMatrix, matrixElimination
from footprint import rrff


def test(basis, C):
    for base in basis:
        res = base @ C
        for i in range(res.shape[0]):
            if res[i] != 0:
                print("Test Failed")
                print(base)
                break

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <xml_file>")
        return
    
    # This is incident matrix
    C, M, N = createMatrix(sys.argv[1])

    # Augmented matrix to solve 
    aug = np.hstack((C,np.eye(M, dtype=int))).tolist()

    basis = matrixElimination(aug, M, N)
    test(basis, C)
    new = rrff(basis)
    test(new, C)
    print(f"Num places: {M}; Num transition: {N}")
    print(f"basis shape: {basis.shape}")
    print(f"fp shape: {new.shape}")


if __name__ == "__main__":
    main()
    
    