from Scripts.utilidades import limpiar_texto

CAPITALES_BASE = {
    "Universidad": "Capital intelectual",
    "Finanzas": "Capital financiero",
    "Salud": "Capital biológico",
    "Empresas": "Capital empresarial",
    "SERPAT": "Capital reputacional",
    "Ancla Mental": "Capital psicológico",
    "Sistema": "Capital organizacional",
    "Desarrollo personal": "Capital cognitivo",
    "Imagen personal": "Capital de presencia",
    "Familia": "Capital familiar",
}

def capital_del_bloque(area):
    return CAPITALES_BASE.get(area, "Capital de continuidad")

def adaptar_por_energia(dia, bloque):
    energia = limpiar_texto(dia.get("nivel_energia")).lower()
    if energia in ["baja", "muy baja", "agotado", "cansado"]:
        bloque["plan_reducido"] = "Plan reducido: versión mínima, registrar evidencia y proteger continuidad."
    else:
        bloque["plan_reducido"] = "Plan normal. Si aparece cansancio real, reducir intensidad sin cortar continuidad."
    return bloque
