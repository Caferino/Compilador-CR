"""
    Proyecto Final
    Autor: Óscar Antonio Hinojosa Salum A00821930
    Mayo 28 2023
    Compilador para lenguaje al estilo R/C++.

    --- VM / Virtual Machine / Máquina Virtual ---
"""

# ======================== Virtual Machine ======================== #

from functools import reduce
import pprint
import copy
import re

class VirtualMachine:
    def __init__(self):
        self.memorySize = 500 # ! MUY IMPORTANTE CUIDAR ESTO, SI SALE "IndexError: list assignment index out of range" PUEDE SER AQUI
        self.registers = [None] * self.memorySize
        self.registers[0] = "GOTO MAIN"
        self.functionJumps = []
        self.program_counter = 0
        self.quadruples = []
        self.symbolTable = []
        self.recursiveTable = [] # Oh boy
        self.recursiveIteration = 0
        self.recursiveResult = 0
        self.returns = []
        self.recursiveRegisters = []


    def start(self, quadruples, newSymbolTable):
        self.quadruples = quadruples
        self.symbolTable = newSymbolTable
        self.run()


    def run(self):
        '''
        Input: Cuádruplos en forma de tuplas tipo:
            [operador, operandoIzquierdo, operandoDerecho, dondeInsertarResultado]

        Output: Resultados del programa.
        '''
        
        while self.program_counter < len(self.quadruples):
            quadruple = self.quadruples[self.program_counter]
            operator, operand1, operand2, target = quadruple

            # Qué asco ya sé, una búsqueda lineal O(n) por cada operando que sea una variable...
            # Si nuestro resultado será un espacio temporal, lo "hacemos" índice (t1 = 1, t82 = 82, ...)
            # "t0", al "no existir", lo dejé reservado para el GOTO MAIN por si acaso y mientras
            isTargetTemp = False   # Exclusivo para los returns
            if isinstance(target, str) and re.match(r"^t\d+$", target) :
                isTargetTemp = True
                target = int(target[1:])
                # self.registers.append(target) # What??
                
            isOperand1Str = isinstance(operand1, str)
            isOperand2Str = isinstance(operand2, str)

            # Si nuestro operando izquierdo es un espacio temporal ...
            if isOperand1Str and re.match(r"^t\d+$", operand1) and operator != 'GOSUB' : 
                if len(self.recursiveRegisters) > 0 : operand1 = self.recursiveRegisters[-1][int(operand1[1:])]
                else : operand1 = self.registers[int(operand1[1:])]
            # Si no, debe ser un ID cuyo valor debemos sacar de la SymbolTable
            elif isOperand1Str :
                foundRecursiveVar = False
                if self.recursiveIteration > 0:
                    table = self.recursiveTable[-1]
                    for tuple in table :
                        if operand1 == tuple[1] :
                            foundRecursiveVar = True
                            # Si es una lista de un solo elemento, sacarlo
                            if isinstance(tuple[6], list) and len(tuple[6]) == 1 : operand1 = tuple[6][0]
                            # Si sufrió alguna actualización antes de aquí, lo más seguro es
                            # que ya no es una lista de un elemento, sino número o string ...
                            else : operand1 = tuple[6]
                            break
                if not foundRecursiveVar:
                    for tuple in self.symbolTable :
                        if operand1 == tuple[1] :
                            # Si es una lista de un solo elemento, sacarlo
                            if isinstance(tuple[6], list) and len(tuple[6]) == 1 : operand1 = tuple[6][0]
                            # Si sufrió alguna actualización antes de aquí, lo más seguro es
                            # que ya no es una lista de un elemento, sino número o string ...
                            else : operand1 = tuple[6]
                            break

            # Para lidiar con condicionales, el problema de bool() es que si es una string
            # con valor de 'False' la convierte a un booleano True porque lo que checa es que
            # la string está vacía o no. El que nos interesa es eval(), pero solo funciona con
            # strings; no importa si usamos bool() para valores numéricos
            if operand1 == 'True' or operand1 == "False" :
                operand1 = eval(operand1)

            # Si nuestro operando derecho es un espacio temporal ...
            if isOperand2Str and re.match(r"^t\d+$", operand2) and operator != 'GOSUB' : 
                if len(self.recursiveRegisters) > 0 : operand2 = self.recursiveRegisters[-1][int(operand2[1:])]
                else : operand2 = self.registers[int(operand2[1:])]
            # Si no, debe ser un ID cuyo valor debemos sacar de la SymbolTable
            elif isOperand2Str:
                foundRecursiveVar = False
                if self.recursiveIteration > 0:
                    table = self.recursiveTable[-1]
                    for tuple in table :
                        if operand2 == tuple[1] :
                            foundRecursiveVar = True
                            # Si es una lista de un elemento, sacarlo
                            if isinstance(tuple[6], list) : operand2 = tuple[6][0]
                            else : operand2 = tuple[6]
                            break
                if not foundRecursiveVar:
                    for tuple in self.symbolTable :
                        if operand2 == tuple[1] :
                            # Si es una lista de un elemento, sacarlo
                            if isinstance(tuple[6], list) : operand2 = tuple[6][0]
                            else : operand2 = tuple[6]
                            break

            if operand2 == 'True' or operand2 == "False" :
                operand2 = eval(operand2)

            if operand1 == None : operand1 = 1
            if operand2 == None : operand2 = 1
            
            

            # ======= REGISTERS ========
            if operator == '+':
                if len(self.recursiveRegisters) > 0 : self.recursiveRegisters[-1][target] = operand1 + operand2
                else : self.registers[target] = operand1 + operand2
            elif operator == '-':
                if len(self.recursiveRegisters) > 0 : self.recursiveRegisters[-1][target] = operand1 - operand2
                else : self.registers[target] = operand1 - operand2
            elif operator == '*':
                if len(self.recursiveRegisters) > 0 : self.recursiveRegisters[-1][target] = operand1 * operand2
                else : self.registers[target] = operand1 * operand2
            elif operator == '**':
                if len(self.recursiveRegisters) > 0 : self.recursiveRegisters[-1][target] = operand1 ** operand2
                else : self.registers[target] = operand1 ** operand2
            elif operator == '/':
                if len(self.recursiveRegisters) > 0 : self.recursiveRegisters[-1][target] = operand1 / operand2
                else : self.registers[target] = operand1 / operand2
            elif operator == '>':
                if len(self.recursiveRegisters) > 0 : self.recursiveRegisters[-1][target] = int(operand1 > operand2)
                else : self.registers[target] = int(operand1 > operand2)
            elif operator == '<':
                if len(self.recursiveRegisters) > 0 : self.recursiveRegisters[-1][target] = int(operand1 < operand2)
                else : self.registers[target] = int(operand1 < operand2)
            elif operator == '<=':
                if len(self.recursiveRegisters) > 0 : self.recursiveRegisters[-1][target] = int(operand1 <= operand2)
                else : self.registers[target] = int(operand1 <= operand2)
            elif operator == '==':
                if len(self.recursiveRegisters) > 0 : self.recursiveRegisters[-1][target] = bool(operand1) == bool(operand2)
                else : self.registers[target] = bool(operand1) == bool(operand2)
            elif operator == '!=' or operator == '<>':
                if len(self.recursiveRegisters) > 0 : self.recursiveRegisters[-1][target] = bool(operand1) != bool(operand2)
                else : self.registers[target] = bool(operand1) != bool(operand2)
            if operator == '&&':
                if len(self.recursiveRegisters) > 0 : self.recursiveRegisters[-1][target] = bool(operand1) and bool(operand2)
                else : self.registers[target] = bool(operand1) and bool(operand2)
            if operator == '||':
                if len(self.recursiveRegisters) > 0 : self.recursiveRegisters[-1][target] = bool(operand1) or bool(operand2)
                else : self.registers[target] = bool(operand1) or bool(operand2)
            elif operator == '=' or operator == '<-':
                # Si es un string, es porque a fuerza es un ID ...
                if target.__class__.__name__ == 'str' :
                    # En caso de estar en una función cualquiera, verificar la variable en su memoria exclusiva/recursiva
                    foundRecursiveVar = False
                    if self.recursiveIteration > 0:
                        table = copy.deepcopy(self.recursiveTable.pop()) # [-1], Pop y append no funcionaron, esta libreria fue obligatoria
                        for i, tuple_item in enumerate(table):
                            if target == tuple_item[1]:
                                foundRecursiveVar = True
                                currentRow = table[i]
                                # Actualizamos la columna "value"
                                index_to_change = 6
                                currentRow = currentRow[:index_to_change] + (operand1,)
                                table[i] = currentRow
                                # En caso de haberse transformado de INT a FLOAT, actualizar TYPE
                                if currentRow[0] != operand1.__class__.__name__ :
                                    currentRow = (operand1.__class__.__name__,) + currentRow[1:]
                                    table[i] = currentRow
                        self.recursiveTable.append(table) # Esto fue lo que resolvió la recursión compleja, me llevó días
                    # Si no se encontró alguna varible en la tabla recursiva, es porque es global o ni siquiera estamos en una función
                    if not foundRecursiveVar:
                        for i, tuple_item in enumerate(self.symbolTable):
                            if target == tuple_item[1]:
                                currentRow = self.symbolTable[i]
                                # Actualizamos la columna "value"
                                index_to_change = 6
                                currentRow = currentRow[:index_to_change] + (operand1,)
                                self.symbolTable[i] = currentRow
                                # En caso de haberse transformado de INT a FLOAT, actualizar TYPE
                                if currentRow[0] != operand1.__class__.__name__ :
                                    currentRow = (operand1.__class__.__name__,) + currentRow[1:]
                                    self.symbolTable[i] = currentRow
                # Si no, es el index de un espacio temporal
                else:
                    if len(self.recursiveRegisters) > 0 : self.recursiveRegisters[-1][target] = operand1
                    else : self.registers[target] = operand1
            elif operator.lower() == 'goto':
                self.program_counter = target
                continue
            elif operator.lower() == 'gotof':
                if operand1 == 'False' or operand1 == 0 : self.program_counter = target
                else : self.program_counter += 1
                continue
            elif operator.lower() == 'gotov':
                # Aquí se me ocurrió cambiar el chequeo de booleanos igual a Python o C++ :
                # if num != 0 = TRUE, else FALSE no matter what
                if operand1 == 'True' or operand1 != 0 : self.program_counter = target
                else : self.program_counter += 1
                continue
            elif operator.lower() == 'print':
                if isinstance(operand1, list):
                    for index, element in enumerate(operand1) :
                        if isinstance(element, str) and re.match(r"^t\d+$", element) : 
                            if len(self.recursiveRegisters) > 0 : operand1[index] = str(self.recursiveRegisters[-1][int(element[1:])])
                            else : operand1[index] = str(self.registers[int(element[1:])])
                        elif isinstance(element, str) and '"' not in element and "'" not in element :
                            # En caso de estar en una función cualquiera, verificar la variable en su memoria exclusiva/recursiva
                            foundRecursiveVar = False
                            if self.recursiveIteration > 0:
                                table = self.recursiveTable[-1]
                                for i, tuple_item in enumerate(table):
                                    if element == tuple_item[1]:
                                        foundRecursiveVar = True
                                        operand1[index] = str(tuple_item[6])
                            # Si no se encontró alguna variable en la tabla recursiva, es porque es global o ni siquiera estamos en una función
                            if not foundRecursiveVar:
                                for i, tuple_item in enumerate(self.symbolTable):
                                    if element == tuple_item[1]:
                                        operand1[index] = str(tuple_item[6])
                        elif '"' in element :
                            operand1[index] = element.strip('"')
                        elif "'" in element :
                            operand1[index] = element.strip("'")
                                        
                    operand1 = " ".join(reversed(operand1))
                print(operand1.strip('"')) if operand1.__class__.__name__ == 'str' else print(operand1)
            elif operator.lower() == 'gosub':
                self.program_counter = target
                self.functionJumps.append(operand2)
                self.returns.append(operand1)
                continue
            elif operator.lower() == 'endfunc' or operator.lower() == 'return':
                if operator.lower() == 'return' :
                    temporal = int(self.returns.pop()[1:])
                    # Tu mete el target al maldito tn que sea, checa que no metas un string o char, y el pop
                    if target.__class__.__name__ == 'str' or target.__class__.__name__ == 'char' :
                        # En caso de estar en una función cualquiera, verificar la variable en su memoria exclusiva/recursiva
                        foundRecursiveVar = False
                        if self.recursiveIteration > 0:
                            table = self.recursiveTable[-1]
                            for i, tuple_item in enumerate(table):
                                if target == tuple_item[1]:
                                    foundRecursiveVar = True
                                    if len(self.recursiveRegisters) > 1 : self.recursiveRegisters[-2][temporal] = tuple_item[6]
                                    else : self.registers[temporal] = tuple_item[6]
                                    self.recursiveResult += tuple_item[6] # ! DEBUGGER
                        # Si no se encontró alguna variable en la tabla recursiva, es porque es global o ni siquiera estamos en una función
                        if not foundRecursiveVar:
                            for i, tuple_item in enumerate(self.symbolTable):
                                if target == tuple_item[1]:
                                    self.registers[temporal] = tuple_item[6]
                                    if tuple_item[6] == 1 : self.recursiveResult += tuple_item[6] # ! DEBUGGER
                    elif isTargetTemp:
                        if len(self.recursiveRegisters) > 1 : self.recursiveRegisters[-2][temporal] = self.recursiveRegisters[-1][target]
                        else : self.registers[temporal] = self.recursiveRegisters[-1][target]
                    else:
                        if len(self.recursiveRegisters) > 1 : self.recursiveRegisters[-2][temporal] = target
                        else : self.registers[temporal] = target
                    
                self.recursiveIteration -= 1
                self.recursiveTable.pop()
                self.recursiveRegisters.pop()
                if self.functionJumps : 
                    self.program_counter = self.functionJumps.pop()
                    continue
                # PJumps...
                # Hacer el salto a la linea en la que estaba...
            elif operator.lower() == 'endprog':
                if operand1:
                    print("v v v v v v    === DEBUGGING ===    v v v v v v")
                    print("-------------- === Final Quadruples === --------------")
                    for i, item in enumerate(self.quadruples):
                        print(f"{i}: {item}")
                    print("-------------- === Final Symbol Table (Updated Values) === --------------")
                    pprint.pprint(self.symbolTable)
                # print('Registers:', self.registers)   # It's so big
                # print('Recursive Registers:', self.recursiveRegisters)   # Should always be empty
                # print('Recursive Result:', self.recursiveResult)   # Can check if a recursive module branchs out well
                print('Compilation Completed')
            elif operator.lower() == 'era':
                self.recursiveIteration += 1
                if self.recursiveIteration > 1 and self.recursiveTable :
                    self.recursiveTable.append(self.recursiveTable[-1].copy())
                    self.recursiveRegisters.append(self.registers.copy())   # Encontrar estos .copy() me hizo demasiado daño
                else :
                    self.recursiveResult = 0
                    self.recursiveTable.append([entry for entry in self.symbolTable if entry[5] == target].copy())
                    self.recursiveRegisters.append(self.registers.copy())

            self.program_counter += 1