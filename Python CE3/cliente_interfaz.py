import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def ejecutar_programa(opcion, archivo_path):
    ejecutable = "ControllerNodeCPP.exe"  # Asegúrate de que esté en el mismo directorio que este script
    if not os.path.exists(ejecutable):
        messagebox.showerror("Error", "No se encuentra el ejecutable ControllerNodeCPP.exe en el directorio actual.")
        return

    try:
        proceso = subprocess.Popen([ejecutable], stdin=subprocess.PIPE, text=True)
        proceso.stdin.write(f"{opcion}\n")
        proceso.stdin.write(f"{archivo_path}\n")
        proceso.stdin.flush()
        proceso.stdin.close()
    except Exception as e:
        messagebox.showerror("Error al ejecutar", str(e))


def seleccionar_y_enviar():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo a enviar")
    if archivo:
        ejecutar_programa(1, archivo)

def seleccionar_y_reconstruir():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de metadatos", filetypes=[("JSON files", "*.json")])
    if archivo:
        ejecutar_programa(2, archivo)

def seleccionar_y_eliminar():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de metadatos", filetypes=[("JSON files", "*.json")])
    if archivo:
        ejecutar_programa(3, archivo)

# Interfaz
ventana = tk.Tk()
ventana.title("Cliente - Control de Archivos")
ventana.geometry("500x400")

tk.Label(ventana, text="Sistema Distribuido - Cliente", font=("Arial", 16)).pack(pady=15)

tk.Button(ventana, text="📤 Enviar archivo", width=30, command=seleccionar_y_enviar).pack(pady=10)
tk.Button(ventana, text="🧱 Reconstruir archivo", width=30, command=seleccionar_y_reconstruir).pack(pady=10)
tk.Button(ventana, text="❌ Eliminar archivo", width=30, command=seleccionar_y_eliminar).pack(pady=10)

tk.Button(ventana, text="Salir", width=30, command=ventana.destroy).pack(pady=25)

ventana.mainloop()
