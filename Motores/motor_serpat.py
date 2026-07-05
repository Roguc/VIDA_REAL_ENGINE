from Config.config import HOJA_SERPAT
from Scripts.utilidades import limpiar_texto, normalizar_fecha, normalizar_hora, nombre_dia_es


def _norm(txt):
    return limpiar_texto(txt).upper().replace(" ", "_").replace("-", "_")


def _resolver_hoja_serpat(wb):
    if HOJA_SERPAT in wb.sheetnames:
        return wb[HOJA_SERPAT]

    objetivo = _norm(HOJA_SERPAT)
    for name in wb.sheetnames:
        n = _norm(name)
        if objetivo == n or objetivo in n or n in objetivo:
            return wb[name]
    return None

def leer_turnos_serpat(wb):
    ws = _resolver_hoja_serpat(wb)
    if ws is None:
        return []

    header_row = None
    headers = []

    for idx, row in enumerate(ws.iter_rows(min_row=1, max_row=15, values_only=True), start=1):
        valores = [limpiar_texto(v) for v in row]
        valores_norm = [_norm(v) for v in valores]
        if "FECHA" in valores_norm and "TURNO" in valores_norm:
            header_row = idx
            headers = valores
            break

    if not header_row:
        return []

    turnos = []
    for row in ws.iter_rows(min_row=header_row + 1, values_only=True):
        if not row or row[0] is None:
            continue

        item = {}
        for i, h in enumerate(headers):
            if not h:
                continue
            item[h] = row[i] if i < len(row) else ""

        fecha = normalizar_fecha(item.get("Fecha"))
        if not fecha:
            continue

        ingreso = normalizar_hora(item.get("Ingreso"))
        salida = normalizar_hora(item.get("Salida"))

        turno = limpiar_texto(item.get("Turno"))
        tipo = limpiar_texto(item.get("Tipo"))
        obs = limpiar_texto(item.get("Observaciones"))

        if turno.lower() == "libre" or tipo.lower() == "libre":
            tipo_dia = "Libre"
            turno_txt = "Libre"
        elif "tex" in turno.lower() or "tex" in tipo.lower():
            tipo_dia = "TEX"
            turno_txt = "TEX"
        elif turno.upper() == "N" or "noche" in tipo.lower():
            tipo_dia = "Turno de Noche"
            turno_txt = f"{ingreso or '21:00'}–{salida or '08:00'}"
        elif turno.upper() == "M" or "mañana" in tipo.lower():
            tipo_dia = "Turno de Mañana"
            turno_txt = f"{ingreso or '08:00'}–{salida or '17:00'}"
        elif turno.upper() == "T" or "tarde" in tipo.lower():
            tipo_dia = "Turno de Tarde"
            turno_txt = f"{ingreso or '12:30'}–{salida or '21:00'}"
        else:
            tipo_dia = tipo or turno or "Día operativo"
            turno_txt = f"{ingreso}–{salida}" if ingreso or salida else tipo_dia

        turnos.append({
            "fecha": fecha,
            "dia": limpiar_texto(item.get("Día")) or nombre_dia_es(fecha),
            "turno": turno,
            "tipo": tipo,
            "tipo_dia": tipo_dia,
            "turno_serpat": turno_txt,
            "salida_casa": normalizar_hora(item.get("Salida Casa")),
            "ingreso": ingreso,
            "colacion": normalizar_hora(item.get("Colación")),
            "salida": salida,
            "llegada_casa": normalizar_hora(item.get("Llegada Casa")),
            "trabajadas": item.get("Trabajadas"),
            "nocturnas": item.get("Nocturnas"),
            "extras": item.get("Extras"),
            "estado": limpiar_texto(item.get("Estado")),
            "observaciones": obs,
        })

    return turnos

def obtener_turno_fecha(wb, fecha):
    for t in leer_turnos_serpat(wb):
        if t["fecha"] == fecha:
            return t
    return None
