import ply.yacc as yacc
import numpy as np
import math
from tsp.tsp_lexer import tokens


# =========================================================
# GLOBAL STATE (still used, but safer)
# =========================================================
adj_matrix = None
coord_matrix = None
instance_name = None


# =========================================================
# DISTANCE FUNCTION
# =========================================================
def compute_distance(p1, p2):
    return math.sqrt(
        (p2[0] - p1[0]) ** 2 +
        (p2[1] - p1[1]) ** 2
    )


# =========================================================
# START RULE
# =========================================================
def p_tsp(p):
    """tsp : definition_section coordination_section end_of_file"""

    global adj_matrix, coord_matrix

    n = coord_matrix.shape[0]

    adj_matrix = np.zeros((n, n))

    # build full symmetric matrix AFTER parsing
    for i in range(n):
        for j in range(n):
            if i != j:
                d = compute_distance(
                    coord_matrix[i],
                    coord_matrix[j]
                )
                adj_matrix[i][j] = d

    p[0] = {
        "name": instance_name,
        "adj_mat": adj_matrix,
        "coord_mat": coord_matrix
    }


# =========================================================
# HEADER SECTION
# =========================================================
def p_definition_section(p):
    """definition_section : NAME DIMENSION NUMBER"""

    global coord_matrix, instance_name

    n = int(p[3])

    if n > 3000:
        raise ValueError(f"Too large instance: {n}")

    instance_name = p[1]

    coord_matrix = np.zeros((n, 2))


# =========================================================
# COORD SECTION
# =========================================================
def p_coord_section(p):
    """coordination_section : COORDINATION_SECTION coord_list"""


def p_coord_list(p):
    """coord_list : coord_list coord
                  | coord"""


def p_coord(p):
    """coord : NUMBER NUMBER NUMBER"""

    node_id = int(p[1]) - 1
    x = float(p[2])
    y = float(p[3])

    coord_matrix[node_id] = [x, y]


# =========================================================
# END
# =========================================================
def p_end(p):
    """end_of_file : EOF
                   | empty"""


def p_empty(p):
    """empty :"""
    pass


# =========================================================
# ERROR HANDLING
# =========================================================
def p_error(p):
    if p:
        print(f"[Parser Error] Token {p.type} -> {p.value}")
    else:
        print("[Parser Error] EOF")


# =========================================================
# BUILD PARSER
# =========================================================
parser = yacc.yacc()