from Scripts.utilidades import limpiar_texto

def construir_bloque_universidad(dia):
    prioridad = limpiar_texto(dia.get("prioridad_academica")) or "Ramo prioritario"
    evaluacion = limpiar_texto(dia.get("evaluacion_critica")) or "sin evaluación crítica registrada"
    semana = limpiar_texto(dia.get("semana_academica")) or "semana activa"
    return {
        "area": "Universidad",
        "titulo": f"UNIVERSIDAD — {prioridad}",
        "objetivo": f"Construir capital intelectual en {semana}, considerando {evaluacion}.",
        "actividad": "Abrir Canvas. Revisar ramo prioritario. Confirmar contenido exacto, evaluación, material disponible, errores abiertos y avance anterior. Registrar exactamente dónde quedaste.",
        "registro": "61_T2_Ramos; 62_T2_Evaluaciones; 63_T2_Bloques; 64_T2_Errores; 65_T2_Dashboard; 66_T2_Calendario",
        "evidencia": "✓ Contenido trabajado. ✓ Errores/dudas registrados. ✓ Avance actualizado.",
        "seguimiento": "Registrar materia exacta, ejercicio/página, duda, error y próximo paso.",
    }
