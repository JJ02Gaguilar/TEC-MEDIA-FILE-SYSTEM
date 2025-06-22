import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import json
import os

# ---------------------------- Funciones de Cliente ----------------------------
BLOCK_SIZE = 4096

def dividir_archivo_en_bloques(filepath):
    with open(filepath, "rb") as f:
        bloques = []
        while True:
            bloque = f.read(BLOCK_SIZE)
            if not bloque:
                break
            bloques.append(bloque)
    return bloques

def enviar_archivo():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not filepath:
        return

    nombre_archivo = os.path.basename(filepath)
    bloques = dividir_archivo_en_bloques(filepath)

    metadata = {
        "filename": nombre_archivo,
        "blocks": []
    }

    for i, bloque in enumerate(bloques):
        bloque_str = bloque.decode("latin1")
        payload = {
            "block_id": i,
            "data": bloque_str
        }

        try:
            res = requests.post("http://127.0.0.1:5001/store_block", json=payload)
            if res.status_code == 200:
                metadata["blocks"].append({
                    "block_id": i,
                    "node": "127.0.0.1",
                    "port": 5001
                })
        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar bloque {i}: {e}")
            return

    with open(f"metadata_{nombre_archivo}.json", "w") as f:
        json.dump(metadata, f, indent=4)

    messagebox.showinfo("Éxito", "Archivo enviado y metadatos guardados.")

def reconstruir_archivo():
    metadata_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not metadata_path:
        return

    try:
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
    except:
        messagebox.showerror("Error", "Archivo de metadatos inválido.")
        return

    output_file = f"reconstruido_{metadata['filename']}"
    with open(output_file, "wb") as out:
        for bloque_info in metadata["blocks"]:
            try:
                url = f"http://{bloque_info['node']}:{bloque_info['port']}/read_block/{bloque_info['block_id']}"
                res = requests.get(url)
                if res.status_code == 200:
                    bloque = res.json()["data"].encode("latin1")
                    out.write(bloque)
            except:
                messagebox.showerror("Error", f"No se pudo recuperar el bloque {bloque_info['block_id']}.")

    messagebox.showinfo("Éxito", f"Archivo reconstruido: {output_file}")

def eliminar_archivo():
    metadata_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not metadata_path:
        return

    try:
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
    except:
        messagebox.showerror("Error", "Archivo de metadatos inválido.")
        return

    for bloque_info in metadata["blocks"]:
        try:
            url = f"http://{bloque_info['node']}:{bloque_info['port']}/delete_block/{bloque_info['block_id']}"
            requests.delete(url)
        except:
            pass

    os.remove(metadata_path)
    messagebox.showinfo("Éxito", "Bloques y archivo de metadatos eliminados.")

# ---------------------------- Interfaz Tkinter ----------------------------
ventana = tk.Tk()
ventana.title("Gestor de Archivos PDF Distribuidos")
ventana.geometry("600x400")

tk.Label(ventana, text="Cliente - Sistema Distribuido de Archivos", font=("Arial", 14)).pack(pady=10)

tk.Button(ventana, text="Enviar Archivo PDF", command=enviar_archivo, width=40).pack(pady=5)
tk.Button(ventana, text="Reconstruir Archivo", command=reconstruir_archivo, width=40).pack(pady=5)
tk.Button(ventana, text="Eliminar Archivo", command=eliminar_archivo, width=40).pack(pady=5)
tk.Button(ventana, text="Salir", command=ventana.destroy, width=40).pack(pady=20)

ventana.mainloop()
