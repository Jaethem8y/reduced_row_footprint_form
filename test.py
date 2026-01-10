import numpy as np

M = 0
N = 0
MATRIX = [[]]
BASIS = []

def gcd(a, b):
    if (a == b): return a
    if (a > b): return gcd(a-b, b)
    return gcd(a, b-a)

def lcm(a, b):
    a = abs(a)
    b = abs(b)
    return (a*b) // gcd(a,b)

def cancelByRow(t, update, selected):
    if update == 0: return
    if update[t] == 0: return
    if selected[t] == 0: return
    L = lcm(update[t], selected[t])
    a = L // update[t]
    b = L // selected[t]
    for i in range(M+N):
        update[i] *= a
        update[i] -= b * selected[i]

def normalizeRow(row):
    if 0 == row: return
    g = 0
    numneg = 0
    numpos = 0
    for i in range(N+M):
        if row[i] == 0: continue
        r = None
        if row[i] > 0:
            r = row[i]
            numpos += 1
        else:
            r = -row[i]
            numneg += 1
        g = gcd(g,r) if g else r 
    if (numneg > numpos):
        g = -g
    for i in range(M+N):
        row[i] //= g

def matrixElimination():
    # dumpMatrix(MATRIX)

    for t in range(N):
        row = -1
        for p in range(M-1, -1, -1):
            if (MATRIX[p]):
                if MATRIX[p][t] == 0: continue
                row = p
                break
        
        if row < 0: continue

        for p in range(M):
            if p != row: cancelByRow(t, MATRIX[p], MATRIX[row])
        
        MATRIX[row] = False

        # dumpMatrix(MATRIX)

    for r in range(M):
        normalizeRow(MATRIX[r])

    final = []
    for i in range(M):
        if MATRIX[i]:
            final.append(MATRIX[i])
    
    final = np.array(final)
    final = final[:,-M:]

    global BASIS
    BASIS = final
    
    # dumpMatrix(MATRIX)

def dumpMatrix(matrix):
    for i in range(len(matrix)):
        if not matrix[i]: 
            print("[null]")
        else:
            print("[", end="")
            for j in range(N):
                print(f" {matrix[i][j]} ", end="")
            print(" | ", end="")
            for j in range(N, M+N):
                print(f" {matrix[i][j]} ", end="")
            print("]")
    print()

def main():
    
    global M, N, MATRIX
    M = 6
    N = 3
    MATRIX = [
        [-1,  0,  1,  1, 0, 0, 0, 0, 0],
        [ 1, -1,  0,  0, 1, 0, 0, 0, 0],
        [ 1, -1,  0,  0, 0, 1, 0, 0, 0],
        [ 0,  1, -1,  0, 0, 0, 1, 0, 0],
        [ 0,  1, -1,  0, 0, 0, 0, 1, 0],
        [ 0,  1, -1,  0, 0, 0, 0, 0, 1]
    ]

    matrixElimination()

if __name__ == "__main__":
    main()
    print(BASIS)