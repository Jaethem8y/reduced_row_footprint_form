import xml.etree.ElementTree as ET
import numpy as np
import sys

M = None
N = None

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

def matrixElimination(aug, m, n):
    global M,N

    M = m
    N = n

    for t in range(N):
        row = -1
        for p in range(M-1, -1, -1):
            if (aug[p]):
                if aug[p][t] == 0: continue
                row = p
                break
        
        if row < 0: continue

        for p in range(M):
            if p != row: cancelByRow(t, aug[p], aug[row])
        
        aug[row] = False

    for r in range(M):
        normalizeRow(aug[r])

    final = []
    for i in range(M):
        if aug[i]:
            final.append(aug[i])
    
    final = np.array(final)
    return final[:,-M:]


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

def createMatrix(filename):
    # Parse PNML file
    try:
        # tree = ET.parse(root + filename)
        tree = ET.parse(filename)

        root = tree.getroot()

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
                initial_markings.append(1)
            else:
                initial_markings.append(0)
            
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
        
        global M, N
        M = num_places
        N = num_transitions

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
        
        return Cp, Cm, M, N, initial_markings
    
    except Exception as e:
        print("Error creating Matrix:", e)
        sys.exit(1)