from Config.config import RECURSOS_DIR

def auditar_recursos():
    categorias = []
    if not RECURSOS_DIR.exists():
        return {"total_categorias": 0, "total_archivos": 0, "categorias": [], "alerta": "No existe carpeta Recursos"}

    total = 0
    for carpeta in sorted(RECURSOS_DIR.iterdir()):
        if carpeta.is_dir():
            archivos = [a for a in carpeta.rglob("*") if a.is_file()]
            total += len(archivos)
            categorias.append({
                "categoria": carpeta.name,
                "archivos": len(archivos),
                "ruta": str(carpeta),
            })

    return {
        "total_categorias": len(categorias),
        "total_archivos": total,
        "categorias": categorias,
        "alerta": "",
    }
