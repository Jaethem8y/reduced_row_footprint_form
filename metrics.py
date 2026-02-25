#This is the file where I will encode all of the metrics for variable ordering shtuff.
import os
import pprint
import numpy as np

'''Okay, so now what I need to do is create the methods for some of the petrics, maybe just look at the best ones?'''
'''Soups, PTS, and PTS^p all do the best it seems, maybe focus on those ones?'''
'''In the set of Petrinets used, E is the set of transitions and V is the set of places. When you call
CreateMatrix it outputs the number of events and transitions as M and N'''
'''center of gravity: '''

'''Could we utilize every metric as input to "neural net" and then update it based on the difference between the score
and some other value? So it would take in the values as an array of values and then try to determine what the best heuristic would be?
But then, how does it select the best heuristic/metric?'''

def CenterOfGravity(EventIndex, OutputtIncidencMatrix, InputIncidencMatrix):

    SetofVariable = 0
    LevelSum = 0
    #Since the matrices should both be of the same size the loop limit is arbitrary.
    for row in range(len(InputIncidencMatrix)):
        SetofVariable += OutputtIncidencMatrix[row][EventIndex] + abs(InputIncidencMatrix[row][EventIndex])

        if OutputtIncidencMatrix[row][EventIndex] >= 1 and abs(InputIncidencMatrix[row][EventIndex]) >= 1:
            LevelSum += 2*row 
        elif OutputtIncidencMatrix[row][EventIndex] >= 1 and abs(InputIncidencMatrix[row][EventIndex]) == 0:
            LevelSum += row 
        elif OutputtIncidencMatrix[row][EventIndex] == 0 and abs(InputIncidencMatrix[row][EventIndex]) >= 1:
            LevelSum += row 
        else:
            continue
    
    return (1/SetofVariable)*LevelSum

def HyperPosition(VariableIndex, OutputtIncidencMatrix, InputIncidencMatrix):

    SetofEvents = 0
    COGSum = 0

    for col in range(len(OutputtIncidencMatrix[0])):
        #This is E(v)
        SetofEvents +=  OutputtIncidencMatrix[VariableIndex][col] + abs(InputIncidencMatrix[VariableIndex][col])
        #Now I need to go through an sum up the center of gravity for each column where there is a connection.
        if(OutputtIncidencMatrix[VariableIndex][col] >= 1 or abs(InputIncidencMatrix[VariableIndex][col]) >= 1):
            COGSum += CenterOfGravity(col, OutputtIncidencMatrix, InputIncidencMatrix)
        else:
            continue




    return (1/SetofEvents)*COGSum

def PTS(Cm, Cp):
    #Cm and Cp are matrices that will be passed in. Cm is the representation of states that point to transitions, and Cp is the 
    # representation of the states each transition points to.

    PointTransitionSpan = 0
    
    #for row in Cp:
    #    pprint.pprint(row, width=200)

        #This works for column summation, so that works for one part of V(e), now just add the columns of Cp and Cm.
    #MatrixArrayCp = np.array(Cp)
    #MatrixArrayCm = np.array(Cm)    

    #I think this'll work better instead, then I can just add the abs val from Cm and keep track of what column I am in to acount for level of the variable.                
        
    for col in range(len(Cm[0])):
        for row in range(len(Cm)):
            if(Cm[row][col] >= 1 or Cp[row][col] >= 1):
                PointTransitionSpan += abs(CenterOfGravity(col,Cp,Cm) - HyperPosition(row,Cp,Cm))

    return PointTransitionSpan

def PTS_P(PTSVal,):
    #PTS_P 
    
    return 0

def PSF(PSemiFlowMat):

    SumDif = 0

    #Go through each row in the Psemiflow matrix

    for i in range(len(PSemiFlowMat)):
        max = 0
        min = len(PSemiFlowMat[0])
        for j in range(len(PSemiFlowMat[0])):
            if PSemiFlowMat[i][j] != 0:
                if max < (len(PSemiFlowMat[0]) - j):
                    max = (len(PSemiFlowMat[0]) - j)
                if min > (len(PSemiFlowMat[0]) - j):
                    min = (len(PSemiFlowMat[0]) - j)

        if((max == 0 and min == len(PSemiFlowMat[0])) or (max == min)):
            #Or should this be zero?
            continue

        SumDif += max - min + 1

    return SumDif

def SOUPS():
    
    return 0

def meta_heuristic():

    return 0