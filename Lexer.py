"""
    Proyecto Final
    Autor: Óscar Antonio Hinojosa Salum A00821930
    Abril 15 2023
    Compilador para lenguaje al estilo R/C++.

    --- Lexer / Léxico ---
"""

# ======================== Léxico ======================== #

import ply.lex as lex
from Quadruples import quadsConstructor

# ------ PALABRAS CLAVE ------ #
keywords = {
    'program'  : 'PROGRAM',
    'print'    : 'PRINT',
    'if'       : 'IF',
    'else'     : 'ELSE',
    'int'      : 'INT',
    'float'    : 'FLOAT',
    'string'   : 'STRING',
    'char'     : 'CHAR',
    'bool'     : 'BOOL',
    'void'     : 'VOID',
    'while'    : 'WHILE',
    'return'   : 'RETURN',
    'sort'     : 'SORT',
    'media'    : 'MEDIA',
    'moda'     : 'MODA',
    'mediana'  : 'MEDIANA',
    'varianza' : 'VARIANZA',
    'regsim'   : 'REGSIM',
    'plot'     : 'PLOT'
}


# ------ TOKENS ------ #
tokens = [
    'SEMICOLON', 'SORT', 'MEDIA', 'MODA', 'MEDIANA', 'VARIANZA', 'REGSIM', 'PLOT', 'LEFTBRACKET', 'PERIOD', 'RIGHTBRACKET', 'GREATER', 'LESS',
    'ISLESSOREQUAL', 'ISGREATEROREQUAL', 'NOTEQUAL', 'NOTEQUALNUM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EXPONENTIAL', 'MODULUS', 'LEFTPAREN',
    'RIGHTPAREN', 'ID', 'CTEI', 'CTEF', 'EQUALS', 'ASSIGNL', 'LEFTCORCH', 'RIGHTCORCH', 'CTESTRING', 'COMMA', 'AND', 'OR', 'PRINT', 'IF', 'ELSE',
    'INT', 'FLOAT', 'STRING', 'CHAR', 'BOOL', 'VOID', 'WHILE', 'RETURN',
]


# ------ EXPRESIONES REGULARES DE TOKENS ------ #
t_SEMICOLON = r'\;'
t_LEFTBRACKET = r'\['
t_RIGHTBRACKET = r'\]'
t_GREATER = r'>'
t_LESS = r'<'
t_ISLESSOREQUAL = r'<='
t_ISGREATEROREQUAL = r'>='
t_NOTEQUAL = r'!='
t_NOTEQUALNUM = r'<>'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_EXPONENTIAL = r'\*\*'
t_MODULUS = r'\%\%'
t_LEFTPAREN = r'\('
t_RIGHTPAREN = r'\)'
# t_COLON = r':'        # Este maldito desgraciado me quitó un día de mi vida, a ver si después le tengo algún uso...
t_EQUALS = r'\='
t_ASSIGNL = r'<-'
# t_ASSIGNR = r'->'     # Wakala
t_LEFTCORCH = r'\{'
t_RIGHTCORCH = r'\}'
t_COMMA = r'\,'
t_AND = r'&&'
t_OR = r'\|\|'
t_PERIOD = r'\.'
t_SORT = r'sort'
t_MEDIA = r'media'
t_MODA = r'moda'
t_MEDIANA = r'mediana'
t_VARIANZA = r'varianza'
t_REGSIM = r'regsim'
t_PLOT = r'plot'
t_ignore = " \t"


# ------ EXPRESIONES REGULARES CON OPERACIONES ------ #

# ID
def t_ID(t):
    r'[A-za-z]([A-za-z]|[0-9])*'
    t.type = keywords.get(t.value, 'ID')
    return t

# Strings
def t_CTESTRING(t):
    r'\".*?\"'
    t.value = str(t.value)
    quadsConstructor.PilaO.append(t.value)
    quadsConstructor.PTypes.append('string')
    return t

# Número Flotante (float)
def t_CTEF(t):
    r'-?[0-9]*\.[0-9]+'
    t.value = float(t.value)
    quadsConstructor.insertTypeAndID(t.value)
    return t


# Número Entero (int)
def t_CTEI(t):
    r'-?\d+'
    t.value = int(t.value)
    quadsConstructor.insertTypeAndID(t.value)
    return t


# Línea Nueva o Múltiples líneas nuevas (newlines)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Comentarios
def t_comment(t):
    r'\/\/.*|\#.*'
    pass


# Errores léxicos
def t_error(t):
    print("Error léxico ' {0} ' en la línea ' {1} ' ".format(t.value[0], t.lineno))
    t.lexer.skip(1)


lex.lex()