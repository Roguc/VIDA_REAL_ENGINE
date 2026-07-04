from __future__ import annotations

from Models.sistema_dia import SistemaDia

CAPITALES = {
    "Universidad": "Capital intelectual",
    "Finanzas": "Capital financiero",
    "Salud": "Capital biológico",
    "Empresas": "Capital empresarial",
    "SERPAT": "Capital reputacional",
    "Ancla": "Capital psicológico",
    "Sistema": "Capital organizacional",
    "Desarrollo personal": "Capital cognitivo",
    "Imagen personal": "Capital de presencia",
}


class DecisionEngine:
    def aplicar(self, sistema: SistemaDia) -> SistemaDia:
        self._identidad(sistema)
        self._alertas(sistema)
        self._decisiones(sistema)
        self._cronograma(sistema)
        return sistema

    def _identidad(self, s: SistemaDia) -> None:
        desarrollo = s.desarrollo_personal or {}
        s.identidad = {
            "saludo": "Buenos días, Robinson.",
            "rol": "Director Ejecutivo de la construcción del Robinson 2042",
            "pregunta_maestra": "¿Qué parte del Robinson 2042 estoy construyendo hoy?",
            "ley_001": desarrollo.get("Ley 001") or "Nunca romper la cadena. Si no puedes 100%, avanza 20%. Si no puedes 20%, avanza 5%. Pero nunca cero.",
            "proposito": desarrollo.get("Propósito") or "Convertir cada día en capital acumulado.",
            "vision": desarrollo.get("Visión 2042") or "Holding internacional, patrimonio, salud, liderazgo, legado y libertad.",
        }

    def _alertas(self, s: SistemaDia) -> None:
        if not s.serpat:
            s.alerta("media", "SERPAT", "No se encontró turno SERPAT para la fecha automática.", "Revisar hoja SERPAT TURNOS.")
        if s.contexto.get("energia", "Pendiente") == "Pendiente":
            s.alerta("media", "Salud", "Energía pendiente.", "Registrar energía antes de exigir intensidad.")
        if s.contexto.get("salud_alerta", "Pendiente") == "Pendiente":
            s.alerta("media", "Salud", "Presión / alerta salud pendiente.", "Medir presión si corresponde.")
        if s.universidad.get("evaluacion_critica"):
            s.alerta("alta", "Universidad", f"Evaluación crítica activa: {s.universidad.get('evaluacion_critica')}", "Revisar Canvas y hoja de evaluaciones.")
        criticos = [p for p in s.pendientes if str(p.get("prioridad", "")).lower() in ["crítica", "critica", "alta"]]
        if criticos:
            s.alerta("alta", "Pendientes", f"Hay {len(criticos)} pendiente(s) críticos/altos.", "Resolver o reagendar hoy.")

    def _decisiones(self, s: SistemaDia) -> None:
        tipo = s.contexto.get("tipo_dia", "")
        if "Noche" in tipo:
            s.decision("Carga", "Día adaptado a turno nocturno.", "Proteger sueño y continuidad.")
        elif "Libre" in tipo:
            s.decision("Carga", "Día con mayor capacidad de avance.", "Usar bloques profundos sin saturación.")
        else:
            s.decision("Carga", "Día operativo normal.", "Ejecutar prioridades sin abrir frentes nuevos.")
        s.decision("Universidad", f"Prioridad académica: {s.universidad.get('prioridad', 'Pendiente')}", "Evitar acumulación académica.")
        s.decision("Empresas", f"Prioridad empresa: {s.empresas.get('prioridad', 'Pendiente')}", "Mantener empresas vivas con acción mínima.")

    def _bloque(self, s: SistemaDia, ini, fin, area, titulo, actividad, registro, evidencia="", detalle=None):
        s.bloque(ini, fin, area, titulo, actividad, registro, evidencia, CAPITALES.get(area, "Capital de continuidad"), detalle)

    def _cronograma(self, s: SistemaDia) -> None:
        tipo = s.contexto.get("tipo_dia", "")
        prioridad = s.universidad.get("prioridad") or "Ramo prioritario"
        evaluacion = s.universidad.get("evaluacion_critica") or "sin evaluación crítica registrada"
        lectura = s.desarrollo_personal.get("Leyendo") or s.desarrollo_personal.get("leyendo") or "lectura estratégica"
        capitulo = s.desarrollo_personal.get("Capítulo actual") or "pendiente"

        if "Noche" in tipo:
            bloques = [
                ("08:00", "08:20", "SERPAT", "SALIDA / ENTREGA DEL TURNO", "Entregar novedades, verificar pendientes y salir correctamente.", "No corresponde"),
                ("08:20", "09:10", "Salud", "TRASLADO · LLEGADA A CASA", "Llegar, hidratarse, preparar descanso, registrar estado si corresponde.", "H02_Registro_Salud; H03_Presión_Log"),
                ("09:10", "14:30", "Salud", "SUEÑO PRINCIPAL", "Dormir. Teléfono en silencio. Dormitorio oscuro. Proteger recuperación.", "H02_Registro_Salud al despertar"),
                ("14:30", "14:40", "Ancla", "DESPERTAR · IDENTIDAD · VISUALIZACIÓN", "Tomar agua. Respirar. Visualizar panel 2042. Repetir: no improviso, sigo el sistema.", "Ancla Mental; 21_KPI_Diario"),
                ("14:40", "15:00", "Salud", "SALUD · PRESIÓN · ENERGÍA", "Registrar sueño, energía, presión, pulso, medicamento e hidratación.", "H02_Registro_Salud; H03_Presión_Log"),
                ("15:00", "15:30", "Salud", "ALIMENTACIÓN · HIDRATACIÓN", "Almorzar, hidratarse, evitar gasto impulsivo, registrar comida real.", "H02_Registro_Salud; 12_Gastos si hubo compra"),
                ("15:30", "15:50", "Sistema", "APERTURA DEL SISTEMA", "Revisar dashboard, calendario, alertas, finanzas, universidad, salud, empresas y pendientes.", "20_Registro_Diario; 21_KPI_Diario; 90_Alertas_Correcciones"),
                ("15:50", "16:05", "Universidad", "ALERTA ACADÉMICA", f"Revisar Canvas y evaluación crítica: {evaluacion}.", "62_T2_Evaluaciones; 66_T2_Calendario"),
                ("16:05", "17:20", "Universidad", f"UNIVERSIDAD — {prioridad}", "Estudiar contenido exacto del ramo prioritario. Resolver ejercicios y registrar dudas/errores.", "61_T2_Ramos; 62_T2_Evaluaciones; 63_T2_Bloques; 64_T2_Errores"),
                ("17:20", "17:50", "Universidad", "COMUNICACIÓN / RAMO SECUNDARIO", "Revisar pauta, rúbrica, avance y pendiente exacto.", "61_T2_Ramos; 62_T2_Evaluaciones; 63_T2_Bloques"),
                ("17:50", "18:10", "Universidad", "CÁLCULO II · CONTINUIDAD", "Resolver mínimo 1 ejercicio. Registrar error exacto.", "61_T2_Ramos; 63_T2_Bloques; 64_T2_Errores"),
                ("18:10", "18:25", "Universidad", "FÍSICA · CONTINUIDAD", "Resolver mínimo 1 ejercicio conceptual o numérico. Registrar duda concreta.", "61_T2_Ramos; 63_T2_Bloques; 64_T2_Errores"),
                ("18:25", "18:45", "Empresas", "EMPRESAS · ACCIÓN MÍNIMA", "Ejecutar una acción real: seguimiento, CRM, análisis, respuesta o próxima acción.", "30_MGC_CRM; 33_Seguimientos; 70_Mercado_MGC; 76_CaptaPropIA; 82_LNH_Corporate_System"),
                ("18:45", "19:00", "Finanzas", "FINANZAS", "Registrar gastos, ingresos, saldo, deuda o conciliación. Definir decisión financiera del día.", "11_Ingresos; 12_Gastos; 13_Deudas; 18_Conciliacion_Bancaria_V3"),
                ("19:00", "19:10", "Desarrollo personal", "LECTURA ESTRATÉGICA", f"Leer {lectura}, capítulo {capitulo}. Registrar una idea aplicable.", "Ancla Mental; 20_Registro_Diario"),
                ("19:10", "19:20", "Imagen personal", "IMAGEN PERSONAL · PRESENCIA", "Uniforme limpio, higiene, postura, mochila, credencial, agua y colación.", "21_KPI_Diario"),
                ("19:20", "20:20", "SERPAT", "TRASLADO A SERPAT", "Traslado sin redes. Llegar estable y puntual.", "No corresponde"),
                ("20:20", "21:00", "SERPAT", "PREPARACIÓN OPERACIONAL", "Revisar servicio, equipos, llaves, radio y libro de novedades.", "No corresponde"),
                ("21:00", "08:00", "SERPAT", "SERPAT — TURNO NOCTURNO", "Cumplir responsabilidades, atención, hidratación y novedades.", "No corresponde"),
            ]
        else:
            bloques = [
                ("05:30", "05:45", "Ancla", "DESPERTAR · IDENTIDAD · VISUALIZACIÓN", "Agua, respiración, panel 2042, enfoque del día.", "Ancla Mental; 21_KPI_Diario"),
                ("05:45", "06:15", "Salud", "SALUD · PRESIÓN · ENERGÍA", "Registrar sueño, energía, presión, medicamento e hidratación.", "H02_Registro_Salud; H03_Presión_Log"),
                ("06:15", "06:45", "Imagen personal", "HIGIENE · VESTIMENTA · PRESENCIA", "Ducha, ropa ordenada, postura, bolso y salida preparada.", "21_KPI_Diario"),
                ("06:45", "07:10", "Salud", "DESAYUNO · MEDICAMENTO · AGUA", "Desayunar, tomar medicamento si corresponde, hidratarse.", "H02_Registro_Salud; H03_Presión_Log"),
                ("07:10", "07:30", "Sistema", "APERTURA DEL SISTEMA", "Revisar dashboard, calendario, pendientes y prioridades.", "20_Registro_Diario; 21_KPI_Diario; 90_Alertas_Correcciones"),
                ("07:30", "08:30", "Universidad", f"UNIVERSIDAD — {prioridad}", "Estudiar contenido exacto, ejercicios, dudas y errores.", "61_T2_Ramos; 62_T2_Evaluaciones; 63_T2_Bloques; 64_T2_Errores"),
                ("08:30", "09:00", "Finanzas", "FINANZAS", "Registrar caja, gastos, ingresos y decisión patrimonial.", "11_Ingresos; 12_Gastos; 13_Deudas; 18_Conciliacion_Bancaria_V3"),
                ("09:00", "09:30", "Empresas", "EMPRESAS · ACCIÓN REAL", "Ejecutar una acción empresarial con evidencia y próxima acción.", "30_MGC_CRM; 33_Seguimientos; 76_CaptaPropIA; 82_LNH_Corporate_System"),
                ("20:30", "21:00", "Ancla", "CIERRE ANCLA", "Cerrar día: constructor/sobreviviente, capital aumentado, corrección y prioridad mañana.", "Ancla Mental; 21_KPI_Diario; 90_Alertas_Correcciones"),
            ]
        for b in bloques:
            self._bloque(s, *b)
