from datetime import datetime

from Models.sistema_dia import SistemaDia
from Managers.excel_manager import ExcelManager
from Managers.recursos_manager import RecursosManager

class MotorCentral:
    def __init__(self):
        self.sistema = SistemaDia()
        self.excel = ExcelManager()
        self.recursos = RecursosManager()

    def ejecutar(self):
        ahora = datetime.now()

        self.sistema.fecha = ahora.date()
        self.sistema.fecha_texto = ahora.strftime("%d-%m-%Y")
        self.sistema.hora_actual = ahora.strftime("%H:%M")

        self.excel.cargar()
        self.recursos.cargar()

        self.sistema.contexto["excel"] = self.excel.resumen()
        self.sistema.recursos = self.recursos.resumen()

        self._analizar_contexto()
        self._generar_decisiones_base()
        self.sistema.ordenar_decisiones()

        return self.sistema

    def _analizar_contexto(self):
        hojas = self.sistema.contexto["excel"]["hojas"]

        if "SERPAT TURNOS" in hojas:
            self.sistema.agregar_alerta(
                "SERPAT",
                90,
                "Calendario laboral detectado",
                "Usar SERPAT TURNOS para adaptar el día."
            )

        if "PENDIENTES" in hojas:
            self.sistema.agregar_alerta(
                "Pendientes",
                95,
                "Pendientes detectados",
                "Integrar pendientes en la priorización diaria."
            )

        if "VISION_BOARD" in hojas:
            self.sistema.agregar_alerta(
                "Identidad",
                70,
                "Vision Board detectado",
                "Usar Vision Board para visualización diaria."
            )

        if "DESARROLLO_PERSONAL" in hojas:
            self.sistema.agregar_alerta(
                "Desarrollo Personal",
                75,
                "Desarrollo personal detectado",
                "Integrar lectura, hábitos e identidad."
            )

    def _generar_decisiones_base(self):
        self.sistema.agregar_decision(
            "Sistema",
            100,
            "Abrir Centro de Comando y revisar prioridades.",
            "Motor Central IA activo.",
            "20_Registro_Diario; 21_KPI_Diario"
        )
        self.sistema.agregar_decision(
            "Universidad",
            95,
            "Revisar evaluación crítica, contenidos, errores y próxima entrega.",
            "Universidad debe pasar de bloque genérico a instrucción específica.",
            "61_T2_Ramos; 62_T2_Evaluaciones; 64_T2_Errores"
        )
        self.sistema.agregar_decision(
            "Salud",
            85,
            "Registrar presión, energía, sueño, medicamento e hidratación.",
            "Proteger capital biológico.",
            "H02_Registro_Salud; H03_Presión_Log"
        )
        self.sistema.agregar_decision(
            "Finanzas",
            80,
            "Registrar movimientos, revisar gastos y actualizar caja.",
            "Mantener visibilidad financiera.",
            "11_Ingresos; 12_Gastos; 13_Deudas; 18_Conciliacion_Bancaria_V3"
        )
        self.sistema.agregar_decision(
            "Empresas",
            75,
            "Ejecutar una acción empresarial real con evidencia.",
            "MGC, LNH o CaptaPropIA no deben quedar sin avance.",
            "30_MGC_CRM; 33_Seguimientos; 76_CaptaPropIA"
        )
