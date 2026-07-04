from Config.config import HOJA_VISION, HOJA_PENDIENTES, HOJA_DESARROLLO
from Scripts.utilidades import limpiar_texto

def leer_pendientes(wb, max_items=8):
    if HOJA_PENDIENTES not in wb.sheetnames:
        return []
    ws = wb[HOJA_PENDIENTES]
    pendientes = []
    headers = None

    for row in ws.iter_rows(values_only=True):
        vals = [limpiar_texto(v) for v in row]
        if "ID" in vals and "Área" in vals and "Tarea" in vals:
            headers = vals
            continue
        if headers and vals and vals[0]:
            item = dict(zip(headers, row))
            estado = limpiar_texto(item.get("Estado"))
            if estado.lower() not in ["completado", "cumplido", "cerrado"]:
                pendientes.append({
                    "id": limpiar_texto(item.get("ID")),
                    "area": limpiar_texto(item.get("Área")),
                    "subarea": limpiar_texto(item.get("Subárea")),
                    "tarea": limpiar_texto(item.get("Tarea")) or "Pendiente sin descripción",
                    "prioridad": limpiar_texto(item.get("Prioridad")),
                    "estado": estado,
                    "avance": limpiar_texto(item.get("Avance %")),
                    "observaciones": limpiar_texto(item.get("Observaciones")),
                })
        if len(pendientes) >= max_items:
            break
    return pendientes

def leer_vision_board(wb, max_items=8):
    if HOJA_VISION not in wb.sheetnames:
        return []
    ws = wb[HOJA_VISION]
    vision = []
    headers = None

    for row in ws.iter_rows(values_only=True):
        vals = [limpiar_texto(v) for v in row]
        if "Categoría" in vals and "Objetivo 2042" in vals:
            headers = vals
            continue
        if headers and vals and vals[0]:
            item = dict(zip(headers, row))
            vision.append({
                "categoria": limpiar_texto(item.get("Categoría")),
                "objetivo": limpiar_texto(item.get("Objetivo 2042")),
                "imagen": limpiar_texto(item.get("Imagen / Referencia")),
                "ruta": limpiar_texto(item.get("Ruta (09_PANEL_VISION)")),
                "estado": limpiar_texto(item.get("Estado")),
            })
        if len(vision) >= max_items:
            break
    return vision

def leer_desarrollo_personal(wb):
    data = {
        "mision": "",
        "vision": "",
        "proposito": "",
        "ley": "",
        "valores": "",
        "libro": "",
        "capitulo": "",
        "estado": "",
        "proximos": "",
    }
    if HOJA_DESARROLLO not in wb.sheetnames:
        return data
    ws = wb[HOJA_DESARROLLO]
    for row in ws.iter_rows(values_only=True):
        k = limpiar_texto(row[0] if len(row) > 0 else "")
        v = limpiar_texto(row[1] if len(row) > 1 else "")
        lk = k.lower()
        if lk == "misión":
            data["mision"] = v
        elif lk == "visión 2042":
            data["vision"] = v
        elif lk == "propósito":
            data["proposito"] = v
        elif lk == "ley 001":
            data["ley"] = v
        elif lk == "valores":
            data["valores"] = v
        elif lk == "leyendo":
            data["libro"] = v
        elif lk == "capítulo actual":
            data["capitulo"] = v
        elif lk == "estado":
            data["estado"] = v
        elif lk == "próximos libros":
            data["proximos"] = v
    return data
