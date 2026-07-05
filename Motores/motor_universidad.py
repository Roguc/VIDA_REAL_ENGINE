from datetime import datetime, date
from pathlib import Path


class MotorUniversidad:
    def analizar(self, sistema, excel, recursos):
        hojas = sistema.contexto.get("excel", {}).get("hojas", [])

        hojas_universidad = [
            h for h in hojas
            if (
                "T2" in h.upper()
                or "UNIVERSIDAD" in h.upper()
                or "RAMO" in h.upper()
                or "EVALUACION" in h.upper()
                or "EVALUACIONES" in h.upper()
                or "ERRORES" in h.upper()
                or "CALENDARIO" in h.upper()
                or "CONTENIDOS" in h.upper()
            )
        ]

        evaluaciones = self._leer_evaluaciones(excel)
        errores = self._leer_errores(excel)
        contenidos = self._leer_contenidos(excel)
        recursos_uni = self._leer_recursos_universidad(recursos)

        critica = self._detectar_evaluacion_critica(evaluaciones)

        sistema.universidad = {
            "hojas_detectadas": hojas_universidad,
            "evaluaciones": evaluaciones[:10],
            "errores": errores[:10],
            "contenidos": contenidos[:10],
            "recursos": recursos_uni,
            "critica": critica,
        }

        if critica:
            accion = (
                f"Estudiar {critica.get('ramo', 'ramo crítico')} — "
                f"{critica.get('evaluacion', 'evaluación pendiente')}. "
                f"Revisar contenido asociado, resolver ejercicios y registrar errores."
            )
            motivo = f"Evaluación detectada como prioridad: {critica.get('detalle', 'sin detalle')}."
            prioridad = 98
        else:
            accion = "Revisar evaluaciones, contenidos pendientes y errores registrados de Universidad."
            motivo = "No se detectó una evaluación crítica específica, pero hay información académica disponible."
            prioridad = 88

        sistema.agregar_decision(
            "Universidad",
            prioridad,
            accion,
            motivo,
            "61_T2_Ramos; 62_T2_Evaluaciones; 63_T2_Bloques; 64_T2_Errores"
        )

        if errores:
            sistema.agregar_alerta(
                "Universidad",
                86,
                "Errores académicos detectados",
                f"Hay {len(errores)} registros de errores/dudas que deben revisarse."
            )

        if recursos_uni.get("total_archivos", 0) > 0:
            sistema.agregar_alerta(
                "Universidad",
                80,
                "Recursos universitarios disponibles",
                f"Hay {recursos_uni['total_archivos']} archivos en Recursos/04_UNIVERSIDAD."
            )

    def _leer_evaluaciones(self, excel):
        posibles = [
            "62_T2_Evaluaciones",
            "T2_Evaluaciones",
            "62 Evaluaciones",
            "Evaluaciones",
        ]
        return self._leer_tabla_por_hojas(excel, posibles, max_filas=80)

    def _leer_errores(self, excel):
        posibles = [
            "64_T2_Errores",
            "T2_Errores",
            "64 Errores",
            "Errores",
        ]
        return self._leer_tabla_por_hojas(excel, posibles, max_filas=80)

    def _leer_contenidos(self, excel):
        posibles = [
            "T2_CONTENIDOS_SEM1_SEM4",
            "T2_CONTENIDOS",
            "Contenidos",
            "63_T2_Bloques",
            "61_T2_Ramos",
        ]
        return self._leer_tabla_por_hojas(excel, posibles, max_filas=80)

    def _leer_tabla_por_hojas(self, excel, nombres, max_filas=50):
        datos = []

        # Prioriza lector inteligente del ExcelManager (encabezado flexible + normalizacion)
        if hasattr(excel, "leer_tabla_inteligente"):
            for nombre in nombres:
                try:
                    tabla = excel.leer_tabla_inteligente(nombre)
                except Exception:
                    tabla = []
                if tabla:
                    return tabla[:max_filas]

        for nombre in nombres:
            ws = excel.obtener_hoja(nombre)
            if ws is None:
                continue

            filas = list(ws.iter_rows(values_only=True))
            if not filas:
                continue

            encabezado = [str(c).strip() if c is not None else "" for c in filas[0]]

            for fila in filas[1:max_filas + 1]:
                if not fila or all(c is None for c in fila):
                    continue

                item = {}
                for i, valor in enumerate(fila):
                    key = encabezado[i] if i < len(encabezado) and encabezado[i] else f"col_{i+1}"
                    if valor is not None:
                        item[key] = valor

                if item:
                    item["_hoja"] = nombre
                    datos.append(item)

            if datos:
                break

        return datos

    def _detectar_evaluacion_critica(self, evaluaciones):
        if not evaluaciones:
            return None

        palabras_criticas = ["ev", "evalu", "prueba", "trabajo", "examen", "entrega", "pendiente", "critica", "crítica"]
        candidatas = []

        for ev in evaluaciones:
            texto = " ".join(str(v).lower() for v in ev.values())
            score = sum(1 for p in palabras_criticas if p in texto)

            for key, value in ev.items():
                if isinstance(value, (datetime, date)):
                    score += 3

            if score > 0:
                candidatas.append((score, ev))

        if not candidatas:
            ev = evaluaciones[0]
        else:
            candidatas.sort(key=lambda x: x[0], reverse=True)
            ev = candidatas[0][1]

        ramo = self._buscar_valor(ev, ["ramo", "asignatura", "curso", "materia", "área", "area"])
        evaluacion = self._buscar_valor(ev, ["evaluacion", "evaluación", "actividad", "tipo", "nombre"])
        detalle = " | ".join(str(v) for v in ev.values() if v is not None)[:220]

        return {
            "ramo": str(ramo) if ramo else "Universidad",
            "evaluacion": str(evaluacion) if evaluacion else "Evaluación detectada",
            "detalle": detalle,
            "origen": ev.get("_hoja", ""),
        }

    def _buscar_valor(self, item, palabras):
        for key, value in item.items():
            k = str(key).lower()
            if any(p in k for p in palabras):
                return value
        return None

    def _leer_recursos_universidad(self, recursos):
        resumen = recursos.resumen()
        categorias = resumen.get("categorias", {})

        for nombre, data in categorias.items():
            if "04_UNIVERSIDAD" in nombre.upper() or "UNIVERSIDAD" in nombre.upper():
                archivos = data.get("archivos", [])
                return {
                    "categoria": nombre,
                    "total_archivos": len(archivos),
                    "archivos_relevantes": archivos[:15],
                }

        return {
            "categoria": "",
            "total_archivos": 0,
            "archivos_relevantes": [],
        }
