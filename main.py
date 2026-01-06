import numpy as np
from scipy.linalg import null_space

import math
import sys
import xml.etree.ElementTree as ET
import os
import pprint

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

def example():
    print("Example 1 :")
    print("Original: ")
    A = np.array([
        [ 1,  0,  0,  1,  0,  0,  1],
        [ 1,  0,  0,  0,  1,  1,  1],
        [ 0,  1,  1,  1,  0,  0,  1],
        [ 0,  1,  1,  0,  1,  1,  1]
    ])
    print(A)
    print()
    print("transformed: ")
    tab(rrff(A))

    print("------------------------------")
    print("Example 2:")
    print("Original: ")
    A = np.array([
        [ 5,  0,  0,  2,  0,  0,  1],
        [ 1,  0,  0,  0,  1,  2,  1],
        [ 0,  2,  2,  1,  0,  0,  3],
        [ 0,  3,  2,  0,  1,  3,  1]
    ])
    print(A)
    print()
    print("Transformed: ")
    tab(rrff(A))
    print("------------------------------")

# takes an incident matrix (A), |P| (m) and |T| (n)
def algorithm1(A, m, n):
    AT = A.T
    I = np.identity(n, dtype=int)
    k = 1
    l = 1
    print(A)
    for i in range(min(n,m)):
        pivot_row = np.argmax(np.abs(A[i:n,i])) + i

        if A[pivot_row, i] == 0:
            continue
        
        A[[i, pivot_row]] = A[[pivot_row, i]]
        I[[i, pivot_row]] = I[[pivot_row, i]]
        
        for j in range(i + 1, n):
            factor = A[j, i] / A[i, i]
            A[j, i:] -= factor * A[i, i:]
            I[j, :] -= factor * I[i, :]             
    print("-----------")
    print(A)
    print("-----------")
    print(I)
    print("-----------")   

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <xml_file>")
        return
    
    filename = sys.argv[1]
    root = "/Users/jaehyeokchoi/Desktop/cesr-safe-pnml/"

    # Parse PNML file
    try:
        tree = ET.parse(root + filename)
        root = tree.getroot()

        outfile_name = os.path.basename(filename)

        ns_uri = root.tag.split("}")[0].strip("{")

        # PLACES
        places_nodes = root.findall(f".//{{{ns_uri}}}place")        
        places_dic = {}
        initial_markings = []

        num_places = len(places_nodes)

        for i in range(0, len(places_nodes)):
            places_dic[places_nodes[i].get("id")] = i + 1
            
            initial_marking_node = places_nodes[i].find(f"{{{ns_uri}}}initialMarking/{{{ns_uri}}}text")
            initial_marking = initial_marking_node.text if initial_marking_node is not None else None
            if initial_marking is not None:
                initial_markings.append(i+1)

        # Transitions
        transitions_nodes = root.findall(f".//{{{ns_uri}}}transition")
        transitions_dic = {}

        num_transitions = len(transitions_nodes)

        for i in range(0, len(transitions_nodes)):
            transitions_dic[transitions_nodes[i].get("id")] = i + 1 

        # ARCS
        arcs_nodes = root.findall(f".//{{{ns_uri}}}arc")
        # this should have transition as key and input output specified
        input_arc = {}
        output_arc = {}
        Cm = np.zeros((num_places, num_transitions), dtype=int)
        Cp = np.zeros((num_places, num_transitions), dtype=int)
        for i in range(0, len(arcs_nodes)):
            source = arcs_nodes[i].get("source")
            target = arcs_nodes[i].get("target")
            # This is input arc
            if source in places_dic:
                Cm[places_dic[source]-1, transitions_dic[target]-1] -= 1
                if target not in input_arc:
                    input_arc[target] = [source]
                else:
                    input_arc[target].append(source)
  
            # this is output arc
            elif target in places_dic:
                Cp[places_dic[target]-1, transitions_dic[source]-1] += 1
                if source not in output_arc:
                    output_arc[source] = [target]
                else:
                    output_arc[source].append(target)

        C = Cp + Cm

        # This is for output file BRAVE_DD we don't care about this yet
        # file_path = f"{outfile_name}.txt"

        # with open(file_path, "w") as f:
        #     f.write("BDD\n")
        #     f.write(f"numvars: {len(places_nodes)}\n")
        #     f.write(f"initialMarking:\n")
        #     for i in initial_markings:
        #         f.write(f"\t{i}\n")
        #     f.write("BDD-DONE\n")
        #     f.write("RELATIONS\n")
        #     for i in transitions_dic:
        #         if (i not in input_arc) and (i not in output_arc):
        #             print("ERROR")
        #             print(i + " is not in any")
        #             break

        #         f.write("RELATION\n")
        #         f.write("INPUTS\n")
        #         input_open = True
        #         if i in input_arc:
        #             for j in input_arc[i]:
        #                 f.write(f"\t{places_dic[j]}\n")
        #             f.write("INPUTS-DONE\n")
        #             input_open = False
        #         if (input_open):
        #             f.write("INPUTS-DONE\n")


        #         output_open = True
        #         f.write("OUTPUTS\n")
        #         if i in output_arc:
        #             for j in output_arc[i]:
        #                 f.write(f"\t{places_dic[j]}\n")
        #             f.write("OUTPUTS-DONE\n")
        #             output_open = False
        #         if (output_open):
        #             f.write("OUTPUTS-DONE\n")

        #         f.write("RELATION-DONE\n")

        #     f.write("RELATIONS-DONE\n")
    
    
    except Exception as e:
        print("Error reading XML:", e)
        return

if __name__ == "__main__":
    main()
    
    