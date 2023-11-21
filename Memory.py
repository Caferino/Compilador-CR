"""
    Proyecto Final
    Autor: Óscar Antonio Hinojosa Salum A00821930
    Abril 15 2023
    Compilador para lenguaje al estilo R/C++.

    --- Memoria para la Symbol Table ---
"""

# ======================== Memoria ======================== #

class MemoryMap:
    def __init__(self):
        # self.memory = [None] * size
        self.quadruples = []
        self.symbolTable = []
        self.totalCodeLines = 1
        

    """
        !insertRow
        * Inserta una nueva tupla a la symbolTable
        ? @param new_row Con formato (type, name)
    """
    def insertRow(self, new_row):
        # Si la Symbol Table está vacía, insertar row sí o sí
        if not self.symbolTable:
            self.symbolTable.append(new_row)

        # Si la Symbol Table NO está vacía, verificar existencia de la variable primero
        else:
            found = False
            for each_tuple in self.symbolTable:
                # Si la variable ya existe, actualizamos solo el value
                print('DEBUG EXIST', new_row[1], 'vs', each_tuple[1], 'PARENT:', new_row[5], 'vs', each_tuple[5])
                if new_row[1] == each_tuple[1] and new_row[5] == each_tuple[5]:
                    found = True
                    break

            # Si la variable aún no existe, insertarla
            if not found:
                self.symbolTable.append(new_row)