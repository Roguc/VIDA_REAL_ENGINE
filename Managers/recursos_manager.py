from pathlib import Path

class RecursosManager:
    def __init__(self):
        self.carpeta = Path("Recursos")
        self.indice = {}

    def cargar(self):
        self.indice = {}
        if not self.carpeta.exists():
            return self.indice

        for carpeta in sorted(self.carpeta.iterdir()):
            if carpeta.is_dir():
                archivos = [a for a in carpeta.rglob("*") if a.is_file()]
                self.indice[carpeta.name] = {
                    "ruta": str(carpeta),
                    "total_archivos": len(archivos),
                    "archivos": [str(a) for a in archivos],
                }

        return self.indice

    def resumen(self):
        total = sum(v["total_archivos"] for v in self.indice.values())
        return {
            "total_categorias": len(self.indice),
            "total_archivos": total,
            "categorias": self.indice,
        }
