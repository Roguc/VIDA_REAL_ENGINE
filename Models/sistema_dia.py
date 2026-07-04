from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List

@dataclass
class SistemaDia:
    fecha: date | None = None
    fecha_texto: str = ""
    hora_actual: str = ""
    tipo_dia: str = ""
    turno_serpat: str = ""

    identidad: Dict[str, Any] = field(default_factory=dict)
    contexto: Dict[str, Any] = field(default_factory=dict)

    universidad: Dict[str, Any] = field(default_factory=dict)
    salud: Dict[str, Any] = field(default_factory=dict)
    finanzas: Dict[str, Any] = field(default_factory=dict)
    empresas: Dict[str, Any] = field(default_factory=dict)
    serpat: Dict[str, Any] = field(default_factory=dict)
    ancla: Dict[str, Any] = field(default_factory=dict)
    continuidad: Dict[str, Any] = field(default_factory=dict)
    recursos: Dict[str, Any] = field(default_factory=dict)

    pendientes: List[Dict[str, Any]] = field(default_factory=list)
    alertas: List[Dict[str, Any]] = field(default_factory=list)
    decisiones: List[Dict[str, Any]] = field(default_factory=list)
    cronograma: List[Dict[str, Any]] = field(default_factory=list)

    def agregar_alerta(self, area: str, prioridad: int, titulo: str, detalle: str) -> None:
        self.alertas.append({
            "area": area,
            "prioridad": prioridad,
            "titulo": titulo,
            "detalle": detalle,
        })

    def agregar_decision(self, area: str, prioridad: int, accion: str, motivo: str, registro: str = "") -> None:
        self.decisiones.append({
            "area": area,
            "prioridad": prioridad,
            "accion": accion,
            "motivo": motivo,
            "registro": registro,
        })

    def ordenar_decisiones(self) -> None:
        self.decisiones.sort(key=lambda x: x.get("prioridad", 0), reverse=True)
