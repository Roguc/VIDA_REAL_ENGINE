from __future__ import annotations

from datetime import date, datetime, time
from pathlib import Path
from typing import Any, Dict, List, Optional

from openpyxl import load_workbook

DIAS_ES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def clean(v: Any) -> str:
    if v is None:
        return ""
    return str(v).strip()


def parse_date(v: Any) -> Optional[date]:
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    s = clean(v)
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def parse_time(v: Any) -> str:
    if v is None or v == "":
        return ""
    if isinstance(v, datetime):
        return v.strftime("%H:%M")
    if isinstance(v, time):
        return v.strftime("%H:%M")
    if isinstance(v, (int, float)):
        minutes = int(round(float(v) * 24 * 60))
        return f"{(minutes // 60) % 24:02d}:{minutes % 60:02d}"
    return clean(v).replace(".", ":")


class ExcelManager:
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        self.excel_dir = self.root_dir / "Excel"
        self.path = self._find_excel()
        self.wb = load_workbook(self.path, data_only=True)

    def _find_excel(self) -> Path:
        files = list(self.excel_dir.glob("*.xlsx"))
        if not files:
            raise FileNotFoundError(f"No se encontró archivo Excel en {self.excel_dir}")
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return files[0]

    def sheet_names(self) -> List[str]:
        return list(self.wb.sheetnames)

    def has_sheet(self, name: str) -> bool:
        return name in self.wb.sheetnames

    def workbook_summary(self) -> Dict[str, Any]:
        return {"archivo": self.path.name, "ruta": str(self.path), "hojas": len(self.wb.sheetnames), "lista_hojas": self.sheet_names()}

    def _header_table(self, sheet: str, required_headers: List[str]) -> List[Dict[str, Any]]:
        if sheet not in self.wb.sheetnames:
            return []
        ws = self.wb[sheet]
        headers = None
        header_row = None
        for idx, row in enumerate(ws.iter_rows(values_only=True), start=1):
            vals = [clean(v) for v in row]
            if all(h in vals for h in required_headers):
                headers = vals
                header_row = idx
                break
        if not headers:
            return []
        data = []
        for row in ws.iter_rows(min_row=header_row + 1, values_only=True):
            if not row or all(v is None for v in row):
                continue
            item = {}
            for i, h in enumerate(headers):
                if h:
                    item[h] = row[i] if i < len(row) else None
            data.append(item)
        return data

    def read_generador_dia(self) -> Dict[str, Any]:
        if "00_GENERADOR_DIA" not in self.wb.sheetnames:
            return {}
        ws = self.wb["00_GENERADOR_DIA"]
        out = {}
        for row in ws.iter_rows(min_row=1, max_row=80, values_only=True):
            if not row or row[0] is None:
                continue
            k = clean(row[0])
            v = row[1] if len(row) > 1 else ""
            if k:
                out[k] = v
        return out

    def read_serpat_turnos(self) -> List[Dict[str, Any]]:
        rows = self._header_table("SERPAT TURNOS", ["Fecha", "Turno"])
        out = []
        for r in rows:
            f = parse_date(r.get("Fecha"))
            if not f:
                continue
            turno = clean(r.get("Turno"))
            tipo = clean(r.get("Tipo"))
            ingreso = parse_time(r.get("Ingreso"))
            salida = parse_time(r.get("Salida"))
            low = f"{turno} {tipo}".lower()
            if "libre" in low:
                tipo_dia = "Libre"
                turno_serpat = "Libre"
            elif "tex" in low:
                tipo_dia = "TEX"
                turno_serpat = "TEX"
            elif turno.upper() == "N" or "noche" in low:
                tipo_dia = "Turno de Noche"
                turno_serpat = f"{ingreso or '21:00'}–{salida or '08:00'}"
            elif turno.upper() == "M" or "mañana" in low:
                tipo_dia = "Turno de Mañana"
                turno_serpat = f"{ingreso or '08:00'}–{salida or '17:00'}"
            elif turno.upper() == "T" or "tarde" in low:
                tipo_dia = "Turno de Tarde"
                turno_serpat = f"{ingreso or '12:30'}–{salida or '21:00'}"
            else:
                tipo_dia = tipo or turno or "Día operativo"
                turno_serpat = f"{ingreso}–{salida}" if ingreso or salida else tipo_dia
            out.append({
                "fecha": f,
                "dia": clean(r.get("Día")) or DIAS_ES[f.weekday()],
                "turno": turno,
                "tipo": tipo,
                "tipo_dia": tipo_dia,
                "turno_serpat": turno_serpat,
                "ingreso": ingreso,
                "salida": salida,
                "salida_casa": parse_time(r.get("Salida Casa")),
                "llegada_casa": parse_time(r.get("Llegada Casa")),
                "estado": clean(r.get("Estado")),
                "observaciones": clean(r.get("Observaciones")),
            })
        return out

    def get_turno(self, target: date) -> Dict[str, Any]:
        for t in self.read_serpat_turnos():
            if t["fecha"] == target:
                return t
        return {}

    def read_pendientes(self, max_items: int = 20) -> List[Dict[str, Any]]:
        rows = self._header_table("PENDIENTES", ["ID", "Área", "Tarea"])
        out = []
        for r in rows:
            estado = clean(r.get("Estado"))
            if estado.lower() in {"completado", "cumplido", "cerrado", "ok"}:
                continue
            out.append({
                "id": clean(r.get("ID")),
                "area": clean(r.get("Área")),
                "subarea": clean(r.get("Subárea")),
                "tarea": clean(r.get("Tarea")) or "Pendiente sin descripción",
                "prioridad": clean(r.get("Prioridad")),
                "estado": estado or "Pendiente",
                "fecha_limite": clean(r.get("Fecha Límite")),
                "observaciones": clean(r.get("Observaciones")),
            })
            if len(out) >= max_items:
                break
        return out

    def read_vision_board(self, max_items: int = 20) -> List[Dict[str, Any]]:
        rows = self._header_table("VISION_BOARD", ["Categoría", "Objetivo 2042"])
        out = []
        for r in rows:
            out.append({
                "categoria": clean(r.get("Categoría")),
                "objetivo": clean(r.get("Objetivo 2042")),
                "imagen": clean(r.get("Imagen / Referencia")),
                "ruta": clean(r.get("Ruta (09_PANEL_VISION)")),
                "estado": clean(r.get("Estado")),
                "observaciones": clean(r.get("Observaciones")),
            })
            if len(out) >= max_items:
                break
        return out

    def read_desarrollo_personal(self) -> Dict[str, Any]:
        if "DESARROLLO_PERSONAL" not in self.wb.sheetnames:
            return {}
        ws = self.wb["DESARROLLO_PERSONAL"]
        out = {}
        for row in ws.iter_rows(values_only=True):
            if not row or row[0] is None:
                continue
            k = clean(row[0])
            v = clean(row[1] if len(row) > 1 else "")
            if k and v:
                out[k] = v
        return out

    def read_sheet_preview(self, sheet: str, max_rows: int = 15) -> List[List[Any]]:
        if sheet not in self.wb.sheetnames:
            return []
        ws = self.wb[sheet]
        rows = []
        for row in ws.iter_rows(max_row=max_rows, values_only=True):
            rows.append([clean(v) for v in row])
        return rows

    def read_domain_summary(self) -> Dict[str, Any]:
        domains = {
            "finanzas": [s for s in self.wb.sheetnames if any(x in s.lower() for x in ["ingres", "gastos", "deudas", "finanza", "conciliacion", "patrimonio"])],
            "salud": [s for s in self.wb.sheetnames if s.startswith("H") or "salud" in s.lower()],
            "universidad": [s for s in self.wb.sheetnames if "t2" in s.lower() or "universidad" in s.lower()],
            "empresas": [s for s in self.wb.sheetnames if any(x in s.lower() for x in ["mgc", "lnr", "captaprop", "holding", "empresa"])],
        }
        return {k: {"hojas": v, "total": len(v)} for k, v in domains.items()}
