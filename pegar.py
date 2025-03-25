from pathlib import Path

# Define el directorio donde están los archivos
pages_dir = Path("pages/")

# Crear una lista con los nombres procesados
nombres_filtrados = [
    "_".join(archivo.stem.split("_")[1:])  # Quitar el prefijo como "1_", "2_"
    for archivo in pages_dir.iterdir()
    if archivo.is_file() and archivo.suffix == ".py"  # Solo archivos .py
]

# Mostrar la lista de nombres filtrados
print("Lista de nombres filtrados:")
print(nombres_filtrados)




