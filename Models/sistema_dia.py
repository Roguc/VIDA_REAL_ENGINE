from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List


@dataclass
class SistemaDia:
    fecha: date | None = None
    fecha_iso: str = ""
    fecha_larga: str = ""
    dia_semana: str = ""

    contexto: Dict[str, Any] = field(default_factory=dict)
    identidad: Dict[str, Any] = field(default_factory=dict)
    serpat: Dict[str, Any] = field(default_factory=dict)
    universidad: Dict[str, Any] = field(default_factory=dict)
    finanzas: Dict[str, Any] = field(default_factory=dict)
    salud: Dict[str, Any] = field(default_factory=dict)
    empresas: Dict[str, Any] = field(default_factory=dict)
    ancla: Dict[str, Any] = field(default_factory=dict)
    desarrollo_personal: Dict[str, Any] = field(default_factory=dict)
    vision_board: List[Dict[str, Any]] = field(default_factory=list)
    pendientes: List[Dict[str, Any]] = field(default_factory=list)
    recursos: Dict[str, Any] = field(default_factory=dict)
    excel: Dict[str, Any] = field(default_factory=dict)
    kpis: Dict[str, Any] = field(default_factory=dict)

    cronograma: List[Dict[str, Any]] = field(default_factory=list)
    alertas: List[Dict[str, Any]] = field(default_factory=list)
    decisiones: List[Dict[str, Any]] = field(default_factory=list)
    auditoria: List[Dict[str, Any]] = field(default_factory=list)

    salidas: Dict[str, Any] = field(default_factory=dict)

    def alerta(self, nivel: str, area: str, mensaje: str, accion: str = "") -> None:
        self.alertas.append({"nivel": nivel, "area": area, "mensaje": mensaje, "accion": accion})

    def decision(self, area: str, decision: str, motivo: str = "") -> None:
        self.decisiones.append({"area": area, "decision": decision, "motivo": motivo})

    def bloque(self, hora_inicio: str, hora_fin: str, area: str, titulo: str, actividad: str,
               registro: str = "", evidencia: str = "", capital: str = "", detalle: Dict[str, Any] | None = None) -> None:
        self.cronograma.append({
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "area": area,
            "titulo": titulo,
            "actividad": actividad,
            "registro": registro,
            "evidencia": evidencia,
            "capital": capital,
            "detalle": detalle or {},
        })

    def resumen(self) -> Dict[str, Any]:
        return {
            "fecha": self.fecha_iso,
            "fecha_larga": self.fecha_larga,
            "tipo_dia": self.contexto.get("tipo_dia", ""),
            "turno_serpat": self.serpat.get("turno_serpat", ""),
            "bloques": len(self.cronograma),
            "alertas": len(self.alertas),
            "pendientes": len(self.pendientes),
            "recursos": self.recursos.get("total_archivos", 0),
        }
