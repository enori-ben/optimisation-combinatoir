import ply.yacc as yacc
import numpy as np
import math
from tsp.tsp_lexer import tokens



adj_matrix = None
coordination_matrix = None
infinity = math.inf
instance_name = None

def compute_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def p_tsp(p):
    'tsp : definition_section coordination_section end_of_file'

    global adj_matrix
    global coordination_matrix

    # setting the distance between two cities that have no edge to infinity
    for i in range(adj_matrix.shape[0]):
        for j in range(adj_matrix.shape[1]):
            if adj_matrix[i][j] == 0:
                adj_matrix[i][j] = infinity

    p[0] = { "name" : instance_name, "adj_mat" : adj_matrix, "coordination_mat" : coordination_matrix}

def p_definition_section(p):
    'definition_section : NAME DIMENSION NUMBER'

    dimension = int(p[3])

    if dimension > 3000:
        raise ValueError(f"ABORT: Dimension {dimension} is too large!")

    global adj_matrix
    global coordination_matrix
    global instance_name

    instance_name = p[1] 
    adj_matrix = np.zeros((int(p[3]), int(p[3])))
    coordination_matrix = np.zeros((int(p[3]), 3))

def p_coordination_section(p):
    'coordination_section : COORDINATION_SECTION coordination'

def p_coordination(p):
    'coordination : NUMBER NUMBER NUMBER coordination'

    global adj_matrix
    global coordination_matrix

    coordination_matrix[int(p[1])-1][0] = p[2]
    coordination_matrix[int(p[1])-1][1] = p[3]

    adj_matrix[int(p[1])-1][int(p[1])-1] = infinity

    for i in range(int(p[1]), adj_matrix.shape[1]):
        distance = compute_distance(tuple(coordination_matrix[i]),
                                                      (p[2], p[3]))
        
        adj_matrix[int(p[1]) - 1][i] = distance

        # By symmetry of the matrix
        adj_matrix[i][int(p[1]) - 1] = distance


def p_empty_coordination(p):
    'coordination : empty'

def p_empty(p):
    'empty :'

def p_end_of_file(p):
    '''end_of_file : EOF
                   | empty'''

# Build the parser
parser = yacc.yacc()