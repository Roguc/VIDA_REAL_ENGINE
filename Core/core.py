from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from Managers.excel_manager import ExcelManager, DIAS_ES
from Managers.recursos_manager import RecursosManager
from Models.sistema_dia import SistemaDia
from Core.decision_engine import DecisionEngine


class VidaRealCore:
    def __init__(self, root_dir: Path | None = None):
        self.root_dir = Path(root_dir or Path(__file__).resolve().parent.parent)
        self.excel = ExcelManager(self.root_dir)
        self.recursos = RecursosManager(self.root_dir)
        self.decision_engine = DecisionEngine()

    def construir_sistema_dia(self, fecha_objetivo: date | None = None) -> SistemaDia:
        fecha = fecha_objetivo or datetime.now().date()
        s = SistemaDia()
        s.fecha = fecha
        s.fecha_iso = fecha.strftime("%Y-%m-%d")
        s.dia_semana = DIAS_ES[fecha.weekday()]
        s.fecha_larga = f"{s.dia_semana} {fecha.strftime('%d-%m-%Y')}"

        gen = self.excel.read_generador_dia()
        turno = self.excel.get_turno(fecha)
        desarrollo = self.excel.read_desarrollo_personal()

        s.excel = self.excel.workbook_summary()
        s.recursos = self.recursos.indexar()
        s.serpat = turno
        s.pendientes = self.excel.read_pendientes()
        s.vision_board = self.excel.read_vision_board()
        s.desarrollo_personal = desarrollo

        s.contexto = {
            "tipo_dia": turno.get("tipo_dia") or str(gen.get("Tipo día", "Día operativo")),
            "turno_serpat": turno.get("turno_serpat") or str(gen.get("Turno SERPAT", "")),
            "semana_academica": str(gen.get("Semana académica", "")),
            "energia": str(gen.get("Nivel energía", "Pendiente")),
            "salud_alerta": str(gen.get("Presión / alerta salud", "Pendiente")),
            "cierre_mes": str(gen.get("Cierre de mes", "")),
        }

        s.universidad = {
            "prioridad": str(gen.get("Prioridad académica", "")),
            "evaluacion_critica": str(gen.get("Evaluación crítica", "")),
            "semana": str(gen.get("Semana académica", "")),
            "hojas_detectadas": self.excel.read_domain_summary().get("universidad", {}),
        }
        s.finanzas = {"hojas_detectadas": self.excel.read_domain_summary().get("finanzas", {})}
        s.salud = {"alerta": s.contexto.get("salud_alerta"), "hojas_detectadas": self.excel.read_domain_summary().get("salud", {})}
        s.empresas = {"prioridad": str(gen.get("Prioridad empresa", "")), "hojas_detectadas": self.excel.read_domain_summary().get("empresas", {})}
        s.kpis = {"dominios": self.excel.read_domain_summary()}

        return self.decision_engine.aplicar(s)
