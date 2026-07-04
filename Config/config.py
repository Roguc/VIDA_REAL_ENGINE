from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
EXCEL_DIR = ROOT_DIR / "Excel"
RECURSOS_DIR = ROOT_DIR / "Recursos"
SALIDAS_DIR = ROOT_DIR / "Salidas"
WORD_DIR = SALIDAS_DIR / "Word"
LOGS_DIR = SALIDAS_DIR / "Logs"
DASHBOARD_DIR = SALIDAS_DIR / "Dashboard"
FRONTEND_DIR = ROOT_DIR / "Frontend"

WORD_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
FRONTEND_DIR.mkdir(parents=True, exist_ok=True)

HOJAS_MOTOR = [
    "00_GENERADOR_DIA",
    "00_MOTOR_VIDA_REAL",
    "00_REGLAS_VIDA_REAL",
    "00_PLANTILLAS_BLOQUES",
]

HOJA_SERPAT = "SERPAT TURNOS"
HOJA_VISION = "VISION_BOARD"
HOJA_PENDIENTES = "PENDIENTES"
HOJA_DESARROLLO = "DESARROLLO_PERSONAL"
