TEC Media File System es un sistema de archivos distribuido desarrollado como parte de un proyecto universitario. Utiliza una arquitectura RAID 5 sobre nodos distribuidos, soportando tolerancia a fallos, reconstrucción de archivos y operaciones básicas como agregar, eliminar, buscar y descargar archivos (principalmente PDFs) a través de una GUI en Python y un controlador en C++.

Caracteristicas principales:
- Soporte para archivos PDF y otros formatos
- División en bloques de 4096 bytes (RAID 5)
- Interfaz gráfica en Python (Tkinter)
- Controlador en C++ para gestión de bloques
- Comunicación REST entre cliente y nodos
- Tolerancia a fallos: soporta pérdida de un nodo
- Buscar documentos por nombre
- Eliminar archivos del RAID
- Descargar archivos reconstruidos

Requirimientos:
- Python 3.8 o superior
- CMake 3.16 o superior
- g++ o compilador compatible con C++20
- Bibliotecas: requests (Python), httplib (C++)

Instalacion:
1. Clonar el repositorio
git clone https: https://github.com/JJ02Gaguilar/TEC-MEDIA-FILE-SYSTEM/tree/main
cd TEC-MEDIA-FILE-SYSTEM

3. Compilar el controlador en C++
cd ControllerNodeCPP
cmake .
make

4. Ejecutar nodos Python
Abrir varias terminales:
python disk_node1.py
python disk_node2.py
python disk_node3.py
python disk_node4.py

5. Ejecutar interfaz gráfica
cd ../Python\ CE3
python cliente_interfaz.py

