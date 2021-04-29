from Gramatica import Gramatica
gramaticas = []

def automata(archivo):
    global gramaticas
    print('entro al automata')
    archivo = open(archivo,"r")
    state = 0
    libreContexto = False
    nombreterminal = ''
    nombre = ''
    no_terminal = []
    terminal = []
    inicial = ''
    producciones = []
    while (True):
        linea = archivo.readline()
        x=0
        auxiliar = ''
        while x < len(linea):
            actual = linea[x]
            if state == 0: # Entra a limpiar los espacios en blanco del nombre
                if ord(actual) == 32:
                    x = x + 1
                else:
                    state = 1
            elif state == 1:
                libreContexto = False
                if ord(actual) == 32 or actual == '\n':
                    x = x + 1
                    nombre = auxiliar           
                    auxiliar = ''
                    state = 2
                else:                  
                    auxiliar = auxiliar + actual
                    x = x + 1
            elif state == 2: # agrega a no terminal
                if ord(actual) == 59: # envia a terminales
                    state = 3
                    no_terminal.append(auxiliar)
                    auxiliar = ''
                    x = x + 1
                elif ord(actual) == 44:
                    x = x + 1
                    no_terminal.append(auxiliar)
                    auxiliar = ''
                elif ord(actual) == 32:
                    x = x + 1
                else:
                    x = x + 1
                    auxiliar = auxiliar + actual
            elif state == 3: # agrega termiles
                if ord(actual) == 59: # envia a inicial
                    state = 4
                    terminal.append(auxiliar)
                    auxiliar = ''
                    x = x + 1
                elif ord(actual) == 44:
                    x = x + 1
                    terminal.append(auxiliar)
                    auxiliar = ''
                elif ord(actual) == 32:
                    x = x + 1
                else:
                    x = x + 1
                    auxiliar = auxiliar + actual
            elif state == 4:
                if ord(actual) == 32 or ord(actual) == 10:
                    state = 5
                    inicial = auxiliar
                    auxiliar = ''
                else:
                    auxiliar = auxiliar + actual
                    x = x + 1
            elif state == 5:
                if ord(actual) == 45:
                    dic = {'no terminal':auxiliar}
                    state = 6
                    nombreterminal = auxiliar
                    ingreso = 1
                    auxiliar = ''
                    x = x + 1
                elif ord(actual) == 42:
                    if libreContexto == True:
                        nuevo = Gramatica(nombre,no_terminal,terminal,inicial,producciones)
                        gramaticas.append(nuevo)
                        print(nuevo.nombre)
                    else:
                        print("ERROR 401: La gramatica "+nombre+" no es libre de contexto")
                    state = 1
                    nombre = ''
                    no_terminal = []
                    terminal = []
                    inicial = ''
                    producciones = []
                    x = x + 2
                else:
                    auxiliar = auxiliar + actual
                    x = x + 1
            elif state == 6:
                if ord(actual) == 62:
                    x = x + 1 
                elif ord(actual) == 32:
                    if auxiliar != '':
                        i = 1
                        for key in dic:
                            if i != 1:
                                if dic[key] == auxiliar:
                                    libreContexto = True
                            i = i + 1
                        dic['terminal'+str(ingreso)] = auxiliar
                        ingreso = ingreso + 1
                        auxiliar = ''
                        x = x + 1
                elif ord(actual) == 10:
                    state = 5
                    i = 1
                    for key in dic:
                        if i != 1:
                            if dic[key] == auxiliar:
                                libreContexto = True
                        i = i + 1
                    dic['terminal'+str(ingreso)] = auxiliar
                    ingreso = ingreso + 1
                    producciones.append(dic)
                    auxiliar = ''
                    x = x + 1
                else: 
                    auxiliar = auxiliar + actual
                    x = x + 1
        if not linea:
            break
    archivo.close()
