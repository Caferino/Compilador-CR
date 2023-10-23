"""
    Proyecto Final
    Autor: Óscar Antonio Hinojosa Salum A00821930
    Mayo 28 2023
    Compilador para lenguaje al estilo R/C++.

    --- Constructor de Cuádruplos ---
"""

# ======================== Código Intermedio ======================== #

from VirtualMachine import VirtualMachine
from functools import reduce
import operator
import SemanticCube
import pprint
import sys
import re

virtualMachine = VirtualMachine()

# Pool de variables temporales, espacios temporales, t1, t2, ...
class Avail:
    temporales = []
    next_temp = 1

    # Estático para no tener que declarar un objeto tipo Avail
    @staticmethod
    def next():
        if Avail.temporales:
            return Avail.temporales.pop()
        else:
            # "The letter "f" at the beginning of the string "t{Avail.next_temp}" 
            # denotes that it is a formatted string literal. Introduced in Python 3.6."
            # En este caso, para crear 't1', 't2', 't3', ...
            temp = f"t{Avail.next_temp}"
            Avail.next_temp += 1
            return temp

    # Si algún operando (Izq. o Der.) en el cuádruplo actual
    # es una variable temporal, se debe(n) regresar al Avail
    @staticmethod
    def release(space):
        # Para evitar errores de "out of index", checamos que mida al menos 2, 't1', 't125' ...
        if isinstance(space, str) and space.startswith('t') and space[1:].isdigit():
            Avail.temporales.append(space)



class Quadruples:

    # ------------------ INIT ------------------ #
    def __init__(self):
        # Mom
        self.quadruples = []
        self.symbolTable = []

        # Pilas para construir cuádruplos
        self.PilaO = []
        self.PTypes = []
        self.POper = []

        # Para los estatutos que requieren saltos
        self.PJumps = []
        self.dirFunc = []
        # self.cont = 1  ## ! Los cuádruplos empiezan desde 1.
        self.cont = 0
        self.assignTemp = 'target'
        self.k = 1
        self.extraStringsForPrint = 1


    # ------------------ EXPRESIONES LINEALES ------------------ #
    # ------ 1. Insertando Type y ID ------ #
    def insertTypeAndID(self, token):
        if token.__class__.__name__ == 'int' or token.__class__.__name__ == 'float':
            # Si el token es un número, hacemos lo usual
            self.PilaO.append(token)
            self.PTypes.append(token.__class__.__name__)

        elif token == 'True' or token == 'False':
            self.PilaO.append(token)
            self.PTypes.append('bool')

        else:
            # Si no, es un ID cuyo tipo debemos buscar

            # En caso de ser una matriz, sacamos la dirección del valor
            isMatrix = False
            if '[' in token :
                isMatrix = True
                # Separamos el nombre de las dimensiones
                varName = token
                varNameIndex = varName.index('[')
                varName = varName[:varNameIndex]

                # Guardamos las dimensiones
                indices = re.findall(r'\[(.*?)\]', token)
                indices = [int(index) for index in indices]
                varDimensions = indices
                token = varName
                valueAddress = reduce(operator.mul, varDimensions, 1) - 1

            # Si no, lo buscamos como tal
            i = 0   # I missed you, baby
            for tuple in self.symbolTable:
                if token == tuple[1] and isMatrix :
                    # Metemos el valor de la posición deseada en la matriz
                    self.PilaO.append(tuple[6][valueAddress])
                    self.PTypes.append(tuple[0])
                    break

                elif token == tuple[1]:   ## Posición del ID en la symbolTable
                    self.PilaO.append(token) # Mis cuádruplos se benefician con su nombre
                    self.PTypes.append(tuple[0]) # Posición del tipo
                    break
    
                # Si llegamos a la última tupla y aún no existe la variable...
                elif token != tuple[1] and i == len(self.symbolTable) - 1:
                    raise TypeError('Variable ', token, ' not declared!')
                
                i += 1

    # ------ 2 y 3. Insertando Signos (+, -, *, /, <, >, <>, =, ||, &&, !=, ...) ------ #
    def insertSign(self, token):
        self.POper.append(token)
    

    # ------ 4. Verificando Sumas o Restas ------ #
    def verifySignPlusOrMinus(self):
        # print("Current POper: ", self.POper) # ! DEBUG
        # if self.POper and self.POper[-1] == '-' : print("WTFFFFFFFFF")
        if self.POper:
            if self.POper[-1] == '+' or self.POper[-1] == '-':
                # Asignamos operandos y operador a validar y ejecutar
                ## ! IMPORTANTE: El orden de los .pop() importan!
                right_operand = self.PilaO.pop()
                left_operand = self.PilaO.pop()

                right_Type = self.PTypes.pop()
                left_Type = self.PTypes.pop()

                operator = self.POper.pop()
                result_Type = SemanticCube.Semantics(left_Type, right_Type, operator)

                if(result_Type != 'ERROR'):
                    result = Avail.next()
                    self.generateQuadruple(operator, left_operand, right_operand, result)
                    self.PilaO.append(result)
                    self.PTypes.append(result_Type)

                    # "If any operand were a temporal space, return it to AVAIL"
                    # Se checará que sea un espacio temporal antes de meterlo de vuelta a Avail
                    Avail.release(left_operand)
                    Avail.release(right_operand)

                else:
                    raise TypeError("Type mismatch in: ", left_operand, operator, right_operand)

    # ------ 5. Verificando Multiplicaciones o Divisiones ------ #
    def verifySignTimesOrDivide(self):
        # print("Current POper: ", self.POper) # ! DEBUG
        if self.POper:
            if self.POper[-1] == '*' or self.POper[-1] == '/' or self.POper[-1] == '**':
                # Asignamos operandos y operador a validar y ejecutar
                # ! IMPORTANTE: El orden de los .pop() importan!
                right_operand = self.PilaO.pop()
                left_operand = self.PilaO.pop()

                right_Type = self.PTypes.pop()
                left_Type = self.PTypes.pop()

                operator = self.POper.pop()
                result_Type = SemanticCube.Semantics(left_Type, right_Type, operator)

                if(result_Type != 'ERROR'):
                    result = Avail.next()
                    self.generateQuadruple(operator, left_operand, right_operand, result)
                    self.PilaO.append(result)
                    self.PTypes.append(result_Type)

                    # "If any operand were a temporal space, return it to AVAIL"
                    # Se checará que sea un espacio temporal antes de meterlo de vuelta a Avail
                    Avail.release(left_operand)
                    Avail.release(right_operand)

                else:
                    raise TypeError("Type mismatch in: ", left_operand, operator, right_operand)

    # ------ 6. Verificando Condicionales ------ #
    def verifyConditionals(self):
        # print("Current POper: ", self.POper) # ! DEBUG
        if self.POper:
            if self.POper[-1] == '>' or self.POper[-1] == '<' or self.POper[-1] == '<>' or self.POper[-1] == '!=' or self.POper[-1] == '==' or self.POper[-1] == '||' or self.POper[-1] == '&&' or self.POper[-1] == '<=' :
                # Asignamos operandos y operador a validar y ejecutar
                ## ! IMPORTANTE: El orden de los .pop() importan!
                right_operand = self.PilaO.pop()
                left_operand = self.PilaO.pop()

                right_Type = self.PTypes.pop()
                left_Type = self.PTypes.pop()

                operator = self.POper.pop()
                result_Type = SemanticCube.Semantics(left_Type, right_Type, operator)

                if(result_Type != 'ERROR'):
                    result = Avail.next()
                    self.generateQuadruple(operator, left_operand, right_operand, result)
                    self.PilaO.append(result)
                    self.PTypes.append(result_Type)

                    # "If any operand were a temporal space, return it to AVAIL"
                    # Se checará que sea un espacio temporal antes de meterlo de vuelta a Avail
                    Avail.release(left_operand)
                    Avail.release(right_operand)

                else:
                    raise TypeError("Type mismatch in: ", left_operand, operator, right_operand)




    # ------------------ CONDICIONALES ------------------ #
    # ------ 1. Primer nodo de un IF/ELSE statement ------ #
    def nodoCondicionalUno(self):
        exp_type = self.PTypes.pop()
        if(exp_type != 'bool') : raise TypeError("Type Mismatch in a Conditional!", exp_type, "in", self.quadruples)
        else:
            result = self.PilaO.pop()
            self.generateQuadruple('GotoF', result, '', 'linePlaceHolder')
            self.PJumps.append(self.cont - 1)


    # ------ 2. Segundo nodo de IF/ELSE  ------ #
    def nodoCondicionalDos(self):
        end = self.PJumps.pop()
        # Mandamos a insertar la línea a cuál saltar
        self.fill(end, self.cont)


    # ------ 3. Tercer nodo de IF/ELSE  ------ #
    def nodoCondicionalTres(self):
        self.generateQuadruple('GOTO', '', '', 'linePlaceholder')
        false = self.PJumps.pop()
        self.PJumps.append(self.cont - 1)
        # Mandamos a insertar la línea a cuál saltar
        self.fill(false, self.cont)




    # ------------------ CICLOS WHILE ------------------ #
    # ------ 1. Primer nodo de un WHILE statement ------ #
    def nodoWhileUno(self):
        self.PJumps.append(self.cont)


    # ------ 2. Segundo nodo de WHILE ------ #
    def nodoWhileDos(self):
        exp_type = self.PTypes.pop()
        if(exp_type != 'bool') : raise TypeError("Type Mismatch in a While Loop!", exp_type, "in", self.quadruples)
        else:
            result = self.PilaO.pop()
            self.generateQuadruple('GotoF', result, '', 'linePlaceHolder')
            self.PJumps.append(self.cont - 1)


    # ------ 3. Tercer nodo de WHILE ------ #
    def nodoWhileTres(self):
        end = self.PJumps.pop()
        varReturn = self.PJumps.pop()
        self.generateQuadruple('GOTO', '', '', varReturn)
        self.fill(end, self.cont)




    # ------------------ FUNCTION ------------------ #
    # ------ 1. Nodo para insertar el contador de cuádruplos ------ #
    def nodoFunctionUno(self, funcID):
        print("NODO FUNCTION UNO") # ! DEBUG
        for i, tuple_item in enumerate(self.symbolTable):
            if funcID == tuple_item[1]:
                currentRow = self.symbolTable[i]
                # Añadimos una nueva columna con su posición en los cuádruplos
                currentRow = currentRow + (self.cont,)
                self.symbolTable[i] = currentRow


    def nodoFunctionDos(self):
        print("NODO FUNCTION DOS") # ! DEBUG
        self.generateQuadruple('ENDFUNC', '', '', '')




    # ------------------ FUNCTION CALL ------------------ #
    # ------ 1. Primer nodo de un FUNCTION CALL ------ #
    # ------ Verificar que existe la función, sino error ------ #
    def nodoFunctionCallUno(self, ID):
        exists = False
        for tuple in self.symbolTable :
            if ID == tuple[1] :
                exists = True
                break

        if exists == False : raise TypeError("Function", ID, "not declared.")


    def nodoFunctionCallDos(self, ID):
        print("FUNCTION CALL 2") # ! DEBUG
        self.generateQuadruple('ERA', '', '', ID) # (Activation Record expansion –NEW—size)
        self.k = 1
        # TODO - Add a pointer to the first parameter type in the ParameterTable. """


    def nodoFunctionCallTres(self):
        print("FUNCTION CALL 3") # ! DEBUG
        argument = self.PilaO.pop()
        argumentType = self.PTypes.pop()
        # TODO - Verify ArgumentType against current Parameter (#k) in ParameterTable.
        self.generateQuadruple('PARAM', argument, '', self.k) # Generate action PARAMETER, Argument, Argument#k """


    def nodoFunctionCallCuatro(self):
        print("FUNCTION CALL 4") # ! DEBUG
        self.k = self.k + 1 
        # TODO - Move to next parameter.


    def nodoFunctionCallCinco(self):
        print("FUNCTION CALL 5") # ! DEBUG
        # TODO - Verify that the last parameter points to null (coherence in number of parameters).


    def nodoFunctionCallSeis(self):
        print("FUNCTION CALL 6") # ! DEBUG
        # 6.- Generate action GOSUB, procedure-self.name, , initial-address
        # TODO - Puedo sacar procedureName de un parentFunction en cualquier parámetro
        # ! self.generateQuadruple('GOSUB', prdocedureName, '', initialAddress)




    # ------------------ PRINT, RETURN, ASSIGN ------------------ #
    # ------ 1. Prints ------ #
    def insertPrint(self, token):
        self.POper.append(token)


    def verifyPrint(self):
        if self.POper:
            if self.POper[-1] == 'print':
                # Asignamos operandos y operador a validar y ejecutar
                ## ! IMPORTANTE: El orden de los .pop() importan!
                right_operand = None
                left_operand = self.PilaO.pop()

                right_Type = None
                left_Type = self.PTypes.pop()

                operator = self.POper.pop()
                result_Type = SemanticCube.Semantics(left_Type, right_Type, operator)
                
                if self.extraStringsForPrint > 1 :
                    words = ''
                    while self.extraStringsForPrint > 0 :
                        if '"' not in left_operand :
                            for tuple in self.symbolTable :
                                if left_operand == tuple[1] :
                                    words += (' ' + str(tuple[6][0]).strip('"'))
                                    break
                                    # TODO - Y SI ES MATRIZ? REUTILIZAR LOGICA YA HECHA
                                elif tuple == self.symbolTable[-1] :
                                    raise TypeError("Variable at print doesn't exist: ", left_operand)
                        else :
                            words += (' ' + left_operand.strip('"'))
                        left_operand = self.PilaO.pop()
                        left_type = self.PTypes.pop()
                        self.extraStringsForPrint -= 1
                    
                    words = words.split()
                    left_operand = " ".join(reversed(words))
                    self.extraStringsForPrint = 1
                    

                if(result_Type != 'ERROR'):
                    result = None
                    self.generateQuadruple(operator, left_operand, right_operand, result)

                    # "If any operand were a temporal space, return it to AVAIL"
                    # Se checará que sea un espacio temporal antes de meterlo de vuelta a Avail
                    Avail.release(left_operand)

                else:
                    raise TypeError("Type mismatch in: ", left_operand, operator, right_operand)


    def insertPrintString(self, string):
        self.PilaO.append(string)
        self.PTypes.append('char')


    # ------ 2. Assignments ------ #
    def insertAssignmentSign(self, token):
        self.POper.append(token)


    def insertAssignmentID(self, token):
        self.assignTemp = token


    def verifyAssignment(self):
        if self.POper:
            if self.POper[-1] == '=' or self.POper[-1] == '<-':
                # Asignamos operandos y operador a validar y ejecutar
                ## ! IMPORTANTE: El orden de los .pop() importan!
                right_operand = None
                left_operand = self.PilaO.pop()

                right_Type = None
                left_Type = self.PTypes.pop()

                operator = self.POper.pop()
                result_Type = SemanticCube.Semantics(left_Type, right_Type, operator)

                if(result_Type != 'ERROR'):
                    result = self.assignTemp
                    self.generateQuadruple(operator, left_operand, right_operand, result)
                    self.PilaO.append(result)
                    self.PTypes.append(result_Type)
                    

                else:
                    raise TypeError("Type mismatch in: ", left_operand, operator, right_operand)




    # ------------------ MÉTODOS AUXILIARES ------------------ #
    # ------ Generador de Cuádruplos ------ #
    def generateQuadruple(self, operator, left_operand, right_operand, result):
        # Empujamos el nuevo cuádruple a nuestra lista o memoria
        self.quadruples.append( (operator, left_operand, right_operand, result) )
        self.cont += 1


    # ------ Llenado de líneas de salto para GOTOF y GOTOV ------ #
    # Mi "QUAD_POINTER" / quad_cont / counter / cont APUNTA siempre hacia el SIGUIENTE
    def fill(self, cont, line):
        self.quadruples[cont] = (self.quadruples[cont][:3] + (line,))


    # ------ Actualizar symbolTable aquí. Fue por error propio ------ #
    def updateSymbolTable(self, newSymbolTable):
        self.symbolTable = newSymbolTable


    # ------ Virtual Machine ------ #
    def startCompiler(self):
        virtualMachine.start(self.quadruples, self.symbolTable)


quadsConstructor = Quadruples()