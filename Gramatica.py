class Gramatica():
    def __init__(self,nombre,no_terminal,terminal,inicial,producciones):
        self.nombre = nombre
        self.no_terminal = no_terminal
        self.terminal = terminal
        self.inicial = inicial
        self.producciones = producciones