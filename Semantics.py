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
import statistics
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
        self.localVariables = []
        self.localVarCounters = {'int': 0, 'float': 0, 'bool': 0, 'string': 0}


        
        
        # -- Old
        # Auxiliares
        self.currentFunctionParams = []
        self.tuplesToModify = []
        self.allTypes = []
        self.inFunction = False
        self.opStack = []
        self.openList = False


    # ------------------------------------- TYPES
    def p_insertType(self, p):
        self.type = p[1]
        
        
    # ------------------------------------- ID
    def p_insertID(self, p):
        varName = p[1]
        
        # Si tiene brackets pegados, es una matriz
        if "[" in varName:
            # Separamos el nombre de las dimensiones
            indices = re.findall(r'\[(.*?)\]', varName)
            indices = [int(index) for index in indices]
            self.varDimensions = indices
            varNameIndex = varName.index('[')
            varName = varName[:varNameIndex]
        
        # SI YA EXISTE varName EN LA symbolTable, QUEBRAR PROGRAMA
        self.verifyVariableExistence(varName)
        self.varName = varName
        
        
        
    # ------------------------------------- SCOPE
    def p_insertScope(self, scope):
        self.scope = scope
        
        
    # ------------------------------------- IS FUNCTION
    def p_isFunction(self):
        self.isFunction = True
        

    # ------------------------------------- SAVE VALUE
    def p_saveValue(self, p):
        # Si estamos en una lista, guardar cada elemento temporalmente
        if '{' not in str(p[1]) and '}' not in str(p[1]):
            self.values.append(p[1])

        # Si ya se va a cerrar la lista, cerramos este loop
        if len(p) > 2:
            if '}' in str(p[3]):
                self.values.append(p[3])


    # ------------------------------------- SAVE COMMA
    def p_saveComma(self, p):
        self.values.append(p[1])


    # ------------------------------------- SAVE SIGN
    def p_saveSign(self, p):
        if p[1] == '-':
            self.values.append(p[1])
        
        
    # ------------------------------------- SAVE LOCAL VARIABLE  
    def p_saveLocalVariable(self):
        self.localVariables.append(self.type)
        
        
    # ------------------------------------- REGISTER LOCAL VARIABLES
    def p_registerLocalVariables(self):
        while self.localVariables :
            currentVar = self.localVariables.pop()
            
            if currentVar == 'int':
                self.localVarCounters['int'] += 1
            elif currentVar == 'float':
                self.localVarCounters['float'] += 1
            elif currentVar == 'bool':
                self.localVarCounters['bool'] += 1
            elif currentVar == 'string':
                self.localVarCounters['string'] += 1
                
        # Find the index of the tuple for parentFunction in the list
        index = -1
        for i, item in enumerate(memory.symbolTable):
            if item[1] == self.parentFunction:
                index = i
                break
            
        if index != -1:
            updated_tuple = (*memory.symbolTable[index][:6], self.localVarCounters)
            memory.symbolTable[index] = updated_tuple
            
        self.localVarCounters = {'int': 0, 'float': 0, 'bool': 0, 'string': 0}
        
    
    
    # ========================================================================================================
    # * ======================================= UPDATE SYMBOLTABLE ========================================= *
    # ========================================================================================================
    def p_updateSymbolTable(self):
        # Separamos las variables en self.values con sus respectivas variables
        self.p_extractVarValues()
        
        # Verificmos que sea una matriz con tamaño válido, si no romper programa
        self.p_verifyMatrix()
            
        # self.type, self.varName, self.varDimensions, self.scope, isFunction, self.parentFunction, self.varValues
        memory.insertRow( (self.type, self.varName, self.varDimensions, self.scope, self.isFunction, self.parentFunction, self.varValues) )
        quadsConstructor.updateSymbolTable(memory.symbolTable) ## ! IMPORTANTE, permite dinamismo
        
        # === New SymbolTable Row ===
        self.varValues = []
        self.varDimensions = []
        self.isFunction = False
        topValue = None
        
        
    # ------------------------------------- FUNCTION ID
    def p_insertFunction(self):
        memory.insertRow( (self.type, self.varName, self.varDimensions, self.scope, self.isFunction, self.parentFunction, self.varValues) )
        self.parentFunction = self.varName
        
        # === RESET ===
        self.isFunction = False


    # ------------------------------------- EXTRACT VAR VALUES
    def p_extractVarValues(self):
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
            self.varValues = [int(num) for num in self.varValues if num is not None and not isinstance(num, str)]
            
        # Por leerse de derecha a izquierda, ocupamos girarlos...
        self.varValues.reverse()
            
        # TODO : If array of bools, change to 1 or 0s or True or False ! Might be useless, I think 0 = False, and >0 = True in my VM
        
    
    # ------------------------------------- VERIFY VAR EXISTENCE
    # TODO - Mejorar con actualizar el value solo y solo si el scope es el mismo.
    def verifyVariableExistence(self, varName):
        for each_tuple in memory.symbolTable :
            if varName == each_tuple[1] :
                raise TypeError("Variable", varName, "already exists.")
                break
            
            
    # ------------------------------------- VERIFY MATRIX SIZE AND FILL EMPTY SPOTS
    def p_verifyMatrix(self):
        matrixSize = reduce(operator.mul, self.varDimensions, 1)
        ## Condicional para validar el tamaño de matriz
        print("Variable:", self.varName)
        print("varValues:", self.varValues)
        print("varDimensions:", self.varDimensions)
        if len(self.varValues) > matrixSize : raise TypeError("Matrix", self.varName, "too large.")

        # Ahora sabemos que la matriz tiene un tamaño correcto, pero está llena?
        # Si el usuario no llenó todos los espacios, llenarlos con 'None'
        length_difference = matrixSize - len(self.varValues)
        if length_difference > 0 : 
            desired_value = None
            self.varValues = self.varValues + [desired_value] * length_difference
            # raise TypeError("Rellenar Matrix", self.varName, "con", length_difference, "Nones") # ! DEBUG
            
            
    # ========================================================================================================
    # * ============================================= EXTRAS =============================================== *
    # ========================================================================================================
    
    # ------------------------------------- SORT MATRIX 
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
            
            
    # ------------------------------------- MEDIA
    def media(self, p):
        i = 0   # I missed you, baby
        for tuple in memory.symbolTable:
            if p[3] == tuple[1]:
                media = sum(tuple[6]) / len(tuple[6])
                quadsConstructor.PTypes.append(tuple[0]) # Value's type
                quadsConstructor.PilaO.append(media) # Value
                quadsConstructor.POper.append(p[1]) # 'MEDIA'
                break

            # Si llegamos a la última tupla y aún no existe la variable...
            if i == len(memory.symbolTable) - 1:
                raise TypeError('Variable ', p[3], ' not declared!')
            
            i += 1
            
            
    # ------------------------------------- MODA
    def moda(self, p):
        i = 0   # I missed you, baby
        for tuple in memory.symbolTable:
            if p[3] == tuple[1]:
                mode = statistics.mode(tuple[6])
                quadsConstructor.PTypes.append(tuple[0]) # Value's type
                quadsConstructor.PilaO.append(mode) # Value
                quadsConstructor.POper.append(p[1]) # 'MODA'
                break

            # Si llegamos a la última tupla y aún no existe la variable...
            if i == len(memory.symbolTable) - 1:
                raise TypeError('Variable ', p[3], ' not declared!')
            
            i += 1
            
            
    # ------------------------------------- MEDIANA
    def mediana(self, p):
        i = 0   # I missed you, baby
        for tuple in memory.symbolTable:
            if p[3] == tuple[1]:
                mode = statistics.median(tuple[6])
                quadsConstructor.PTypes.append(tuple[0]) # Value's type
                quadsConstructor.PilaO.append(mode) # Value
                quadsConstructor.POper.append(p[1]) # 'MODA'
                break

            # Si llegamos a la última tupla y aún no existe la variable...
            if i == len(memory.symbolTable) - 1:
                raise TypeError('Variable ', p[3], ' not declared!')
            
            i += 1


    # ========================================================================================================
    # ! =========================================== END PROGRAM ============================================ ! 
    # ========================================================================================================
    def p_end_program(self):
        # Creo que con esta actualización nos aseguramos de tener las
        # asignaciones que le hayan cambiado el valor a una variable
        quadsConstructor.updateSymbolTable(memory.symbolTable)
        
        print("Final Quadruples: ") # ! DEBUGGER
        pprint.pprint(quadsConstructor.quadruples) # ! DEBUGGER
        print("Final Symbol Table: ") # ! DEBUGGER
        pprint.pprint(memory.symbolTable) # ! DEBUGGER