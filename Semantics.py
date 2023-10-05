"""
    Proyecto Final
    Autor: Óscar Antonio Hinojosa Salum A00821930
    Abril 15 2023
    Compilador para lenguaje al estilo R/C++.

    --- Reglas de Semántica ---
"""

# ======================== Semántica ======================== #

import re # Librería para expresiones regulares RegEX
import pprint # Para imprimir el Symbol Table de manera bonita
from functools import reduce # Para multiplicar listas y matrices
import operator

from Quadruples import quadsConstructor

from Memory import MemoryMap
memory = MemoryMap()

class Rules:
    def __init__(self):
        # Temporales
        self.type = ''
        self.varName = ''
        self.varDimensions = []
        self.scope = 'global'
        self.isFunction = False
        self.values = []
        self.varValues = []
        self.parentFunction = None

        # Auxiliares
        self.currentFunctionParams = []
        self.tuplesToModify = []
        self.allTypes = []
        self.inFunction = False
        self.opStack = []
        self.openList = False


    # ------ TYPES ------ #
    def p_insertType(self, p):
        self.type = p[1]
        self.allTypes.append(p[1])



    # ------ SCOPE ------ #
    def p_insertScope(self, scope):
        self.scope = scope



    # ------ FUNCTION PARAMETER ------ #
    # Esta función mete la variable parámetro en una pila para después
    # asociarlas con el nombre de la función, la cual llega al final
    def p_saveLocalVariable(self, p):
        if len(p) > 2 : self.currentFunctionParams.append(p[2])



    # ------ REGISTER FUNCTION PARAMETER ------ #
    # Esta función vaciará la pila con todas las variables locales de la
    # función a la vez que las registra como tal
    def p_registerLocalVariables(self, p):
        if len(p) > 2:
            functionName = p[2] ## functionParent
            # Empezamos el escaneo de la Symbol Table desde las variables
            # más recientes porque esas serán las de la función, así me guardo
            # procesamiento, creo que de lo mejor, O(1), creo. 
            stackLength = len(self.currentFunctionParams) - 1
            memoryLength = len(memory.symbolTable) - 1

            while stackLength > -1:
                # Sacamos la fila del symbol table con una variable local por actualizar
                currentRow = memory.symbolTable[memoryLength]
                # Actualizamos la columna "functionParent"
                index_to_change = 5
                currentRow = currentRow[:index_to_change] + (functionName,) + currentRow[index_to_change + 1:]
                # Ponemos la nueva fila de vuelta
                memory.symbolTable[memoryLength] = currentRow          
                
                memoryLength -= 1
                stackLength -= 1

            # Vaciamos la pila
            self.currentFunctionParams = []



    # ------ VARIABLES / IDs ------ #
    def p_insertID(self, p, isFunction):
        # El ID siempre tendrá que ser el primer TOKEN de p, lo buscamos
        for row in p:
            # Condicional respetando estructura de "p_vars" y "p_extra_vars" en Parser.py
            if row != None and row != ',':
                varName = row  # Por legibilidad, en vez de 'self.varName'

                # Si tiene brackets pegados, es una matriz
                # Separamos el nombre de sus dimensiones
                if "[" in varName:
                    # Separamos el nombre de las dimensiones
                    varNameIndex = varName.index('[')
                    varName = varName[:varNameIndex]

                    # Guardamos las dimensiones
                    indices = re.findall(r'\[(.*?)\]', row)
                    indices = [int(index) for index in indices]
                    self.varDimensions = indices

                self.varName = varName


                # SI YA EXISTE varName EN LA symbolTable, QUEBRAR PROGRAMA
                self.verifyVariableExistence(varName)


                # Si es una variable local, la anexamos con su función para facilitarme la vida después
                if self.scope == 'local' and varName not in self.currentFunctionParams: 
                    self.currentFunctionParams.append(varName)

                # Descubrí que para meter los values tendré que crear una pila que los separe por las comas
                # Ya que estoy leyendo esto de derecha a izquierda, arigato ozymndas

                
                # Separamos las variables en self.values con sus respectivas variables
                if self.values : topValue = self.values.pop()
                else : topValue = ','
                while topValue != ',' and topValue != '}' :
                    # Si es un signo de menos, juntarlo con el siguiente valor
                    if topValue == '-' : topValue = float(self.varValues.pop()) * -1

                    self.varValues.append(topValue)
                    if self.values : topValue = self.values.pop()
                    else : break
                
                # Antes de meter los values, conviene transformar sus elementos al type apropiado
                if self.type == 'int':
                    self.varValues = [int(num) for num in self.varValues]
                # Como ya llegan como floats... ignoramos ese caso
                # Con bools puede ser, x > 0 = True, x == 0 or x == -1 = False tal vez, gusto propio...

                # Por leerse de derecha a izquierda, ocupamos girarlos...
                self.varValues.reverse()

            
                # Pude hacerlo antes de lo anterior para "eficiencia", pero no podré enfocarme en limpieza aquí
                self.verifyMatrix()


                # Sacamos el type más actual, por si llegasen a ser parámetros
                # Al declarar multiples variables (e.g. int a, b, c ...) solo
                # se guarda un type a la vez, por ello esta pila allTypes
                if len(self.allTypes) > 0 : self.type = self.allTypes.pop()

                # Insertamos la data en forma de TUPLA a la Symbol Table
                memory.insertRow( (self.type, self.varName, self.varDimensions, self.scope, isFunction, self.parentFunction, self.varValues) )
                quadsConstructor.updateSymbolTable(memory.symbolTable) ## ! IMPORTANTE, permite dinamismo


                # Si llegamos a insertar una función, podemos de una vez contar sus variables
                if isFunction :
                    counter = len(memory.symbolTable) - 2  # Sabemos que estarán mero arriba, O(1)
                    iCount = 0   # ints adentro de la función (incluyo parámetros)
                    fCount = 0   # floats
                    bCount = 0   # bools
                    sCount = 0   # strings

                    while counter >= 0 :
                        # Solo es cuestión de contarlos ...
                        if memory.symbolTable[counter][5] == self.varName :
                            if memory.symbolTable[counter][0] == 'int' : iCount += 1
                            if memory.symbolTable[counter][0] == 'float' : fCount += 1
                            if memory.symbolTable[counter][0] == 'bool' : bCount += 1
                            if memory.symbolTable[counter][0] == 'str' : sCount += 1
                        
                        # Si ya no sigue un local, significa que ya concluyó la función
                        else:
                            iCount = str(iCount) + "i"
                            fCount = str(fCount) + "f"
                            bCount = str(bCount) + "b"
                            sCount = str(sCount) + "s"
                            # Actualizamos la row actual de la symbolTable
                            currentRow = memory.symbolTable.pop()
                            currentRow = currentRow + (tuple([iCount, fCount, bCount, sCount]),)
                            memory.insertRow(currentRow)
                            break

                        counter -= 1

                # Reseteamos auxiliares
                self.varValues = [] # Vaciamos los valores de esta variable para prestársela a la siguiente
                self.isFunction = False
                self.varDimensions = []
                self.parentFunction = None
                topValue = None

                # Al ya tener el ID/Valores, ignoramos lo que siga de la production rule
                break



    # ------ VALUES ------ #
    # Comas para separar los valores/listas de valores de cada variables
    def p_saveComma(self, p):
        self.values.append(p[1])


    # Si es un signo primero
    def p_saveSign(self, p):
        if p[1] == '-':
            self.values.append(p[1])


    # La super pila Operadores que guardará todos los tokens necesarios del programa
    # para las operaciones de los cuádruplos
    def p_saveToOpStack(self, p):
        if p[1] != None : self.opStack.append(p[1])
        else : self.opStack.append(';')


    # Si es un valor numérico o lista de
    def p_saveValue(self, p):
        # Si estamos en una lista, guardar cada elemento temporalmente
        if '{' not in str(p[1]) and '}' not in str(p[1]):
            self.values.append(p[1])

        # Si ya se va a cerrar la lista, cerramos este loop
        if len(p) > 2:
            if '}' in str(p[3]):
                self.values.append(p[3])

        """ elif '}' in str(p[4]): # Respecto a las production rules
                self.openList = False

        # Si no es valor de una lista/matriz, lo agregamos directamente
        if '{' in str(p[1]):
            self.openList = True  """ # Si el value viene dentro de "{}", será una lista de uno o más


    # ------ Verify Variable Existence (I decided to hang the program if so) ------ #
    # TODO - Mejorar con actualizar el value solo y solo si el scope es el mismo.
    def verifyVariableExistence(self, varName):
        for each_tuple in memory.symbolTable :
            if varName == each_tuple[1] :
                raise TypeError("Variable", varName, "already exists.")
                break


    # ------ Verify Matrix Size and Fill Empty Spots ------ #
    def verifyMatrix(self):
        matrixSize = reduce(operator.mul, self.varDimensions, 1)
        ## Condicional para validar el tamaño de matriz
        if len(self.varValues) > matrixSize : raise TypeError("Matrix", self.varName, "too large.")

        # Ahora sabemos que la matriz tiene un tamaño correcto, pero está llena?
        # Si el usuario no llenó todos los espacios, llenarlos con 'None'
        length_difference = matrixSize - len(self.varValues)
        if length_difference > 0 : 
            desired_value = None
            self.varValues = self.varValues + [desired_value] * length_difference
            # raise TypeError("Rellenar Matrix", self.varName, "con", length_difference, "Nones") # ! DEBUG
        

    def sortMatrix(self, p):
        # Si no, lo buscamos como tal
        i = 0   # I missed you, baby
        for tuple in memory.symbolTable:
            if p[1] == tuple[1]:
                sortedValues = sorted(tuple[6], key=lambda x: (x is None, x))
                # print(sortedValues)

                # Sacamos la fila del symbol table con la variable por actualizar
                currentRow = tuple
                # Actualizamos la columna "value"
                index_to_change = 6
                currentRow = currentRow[:index_to_change] + (sortedValues,)
                # Ponemos la nueva fila de vuelta
                memory.symbolTable[i] = currentRow
                # pprint.pprint(memory.symbolTable) # ! DEBUG
                break

            # Si llegamos a la última tupla y aún no existe la variable...
            if i == len(memory.symbolTable) - 1:
                raise TypeError('Variable ', p[1], ' not declared!')
            
            i += 1


    # ------ END PROGRAM ------ #
    def p_end_program(self):
        # Creo que con esta actualización nos aseguramos de tener las
        # asignaciones que le hayan cambiado el valor a una variable
        quadsConstructor.updateSymbolTable(memory.symbolTable)
        
        # print("Final Symbol Table: ") # ! DEBUGGER
        # pprint.pprint(memory.symbolTable) # ! DEBUGGER