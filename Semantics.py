"""
    Proyecto Final
    Autor: Óscar Antonio Hinojosa Salum A00821930
    Abril 15 2023
    Compilador para lenguaje al estilo R/C++.

    --- Reglas de Semántica ---
"""

# ======================== Semántica ======================== #

from sklearn.linear_model import LinearRegression
from Plotter import plotThis
from functools import reduce # Para multiplicar listas y matrices
import numpy as np
import statistics
import operator
import re                    # Librería para expresiones regulares RegEX
#import pprint               # Para debugging, (opcional)

from Quadruples import quadsConstructor

from Memory import MemoryMap
memory = MemoryMap()

class Rules:
    def __init__(self):
        """
        * - * - * - * - * - * - * - * - * - * - * - * - * - *
        *                   DEBUG MODE                      *
        * - * - * - * - * - * - * - * - * - * - * - * - * - *
        ?     Set to True to turn it on, otherwise False    ?
        """
        self.debugMode = True
        
        ##### Variables
        self.type = ''
        self.varName = ''
        self.varDimensions = []
        self.scope = 'global'
        self.isFunction = False
        self.values = []
        self.varValues = []
        self.parentFunction = None
        self.parentFunctionType = None
        self.localVariables = []
        self.parameters = {}
        self.parameterscont = 1
        self.localVarCounters = {'int': 0, 'float': 0, 'bool': 0, 'string': 0}
        #### Auxiliares
        self.currentFunctionParams = []
        self.tuplesToModify = []
        self.allTypes = []
        self.opStack = []
        self.openList = False


    # ========================================================================================================
    # * ======================================= INSERTIONS & MORE ========================================== *
    # ========================================================================================================
    # ------ Aumentar cantidad total de líneas de código ------ #
    def p_addCodeLine(self):
        memory.totalCodeLines += 1
        
        
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
        
        # Si ya existe varName en la symbolTable, quebrar programa
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
        self.values.append(p[1])


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
        self.parameters[self.parameterscont] = (self.type, self.varName)
        self.parameterscont += 1
        
        
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
            updated_tuple = (*memory.symbolTable[index][:6], self.localVarCounters, quadsConstructor.cont + 1, self.parameters)
            memory.symbolTable[index] = updated_tuple
            
        self.localVarCounters = {'int': 0, 'float': 0, 'bool': 0, 'string': 0}
        self.parameters = {}
        self.parameterscont = 1
        
    
    
    # ========================================================================================================
    # * ======================================= UPDATE SYMBOLTABLE ========================================= *
    # ========================================================================================================
    def p_updateSymbolTable(self):
        # Separamos las variables en self.values con sus respectivas variables
        self.p_extractVarValues()
        
        # Verificamos que sea una matriz con tamaño válido, si no, romper programa
        self.p_verifyMatrix()
            
        # self.type, self.varName, self.varDimensions, self.scope, isFunction, self.parentFunction, self.varValues
        memory.insertRow( (self.type, self.varName, self.varDimensions, self.scope, self.isFunction, self.parentFunction, self.varValues) )
        quadsConstructor.updateSymbolTable(memory.symbolTable)   # ! IMPORTANTE, permite dinamismo
        
        # === New SymbolTable Row ===
        self.varValues = []
        self.varDimensions = []
        self.isFunction = False
        
        
    # ------------------------------------- FUNCTION ID
    def p_insertFunction(self):
        memory.insertRow( (self.type, self.varName, self.varDimensions, self.scope, self.isFunction, self.parentFunction, self.varValues) )
        quadsConstructor.updateSymbolTable(memory.symbolTable)   # ! IMPORTANTE, permite dinamismo
        self.parentFunction = self.varName
        self.parentFunctionType = self.type
        
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
        
    
    # ------------------------------------- VERIFY VARIABLE EXISTENCE
    def verifyVariableExistence(self, varName):
        for each_tuple in memory.symbolTable :
            if varName == each_tuple[1] and self.parentFunction == each_tuple[5]:
                raise TypeError(f"Variable '{varName}' already exists! - line {memory.totalCodeLines}")
                break
            
            
    # ------------------------------------- VERIFY MATRIX SIZE AND FILL EMPTY SPOTS
    def p_verifyMatrix(self):
        matrixSize = reduce(operator.mul, self.varDimensions, 1)
        ## Condicional para validar el tamaño de matriz
        if len(self.varValues) > matrixSize : raise TypeError(f"Matrix '{self.varName}' too large! - line {memory.totalCodeLines}")

        # Ahora sabemos que la matriz tiene un tamaño correcto, pero está llena?
        # Si el usuario no llenó todos los espacios, llenarlos con 'None'
        length_difference = matrixSize - len(self.varValues)
        if length_difference > 0 : 
            desired_value = None
            self.varValues = self.varValues + [desired_value] * length_difference
            
            
    # ========================================================================================================
    # * ============================================= EXTRAS =============================================== *
    # ========================================================================================================
    
    # ------------------------------------- SORT MATRIX 
    def sortMatrix(self, p):
        i = 0
        for tuple in memory.symbolTable:
            if p[1] == tuple[1]:
                sortedValues = sorted(tuple[6], key=lambda x: (x is None, x))

                # Sacamos la fila del symbol table con la variable por actualizar
                currentRow = tuple
                # Actualizamos la columna "value"
                index_to_change = 6
                currentRow = currentRow[:index_to_change] + (sortedValues,)
                # Ponemos la nueva fila de vuelta
                memory.symbolTable[i] = currentRow
                break
            # Si llegamos a la última tupla y aún no existe la variable...
            if i == len(memory.symbolTable) - 1:
                raise TypeError(f"Variable '{p[1]}' not declared! - line {memory.totalCodeLines}")
            i += 1
            
            
    # ------------------------------------- MEDIA
    def media(self, p):
        i = 0
        for tuple in memory.symbolTable:
            if p[3] == tuple[1]:
                media = sum(tuple[6]) / len(tuple[6])
                quadsConstructor.PTypes.append(tuple[0]) # Value's type
                quadsConstructor.PilaO.append(media) # Value
                quadsConstructor.POper.append(p[1]) # 'MEDIA'
                break
            # Si llegamos a la última tupla y aún no existe la variable...
            if i == len(memory.symbolTable) - 1:
                raise TypeError(f"Variable '{p[3]}' not declared! - line {memory.totalCodeLines}")
            i += 1
            
            
    # ------------------------------------- MODA
    def moda(self, p):
        i = 0
        for tuple in memory.symbolTable:
            if p[3] == tuple[1]:
                mode = statistics.mode(tuple[6])
                quadsConstructor.PTypes.append(tuple[0]) # Value's type
                quadsConstructor.PilaO.append(mode) # Value
                quadsConstructor.POper.append(p[1]) # 'MODA'
                break
            # Si llegamos a la última tupla y aún no existe la variable...
            if i == len(memory.symbolTable) - 1:
                raise TypeError(f"Variable '{p[3]}' not declared! - line {memory.totalCodeLines}")
            i += 1
            
            
    # ------------------------------------- MEDIANA
    def mediana(self, p):
        i = 0
        for tuple in memory.symbolTable:
            if p[3] == tuple[1]:
                median = statistics.median(tuple[6])
                quadsConstructor.PTypes.append(tuple[0]) # Value's type
                quadsConstructor.PilaO.append(median) # Value
                quadsConstructor.POper.append(p[1]) # 'MEDIANA'
                break
            # Si llegamos a la última tupla y aún no existe la variable...
            if i == len(memory.symbolTable) - 1:
                raise TypeError(f"Variable '{p[3]}' not declared! - line {memory.totalCodeLines}")
            i += 1
            
            
    # ------------------------------------- VARIANZA
    def varianza(self, p):
        i = 0
        for tuple in memory.symbolTable:
            if p[3] == tuple[1]:
                variance = statistics.variance(tuple[6])
                quadsConstructor.PTypes.append(tuple[0]) # Value's type
                quadsConstructor.PilaO.append(variance) # Value
                quadsConstructor.POper.append(p[1]) # 'VARIANZA'
                break
            # Si llegamos a la última tupla y aún no existe la variable...
            if i == len(memory.symbolTable) - 1:
                raise TypeError(f"Variable '{p[3]}' not declared! - line {memory.totalCodeLines}")
            i += 1
            
            
    # ------------------------------------- REGRESIÓN SIMPLE
    def regsim(self, p):
        i = 0   # I missed you, baby
        x = None
        y = None
        for tuple in memory.symbolTable:
            if p[3] == tuple[1]:
                x = tuple[6]
            if p[5] == tuple[1]:
                y = tuple[6]

            # Si llegamos a la última tupla y aún no existe la variable...
            if i == len(memory.symbolTable) - 1:
                if x == None :
                    raise TypeError(f"Variable '{p[3]}' not declared! - line {memory.totalCodeLines}")
                elif y == None :
                    raise TypeError(f"Variable '{p[5]}' not declared! - line {memory.totalCodeLines}")
            
            i += 1
        x = np.array(x).reshape(-1, 1)
        y = np.array(y)
        # Create and fit data into a linear regression model
        model = LinearRegression()
        model.fit(x, y)
        # Predict the value given by the user
        var = p[7]
        # En caso de ser un ID...
        if var.__class__.__name__ == 'str' :
            # En caso de ser una matriz, sacamos la dirección del valor
            if '[' in var :
                # Separamos el nombre de las dimensiones
                varIndex = var.index('[')
                var = var[:varIndex]

                # Guardamos la/s dimension/es
                indices = re.findall(r'\[(.*?)\]', p[7])
                indices = [int(index) for index in indices]
                if len(indices) == 1 : column = indices[0] - 1
                elif len(indices) == 2 : row, column = indices
                elif len(indices) == 3 : depth, row, column = indices
                
                # Lo buscamos en la symbolTable
                for tuple in memory.symbolTable :
                    if var == tuple[1] :
                        if len(indices) == 1 :
                            valueAddress = column
                        elif len(indices) == 2 :
                            num_columns = tuple[2][1]
                            valueAddress = (row - 1) * num_columns + (column - 1)
                        elif len(indices) == 3 :
                            num_rows = tuple[2][0]
                            num_columns = tuple[2][1]
                            valueAddress = (depth - 1) * (num_rows * num_columns) + (row - 1) * num_columns + (column - 1)
                        var = tuple[6][valueAddress]
                        break
                    elif tuple == memory.symbolTable[-1] :
                        raise TypeError(f"Variable '{p[7]}' doesn't exist!")
                    
            else :
                for tuple in memory.symbolTable :
                    if var == tuple[1] :
                        var = tuple[6][0]
        
        new_value = var
        predicted_value = float(model.predict(np.array([[new_value]])))
        quadsConstructor.PTypes.append('float') # Value's type
        quadsConstructor.PilaO.append(predicted_value) # Value
        quadsConstructor.POper.append(p[1]) # 'REGSIM'
        
        
    # ------------------------------------- PLOTTER
    def plot(self, p):
        i = 0
        x = None
        y = None
        for tuple in memory.symbolTable:
            if p[3] == tuple[1]:
                x = tuple[6]
            if p[5] == tuple[1]:
                y = tuple[6]
            # Si llegamos a la última tupla y aún no existe la variable...
            if i == len(memory.symbolTable) - 1:
                if x == None :
                    raise TypeError(f"Variable '{p[3]}' not declared! - line {memory.totalCodeLines}")
                elif y == None :
                    raise TypeError(f"Variable '{p[5]}' not declared! - line {memory.totalCodeLines}")
            i += 1
        plotThis(x, y)


    # ========================================================================================================
    # ! =========================================== END PROGRAM ============================================ ! 
    # ========================================================================================================
    def p_end_program(self):
        # Creo que con esta actualización nos aseguramos de tener las
        # asignaciones que le hayan cambiado el valor a una variable
        quadsConstructor.updateSymbolTable(memory.symbolTable)
        quadsConstructor.generateQuadruple('ENDPROG', self.debugMode, '', '')