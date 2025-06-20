import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def ejecutar_opcion(opcion):
    ejecutable = "ControllerNodeCPP.exe"
    if not os.path.exists(ejecutable):
        messagebox.showerror("Error", "No se encuentra el ejecutable ControllerNodeCPP.exe.")
        return

    try:
        proceso = subprocess.Popen([ejecutable], stdin=subprocess.PIPE)
        proceso.stdin.write(f"{opcion}\n".encode())
        proceso.stdin.flush()
    except Exception as e:
        messagebox.showerror("Error al ejecutar", str(e))

# Interfaz
ventana = tk.Tk()
ventana.title("Cliente - Control de Archivos")
ventana.geometry("350x250")

tk.Label(ventana, text="Control de archivos distribuido", font=("Arial", 14)).pack(pady=10)

tk.Button(ventana, text="1️⃣ Enviar archivo", width=25, command=lambda: ejecutar_opcion(1)).pack(pady=5)
tk.Button(ventana, text="2️⃣ Reconstruir archivo", width=25, command=lambda: ejecutar_opcion(2)).pack(pady=5)
tk.Button(ventana, text="3️⃣ Eliminar archivo", width=25, command=lambda: ejecutar_opcion(3)).pack(pady=5)

tk.Button(ventana, text="❌ Salir", width=25, command=ventana.destroy).pack(pady=20)

ventana.mainloop()
