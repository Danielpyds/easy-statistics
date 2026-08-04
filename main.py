#importar tkinter y su modulo ttk para otros widgets
#importar el modulo de "funciones" la cual le dara comandos a los botones

from tkinter import *
from tkinter import ttk
from funciones import *
import os
import sys

def resource_path(nombre_archivo):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, nombre_archivo)

#--------------------------------------Raiz-----------------------------------
root = Tk()
root.state("zoomed") #incializar el programa
root.title("Easy Statistics") #nombre del programa 
#root.iconbitmap(resource_path("icono.ico")) 
#al no tener el archivo de icono en su dispotivo desactivo la funcion para evitar que se le presente algun error
#root.rowconfigure(0, weight=1)
#root.columnconfigure(0, weight=2)
#root.columnconfigure(1, weight=1)

#-------------------------------------Pestañas-------------------------------

notebook = ttk.Notebook(root) #crear el widget de notebook para simular las ventanas de un navegador
notebook.pack(expand=True, fill="both")

resultados = ttk.Frame(notebook) #ventana principal 
tablas = ttk.Frame(notebook) #ventana para visualizar el conjunto de datos
descripcion = ttk.Frame(notebook) #ventana para visualizar la descripcion del data set

notebook.add(resultados, text="Resultados")
notebook.add(tablas, text="Datos", sticky="nsew")
notebook.add(descripcion, text="Descripcion", sticky="nsew")

#inicializar las ventanas desactivadas para evitar errores con el usuario
notebook.tab(tablas, state="disabled") 
notebook.tab(descripcion, state="disabled")

#dividir la pantalla de resultados para la caja de resultados y los botones
resultados.rowconfigure(0, weight=1)
resultados.columnconfigure(0, weight=2)
resultados.columnconfigure(1, weight=1)

#-----------------------------------Resultados-------------------------------------

#caja de texto donde se visualizaran algunos resultados
cajaDeTexto = Frame(resultados, bg="lightgray")
cajaDeTexto.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
cajaDeTexto.rowconfigure(0, weight=1)
cajaDeTexto.columnconfigure(0, weight=1)

caja = Text(cajaDeTexto, border=5, relief="groove", state="disabled")
caja.grid(row=0, column=0, sticky="nsew")

#espacio donde se visualizaran los botones que modificaran la caja de resultados
conjuntoBotones = Frame(resultados, bg="lightgray")
conjuntoBotones.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
conjuntoBotones.columnconfigure(0, weight=1)
for i in range(8):
    conjuntoBotones.rowconfigure(i, weight=1) #crear 8 divisiones para cada boton con un bucle for

boton1 = Button(
    conjuntoBotones, 
    text="Importar datos", 
    cursor="hand2", 
    command=lambda: abrirArchivo(caja, boton2, boton3, boton4, boton5, boton6, boton7, boton8), 
    overrelief="flat"
    )
boton1.grid(row=0, sticky="nsew", padx=5 ,pady=5) #unico boton activo, al cargar un archivo activa el resto

boton2 = Button(conjuntoBotones, 
                text="Tamaño del conjunto de datos", 
                cursor="hand2",
                command=lambda: tamaño(caja),
                overrelief="flat",
                state="disabled"
                )
boton2.grid(row=1, sticky="nsew", padx=5 ,pady=5) #visualizar tamaño del data set

boton3 = Button(conjuntoBotones, 
                text="Nombre de las columnas", 
                cursor="hand2",
                command=lambda: nombres(caja),
                overrelief="flat",
                state="disabled")
boton3.grid(row=2, sticky="nsew", padx=5 ,pady=5) #visualizar el nombre de las columnas

boton4 = Button(conjuntoBotones, 
                text="Ver conjuntos de datos", 
                cursor="hand2",
                command=lambda: ver_datos(arbol, notebook),
                overrelief="flat",
                state="disabled")
boton4.grid(row=3, sticky="nsew", padx=5 ,pady=5) #visualizar el conjunto de datos

boton5 = Button(conjuntoBotones, 
                text="Informacion de los datos", 
                cursor="hand2", 
                command=lambda: ver_info(caja),
                overrelief="flat",
                state="disabled")
boton5.grid(row=4, sticky="nsew", padx=5 ,pady=5) #visualizar informacion de los datos como tipo de datos o valores faltantes

boton6 = Button(conjuntoBotones, 
                text="Descripcion de los datos", 
                cursor="hand2",
                command=lambda: ver_desc(desc, notebook),
                overrelief="flat",
                state="disabled")
boton6.grid(row=5, sticky="nsew", padx=5 ,pady=5) #visualizar estadisticas descriptivas

boton7 = Button(conjuntoBotones, 
                text="Regresion lineal", 
                cursor="hand2",
                command = lambda: regresion(caja),
                overrelief="flat",
                state="disabled")
boton7.grid(row=6, sticky="nsew", padx=5 ,pady=5) #ejecutar una regresion lineal simple o multiple

boton8 = Button(conjuntoBotones, 
                text="Otros graficos", 
                cursor="hand2",
                command=lambda: graficos(),
                overrelief="flat",
                state="disabled")
boton8.grid(row=7, sticky="nsew", padx=5 ,pady=5) #visualizar un grafico de correlacion, histograma de errores o scatter plot

#---------------------------------Arboles--------------------------------

arbol_tabla = Frame(tablas)
arbol_tabla.pack(expand=True, fill="both", padx=10, pady=10)
arbol_tabla.rowconfigure(0, weight=1) #con esto la tabla se visualizara por completo en el eje x
arbol_tabla.columnconfigure(0, weight=1)#con esto la tabla se visualizara por completo en el eje y

arbol = ttk.Treeview(arbol_tabla, show="headings") #crear la tabla
arbol.grid(row=0, column=0, sticky="nsew") #esto es para añadir las barras de scroll

scrolly = Scrollbar(arbol_tabla, command=arbol.yview) #con ello le damos el poder de mover la tabla
scrolly.grid(row=0, column=1, sticky="ns") #se añade la barra al lado de la tabla

arbol.config(yscrollcommand=scrolly.set)

scrollx = ttk.Scrollbar(arbol_tabla, orient="horizontal", command=arbol.xview)
scrollx.grid(row=1, column=0, sticky="ew")

arbol.config(xscrollcommand=scrollx.set)

arbol_desc = Frame(descripcion)
arbol_desc.pack(expand=True, fill="both", padx=10, pady=10)
arbol_desc.rowconfigure(0, weight=1)
arbol_desc.columnconfigure(0, weight=1)

desc = ttk.Treeview(arbol_desc, show="headings")
desc.grid(row=0, column=0, sticky="nsew")

descy = Scrollbar(arbol_desc, command=desc.yview)
descy.grid(row=0, column=1, sticky="ns")

desc.config(yscrollcommand=descy.set)

descx = Scrollbar(arbol_desc, command=desc.yview)
descx.grid(row=0, column=1, sticky="ns")

desc.config(yscrollcommand=descx.set)

root.mainloop()