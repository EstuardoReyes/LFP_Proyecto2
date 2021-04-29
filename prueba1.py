diccionario = {'nombres' : 'Carlos', 'edad' : 'A', 'cursos':23 }

for key in diccionario:
    if key == 'nombre':
        print("saltar")
    else:
       if diccionario[key] == 'A':
           print("es libre")