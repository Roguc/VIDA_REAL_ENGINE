from Scripts.utilidades import limpiar_texto

def construir_bloque_empresas(dia):
    prioridad = limpiar_texto(dia.get("prioridad_empresa")) or "MGC / LNH / CaptaPropIA"
    return {
        "area": "Empresas",
        "titulo": f"EMPRESAS — {prioridad}",
        "objetivo": "Construir capital empresarial con una acción concreta, registrable y acumulativa.",
        "actividad": "Revisar CRM, seguimiento, mercado o proyecto activo. Ejecutar una acción concreta: contacto, análisis, respuesta, registro, hipótesis, aprendizaje o siguiente acción.",
        "registro": "30_MGC_CRM; 33_Seguimientos; 70_Mercado_MGC; 71_Mercado_LNR; 76_CaptaPropIA; 82_LNH_Corporate_System",
        "evidencia": "✓ Acción empresarial real. ✓ Próximo paso definido.",
        "seguimiento": "Registrar actor/proyecto, acción, resultado y próxima fecha.",
    }
