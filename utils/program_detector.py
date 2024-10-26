# utils/program_detector.py
import os

def detect_installed_programs(directories=None):
    """Detecta archivos .exe en las rutas proporcionadas."""
    if directories is None:
        # Rutas típicas donde se encuentran los programas instalados en Windows
        directories = [
            "C:\\Program Files",
            "C:\\Program Files (x86)"
        ]
    
    exe_files = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".exe"):
                    exe_files.append(file)
    return sorted(set(exe_files))  # Eliminar duplicados y ordenar alfabéticamente
