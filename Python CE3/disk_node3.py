import xml.etree.ElementTree as ET
import os
from flask import Flask, request, jsonify

# Leer configuración
def read_config():
    tree = ET.parse('config3.xml')#Para el disk_node3.py
    root = tree.getroot()
    ip = root.find('ip').text
    port = int(root.find('port').text)
    path = root.find('path').text
    return ip, port, path

ip, port, storage_path = read_config()

# Crear carpeta de almacenamiento si no existe
os.makedirs(storage_path, exist_ok=True)

app = Flask(__name__)

# Endpoint para guardar un bloque
@app.route('/store_block', methods=['POST'])
def store_block():
    data = request.get_json()
    block_id = data['block_id']
    content = data['data']
    with open(f"{storage_path}/{block_id}.blk", "w") as f:
        f.write(content)
    return jsonify({"status": "ok", "message": "Block stored"}), 200

# Endpoint para leer un bloque
@app.route('/read_block/<block_id>', methods=['GET'])
def read_block(block_id):
    try:
        with open(f"{storage_path}/{block_id}.blk", "r") as f:
            content = f.read()
        return jsonify({"status": "ok", "data": content}), 200
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "Block not found"}), 404


@app.route('/delete_block/<block_id>', methods=['DELETE'])
def delete_block(block_id):
    file_path = f"{storage_path}/{block_id}.blk"
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"status": "ok", "message": f"Block {block_id} deleted"}), 200
    else:
        return jsonify({"status": "error", "message": f"Block {block_id} not found"}), 404

if __name__ == "__main__":
    print(f"Iniciando Disk Node en http://{ip}:{port}")
    app.run(host=ip, port=port)
