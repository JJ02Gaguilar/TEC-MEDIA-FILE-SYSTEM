import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Listbox, Scrollbar
import os
import subprocess
import shutil

# Config
METADATA_DIR = "pdfs"
EXECUTABLE = "ControllerNodeCPP.exe"

os.makedirs(METADATA_DIR, exist_ok=True)

# Funciones
def ejecutar_backend(opcion):
    try:
        proceso = subprocess.Popen([EXECUTABLE], stdin=subprocess.PIPE)
        proceso.stdin.write(f"{opcion}\n".encode())
        proceso.stdin.flush()
        proceso.communicate()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def agregar_archivo():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not filepath:
        return
    filename = os.path.basename(filepath)
    shutil.copy(filepath, filename)  # Copiar al directorio actual
    ejecutar_backend(1)
    listar_documentos()

def eliminar_documento():
    selected = lista.curselection()
    if not selected:
        return
    nombre = lista.get(selected[0])
    os.rename(nombre, "tempinput")  # Renombrar para que el C++ lo use como entrada
    meta = f"metadata_{nombre}.json"
    if os.path.exists(meta):
        shutil.copy(meta, "tempinput.json")
    ejecutar_backend(3)
    listar_documentos()

def reconstruir_documento():
    selected = lista.curselection()
    if not selected:
        return
    nombre = lista.get(selected[0])
    os.rename(f"metadata_{nombre}.json", "tempinput.json")
    ejecutar_backend(2)
    salida = f"reconstruido_{nombre}"
    if os.path.exists(salida):
        os.startfile(salida)
    listar_documentos()

def buscar_documento():
    nombre = simpledialog.askstring("Buscar", "Ingrese nombre del documento:")
    if nombre:
        resultados = [f for f in os.listdir() if f.endswith(".json") and nombre in f]
        lista.delete(0, tk.END)
        for r in resultados:
            nombre_pdf = r.replace("metadata_", "").replace(".json", "")
            lista.insert(tk.END, nombre_pdf)

def listar_documentos():
    lista.delete(0, tk.END)
    for f in os.listdir():
        if f.startswith("metadata_") and f.endswith(".json"):
            nombre = f.replace("metadata_", "").replace(".json", "")
            lista.insert(tk.END, nombre)

# GUI
ventana = tk.Tk()
ventana.title("Gestor de Archivos PDF")
ventana.geometry("500x450")

tk.Label(ventana, text="Documentos disponibles", font=("Arial", 14)).pack(pady=5)

frame_lista = tk.Frame(ventana)
frame_lista.pack()

scrollbar = Scrollbar(frame_lista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista = Listbox(frame_lista, height=10, width=50, yscrollcommand=scrollbar.set)
lista.pack()
scrollbar.config(command=lista.yview)

tk.Button(ventana, text=" Agregar PDF", command=agregar_archivo, width=30).pack(pady=5)
tk.Button(ventana, text=" Buscar documento", command=buscar_documento, width=30).pack(pady=5)
tk.Button(ventana, text=" Eliminar documento", command=eliminar_documento, width=30).pack(pady=5)
tk.Button(ventana, text=" Descargar / Ver PDF", command=reconstruir_documento, width=30).pack(pady=5)
tk.Button(ventana, text=" Refrescar lista", command=listar_documentos, width=30).pack(pady=5)
tk.Button(ventana, text="Salir", command=ventana.destroy, width=30).pack(pady=10)

listar_documentos()
ventana.mainloop()
