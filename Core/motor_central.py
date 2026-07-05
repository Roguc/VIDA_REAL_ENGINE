from datetime import datetime
from pathlib import Path

from Models.sistema_dia import SistemaDia
from Managers.excel_manager import ExcelManager
from Managers.recursos_manager import RecursosManager
from Motores.motor_universidad import MotorUniversidad
from Motores import motor_serpat, motor_fuentes, motor_finanzas, motor_salud, motor_empresas, motor_ancla, motor_continuidad, motor_recursos
from Scripts.utilidades import limpiar_texto


class MotorCentral:
    def __init__(self):
        self.sistema = SistemaDia()
        self.excel = ExcelManager()
        self.recursos = RecursosManager()
        self.motor_universidad = MotorUniversidad()
        self.errores = []

    def ejecutar(self):
        ahora = datetime.now()

        self.sistema.fecha = ahora.date()
        self.sistema.fecha_texto = ahora.strftime("%d-%m-%Y")
        self.sistema.hora_actual = ahora.strftime("%H:%M")

        try:
            self.excel.cargar()
        except Exception as e:
            self.errores.append(f"Error cargando Excel: {str(e)}")
            return self.sistema

        try:
            self.excel.escanear_excel_completo()
            self.excel.generar_reporte_excel("Salidas/Logs/EXCEL_INTELLIGENCE_REPORT.txt")
        except Exception as e:
            self.errores.append(f"Error generando reporte Excel: {str(e)}")

        try:
            self.recursos.cargar()
        except Exception as e:
            self.errores.append(f"Error cargando recursos: {str(e)}")

        self.sistema.contexto["excel"] = self.excel.resumen()
        self.sistema.contexto["excel_scan_report"] = str(Path("Salidas/Logs/EXCEL_INTELLIGENCE_REPORT.txt"))
        self.sistema.contexto["excel_intelligence_report"] = str(Path("Salidas/Logs/EXCEL_INTELLIGENCE_REPORT.txt"))
        self.sistema.contexto["excel_dominios"] = self.excel.obtener_resumen_dominios()
        self.sistema.recursos = self.recursos.resumen()

        print("EXCEL INTELLIGENCE LAYER ACTIVA")
        print(f"Total hojas: {self.sistema.contexto['excel'].get('total_hojas', 0)}")
        print(f"Dominios detectados: {self.sistema.contexto['excel'].get('dominios_detectados', 0)}")
        print("Reporte generado: Salidas/Logs/EXCEL_INTELLIGENCE_REPORT.txt")

        # Agregar decisión inicial del Sistema
        self.sistema.agregar_decision(
            "Sistema",
            100,
            "Abrir Centro de Comando y revisar prioridades.",
            "Motor Central IA activo.",
            "20_Registro_Diario; 21_KPI_Diario"
        )

        self._analizar_contexto()
        
        # Ejecutar todos los motores (EN ORDEN DE PRIORIDAD)
        self._analizar_universidad()
        self._analizar_serpat()
        self._analizar_pendientes()
        self._analizar_vision_board()
        self._analizar_desarrollo_personal()
        self._analizar_salud()
        self._analizar_finanzas()
        self._analizar_empresas()
        self._analizar_ancla()
        self._analizar_continuidad()
        
        # Consolidar decisiones duplicadas y ordenar
        self._consolidar_decisiones()
        self.sistema.ordenar_decisiones()
        return self.sistema

    def _analizar_contexto(self):
        hojas = self.sistema.contexto["excel"]["hojas"]

        if self.excel.existe_alias("SERPAT TURNOS"):
            self.sistema.agregar_alerta(
                "SERPAT",
                90,
                "Calendario laboral detectado",
                "Usar SERPAT TURNOS para adaptar el día."
            )

        if self.excel.existe_alias("PENDIENTES"):
            self.sistema.agregar_alerta(
                "Pendientes",
                95,
                "Pendientes detectados",
                "Integrar pendientes en la priorización diaria."
            )

        if self.excel.existe_alias("VISION_BOARD"):
            self.sistema.agregar_alerta(
                "Identidad",
                70,
                "Vision Board detectado",
                "Usar Vision Board para visualización diaria."
            )

        if self.excel.existe_alias("DESARROLLO_PERSONAL"):
            self.sistema.agregar_alerta(
                "Desarrollo Personal",
                75,
                "Desarrollo personal detectado",
                "Integrar lectura, hábitos e identidad."
            )

    def _consolidar_decisiones(self):
        """Elimina decisiones duplicadas, mantiene la más específica por área"""
        areas_vistas = {}
        decisiones_consolidadas = []
        
        for decision in self.sistema.decisiones:
            area = decision.get("area", "Sistema")
            
            if area == "Sistema":
                # Sistema siempre se mantiene
                decisiones_consolidadas.append(decision)
            elif area not in areas_vistas:
                # Primera vez que vemos esta área
                areas_vistas[area] = decision
                decisiones_consolidadas.append(decision)
            else:
                # Comparar prioridades: mantener la más alta (más específica)
                prev = areas_vistas[area]
                if decision.get("prioridad", 0) > prev.get("prioridad", 0):
                    # Nueva decisión tiene más prioridad, reemplazar
                    idx = decisiones_consolidadas.index(prev)
                    decisiones_consolidadas[idx] = decision
                    areas_vistas[area] = decision
                # Si la anterior tiene más prioridad, ignorar la nueva
        
        self.sistema.decisiones = decisiones_consolidadas

    def _generar_decisiones_base(self):
        """DEPRECATED: Se consolidó en ejecutar() y _consolidar_decisiones()"""
        pass


    def _analizar_universidad(self):
        try:
            self.motor_universidad.analizar(self.sistema, self.excel, self.recursos)
        except Exception as e:
            self.errores.append(f"Error en MotorUniversidad: {str(e)}")

    def _analizar_serpat(self):
        try:
            if self.excel.existe_alias("SERPAT TURNOS") or self.excel.existe_hoja("SERPAT TURNOS"):
                turno = motor_serpat.obtener_turno_fecha(self.excel.workbook, self.sistema.fecha)
                if turno:
                    self.sistema.serpat = turno
                    self.sistema.tipo_dia = turno.get("tipo_dia", "")
                    self.sistema.turno_serpat = turno.get("turno_serpat", "")
                    
                    tipo_dia = turno.get("tipo_dia", "").strip()
                    
                    # Manejo especial para Día Libre
                    if "Libre" in tipo_dia:
                        accion = "Día libre SERPAT — Usar para avance estratégico sin restricción horaria."
                        motivo = "Calendario laboral: Día libre disponible"
                        prioridad = 91
                        registro = "09_PANEL_VISION; 20_Registro_Diario"
                    else:
                        ingreso = (turno.get("ingreso") or "?").strip()
                        salida = (turno.get("salida") or "?").strip()
                        horario = f"{ingreso} a {salida}" if ingreso != "?" or salida != "?" else tipo_dia
                        accion = f"Trabajar turno {tipo_dia} — Horario: {horario}"
                        motivo = f"Calendario laboral: {tipo_dia}"
                        prioridad = 92
                        registro = "SERPAT TURNOS"
                    
                    self.sistema.agregar_decision(
                        "SERPAT",
                        prioridad,
                        accion,
                        motivo,
                        registro
                    )
        except Exception as e:
            self.errores.append(f"Error en MotorSerpat: {str(e)}")

    def _analizar_pendientes(self):
        try:
            if self.excel.existe_alias("PENDIENTES") or self.excel.existe_hoja("PENDIENTES"):
                pendientes = []
                try:
                    tabla = self.excel.leer_tabla_inteligente("PENDIENTES")
                    for item in tabla:
                        estado = limpiar_texto(item.get("Estado", ""))
                        if estado.lower() in ["completado", "cumplido", "cerrado"]:
                            continue
                        pendientes.append({
                            "id": limpiar_texto(item.get("ID", item.get("Id", ""))),
                            "area": limpiar_texto(item.get("Área", item.get("Area", ""))),
                            "subarea": limpiar_texto(item.get("Subárea", item.get("Subarea", ""))),
                            "tarea": limpiar_texto(item.get("Tarea", "")) or "Pendiente sin descripción",
                            "prioridad": limpiar_texto(item.get("Prioridad", "")),
                            "estado": estado,
                            "avance": limpiar_texto(item.get("Avance %", item.get("Avance", ""))),
                            "observaciones": limpiar_texto(item.get("Observaciones", "")),
                        })
                    pendientes = pendientes[:20]
                except Exception:
                    pendientes = []

                if not pendientes:
                    pendientes = motor_fuentes.leer_pendientes(self.excel.workbook, max_items=20)
                self.sistema.pendientes = pendientes
                
                criticos = [p for p in pendientes if limpiar_texto(p.get("prioridad", "")).lower() in ["crítica", "critica", "alta"]]
                if criticos:
                    critico = criticos[0]
                    # Si no tiene descripción, usar área + prioridad
                    tarea = limpiar_texto(critico.get("tarea", ""))
                    if not tarea or tarea == "Pendiente sin descripción":
                        area = limpiar_texto(critico.get("area", "general"))
                        prioridad = limpiar_texto(critico.get("prioridad", "alta"))
                        tarea = f"{area} ({prioridad})"
                    
                    self.sistema.agregar_alerta(
                        "Pendientes",
                        96,
                        f"Hay {len(criticos)} pendiente(s) crítico(s)/alto(s)",
                        f"Resolver o reagendar: {tarea[:70]}"
                    )
                    self.sistema.agregar_decision(
                        "Pendientes",
                        93,
                        f"Resolver pendiente crítico: {tarea[:70]}",
                        f"Prioridad {critico.get('prioridad', 'alta')} — Área: {critico.get('area', 'general')}",
                        "20_Registro_Diario; 90_Alertas_Correcciones"
                    )
        except Exception as e:
            self.errores.append(f"Error en leer_pendientes: {str(e)}")

    def _analizar_vision_board(self):
        try:
            if self.excel.existe_alias("VISION_BOARD") or self.excel.existe_hoja("VISION_BOARD"):
                vision = []
                try:
                    tabla = self.excel.leer_tabla_inteligente("VISION_BOARD")
                    for item in tabla[:12]:
                        vision.append({
                            "categoria": limpiar_texto(item.get("Categoría", item.get("Categoria", ""))),
                            "objetivo": limpiar_texto(item.get("Objetivo 2042", item.get("Objetivo", ""))),
                            "imagen": limpiar_texto(item.get("Imagen / Referencia", item.get("Imagen", ""))),
                            "ruta": limpiar_texto(item.get("Ruta (09_PANEL_VISION)", item.get("Ruta", ""))),
                            "estado": limpiar_texto(item.get("Estado", "")),
                        })
                except Exception:
                    vision = []

                if not vision:
                    vision = motor_fuentes.leer_vision_board(self.excel.workbook, max_items=12)
                self.sistema.vision_board = vision
                if vision:
                    self.sistema.agregar_alerta(
                        "Identidad",
                        82,
                        "Panel Vision 2042 disponible",
                        f"Visualizar: {vision[0].get('categoria', 'objetivo 2042')}"
                    )
        except Exception as e:
            self.errores.append(f"Error en leer_vision_board: {str(e)}")

    def _analizar_desarrollo_personal(self):
        try:
            if self.excel.existe_alias("DESARROLLO_PERSONAL") or self.excel.existe_hoja("DESARROLLO_PERSONAL"):
                desarrollo = {}
                try:
                    tabla = self.excel.leer_tabla_inteligente("DESARROLLO_PERSONAL")
                    for item in tabla:
                        for key, value in item.items():
                            if key.startswith("_"):
                                continue
                            k = limpiar_texto(key).lower()
                            v = limpiar_texto(value)
                            if k in ["misión", "mision"]:
                                desarrollo["mision"] = v
                            elif k in ["visión 2042", "vision 2042"]:
                                desarrollo["vision"] = v
                            elif k in ["propósito", "proposito"]:
                                desarrollo["proposito"] = v
                            elif k in ["ley 001", "ley"]:
                                desarrollo["ley"] = v
                            elif k in ["valores"]:
                                desarrollo["valores"] = v
                            elif k in ["leyendo", "libro"]:
                                desarrollo["libro"] = v
                            elif k in ["capítulo actual", "capitulo actual", "capitulo"]:
                                desarrollo["capitulo"] = v
                            elif k in ["estado"]:
                                desarrollo["estado"] = v
                            elif k in ["próximos libros", "proximos libros", "proximos"]:
                                desarrollo["proximos"] = v
                except Exception:
                    desarrollo = {}

                if not desarrollo:
                    desarrollo = motor_fuentes.leer_desarrollo_personal(self.excel.workbook)
                self.sistema.desarrollo_personal = desarrollo
                
                if desarrollo.get("ley", ""):
                    self.sistema.identidad = {
                        "ley_001": desarrollo.get("ley", ""),
                        "proposito": desarrollo.get("proposito", ""),
                        "vision": desarrollo.get("vision", ""),
                        "mision": desarrollo.get("mision", ""),
                    }
                    self.sistema.agregar_alerta(
                        "Identidad",
                        88,
                        "Ley 001 activa",
                        f"'{desarrollo.get('ley', '')}'"
                    )
        except Exception as e:
            self.errores.append(f"Error en leer_desarrollo_personal: {str(e)}")

    def _analizar_salud(self):
        try:
            salud_excel = self._resumen_categoria_excel("salud")
            bloque_salud = motor_salud.construir_bloque_salud({})
            self.sistema.salud = {
                "titulo": bloque_salud.get("titulo", ""),
                "objetivo": bloque_salud.get("objetivo", ""),
                "actividad": bloque_salud.get("actividad", ""),
                "registro": bloque_salud.get("registro", ""),
                "datos_excel": salud_excel,
            }
            self.sistema.agregar_decision(
                "Salud",
                84,
                bloque_salud.get("actividad", "Registrar salud"),
                bloque_salud.get("objetivo", "Proteger capital biológico"),
                bloque_salud.get("registro", "H02_Registro_Salud; H03_Presión_Log")
            )
        except Exception as e:
            self.errores.append(f"Error en MotorSalud: {str(e)}")

    def _analizar_finanzas(self):
        try:
            finanzas_excel = self._resumen_categoria_excel("finanzas") + self._resumen_categoria_excel("registro")
            bloque_finanzas = motor_finanzas.construir_bloque_finanzas({})
            self.sistema.finanzas = {
                "titulo": bloque_finanzas.get("titulo", ""),
                "objetivo": bloque_finanzas.get("objetivo", ""),
                "actividad": bloque_finanzas.get("actividad", ""),
                "registro": bloque_finanzas.get("registro", ""),
                "datos_excel": finanzas_excel[:6],
            }
            self.sistema.agregar_decision(
                "Finanzas",
                79,
                bloque_finanzas.get("actividad", "Registrar movimientos"),
                bloque_finanzas.get("objetivo", "Mantener visibilidad financiera"),
                bloque_finanzas.get("registro", "11_Ingresos; 12_Gastos")
            )
        except Exception as e:
            self.errores.append(f"Error en MotorFinanzas: {str(e)}")

    def _analizar_empresas(self):
        try:
            empresas_excel = self._resumen_categoria_excel("empresas")
            bloque_empresas = motor_empresas.construir_bloque_empresas({})
            self.sistema.empresas = {
                "titulo": bloque_empresas.get("titulo", ""),
                "objetivo": bloque_empresas.get("objetivo", ""),
                "actividad": bloque_empresas.get("actividad", ""),
                "registro": bloque_empresas.get("registro", ""),
                "datos_excel": empresas_excel,
            }
            self.sistema.agregar_decision(
                "Empresas",
                74,
                bloque_empresas.get("actividad", "Ejecutar acción empresarial"),
                bloque_empresas.get("objetivo", "Construir capital empresarial"),
                bloque_empresas.get("registro", "30_MGC_CRM; 33_Seguimientos")
            )
        except Exception as e:
            self.errores.append(f"Error en MotorEmpresas: {str(e)}")

    def _analizar_ancla(self):
        try:
            bloque_ancla = motor_ancla.construir_bloque_ancla({})
            self.sistema.ancla = {
                "titulo": bloque_ancla.get("titulo", ""),
                "objetivo": bloque_ancla.get("objetivo", ""),
                "actividad": bloque_ancla.get("actividad", ""),
                "registro": bloque_ancla.get("registro", ""),
            }
            self.sistema.agregar_decision(
                "Ancla Mental",
                86,
                bloque_ancla.get("actividad", "Cierre de identidad"),
                bloque_ancla.get("objetivo", "Evitar volver al Robinson anterior"),
                bloque_ancla.get("registro", "Ancla Mental; 21_KPI_Diario")
            )
        except Exception as e:
            self.errores.append(f"Error en MotorAncla: {str(e)}")

    def _analizar_continuidad(self):
        try:
            capital = motor_continuidad.capital_del_bloque("Universidad")
            self.sistema.continuidad = {
                "capital_base": capital,
                "capitales": motor_continuidad.CAPITALES_BASE.copy(),
            }
            self.sistema.agregar_alerta(
                "Continuidad",
                77,
                "Sistema de capitales activo",
                "Cada acción construye capital en un dominio"
            )
        except Exception as e:
            self.errores.append(f"Error en MotorContinuidad: {str(e)}")

    def _resumen_categoria_excel(self, categoria: str, max_items: int = 3):
        try:
            hojas = self.excel.buscar_hojas_por_categoria(categoria)
            salida = []
            for hoja in hojas[:3]:
                registros = self.excel.leer_ultimos_registros(hoja, max_items)
                salida.append(
                    {
                        "hoja": hoja,
                        "registros": registros,
                    }
                )
            return salida
        except Exception:
            return []

