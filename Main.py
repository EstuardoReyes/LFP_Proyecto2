from tkinter import Tk     
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from Automata import automata
from Automata import gramaticas
import webbrowser
from datetime import datetime
from graphviz import Digraph
from graphviz import Source
import os
import time

archivo_Menu_Seleccionado = False

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
        for i in gramati.producciones:
            aux = ''
            for e in i:
                if i != "no terminal":
                    aux = aux + i[e]
            aux1 = aux1 + "λ,"+i["no terminal"]+";"+aux +"\\n"
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
        
        me = """</span></h3>
                        </section>
                        <section class="banner">
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
      



def Menu():
    salida = False
    while salida == False:
        print("          Proyecto 2 - LFP")
        print("")
        print("          1. Cargar Archivo")
        print("          2. Cargar Informacion")
        print("          3. Generar Automata de pila equivalente")
        print("          4. Generar Factura")
        print("          5. Generar Arbol")
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
            generarFactura()
        elif (a == '5'):
            graphi()
        elif (a == '6'):
            salida = True
        else:
            print("Opcion "+a+" no se encuentra entre las opciones")

Menu()