from datetime import datetime
from pathlib import Path

def log(texto: str) -> None:
    ahora = datetime.now().strftime("%H:%M:%S")
    print(f"[{ahora}] {texto}")

def guardar_log(contenido: str, nombre_archivo: str = "ejecucion.log") -> str:
    """Guarda contenido en archivo de log y retorna la ruta"""
    carpeta_logs = Path("Salidas/Logs")
    carpeta_logs.mkdir(parents=True, exist_ok=True)
    
    archivo = carpeta_logs / nombre_archivo
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return str(archivo)
    except Exception as e:
        print(f"Error guardando log: {e}")
        return ""
