from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from pathlib import Path
import pandas as pd 

def modificarCaja(cajaTexto, texto):
    cajaTexto.config(state="normal")
    cajaTexto.insert(END, texto+"\n\n")
    cajaTexto.config(state="disabled")
    
def abrirArchivo(cajaTexto, boton2, boton3, boton4, boton5, boton6, boton7, boton8):
    global df
    df = None
    archivo = fd.askopenfilename(
        title = "Busca tu conjunto de datos",
        initialdir = ".",
        filetypes=[("Archivos excel", "*.xlsx"), ("Archivos Stata", "*.DTA"), ("Archivos separados por comas", "*.csv")]
    )
    extension = Path(archivo).suffix.lower()
    if extension == ".xlsx":
        df = pd.read_excel(archivo)
    elif extension == ".dta":
        df = pd.read_stata(archivo)
    elif extension == ".csv":  
        df = pd.read_csv(archivo)
    
    if archivo:
        modificarCaja(cajaTexto, "¡Archivo importado con exito!")
        if archivo != None:
            boton2.config(state="normal")
            boton3.config(state="normal")
            boton4.config(state="normal")
            boton5.config(state="normal")
            boton6.config(state="normal")
            boton7.config(state="normal")
            boton8.config(state="normal")
            
def tamaño(cajaTexto):
    observaciones = df.shape[0]
    variables = df.shape[1]
    
    resultado = f"Numero de observaciones: {observaciones}\nNumero de variables: {variables}" 
    modificarCaja(cajaTexto, resultado)
    
def nombres(cajaTexto):
    nom_col = []
    for columna in df.columns:
        nom_col.append(columna)
        
    nom_col = str(nom_col)
    modificarCaja(cajaTexto, nom_col)
    
def ver_datos(arbol, notebook):
    notebook.tab(1, state="normal")
    
    for elemento in arbol.get_children():
        arbol.delete(elemento)
    
    arbol["columns"] = list(df.columns)
    
    for columna in df.columns:
        arbol.heading(columna, text=columna)
        arbol.column(columna, width=100, anchor="center")
        
    for filas in df.itertuples(index=False):
        arbol.insert("", "end", values=filas)
        
    notebook.select(1)
    
def ver_desc(arbol, notebook):
    
    notebook.tab(2, state="normal")
     
    for elemento in arbol.get_children():
        arbol.delete(elemento)
        
    arbol["show"] = "headings"
    columnas_stats = ["Variable"] + list(df.describe().transpose().columns)
    arbol["columns"] = columnas_stats
    
    for columna in columnas_stats:
        arbol.heading(columna, text=columna)
        arbol.column(columna, width=100, anchor="center")
        
    for filas in df.describe().transpose().itertuples(index=True):
        arbol.insert("", "end", values=filas)
        
    notebook.select(2)   
    #resultado = df.describe().transpose()
    
    #modificarCaja(cajaTexto, str(resultado))
    
def ver_info(cajaTexto):
    import io
    buffer = io.StringIO()
    df.info(buf=buffer)
    
    modificarCaja(cajaTexto, buffer.getvalue())

def regresion(cajaTexto):
    wnd = Toplevel()
    wnd.title("Parametros de la regresion")
    wnd.resizable(False, False)
    wnd.config(bg="lightgray")

    Label(wnd, text="Variable dependiente (Y)").pack(padx=50, pady=10)
    
    variables = list(df.select_dtypes(include="number").columns)
    
    def actualizar_explicativas(event):
        variable_seleccionada_y = combo.get()
            
        lista.config(state="normal")
        lista.delete(0, END)
            
        for var in variables:
            if var != variable_seleccionada_y:
                lista.insert(END, var)
                
    def mandar_datos():
        global variable_y
        global variables_regresion
        
        variable_y = combo.get()
        indices_seleccionados = lista.curselection()
        variables_regresion =[lista.get(i) for i in indices_seleccionados]

        if not variable_y or not variables_regresion:
            from tkinter import messagebox
            wnd.destroy()
            messagebox.showwarning("Atencion", "Por favor selecciona una variable Y y al menos una variable X")
        
        else:
            try:
                import statsmodels.api as sm
                import matplotlib.pyplot as plt
                import seaborn as sns
                
                global errores
                y = df[variable_y]
                X = df[variables_regresion]
            
                x = sm.add_constant(X)
                regresion = sm.OLS(y, x).fit()
                
                y_pred = regresion.predict(x)
                errores = list(regresion.resid)
                modificarCaja(cajaTexto, str(regresion.summary()))
                
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.regplot(
                    x = y_pred,
                    y = y,
                    line_kws={"color":"red", "linewidth":1.5},
                    ax = ax
                )
                plt.xlabel("Valores predecidos")
            
                wnd.destroy()
                plt.show()
            except:
                from tkinter import messagebox
                wnd.destroy()
                messagebox.showwarning("Presencia de valores faltantes", "Valores faltantes en columnas seleccionadas")
    
    combo = ttk.Combobox(wnd, values=variables, state="readonly")
    combo.pack(padx=50, pady=10)
    
    Label(wnd, text="Variables explicativas (X)").pack(padx=50, pady=10)
    
    lista = Listbox(wnd, selectmode="multiple", height=6, state="disabled")
    lista.pack(padx=50, pady=10)

    combo.bind("<<ComboboxSelected>>", actualizar_explicativas)    
    Button(wnd, text="Ejecutar", command=mandar_datos).pack(padx=50, pady=10)
   
def graficos():
    venCal = Toplevel()
    venCal.title("Otros graficos")
    venCal.resizable(False, False)
    
    def seleccionCalculo():
        calculoSelect = opc.get()
        
        if not calculoSelect:
            from tkinter import messagebox
            venCal.destroy()
            messagebox.showwarning("Atencion", "Por favor selecciona una opcion")
        else:
            import matplotlib.pyplot as plt
            import seaborn as sns
            if calculoSelect == "Matriz de correlacion":
                cor = df.corr(numeric_only=True)
                
                sns.heatmap(cor)
                plt.title("Correlacion de variables")
                
                venCal.destroy()
                plt.show()
            elif calculoSelect == "Histograma de los errores":
                try:
                    sns.histplot(errores)
                    plt.title("Histograma de los errores")
                                        
                    venCal.destroy()
                    plt.show()
                except NameError:
                    from tkinter import messagebox  
                    venCal.destroy()                
                    messagebox.showwarning("Atencion", "Por favor ejecutar regresion")
            elif calculoSelect == "Puntos de relacion":
                venReg = Toplevel()
                venReg.title("Grafico de puntos")
                venReg.resizable(False, False)
                
                Label(venReg, text="Variable Y").pack(padx=50, pady=10)
                vari = list(df.select_dtypes("number").columns)
                
                
                def ejecutarFuncion():
                    var_y = lista1.get()
                    var_x = lista2.get()
                    
                    if not var_y or not var_x:
                        from tkinter import messagebox
                        venReg.destroy()
                        venCal.destroy()
                        messagebox.showwarning("Atencion", "Por favor selecciona una variable Y y una variable X")
                    
                    else:
                        try: 
                            eje_x = df[var_x]
                            eje_y = df[var_y]
                            fig, ax = plt.subplots(figsize=(8, 6))
                            sns.regplot(
                                x = eje_x,
                                y = eje_y,
                                line_kws={"color":"red", "linewidth":1.5},
                                ax = ax
                                            
                            )
                            venReg.destroy()
                            venCal.destroy()
                            plt.show()
                        except:
                            from tkinter import messagebox
                            venReg.destroy()
                            venCal.destroy()
                            messagebox.showwarning("Presencia de valores faltantes", "Valores faltantes en columnas seleccionadas")
                
                lista1 = ttk.Combobox(venReg, values=vari, state="readonly")
                lista1.pack(padx=50, pady=10)
                
                Label(venReg, text="Variable X").pack(padx=50, pady=10)
                                
                lista2 = ttk.Combobox(venReg, values=vari, state="readonly")
                lista2.pack(padx=50, pady=10)
                
                Button(venReg, text="Ejecutar", command=ejecutarFuncion).pack(padx=50, pady=50)
                    
    Label(venCal, text="Seleccione una opcion").pack(padx=50, pady=10)   
    opciones = ["Matriz de correlacion", "Histograma de los errores", "Puntos de relacion"]
    opc = ttk.Combobox(venCal, values=opciones, state="readonly")
    opc.pack(padx=50, pady=10)
    
    Button(venCal, text="Ejecutar", command=seleccionCalculo).pack(padx=50, pady=10) 