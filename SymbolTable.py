# Tuve que crear este interface por un error que cometí, de hacer Semantics.py
# dependiente de Quadruples.py. Semantics.py poseía la symbolTable que necesitaba
# llamar en Quadruples.py, pero no puedo importar librerías que dependen de sí.

class SymbolTable:
    symbolTable = []

    def updateSymbolTable(newSymbolTable):
        symbolTable = newSymbolTable