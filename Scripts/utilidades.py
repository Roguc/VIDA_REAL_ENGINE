from datetime import datetime, date, time, timedelta
from pathlib import Path

def limpiar_texto(valor):
    if valor is None:
        return ""
    return str(valor).strip()

def buscar_excel(carpeta_excel: Path):
    archivos = list(carpeta_excel.glob("*.xlsx"))
    if not archivos:
        raise FileNotFoundError(f"No se encontró Excel en: {carpeta_excel}")
    archivos.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return archivos[0]

def escribir_log(ruta_log: Path, mensaje: str):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ruta_log, "a", encoding="utf-8") as f:
        f.write(f"[{fecha}] {mensaje}\n")

def normalizar_fecha(valor):
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    texto = limpiar_texto(valor)
    if not texto:
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(texto, fmt).date()
        except ValueError:
            pass
    return None

def normalizar_hora(valor):
    if valor is None or valor == "":
        return ""
    if isinstance(valor, datetime):
        return valor.strftime("%H:%M")
    if isinstance(valor, time):
        return valor.strftime("%H:%M")
    if isinstance(valor, (int, float)):
        # Excel time as fraction of day
        total_min = int(round(float(valor) * 24 * 60))
        h = (total_min // 60) % 24
        m = total_min % 60
        return f"{h:02d}:{m:02d}"
    texto = limpiar_texto(valor)
    if not texto:
        return ""
    return texto.replace(".", ":")

def hoy():
    return datetime.now().date()

def nombre_dia_es(fecha):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return dias[fecha.weekday()]
