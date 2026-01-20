import numpy as np
import math

def leading(row):
    for i,v in enumerate(row):
        if v != 0:
            return i
    return -1

#----------------------------------------------------------------------------------
def trailing(row):
    for i,v in reversed(list(enumerate(row))):
        if v != 0:
            return i
    return -1

#----------------------------------------------------------------------------------
def is_negative(i):
    return i<0

#----------------------------------------------------------------------------------
# GCD of a python list. Note that in Python math.gcd(x,0) == x
def gcd_list_abs(lst, i=0):
    if i==len(lst):  
        return 0
    return math.gcd(abs(lst[i]), gcd_list_abs(lst, i+1))
    
#----------------------------------------------------------------------------------
def canonicalize(row):
    if np.count_nonzero(row) > 0:
        l = leading(row)
        row = -row if row[l] < 0 else row
        row = row / gcd_list_abs(row)
    return row

#----------------------------------------------------------------------------------
# replace row i with a linear combination of both row i and k s.t. B[i,j] becomes 0
def annul_column(B, i, k, j):
    assert B[i,j] != 0 and B[k,j] != 0
    mult_k = abs(B[i,j])
    mult_i = abs(B[k,j])
    gcd_ik = math.gcd(mult_k, mult_i)
    mult_k /= gcd_ik
    mult_i /= gcd_ik
    # ensure opposing signs
    if is_negative(B[i,j]) == is_negative(B[k,j]):
        mult_k = -mult_k
    # Sum and verify that B[i,j] is 0
    B[i,:] = mult_k * B[k,:] + mult_i * B[i,:]
    assert B[i,j] == 0, repr(B[i,j])
    # canonicalize
    B[i,:] = canonicalize(B[i,:])
    
#----------------------------------------------------------------------------------
# reduced row footprint form
def rrff(A): 
    B = np.copy(A)
    for k in range(len(B)):
        # Find the k-th pivot row
        i_max = k
        for i in range(k, len(B)):
            if (np.count_nonzero(B[i_max,:]) == 0 or
                (np.count_nonzero(B[i,:]) > 0 and
                 leading(B[i,:]) < leading(B[i_max,:]))):
                i_max = i
        #  Move the pivot in position k
        if k != i_max: # swap pivot row with row k
            B[k,:], B[i_max,:] = B[i_max,:], B[k,:]
        # Annul column j0 to all the rows below the pivot (row k)
        if np.count_nonzero(B[k,:]) > 0:
            j0 = leading(B[k,:])
            for i in range(k+1, len(B)): # Get into a row-echelon form
                if B[i,j0] != 0:
                    annul_column(B, i, k, j0)
    # Step 2: Find row-trailing entries and annul all entries above each of them. 
    for k in reversed(range(len(B))):
        # Annul the last column of B[k] to all the rows above the pivot row k
        if np.count_nonzero(B[k,:]) > 0:
            jN = trailing(B[k,:])
            for i in reversed(range(k)): # get into footprint form
                if B[i,jN] != 0:
                    annul_column(B, i, k, jN)
    return B

# tabulate matrix, highlighting the footprint form.
def tab(A):
    for row in range(A.shape[0]):
        lead, trail = leading(A[row,:]), trailing(A[row,:])
        for col in range(A.shape[1]):
            if A[row,col]!=0: #  lead <= col <= trail: 
                print('%4d' % A[row,col], end='')
            elif lead < col < trail:
                print('   0', end='')                
            else:
                print('   .', end='')
        print()