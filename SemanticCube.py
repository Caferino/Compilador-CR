"""
    Proyecto Final
    Autor: Óscar Antonio Hinojosa Salum A00821930
    Mayo 28 2023
    Compilador para lenguaje al estilo R/C++.

    --- Cubo Semántico ---
"""

# ======================== Cubo Semántico ======================== #

typesTable = [
#    lType    rType      **       *         /       %        +        -        >        <       <>      !=       ==       =       &&        ||
#    --------------------------------------------------------------------------------------------------------------------------------------------
    ['int',   'int',   'int',   'int',   'float', 'int',   'int',   'int',   'bool',  'bool',  'bool', 'bool', 'bool',  'int',   'bool',  'bool' ],
    ['int',   'float', 'float', 'float', 'float', 'float', 'float', 'float', 'bool',  'bool',  'bool', 'bool', 'bool',  'float', 'bool',  'bool' ],
    ['int',   'char',  'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'bool', 'bool', 'ERROR', 'ERROR', 'ERROR', 'ERROR'],
    ['int',   'bool',  'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'bool',  'bool',  'bool', 'bool', 'bool',  'bool',  'bool',  'bool' ],
    ['float', 'int',   'float', 'float', 'float', 'float', 'float', 'float', 'bool',  'bool',  'bool', 'bool', 'bool',  'float', 'bool',  'bool' ],
    ['float', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'bool',  'bool',  'bool', 'bool', 'bool',  'float', 'bool',  'bool' ],
    ['float', 'char',  'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'bool', 'bool', 'ERROR', 'ERROR', 'ERROR', 'ERROR'],
    ['float', 'bool',  'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'bool',  'bool',  'bool', 'bool', 'bool',  'bool',  'bool',  'bool' ],
    ['char',  'int',   'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'bool', 'bool', 'ERROR', 'ERROR', 'ERROR', 'ERROR'],
    ['char',  'float', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'bool', 'bool', 'ERROR', 'ERROR', 'ERROR', 'ERROR'],
    ['char',  'char',  'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'bool', 'bool', 'char',  'ERROR', 'ERROR', 'ERROR'],
    ['char',  'bool',  'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'bool', 'bool', 'bool',  'bool',  'ERROR', 'ERROR'],
    ['bool',  'int',   'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'bool',  'bool',  'bool', 'bool', 'bool',  'bool',  'bool',  'bool' ],
    ['bool',  'float', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'bool',  'bool',  'bool', 'bool', 'bool',  'bool',  'bool',  'bool' ],
    ['bool',  'char',  'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'bool', 'bool', 'ERROR', 'ERROR', 'ERROR', 'ERROR'],
    ['bool',  'bool',  'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'ERROR', 'bool', 'bool', 'bool',  'bool',  'bool',  'bool' ]
]

def Semantics(left_Type, right_Type, operator):
    # Con esto me ahorro tanto rollo para implementar las srings:
    if left_Type == 'string' : left_Type = 'char'
    # ------------- PAPÁ CUBOTE SEMÁNTICO ------------- #
    # ------------- INT operator OPERAND ------------- #
    if left_Type == typesTable[0][0]:                       # Si INT operator OPERAND ...
        if right_Type == typesTable[0][1]:                  # Si INT operator INT
            if operator == '**': return typesTable[0][2]     # Si INT ** INT return INT ...
            if operator == '*': return typesTable[0][3]
            if operator == '/': return typesTable[0][4]
            if operator == '%': return typesTable[0][5]
            if operator == '+': return typesTable[0][6]
            if operator == '-': return typesTable[0][7]
            if operator == '>': return typesTable[0][8]
            if operator == '<': return typesTable[0][9]
            if operator == '<>': return typesTable[0][10]
            if operator == '!=': return typesTable[0][11]
            if operator == '==': return typesTable[0][12]
            if operator == '=': return typesTable[0][13]
            if operator == '&&': return typesTable[0][14]
            if operator == '||': return typesTable[0][15]
        if right_Type == typesTable[1][1]:                  # Si INT operator FLOAT
            if operator == '**': return typesTable[1][2]     # Si INT ** FLOAT return FLOAT ...
            if operator == '*': return typesTable[1][3]
            if operator == '/': return typesTable[1][4]
            if operator == '%': return typesTable[1][5]
            if operator == '+': return typesTable[1][6]
            if operator == '-': return typesTable[1][7]
            if operator == '>': return typesTable[1][8]
            if operator == '<': return typesTable[1][9]
            if operator == '<>': return typesTable[1][10]
            if operator == '!=': return typesTable[1][11]
            if operator == '==': return typesTable[1][12]
            if operator == '=': return typesTable[1][13]
            if operator == '&&': return typesTable[1][14]
            if operator == '||': return typesTable[1][15]
        if right_Type == typesTable[2][1]:                  # Si INT operator CHAR
            if operator == '**': return typesTable[2][2]     # Si INT ** CHAR return ERROR ...
            if operator == '*': return typesTable[2][3]
            if operator == '/': return typesTable[2][4]
            if operator == '%': return typesTable[2][5]
            if operator == '+': return typesTable[2][6]
            if operator == '-': return typesTable[2][7]
            if operator == '>': return typesTable[2][8]
            if operator == '<': return typesTable[2][9]
            if operator == '<>': return typesTable[2][10]
            if operator == '!=': return typesTable[2][11]
            if operator == '==': return typesTable[2][12]
            if operator == '=': return typesTable[2][13]
            if operator == '&&': return typesTable[2][14]
            if operator == '||': return typesTable[2][15]
        if right_Type == typesTable[3][1]:                  # Si INT operator BOOL
            if operator == '**': return typesTable[3][2]     # Si INT ** BOOL return ERROR ...
            if operator == '*': return typesTable[3][3]
            if operator == '/': return typesTable[3][4]
            if operator == '%': return typesTable[3][5]
            if operator == '+': return typesTable[3][6]
            if operator == '-': return typesTable[3][7]
            if operator == '>': return typesTable[3][8]
            if operator == '<': return typesTable[3][9]
            if operator == '<>': return typesTable[3][10]
            if operator == '!=': return typesTable[3][11]
            if operator == '==': return typesTable[3][12]
            if operator == '=': return typesTable[3][13]
            if operator == '&&': return typesTable[3][14]
            if operator == '||': return typesTable[3][15]


    # ------------- FLOAT operator OPERAND ------------- #
    elif left_Type == typesTable[4][0]:                     # Si FLOAT operator OPERAND ...
        if right_Type == typesTable[4][1]:                  # Si FLOAT operator INT
            if operator == '**': return typesTable[4][2]     # Si FLOAT ** INT return FLOAT ...
            if operator == '*': return typesTable[4][3]
            if operator == '/': return typesTable[4][4]
            if operator == '%': return typesTable[4][5]
            if operator == '+': return typesTable[4][6]
            if operator == '-': return typesTable[4][7]
            if operator == '>': return typesTable[4][8]
            if operator == '<': return typesTable[4][9]
            if operator == '<>': return typesTable[4][10]
            if operator == '!=': return typesTable[4][11]
            if operator == '==': return typesTable[4][12]
            if operator == '=': return typesTable[4][13]
            if operator == '&&': return typesTable[4][14]
            if operator == '||': return typesTable[4][15]
        if right_Type == typesTable[5][1]:                  # Si FLOAT operator FLOAT
            if operator == '**': return typesTable[5][2]     # Si FLOAT ** FLOAT return FLOAT ...
            if operator == '*': return typesTable[5][3]
            if operator == '/': return typesTable[5][4]
            if operator == '%': return typesTable[5][5]
            if operator == '+': return typesTable[5][6]
            if operator == '-': return typesTable[5][7]
            if operator == '>': return typesTable[5][8]
            if operator == '<': return typesTable[5][9]
            if operator == '<>': return typesTable[5][10]
            if operator == '!=': return typesTable[5][11]
            if operator == '==': return typesTable[5][12]
            if operator == '=': return typesTable[5][13]
            if operator == '&&': return typesTable[5][14]
            if operator == '||': return typesTable[5][15]
        if right_Type == typesTable[6][1]:                  # Si FLOAT operator CHAR
            if operator == '**': return typesTable[6][2]     # Si FLOAT ** CHAR return ERROR ...
            if operator == '*': return typesTable[6][3]
            if operator == '/': return typesTable[6][4]
            if operator == '%': return typesTable[6][5]
            if operator == '+': return typesTable[6][6]
            if operator == '-': return typesTable[6][7]
            if operator == '>': return typesTable[6][8]
            if operator == '<': return typesTable[6][9]
            if operator == '<>': return typesTable[6][10]
            if operator == '!=': return typesTable[6][11]
            if operator == '==': return typesTable[6][12]
            if operator == '=': return typesTable[6][13]
            if operator == '&&': return typesTable[6][14]
            if operator == '||': return typesTable[6][15]
        if right_Type == typesTable[7][1]:                  # Si FLOAT operator BOOL
            if operator == '**': return typesTable[7][2]     # Si FLOAT ** BOOL return ERROR ...
            if operator == '*': return typesTable[7][3]
            if operator == '/': return typesTable[7][4]
            if operator == '%': return typesTable[7][5]
            if operator == '+': return typesTable[7][6]
            if operator == '-': return typesTable[7][7]
            if operator == '>': return typesTable[7][8]
            if operator == '<': return typesTable[7][9]
            if operator == '<>': return typesTable[7][10]
            if operator == '!=': return typesTable[7][11]
            if operator == '==': return typesTable[7][12]
            if operator == '=': return typesTable[7][13]
            if operator == '&&': return typesTable[7][14]
            if operator == '||': return typesTable[7][15]


    # ------------- CHAR operator OPERAND ------------- #
    elif left_Type == typesTable[8][0]:                     # Si CHAR operator OPERAND ...
        if right_Type == typesTable[8][1]:                  # Si CHAR operator INT
            if operator == '**': return typesTable[8][2]     # Si CHAR ** INT return ERROR ...
            if operator == '*': return typesTable[8][3]
            if operator == '/': return typesTable[8][4]
            if operator == '%': return typesTable[8][5]
            if operator == '+': return typesTable[8][6]
            if operator == '-': return typesTable[8][7]
            if operator == '>': return typesTable[8][8]
            if operator == '<': return typesTable[8][9]
            if operator == '<>': return typesTable[8][10]
            if operator == '!=': return typesTable[8][11]
            if operator == '==': return typesTable[8][12]
            if operator == '=': return typesTable[8][13]
            if operator == '&&': return typesTable[8][14]
            if operator == '||': return typesTable[8][15]
        if right_Type == typesTable[9][1]:                  # Si CHAR operator FLOAT
            if operator == '**': return typesTable[9][2]     # Si CHAR ** FLOAT return ERROR ...
            if operator == '*': return typesTable[9][3]
            if operator == '/': return typesTable[9][4]
            if operator == '%': return typesTable[9][5]
            if operator == '+': return typesTable[9][6]
            if operator == '-': return typesTable[9][7]
            if operator == '>': return typesTable[9][8]
            if operator == '<': return typesTable[9][9]
            if operator == '<>': return typesTable[9][10]
            if operator == '!=': return typesTable[9][11]
            if operator == '==': return typesTable[9][12]
            if operator == '=': return typesTable[9][13]
            if operator == '&&': return typesTable[9][14]
            if operator == '||': return typesTable[9][15]
        if right_Type == typesTable[10][1]:                 # Si CHAR operator CHAR
            if operator == '**': return typesTable[10][2]    # Si CHAR ** CHAR return ERROR ...
            if operator == '*': return typesTable[10][3]
            if operator == '/': return typesTable[10][4]
            if operator == '%': return typesTable[10][5]
            if operator == '+': return typesTable[10][6]
            if operator == '-': return typesTable[10][7]
            if operator == '>': return typesTable[10][8]
            if operator == '<': return typesTable[10][9]
            if operator == '<>': return typesTable[10][10]
            if operator == '!=': return typesTable[10][11]
            if operator == '==': return typesTable[10][12]
            if operator == '=': return typesTable[10][13]
            if operator == '&&': return typesTable[10][14]
            if operator == '||': return typesTable[10][15]
        if right_Type == typesTable[11][1]:                 # Si CHAR operator BOOL
            if operator == '**': return typesTable[11][2]    # Si CHAR ** BOOL return ERROR ...
            if operator == '*': return typesTable[11][3]
            if operator == '/': return typesTable[11][4]
            if operator == '%': return typesTable[11][5]
            if operator == '+': return typesTable[11][6]
            if operator == '-': return typesTable[11][7]
            if operator == '>': return typesTable[11][8]
            if operator == '<': return typesTable[11][9]
            if operator == '<>': return typesTable[11][10]
            if operator == '!=': return typesTable[11][11]
            if operator == '==': return typesTable[11][12]
            if operator == '=': return typesTable[11][13]
            if operator == '&&': return typesTable[11][14]
            if operator == '||': return typesTable[11][15]


    # ------------- BOOL operator OPERAND ------------- #
    elif left_Type == typesTable[12][0]:                    # Si BOOL operator OPERAND ...
        if right_Type == typesTable[12][1]:                 # Si BOOL operator INT
            if operator == '**': return typesTable[12][2]    # Si BOOL ** INT return ERROR ...
            if operator == '*': return typesTable[12][3]
            if operator == '/': return typesTable[12][4]
            if operator == '%': return typesTable[12][5]
            if operator == '+': return typesTable[12][6]
            if operator == '-': return typesTable[12][7]
            if operator == '>': return typesTable[12][8]
            if operator == '<': return typesTable[12][9]
            if operator == '<>': return typesTable[12][10]
            if operator == '!=': return typesTable[12][11]
            if operator == '==': return typesTable[12][12]
            if operator == '=': return typesTable[12][13]
            if operator == '&&': return typesTable[12][14]
            if operator == '||': return typesTable[12][15]
        if right_Type == typesTable[13][1]:                 # Si BOOL op FLOAT
            if operator == '**': return typesTable[13][2]    # Si BOOL ** FLOAT return ERROR ...
            if operator == '*': return typesTable[13][3]
            if operator == '/': return typesTable[13][4]
            if operator == '%': return typesTable[13][5]
            if operator == '+': return typesTable[13][6]
            if operator == '-': return typesTable[13][7]
            if operator == '>': return typesTable[13][8]
            if operator == '<': return typesTable[13][9]
            if operator == '<>': return typesTable[13][10]
            if operator == '!=': return typesTable[13][11]
            if operator == '==': return typesTable[13][12]
            if operator == '=': return typesTable[13][13]
            if operator == '&&': return typesTable[13][14]
            if operator == '||': return typesTable[13][15]
        if right_Type == typesTable[14][1]:                 # Si BOOL operator CHAR
            if operator == '**': return typesTable[14][2]    # Si BOOL ** CHAR return ERROR ...
            if operator == '*': return typesTable[14][3]
            if operator == '/': return typesTable[14][4]
            if operator == '%': return typesTable[14][5]
            if operator == '+': return typesTable[14][6]
            if operator == '-': return typesTable[14][7]
            if operator == '>': return typesTable[14][8]
            if operator == '<': return typesTable[14][9]
            if operator == '<>': return typesTable[14][10]
            if operator == '!=': return typesTable[14][11]
            if operator == '==': return typesTable[14][12]
            if operator == '=': return typesTable[14][13]
            if operator == '&&': return typesTable[14][14]
            if operator == '||': return typesTable[14][15]
        if right_Type == typesTable[15][1]:                 # Si BOOL operator BOOL
            if operator == '**': return typesTable[15][2]    # Si BOOL ** BOOL return ERROR ...
            if operator == '*': return typesTable[15][3]
            if operator == '/': return typesTable[15][4]
            if operator == '%': return typesTable[15][5]
            if operator == '+': return typesTable[15][6]
            if operator == '-': return typesTable[15][7]
            if operator == '>': return typesTable[15][8]
            if operator == '<': return typesTable[15][9]
            if operator == '<>': return typesTable[15][10]
            if operator == '!=': return typesTable[15][11]
            if operator == '==': return typesTable[15][12]
            if operator == '=': return typesTable[15][13]
            if operator == '&&': return typesTable[15][14]
            if operator == '||': return typesTable[15][15]

    # ------------- ??? ??? ??? ------------- #
    else: return 'ERROR'