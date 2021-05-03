from tkinter import Tk     
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from Automata import automata
from Automata import gramaticas
from AP import AP
import webbrowser
from datetime import datetime
from graphviz import Digraph
from graphviz import Source
import os
import time

archivo_Menu_Seleccionado = False
AP_Pila = []
listaDeProducciones = []

if os.name == "posix":
   var = "clear"
elif os.name == "ce" or os.name == "nt" or os.name == "dos":
   var = "cls"

os.system(var) ##limpia la pantalla


def Carga():
    global archivoMenu
    global archivo_Menu_Seleccionado
    global name
    root = Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    archivoMenu = askopenfilename(initialdir="D:\Galeria\Escritorio",filetypes =(("Archivo GLC", "*.glc"),("Todos Los Archivos","*.*")),title = "Busque su archivo.")
    root.update()
    root.destroy()
    print("Archivo Menu seleccionada correctamente")
    archivo_Menu_Seleccionado = True
    automata(archivoMenu)

def Informacion():
    global archivo_Menu_Seleccionado 
    if archivo_Menu_Seleccionado == False:
        print("")
        print("Seleccione primeramente archivo de entrada ")
        time.sleep(2)
        os.system(var)
    else:
        os.system(var)
        print("          Seleccione una gramatica ")
        i = 1
        for archivo in gramaticas:
            print("         "+str(i)+". "+archivo.nombre)
            i = i + 1
        a = input("      Ingrese numero")
        os.system(var)
        gramati = gramaticas[int(a)-1]
        print(" Nombre de la gramatica tipo 2: "+gramati.nombre)
        print(" No Terminales = {", end=" ")
        for noterminal in gramati.no_terminal:
            print(noterminal+",", end=" ")
        print("}")
        print(" Terminales = {", end=" ")
        for notermina in gramati.terminal:
            print(notermina+",", end=" ")
        print("}")
        print(" No terminal inicial = "+gramati.inicial)
        print(" Producciones:")
        producciones = gramati.producciones
        for produ in producciones:
            print(" "+produ["no terminal"]+" -> "+produ["terminal1"])
            for key in produ:
                if key != 'no terminal' and key != 'terminal1': 
                    print("   | "+produ[key])

def pila():
    global archivo_Menu_Seleccionado 
    if archivo_Menu_Seleccionado == False:
        print("")
        print("Seleccione primeramente archivo de entrada ")
        time.sleep(2)
        os.system(var)
    else:
        os.system(var)
        print("          Seleccione una gramatica ")
        i = 1
        for archivo in gramaticas:
            print("         "+str(i)+". "+archivo.nombre)
            i = i + 1
        a = input("      Ingrese numero")
        os.system(var)
        gramati = gramaticas[int(a)-1]
        g = Digraph('unix', filename='AP_'+gramati.nombre+'.jpg')
        g.attr(rankdir='LR', size='8,5')
        g.node("",shape="plaintext",witdh="0.0001",height="0.0001")
        g.node("i",shape="circle")
        g.node("p",shape="circle")
        g.node("q",shape="circle",witdh="1",height="1")
        g.node("f",shape="doublecircle")
        g.edge("","i")
        g.edge("i","p",label="λ,λ;#")
        g.edge("p","q",label="λ,λ;"+gramati.inicial)
        aux1 = ''
        aux2 = ''
        produ = []
        for i in gramati.producciones:
            aux = ''
            t = 0
            for e in i:
                if t != 0:
                    aux = aux + i[e]
                t = t + 1
            aux1 = aux1 + "λ,"+i["no terminal"]+";"+aux +"\\n"
            dic = {"noterminal":i["no terminal"],"terminal":aux}
            produ.append(dic)
        for f in gramati.terminal:
            aux2 = aux2 +f+","+f+";λ \\n"
        g.edge("q","q",label=aux1)
        g.edge("q","q",label=aux2,tailport="s",headport="sw")
        g.edge("q","f",label="λ,#;λ")
        g.render(filename="AP_"+gramati.nombre,format='jpg')

        mensaje= """<!doctype html>
                        <html>
                        <head>
                        <title>Generar autómata de pila equivalente</title>
                        <link href="CSS\pariencia.css" rel="stylesheet" type="text/css">
                        </head>
                        <body>
                        <div class="container"> 
                        <header> <a href="">
                        </a>
                        <nav>
                        <ul>
                        </ul>
                        </nav>
                        </header>
                        <section class="hero" id="hero">
                        <h3 class="hero_header">Generar automata de pila<span class="light">"""
        termi = []
        terminal = '{'
        for a in gramati.terminal:
            terminal = terminal + a+","
            termi.append(a)
        final=terminal[:-1]
        final = final + "}"

        alfabeto = "{"
        for a in gramati.terminal:
            alfabeto = alfabeto + a+","
        for a in gramati.no_terminal:
            alfabeto = alfabeto + a+","
        alfabeto=alfabeto[:-1]
        alfabeto = alfabeto + "}"
        nuevo = AP("AP_"+gramati.nombre,alfabeto,termi,gramati.inicial,produ)
        AP_Pila.append(nuevo)

        me = """</span></h3>
                        </section>
                        <section class="banner">
                        <h2 class="parallaxx">Nombre: AP_"""+gramati.nombre+"""   </h2>
                        <h4 class="parallaxx">Terminales = """+final+"""<h4>
                        <h4 class="parallaxx">Alfabeto de pila = """+alfabeto+"""<h4>
                        <h4 class="parallaxx">Estados = { i, q, p, f }<h4>
                        <h4 class="parallaxx">Estado Inicial = { i, }<h4>
                        <h4 class="parallaxx">Estado de aceptacion =  { f,}<h4>
                        <p class="centrado">
                        <img src=" AP_"""+gramati.nombre+""".jpg ">
                        </p>
                        
                        """
        mensaje = mensaje + me
        tamaño = 75
            
            

        for i in range(4):
            mensaje = mensaje + """<h1 class="paralla"> </h1>"""
        mi = """<div class="copyright">&copy;2021 - <strong>Edwin estuardo reyes reyes</strong></div>
                        </div>
                        </body>
                        </html>"""
        mensaje = mensaje + mi

        css = """@charset "UTF-8";
                    /* Body */
                    html {
                            font-size: 40px;
                        }

                        p.centrado {
                             text-align: center;
                            }

                        body {
                            font-family: source-sans-pro;
                            background-color: #f2f2f2;
                            margin-top: 0px;
                            margin-right: 0px;
                            margin-bottom: 0px;
                            margin-left: 0px;
                            font-style: normal;
                            font-weight: 200;
                            }
                            .container {
                            width: 70%;
                            margin-left: auto;
                            margin-right: auto;
                            height: 700px;
                                        }
                            header {
                            width: 100%;
                            height: 8%;
                            background-color: #52bad5;
                            border-bottom: 1px solid #2C9AB7;
                            }
                            .logo {
                        color: #fff;
                            font-weight: bold;
                            text-align: undefined;
                            width: 10%;
                            float: left;
                            margin-top: 15px;
                            margin-left: 25px;
                            letter-spacing: 4px;
                                }
                            .hero_header {
                            color: #FFFFFF;
                            text-align: center;
                            margin-top: 0px;
                            margin-right: 0px;
                            margin-bottom: 0px;
                            margin-left: 0px;
                            letter-spacing: 4px;
                                }
                            .hero {
                            background-color: #B3B3B3;
                            padding-top: 100px;
                            padding-bottom: 80px;
                            }
                            .light {
                                font-weight: bold;
                                color: #717070;
                            }
                            .tagline {
                                text-align: center;
                                color: #FFFFFF;
                                margin-top: 4px;
                                font-weight: lighter;
                                text-transform: uppercase;
                                letter-spacing: 1px;
                            }

                            .banner {
                                background-color: #2D9AB7;
                                background-image: url(../images/parallax.png);
                                +height:"""+str(tamaño)+"""px;
                                background-attachment: fixed;
                                background-size: cover;
                                background-repeat: no-repeat;
                            }
                            .parallaxx {
                                color: #FFFFFF;
                                text-align: left;
                                padding-left: 200px;
                                padding-right: 100px;
                                padding-top: 50px;
                                letter-spacing: 2px;
                                margin-top: 0px;
                                margin-bottom: 0px
                            }
                            .parallax {
                                color: #FFFFFF;
                                text-align: left;
                                padding-left: 200px;
                                padding-right: 100px;
                                padding-top: 10px;
                                letter-spacing: 2px;
                                margin-top: 0px;
                                margin-bottom: 0px
                            }

                            .paralla {
                                color: #ffffff5e;
                                text-align: left;
                                padding-left: 200px;
                                padding-right: 100px;
                                padding-top: 10px;
                                letter-spacing: 2px;
                                margin-top: 0px;
                                margin-bottom: 0px
                            }


                            .copyright {
                                text-align: center;
                                padding-top: 20px;
                                padding-bottom: 20px;
                                background-color: #717070;
                                color: #ffffff;
                                text-transform: uppercase;
                                font-weight: lighter;
                                letter-spacing: 2px;
                                border-top-width: 2px;
                            }
                            """
           
        g = open("CSS\pariencia.css",'wb')
        g.write(bytes(css,"ascii"))
        g.close()
        f = open('imagen.html','wb')
        f.write(mensaje.encode())
        f.close()
        webbrowser.open_new_tab('imagen.html')

def verificar(gramatica,palabra):
    global listaDeProducciones
    x = 0
    state = "i"
    pila = ''
    interacciones = []
    o = 0
    for i in gramatica.producciones:
        interacciones.append(o)
        o = o + 1
    try:
        while(True):
            if x < len(palabra):
                actual = palabra[x]
            if state == "i":  
                state  = 'p'
                pila = '#'
            elif state == 'p':
                state  = 'q'
                pila = gramatica.inicial+'#'
            elif state == 'q':
                n_produccion = 0
                ultimaInteraccion = 0
                while (True):
                    state  = 'f'
                    if pila[0] in gramatica.terminal or actual == "":
                        if pila[0] == actual: 
                            x = x + 1
                            pila = pila[1:]
                            if x < len(palabra):
                                actual = palabra[x]
                            else:
                                actual = ""
                                
                        else:
                            t = len(interacciones)-1
                            while interacciones[t] != ultimaInteraccion:
                                interacciones.pop(t)
                                t = len(interacciones)-1
                            interacciones.append(elimina+1)
                            t = interacciones[len(interacciones)-1]
                            while t < len(gramatica.producciones)-1: 
                                t = t + 1
                                interacciones.append(t)
                            x = 0 
                            state = "i"
                            break
                    elif gramatica.producciones[interacciones[n_produccion]]['noterminal'] == pila[0] :
                        try:
                            if gramatica.producciones[interacciones[n_produccion+1]]['noterminal']  == pila[0]:
                                ultimaInteraccion = interacciones[n_produccion-1]
                                elimina = interacciones[n_produccion]
                        except:
                            print("")
                        pila = pila[1:]
                        pila = gramatica.producciones[interacciones[n_produccion]]['terminal'] + pila            
                        listaDeProducciones.append(n_produccion)
                        n_produccion = n_produccion + 1
                    else:
                        n_produccion = n_produccion + 1
                    if pila == '#':##salio
                        state = "f"
                        break
            elif state == 'f' :
                return interacciones
                break
    except:
        mensaje= """<!doctype html>
                        <html>
                        <head>
                        <title>Generar autómata de pila equivalente</title>
                        <link href="CSS\pariencia.css" rel="stylesheet" type="text/css">
                        </head>
                        <body>
                        <div class="container"> 
                        <header> <a href="">
                        </a>
                        <nav>
                        <ul>
                        </ul>
                        </nav>
                        </header>
                        <section class="hero" id="hero">
                        <h3 class="hero_header">Generar automata de pila<span class="light">
                        </span></h3></section>
                        <section class="banner">
                        <h1 class=parallax><FONT COLOR="white">PALABRA INGRESADA NO PERTENECE A LA GRAAMTICA</FONT></h1>"""
        
        mi = """</section><div class="copyright">&copy;2021 - <strong>Edwin estuardo reyes reyes</strong></div>
                        </div>
                        </body>
                        </html>"""
        mensaje = mensaje + mi
        tamaño = 150
        css = """@charset "UTF-8";
                    /* Body */
                    html {
                            font-size: 40px;
                        }

                        p.centrado {
                             text-align: center;
                            }

                        body {
                            font-family: source-sans-pro;
                            background-color: #f2f2f2;
                            margin-top: 0px;
                            margin-right: 0px;
                            margin-bottom: 0px;
                            margin-left: 0px;
                            font-style: normal;
                            font-weight: 200;
                            }
                            .container {
                            width: 70%;
                            margin-left: auto;
                            margin-right: auto;
                            height: 700px;
                                        }
                            header {
                            width: 100%;
                            height: 8%;
                            background-color: #52bad5;
                            border-bottom: 1px solid #2C9AB7;
                            }
                            .logo {
                        color: #fff;
                            font-weight: bold;
                            text-align: undefined;
                            width: 10%;
                            float: left;
                            margin-top: 15px;
                            margin-left: 25px;
                            letter-spacing: 4px;
                                }
                            .hero_header {
                            color: #FFFFFF;
                            text-align: center;
                            margin-top: 0px;
                            margin-right: 0px;
                            margin-bottom: 0px;
                            margin-left: 0px;
                            letter-spacing: 4px;
                                }
                            .hero {
                            background-color: #B3B3B3;
                            padding-top: 100px;
                            padding-bottom: 80px;
                            }
                            .light {
                                font-weight: bold;
                                color: #717070;
                            }
                            .tagline {
                                text-align: center;
                                color: #FFFFFF;
                                margin-top: 4px;
                                font-weight: lighter;
                                text-transform: uppercase;
                                letter-spacing: 1px;
                            }

                            .banner {
                                background-color: #2D9AB7;
                                background-image: url(../images/parallax.png);
                                +height:"""+str(tamaño)+"""px;
                                background-attachment: fixed;
                                background-size: cover;
                                background-repeat: no-repeat;
                            }
                            .parallaxx {
                                color: #FFFFFF;
                                text-align: left;
                                padding-left: 200px;
                                padding-right: 100px;
                                padding-top: 50px;
                                letter-spacing: 2px;
                                margin-top: 0px;
                                margin-bottom: 0px
                            }
                            .parallax {
                                color: #FFFFFF;
                                text-align: left;
                                padding-left: 200px;
                                padding-right: 100px;
                                padding-top: 10px;
                                letter-spacing: 2px;
                                margin-top: 0px;
                                margin-bottom: 0px
                            }

                            .paralla {
                                color: #ffffff5e;
                                text-align: left;
                                padding-left: 200px;
                                padding-right: 100px;
                                padding-top: 10px;
                                letter-spacing: 2px;
                                margin-top: 0px;
                                margin-bottom: 0px
                            }


                            .copyright {
                                text-align: center;
                                padding-top: 20px;
                                padding-bottom: 20px;
                                background-color: #717070;
                                color: #ffffff;
                                text-transform: uppercase;
                                font-weight: lighter;
                                letter-spacing: 2px;
                                border-top-width: 2px;
                            }
                            """
           
        g = open("CSS\pariencia.css",'wb')
        g.write(bytes(css,"ascii"))
        g.close()
        f = open('ERROR.html','wb')
        f.write(mensaje.encode())
        f.close()
        webbrowser.open_new_tab('ERROR.html')
        return False
        

                    


        

    

def evaluar():
    global archivo_Menu_Seleccionado 
    fallo = True
    interaccion = 0
    if archivo_Menu_Seleccionado == False:
        print("")
        print("Seleccione primeramente archivo de entrada ")
        os.system(var)
    else:
        os.system(var)
        print("          Seleccione una AP ")
        i = 1
        for archivo in AP_Pila:
            print("         "+str(i)+". "+archivo.nombre)
            i = i + 1
        a = input("      Ingrese numero: ")
        os.system(var)
        gramati = AP_Pila[int(a)-1]
        palabra = input("Ingrese palabra: ")
        x = 0
        state = "i"
        pila = ''
        interacciones = verificar(gramati,palabra)
        if interacciones != False:
            while(True):
                if x < len(palabra):
                    actual = palabra[x]
                else:
                    actual = 'λ'
                if state == "i":
                    interaccion = 0
                    state  = 'p'
                    g = Digraph('unix', filename='AP_'+gramati.nombre+'.jpg')
                    g.attr(rankdir='LR', size='8,5')
                    g.node("Pila: "+pila+"\\n"+"Entrada: ",shape="box")
                    g.node("",shape="plaintext",witdh="0.0001",height="0.0001")
                    g.node("i",shape="circle",color="yellow",style="filled")
                    g.node("p",shape="circle")
                    g.node("q",shape="circle",witdh="1",height="1")
                    g.node("f",shape="doublecircle")
                    g.edge("","i")
                    g.edge("i","p",label='<<FONT COLOR="red">λ,λ;#</FONT>>')
                    g.edge("p","q",label="λ,λ;"+gramati.inicial)
                    aux1 = ''
                    aux2 = ''
                    produ = []
                    for i in gramati.producciones: 
                        aux1 = aux1 + "λ,"+i["noterminal"]+";"+i["terminal"] +"\\n"
                    for f in gramati.terminal:
                        aux2 = aux2 +f+","+f+";λ \\n"
                    g.edge("q","q",label=aux1)
                    g.edge("q","q",label=aux2,tailport="s",headport="sw")
                    g.edge("q","f",label="λ,#;λ")
                    g.render(filename="0",format='jpg')
                    pila = '#'
                elif state == 'p':
                    interaccion = interaccion + 1
                    state  = 'q'
                    g = Digraph('unix', filename='AP_'+gramati.nombre+'.jpg')
                    g.attr(rankdir='LR', size='8,5')
                    g.node("Pila: "+pila+"\\n"+"Entrada: ",shape="box")
                    g.node("",shape="plaintext",witdh="0.0001",height="0.0001")
                    g.node("i",shape="circle")
                    g.node("p",shape="circle",color="yellow",style="filled")
                    g.node("q",shape="circle",witdh="1",height="1")
                    g.node("f",shape="doublecircle")
                    g.edge("","i")
                    g.edge("i","p",label='λ,λ;#')
                    g.edge("p","q",label='<<FONT COLOR="red">λ,λ;'+gramati.inicial+'</FONT>>')
                    aux1 = ''
                    aux2 = ''
                    produ = []
                    for i in gramati.producciones: 
                        aux1 = aux1 + "λ,"+i["noterminal"]+";"+i["terminal"] +"\\n"
                    for f in gramati.terminal:
                        aux2 = aux2 +f+","+f+";λ \\n"
                    g.edge("q","q",label=aux1)
                    g.edge("q","q",label=aux2,tailport="s",headport="sw")
                    g.edge("q","f",label="λ,#;λ")
                    g.render(filename="1",format='jpg')
                    pila = gramati.inicial+'#'
                elif state == 'q':
                    n_produccion = 0
                    while (True):
                        interaccion = interaccion + 1
                        pArriba = False
                        pAbajo = False
                        g = Digraph('unix', filename='AP_'+gramati.nombre+'.jpg')
                        g.attr(rankdir='LR', size='8,5')
                        g.node("Pila: "+pila+"\\n"+"Entrada: "+actual,shape="box")
                        g.node("",shape="plaintext",witdh="0.0001",height="0.0001")
                        g.node("i",shape="circle")
                        g.node("p",shape="circle")
                        g.node("q",shape="circle",witdh="1",height="1",color="yellow",style="filled")
                        g.node("f",shape="doublecircle")
                        g.edge("","i")
                        g.edge("i","p",label='λ,λ;#')
                        g.edge("p","q",label='λ,λ;'+gramati.inicial)
                        aux1 = ''
                        aux2 = ''
                        produ = []
                        try:
                            producci = gramati.producciones[interacciones[n_produccion]]
                        except:
                            print("")
                        if producci['noterminal'] == pila[0]: #cambia de pila
                            pila = pila[1:]
                            pila = producci['terminal']+pila
                            pArriba = True
                            n_produccion = n_produccion + 1
                        elif pila[0] == actual:
                            pAbajo = True
                            letra = pila[0]
                            pila = pila[1:]
                            x = x + 1
                            if x < len(palabra):
                                actual = palabra[x]
                            else:
                                actual = 'λ'
                        else:
                            fallo = False
                            break
                            break
                        w = 0
                        for i in gramati.producciones:  #agrega solo las producciones

                            if pArriba==True and w == interacciones[n_produccion-1]:
                                aux1 = aux1 + 'λ,'+i["noterminal"]+';'+i["terminal"] +" <---- \\n"
                                pArriba = False
                            else:
                                aux1 = aux1 + 'λ,'+i["noterminal"]+';'+i["terminal"] +'\\n'
                            w = w + 1
                        for f in gramati.terminal:
                            if pAbajo == True and f == letra:
                                aux2 = aux2 +f+','+f+';λ <----  \\n'
                                pAbajo = False
                            else:
                                aux2 = aux2 +f+','+f+';λ \\n'
                        g.edge("q","q",label=aux1)
                        g.edge("q","q",label=aux2,tailport="s",headport="sw")
                        g.edge("q","f",label="λ,#;λ")
                        g.render(filename=str(interaccion),format='jpg')
                        if pila == "#":
                            state = 'f'
                            break
                elif state == 'f':
                    interaccion = interaccion + 1
                    g = Digraph('unix', filename='AP_'+gramati.nombre+'.jpg')
                    g.attr(rankdir='LR', size='8,5')
                    g.node("Pila: "+pila+" \\n"+"Entrada: ",shape="box")
                    g.node("",shape="plaintext",witdh="0.0001",height="0.0001")
                    g.node("i",shape="circle")
                    g.node("p",shape="circle")
                    g.node("q",shape="circle",witdh="1",height="1",color="yellow",style="filled")
                    g.node("f",shape="doublecircle")
                    g.edge("","i")
                    g.edge("i","p",label='λ,λ;#')
                    g.edge("p","q",label='λ,λ;'+gramati.inicial)
                    aux1 = ''
                    aux2 = ''
                    produ = []
                    for i in gramati.producciones: 
                        aux1 = aux1 + "λ,"+i["noterminal"]+";"+i["terminal"] +"\\n"
                    for f in gramati.terminal:
                        aux2 = aux2 +f+","+f+";λ \\n"
                    g.edge("q","q",label=aux1)
                    g.edge("q","q",label=aux2,tailport="s",headport="sw")
                    g.edge("q","f",label='<<FONT COLOR="red">λ,#;λ</FONT>>')
                    g.render(filename=str(interaccion),format='jpg')
                    ################################################################################
                    interaccion = interaccion + 1
                    g = Digraph('unix', filename='AP_'+gramati.nombre+'.jpg')
                    g.attr(rankdir='LR', size='8,5')
                    g.node("Pila: \\n"+"Entrada: ",shape="box")
                    g.node("",shape="plaintext",witdh="0.0001",height="0.0001")
                    g.node("i",shape="circle")
                    g.node("p",shape="circle")
                    g.node("q",shape="circle",witdh="1",height="1")
                    g.node("f",shape="doublecircle",color="yellow",style="filled")
                    g.edge("","i")
                    g.edge("i","p",label='λ,λ;#')
                    g.edge("p","q",label='λ,λ;'+gramati.inicial)
                    aux1 = ''
                    aux2 = ''
                    produ = []
                    for i in gramati.producciones: 
                        aux1 = aux1 + "λ,"+i["noterminal"]+";"+i["terminal"] +"\\n"
                    for f in gramati.terminal:
                        aux2 = aux2 +f+","+f+";λ \\n"
                    g.edge("q","q",label=aux1)
                    g.edge("q","q",label=aux2,tailport="s",headport="sw")
                    g.edge("q","f",label='λ,#;λ')
                    g.render(filename=str(interaccion),format='jpg')
                    break
        if interacciones!= False:    
            mensaje= """<!doctype html>
                        <html>
                        <head>
                        <title>Generar autómata de pila equivalente</title>
                        <link href="CSS\pariencia.css" rel="stylesheet" type="text/css">
                        </head>
                        <body>
                        <div class="container"> 
                        <header> <a href="">
                        </a>
                        <nav>
                        <ul>
                        </ul>
                        </nav>
                        </header>
                        <section class="hero" id="hero">
                        <h3 class="hero_header">Generar automata de pila<span class="light">
                        </span></h3></section>
                        <section class="banner">"""
            m = ''
            mi = ''           
            for i in range(0,interaccion+1):
                m = m + '<h3 class=parallax>Interaccion #'+str(i)+'</h3><p class="centrado"><img src='+str(i)+'.jpg> </p>'
            mensaje = mensaje + m 
            tamaño = 75    
            if fallo == True:
                mi = mi + '<h2 class=parallax><FONT COLOR="white">        ACEPTADA</FONT></h2>'
            else:
                mi = mi + '<h2 class=parallax><FONT COLOR="white">       RECHAZADA</FONT></h2>'
            mi = mi +"""</section><div class="copyright">&copy;2021 - <strong>Edwin estuardo reyes reyes</strong></div>
                            </div>
                            </body>
                            </html>"""
            mensaje = mensaje + mi
            css = """@charset "UTF-8";
                        /* Body */
                        html {
                                font-size: 40px;
                            }

                            p.centrado {
                                text-align: center;
                                }

                            body {
                                font-family: source-sans-pro;
                                background-color: #f2f2f2;
                                margin-top: 0px;
                                margin-right: 0px;
                                margin-bottom: 0px;
                                margin-left: 0px;
                                font-style: normal;
                                font-weight: 200;
                                }
                                .container {
                                width: 70%;
                                margin-left: auto;
                                margin-right: auto;
                                height: 700px;
                                            }
                                header {
                                width: 100%;
                                height: 8%;
                                background-color: #52bad5;
                                border-bottom: 1px solid #2C9AB7;
                                }
                                .logo {
                            color: #fff;
                                font-weight: bold;
                                text-align: undefined;
                                width: 10%;
                                float: left;
                                margin-top: 15px;
                                margin-left: 25px;
                                letter-spacing: 4px;
                                    }
                                .hero_header {
                                color: #FFFFFF;
                                text-align: center;
                                margin-top: 0px;
                                margin-right: 0px;
                                margin-bottom: 0px;
                                margin-left: 0px;
                                letter-spacing: 4px;
                                    }
                                .hero {
                                background-color: #B3B3B3;
                                padding-top: 100px;
                                padding-bottom: 80px;
                                }
                                .light {
                                    font-weight: bold;
                                    color: #717070;
                                }
                                .tagline {
                                    text-align: center;
                                    color: #FFFFFF;
                                    margin-top: 4px;
                                    font-weight: lighter;
                                    text-transform: uppercase;
                                    letter-spacing: 1px;
                                }

                                .banner {
                                    background-color: #2D9AB7;
                                    background-image: url(../images/parallax.png);
                                    +height:"""+str(tamaño)+"""px;
                                    background-attachment: fixed;
                                    background-size: cover;
                                    background-repeat: no-repeat;
                                }
                                .parallaxx {
                                    color: #FFFFFF;
                                    text-align: left;
                                    padding-left: 200px;
                                    padding-right: 100px;
                                    padding-top: 50px;
                                    letter-spacing: 2px;
                                    margin-top: 0px;
                                    margin-bottom: 0px
                                }
                                .parallax {
                                    color: #FFFFFF;
                                    text-align: left;
                                    padding-left: 200px;
                                    padding-right: 100px;
                                    padding-top: 10px;
                                    letter-spacing: 2px;
                                    margin-top: 0px;
                                    margin-bottom: 0px
                                }

                                .paralla {
                                    color: #ffffff5e;
                                    text-align: left;
                                    padding-left: 200px;
                                    padding-right: 100px;
                                    padding-top: 10px;
                                    letter-spacing: 2px;
                                    margin-top: 0px;
                                    margin-bottom: 0px
                                }


                                .copyright {
                                    text-align: center;
                                    padding-top: 20px;
                                    padding-bottom: 20px;
                                    background-color: #717070;
                                    color: #ffffff;
                                    text-transform: uppercase;
                                    font-weight: lighter;
                                    letter-spacing: 2px;
                                    border-top-width: 2px;
                                }
                                """
            
            g = open("CSS\pariencia.css",'wb')
            g.write(bytes(css,"ascii"))
            g.close()
            f = open('imagen.html','wb')
            f.write(mensaje.encode())
            f.close()
            webbrowser.open_new_tab('imagen.html')
                
def tabla():
    global archivo_Menu_Seleccionado 
    pilas = []
    transiciones = []
    entradas = []
    fallo = True
    if archivo_Menu_Seleccionado == False:
        print("")
        print("Seleccione primeramente archivo de entrada ")
        os.system(var)
    else:
        os.system(var)
        print("          Seleccione una AP ")
        i = 1
        for archivo in AP_Pila:
            print("         "+str(i)+". "+archivo.nombre)
            i = i + 1
        a = input("      Ingrese numero: ")
        os.system(var)
        gramati = AP_Pila[int(a)-1]
        palabra = input("Ingrese palabra: ")
        x = 0
        state = "i"
        pila = ''
        interacciones = verificar(gramati,palabra)
        if interacciones != False:
            while(True):  
                if x < len(palabra):
                    actual = palabra[x]
                else:
                    actual = 'λ'
                if state == "i":
                    interaccion = 0
                    state  = 'p'
                    pilas.append(pila)
                    entradas.append(actual)
                    transiciones.append("(i, λ, λ;p,#)")
                    pila = '#'
                elif state == 'p':
                    interaccion = interaccion + 1
                    state  = 'q'
                    entradas.append(actual)
                    transiciones.append("(p, λ, λ;q,"+gramati.inicial+")")
                    pilas.append(pila)
                    pila = gramati.inicial+'#'
                
                elif state == 'q':
                    n_produccion = 0
                    while (True):
                        interaccion = interaccion + 1
                        try:
                            producci = gramati.producciones[interacciones[n_produccion]]
                        except:
                            print("")
                        if producci['noterminal'] == pila[0]: #cambia de pila
                            pilas.append(pila)
                            pila = pila[1:]
                            pila = producci['terminal']+pila
                            pArriba = True
                            entradas.append(actual)
                            transiciones.append("(q, λ,"+producci['noterminal']+" ;q,"+producci['terminal']+")")
                            n_produccion = n_produccion + 1
                        elif pila[0] == actual:
                            pAbajo = True
                            pilas.append(pila)
                            letra = pila[0]
                            pila = pila[1:]
                            entradas.append(actual)
                            transiciones.append("(q,"+letra+" , "+letra+";q,λ)")
                            x = x + 1
                            if x < len(palabra):
                                actual = palabra[x]
                            else:
                                actual = 'λ'
                        else:
                            fallo = True
                            break
                            break

                        if pila == "#":
                            state = 'f'
                            pilas.append(pila)
                            entradas.append(actual)
                            transiciones.append("(q,λ,"+pila[0]+";f,λ)")

                            break
                elif state == 'f':
                    interaccion = interaccion + 1
                    pilas.append('λ')
                    entradas.append(actual)
                    transiciones.append("f")       
                    break
        if interaccion != False:   
            mensaje= """<!doctype html>
                            <html>
                            <head>
                            <title>Generar autómata de pila equivalente</title>
                            <link href="CSS\pariencia.css" rel="stylesheet" type="text/css">
                            </head>
                            <body>
                            <div class="container"> 
                            <header> <a href="">
                            </a>
                            <nav>
                            <ul>
                            </ul>
                            </nav>
                            </header>
                            <section class="hero" id="hero">
                            <h3 class="hero_header">Generar Tabla de Pila<span class="light">
                            </span></h3></section>
                            <section class="banner">
                            <div style="text-align:center;">
                            <table border="1" style="margin: 0 auto;">
                            <tr> <td><FONT COLOR="white">Interación</FONT></td> <td><FONT COLOR="white">Pila</FONT></td> <td><FONT COLOR="white">Entrada</FONT></td> <td><FONT COLOR="white">Transiciones</FONT></td>  </tr>"""
            mi = ''
            a = 0            
            for i in pilas:
                mi = mi + '<tr> <td><FONT COLOR="white">'+str(a)+'</FONT></td> <td><FONT COLOR="white">'+i+'</FONT></td> <td><FONT COLOR="white">'+entradas[a]+'</FONT></td> <td><FONT COLOR="white">'+transiciones[a]+'</FONT></td>  </tr>'
                a = a + 1
            mensaje = mensaje + mi  
            tamaño = 75    
            mi = "</table></div>"
            if fallo == True:
                mi = mi + '<h2 class=parallax><FONT COLOR="white">        ACEPTADA</FONT></h2>'
            else:
                mi = mi + '<h2 class=parallax><FONT COLOR="white">       RECHAZADA</FONT></h2>'

            mi = mi + """</section><div class="copyright">&copy;2021 - <strong>Edwin estuardo reyes reyes</strong></div>
                        </div>
                            </body>
                            </html>"""
            mensaje = mensaje + mi
            css = """@charset "UTF-8";
                        /* Body */
                        html {
                                font-size: 40px;
                            }

                            p.centrado {
                                text-align: center;
                                }

                            body {
                                font-family: source-sans-pro;
                                background-color: #f2f2f2;
                                margin-top: 0px;
                                margin-right: 0px;
                                margin-bottom: 0px;
                                margin-left: 0px;
                                font-style: normal;
                                font-weight: 200;
                                }
                                .container {
                                width: 70%;
                                margin-left: auto;
                                margin-right: auto;
                                height: 700px;
                                            }
                                header {
                                width: 100%;
                                height: 8%;
                                background-color: #52bad5;
                                border-bottom: 1px solid #2C9AB7;
                                }
                                .logo {
                            color: #fff;
                                font-weight: bold;
                                text-align: undefined;
                                width: 10%;
                                float: left;
                                margin-top: 15px;
                                margin-left: 25px;
                                letter-spacing: 4px;
                                    }
                                .hero_header {
                                color: #FFFFFF;
                                text-align: center;
                                margin-top: 0px;
                                margin-right: 0px;
                                margin-bottom: 0px;
                                margin-left: 0px;
                                letter-spacing: 4px;
                                    }
                                .hero {
                                background-color: #B3B3B3;
                                padding-top: 100px;
                                padding-bottom: 80px;
                                }
                                .light {
                                    font-weight: bold;
                                    color: #717070;
                                }
                                .tagline {
                                    text-align: center;
                                    color: #FFFFFF;
                                    margin-top: 4px;
                                    font-weight: lighter;
                                    text-transform: uppercase;
                                    letter-spacing: 1px;
                                }

                                .banner {
                                    background-color: #2D9AB7;
                                    background-image: url(../images/parallax.png);
                                    +height:"""+str(tamaño)+"""px;
                                    background-attachment: fixed;
                                    background-size: cover;
                                    background-repeat: no-repeat;
                                }
                                .parallaxx {
                                    color: #FFFFFF;
                                    text-align: left;
                                    padding-left: 200px;
                                    padding-right: 100px;
                                    padding-top: 50px;
                                    letter-spacing: 2px;
                                    margin-top: 0px;
                                    margin-bottom: 0px
                                }
                                .parallax {
                                    color: #FFFFFF;
                                    text-align: left;
                                    padding-left: 200px;
                                    padding-right: 100px;
                                    padding-top: 10px;
                                    letter-spacing: 2px;
                                    margin-top: 0px;
                                    margin-bottom: 0px
                                }

                                .paralla {
                                    color: #ffffff5e;
                                    text-align: left;
                                    padding-left: 200px;
                                    padding-right: 100px;
                                    padding-top: 10px;
                                    letter-spacing: 2px;
                                    margin-top: 0px;
                                    margin-bottom: 0px
                                }


                                .copyright {
                                    text-align: center;
                                    padding-top: 20px;
                                    padding-bottom: 20px;
                                    background-color: #717070;
                                    color: #ffffff;
                                    text-transform: uppercase;
                                    font-weight: lighter;
                                    letter-spacing: 2px;
                                    border-top-width: 2px;
                                }
                                """
            
            g = open("CSS\pariencia.css",'wb')
            g.write(bytes(css,"ascii"))
            g.close()
            f = open(gramati.nombre+'.html','wb')
            f.write(mensaje.encode())
            f.close()
            webbrowser.open_new_tab(gramati.nombre+'.html')
                



            


def Menu():
    salida = False
    while salida == False:
        print("          Proyecto 2 - LFP")
        print("")
        print("          1. Cargar Archivo")
        print("          2. Cargar Informacion")
        print("          3. Generar Automata de pila equivalente")
        print("          4. Reporte de Recorrido")
        print("          5. Reporte de Tabla")
        print("          6. Salida")
        print("")
        a = input("      Seleccione una opcion: ")
        if (a == '1'):
            Carga()
        elif (a == '2'):
            Informacion()
        elif (a == '3'):
            pila()
        elif (a == '4'):
            evaluar()
        elif (a == '5'):
            tabla()
        elif (a == '6'):
            salida = True
        else:
            print("Opcion "+a+" no se encuentra entre las opciones")

Menu()