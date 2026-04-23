import sys
import numpy as np
from pathlib import Path

from flows import createMatrix, matrixElimination
from footprint import rrff


Cpfinal = None
Cmfinal = None

M = None
N = None


def createFile(filename, cp, cm, marking, outdir):
    out = Path(filename).stem

    with open(f"/Users/jaehyeokchoi/Desktop/pns/{outdir}/{out}.txt", "w") as f:
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
                    f.write(f"{j} ")
            f.write("\n")
            # this is output
            for j in range(n):
                if cp_t[i][j] != 0:
                    f.write(f"{j} ")
            f.write("\n")
        f.write("done")
def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <xml_file> <out_dir>")
        return
    
    global M, N
    Cp, Cm, M, N, initialMarking = createMatrix(sys.argv[1])

    createFile(sys.argv[1], Cp, Cm, initialMarking, sys.argv[2])

if __name__ == "__main__":
    main()
    
    
