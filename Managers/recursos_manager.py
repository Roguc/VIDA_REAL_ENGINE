from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


class RecursosManager:
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        self.recursos_dir = self.root_dir / "Recursos"

    def indexar(self) -> Dict[str, Any]:
        categorias: List[Dict[str, Any]] = []
        total_archivos = 0
        extensiones: Dict[str, int] = {}
        recientes: List[Dict[str, Any]] = []

        if not self.recursos_dir.exists():
            return {"existe": False, "total_categorias": 0, "total_archivos": 0, "categorias": [], "recientes": []}

        for carpeta in sorted([p for p in self.recursos_dir.iterdir() if p.is_dir()]):
            archivos = [p for p in carpeta.rglob("*") if p.is_file()]
            total_archivos += len(archivos)
            categorias.append({"categoria": carpeta.name, "ruta": str(carpeta), "archivos": len(archivos)})
            for f in archivos:
                ext = f.suffix.lower() or "sin_extension"
                extensiones[ext] = extensiones.get(ext, 0) + 1
                recientes.append({"nombre": f.name, "ruta": str(f), "categoria": carpeta.name, "modificado": f.stat().st_mtime})

        recientes.sort(key=lambda x: x["modificado"], reverse=True)
        return {
            "existe": True,
            "ruta": str(self.recursos_dir),
            "total_categorias": len(categorias),
            "total_archivos": total_archivos,
            "categorias": categorias,
            "extensiones": extensiones,
            "recientes": recientes[:15],
        }
