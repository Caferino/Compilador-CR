"""
    Proyecto Final
    Autor: Óscar Antonio Hinojosa Salum A00821930
    Abril 15 2023
    Compilador para lenguaje al estilo R/C++.

    --- Parser / Sintáxis ---
"""

# ======================== Sintáxis ======================== #

from Semantics import Rules
from Quadruples import quadsConstructor

rules = Rules()

def p_program(p):
    '''program : block'''
    p[0] = "COMPILED"
    rules.p_end_program()
    quadsConstructor.startCompiler()


def p_block(p):
    '''block : statement block
                | empty'''


# Si se llega a pedir matrices cúbicas o más, 
# tal vez pueda ciclarlo aquí y ver cómo sería al guardar en memoria.
# Por ahora solo me interesan las de una o dos dimensiones.
def p_vars(p):
    '''vars : type ID vars_equals SEMICOLON
            | type ID LEFTBRACKET CTEI RIGHTBRACKET vars_equals SEMICOLON
            | type ID LEFTBRACKET CTEI RIGHTBRACKET LEFTBRACKET CTEI RIGHTBRACKET vars_equals SEMICOLON'''
    # Semántica
    rules.p_insertID(p, False)


def p_type(p):
    '''type : INT
            | FLOAT
            | BOOL
            | VOID'''
    rules.p_insertType(p)
    

def p_vars_equals(p):
    '''vars_equals : assignment vars_equals_array extra_vars
                | assignment expression extra_vars
                | extra_vars
                | empty'''


def p_vars_equals_array(p):
    '''vars_equals_array : LEFTCORCH expression array_vars RIGHTCORCH
                | LEFTCORCH empty RIGHTCORCH'''
    rules.p_saveValue(p)


def p_extra_vars_comma(p):
    '''extra_vars_comma : COMMA'''
    rules.p_saveComma(p)


def p_extra_vars(p):
    '''extra_vars : extra_vars_comma ID vars_equals
                | empty'''
    rules.p_insertID(p, False)


def p_array_vars(p):
    '''array_vars : COMMA expression array_vars
                | empty'''


def p_statement(p):
    '''statement : vars
                 | function
                 | assignment_block
                 | expression
                 | function_call
                 | loop
                 | condition
                 | writing
                 | sort
                 | return
                 | empty'''
    rules.p_saveToOpStack(p)


def p_function(p):
    '''function : function_type function_id LEFTPAREN function_type_and_id '''


def p_function_type(p):
    '''function_type : '''


def p_return(p):
    '''return : RETURN expression SEMICOLON
                | RETURN SEMICOLON'''


def p_assignment_block(p):
    '''assignment_block : nodoassign'''
    rules.values = []


def p_nodoassign(p):
    '''nodoassign : ID ASSIGNL expression SEMICOLON
                | ID EQUALS expression SEMICOLON'''
    quadsConstructor.insertAssignmentID(p[1])
    quadsConstructor.insertAssignmentSign(p[2])
    quadsConstructor.verifyAssignment()


def p_assignment(p):
    '''assignment : ASSIGNL
                 | EQUALS'''
    

def p_function_call(p):
    '''function_call : function_call_id expression function_call_expressions RIGHTPAREN'''
    # ! NODOS


def p_function_call_id(p):
    '''function_call_id : ID LEFTPAREN'''
    quadsConstructor.nodoFunctionCallUno(p[1])
    # ! quadsConstructor.nodoFunctionCallDos(p[1])


def p_function_call_expressions(p):
    '''function_call_expressions : COMMA expression function_call_expressions
                 | empty'''
    # ! NODOS


def p_sort(p):
    '''sort : ID PERIOD SORT LEFTPAREN RIGHTPAREN SEMICOLON'''
    rules.sortMatrix(p)


def p_loop(p):
    '''loop : nodowhile LEFTPAREN expression nodowhile2 LEFTCORCH block RIGHTCORCH
                 | empty'''
    quadsConstructor.nodoWhileTres()


def p_nodowhile(p):
    '''nodowhile : WHILE'''
    quadsConstructor.nodoWhileUno()


def p_nodowhile2(p):
    '''nodowhile2 : RIGHTPAREN'''
    quadsConstructor.nodoWhileDos()


def p_condition(p):
    '''condition : IF LEFTPAREN expression nodocond LEFTCORCH block RIGHTCORCH else_condition'''
    quadsConstructor.nodoCondicionalDos()


def p_nodocond(p):
    '''nodocond : RIGHTPAREN'''
    quadsConstructor.nodoCondicionalUno()


def p_else_condition(p):
    '''else_condition : nodoelse LEFTCORCH block RIGHTCORCH
                      | empty'''

def p_nodoelse(p):
    '''nodoelse : ELSE'''
    quadsConstructor.nodoCondicionalTres()


def p_writing(p):
    '''writing : writingprint LEFTPAREN print_val RIGHTPAREN SEMICOLON'''
    # TODO - Lógica de meter el token PRINT a los quads, o qué?
    quadsConstructor.verifyPrint()


def p_writingprint(p):
    '''writingprint : PRINT'''
    quadsConstructor.insertPrint(p[1])


def p_print_val(p):
    '''print_val : expression print_exp
                 | CTESTRING print_exp'''
    # ! if p[1] != None : quadsConstructor.insertPrintString(p[1])


def p_print_exp(p):
    '''print_exp : COMMA print_val
                 | empty'''


def p_var_cte(p):
    '''var_cte : CTEI
               | CTEF
               | ID'''
    # PROBLEMA CON SALSA
    if p.slice[1].type == 'ID' : quadsConstructor.insertTypeAndID(p[1]) # Nuestro lexer lidia con números

    # Semántica
    rules.p_saveValue(p)
    rules.p_saveToOpStack(p)


def p_expression(p):
    '''expression : exp comparation'''
    quadsConstructor.verifyConditionals() # If POper.top == '<' or '>' ...


def p_exp(p):
    '''exp : term operator'''
    quadsConstructor.verifySignPlusOrMinus() # If POper.top == '+' or '-' ...


def p_comparation(p):
    '''comparation : AND exp
                 | OR exp
                 | GREATER exp
                 | LESS exp
                 | NOTEQUAL exp
                 | NOTEQUALNUM exp
                 | empty'''
    if p[1] != None : quadsConstructor.insertSign(p[1])


def p_term(p):
    '''term : fact term_operator'''
    quadsConstructor.verifySignTimesOrDivide()


def p_operator(p):
    '''operator : PLUS term operator
                | MINUS term operator
                | empty'''
    # ! quadsConstructor.verifySignPlusOrMinus() ## ! CREO ESTO ARREGLA EXPRESIONES LINEALES O ROMPE MAS
    if p[1] != None : quadsConstructor.insertSign(p[1])


def p_term_operator(p):
    '''term_operator : EXPONENTIAL fact term_operator
                     | TIMES fact term_operator
                     | DIVIDE fact term_operator
                     | MODULUS fact term_operator
                     | empty'''
    if p[1] != None : quadsConstructor.insertSign(p[1])


def p_fact(p):
    '''fact : LEFTPAREN expression RIGHTPAREN
              | var_cte'''




# # ======================== Reglas de Errores ======================== # #

def p_error(p):
    # raise TypeError("Syntax error in input! - {} ".format(p)) # Para detener la compilación
    print("Syntax error in input! - {} ".format(p))


def p_empty(p):
    '''empty :'''
    pass




# # # = = = = = = = = = = = = = Main - Lector de Archivos = = = = = = = = = = = = = # # #

import sys
import ply.yacc as yacc

from Lexer import tokens

yacc.yacc()

if __name__ == '__main__':

    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.read()
            f.close()
            if yacc.parse(data) == "COMPILED":
                print("Compilation Completed")
        except EOFError:
            print(EOFError)
    else:
        print("File not found")