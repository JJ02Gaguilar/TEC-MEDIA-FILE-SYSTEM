import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import json

def seleccionar_pdf():
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if file_path:
        entry_archivo.delete(0, tk.END)
        entry_archivo.insert(0, file_path)

def seleccionar_metadatos():
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo de metadatos",
        filetypes=[("Archivos JSON", "metadata_*.json")]
    )
    if file_path:
        entry_metadatos.delete(0, tk.END)
        entry_metadatos.insert(0, file_path)

def ejecutar_cpp_con_argumento(opcion, argumento):
    ejecutable = "ControllerNodeCPP.exe"
    if not os.path.exists(ejecutable):
        messagebox.showerror("Error", "No se encuentra el ejecutable ControllerNodeCPP.exe.")
        return

    try:
        proceso = subprocess.Popen([ejecutable], stdin=subprocess.PIPE, text=True)
        proceso.communicate(f"{opcion}\n{argumento}\n")
        return True
    except Exception as e:
        messagebox.showerror("Error al ejecutar", str(e))
        return False

def enviar_archivo():
    path = entry_archivo.get()
    if not path or not path.endswith(".pdf"):
        messagebox.showwarning("Archivo inválido", "Debe seleccionar un archivo PDF válido.")
        return
    nombre = os.path.basename(path)
    destino = os.path.join(os.getcwd(), nombre)
    if path != destino:
        with open(path, "rb") as src, open(destino, "wb") as dst:
            dst.write(src.read())
    if ejecutar_cpp_con_argumento(1, nombre):
        messagebox.showinfo("Éxito", f"Archivo '{nombre}' enviado correctamente.")

def reconstruir_archivo():
    path = entry_metadatos.get()
    if not path.endswith(".json"):
        messagebox.showwarning("Archivo inválido", "Debe seleccionar un archivo JSON válido.")
        return
    nombre = os.path.basename(path)
    if ejecutar_cpp_con_argumento(2, nombre):
        try:
            with open(path, "r") as f:
                metadata = json.load(f)
                original = os.path.basename(metadata["filename"])
                resultado = os.path.join(os.getcwd(), f"reconstruido_{original}")
                if os.path.exists(resultado):
                    os.startfile(resultado)
                    messagebox.showinfo("Reconstruido", f"Archivo reconstruido y abierto: {resultado}")
        except Exception as e:
            messagebox.showwarning("Reconstruido", "Archivo reconstruido pero no se pudo abrir.")

def eliminar_archivo():
    path = entry_metadatos.get()
    if not path.endswith(".json"):
        messagebox.showwarning("Archivo inválido", "Debe seleccionar un archivo JSON válido.")
        return
    nombre = os.path.basename(path)
    if ejecutar_cpp_con_argumento(3, nombre):
        messagebox.showinfo("Eliminado", f"Bloques y metadatos de '{nombre}' eliminados.")

# GUI
ventana = tk.Tk()
ventana.title("Gestor de Archivos PDF Distribuidos")
ventana.geometry("600x400")

tk.Label(ventana, text="Archivo PDF:", font=("Arial", 11)).pack(pady=5)
entry_archivo = tk.Entry(ventana, width=60)
entry_archivo.pack(pady=2)
tk.Button(ventana, text="Seleccionar PDF", command=seleccionar_pdf).pack(pady=2)
tk.Button(ventana, text="Enviar archivo", command=enviar_archivo).pack(pady=8)

tk.Label(ventana, text="Archivo de metadatos:", font=("Arial", 11)).pack(pady=5)
entry_metadatos = tk.Entry(ventana, width=60)
entry_metadatos.pack(pady=2)
tk.Button(ventana, text="Seleccionar metadatos", command=seleccionar_metadatos).pack(pady=2)

tk.Button(ventana, text="Reconstruir archivo", command=reconstruir_archivo).pack(pady=8)
tk.Button(ventana, text="Eliminar archivo", command=eliminar_archivo).pack(pady=4)

tk.Button(ventana, text="Salir", command=ventana.destroy).pack(pady=20)

ventana.mainloop()
