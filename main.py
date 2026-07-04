from pathlib import Path

from Core.core import VidaRealCore
from Core.logger import log
from Builders.dashboard_builder import DashboardBuilder
from Builders.word_builder import WordBuilder


def main():
    root = Path(__file__).resolve().parent
    print()
    print("==============================================")
    print("      VIDA REAL ENGINE V5.0 — BACKEND CORE")
    print("==============================================")
    print()

    core = VidaRealCore(root)
    sistema = core.construir_sistema_dia()

    dashboard = DashboardBuilder(root).build(sistema)
    word = WordBuilder(root).build(sistema)
    sistema.salidas["dashboard"] = str(dashboard)
    sistema.salidas["word"] = str(word)

    log(root, f"V5 Backend Core ejecutado | Dashboard: {dashboard.name} | Word: {word.name}")

    print("✅ Backend Core ejecutado")
    print(f"Fecha: {sistema.fecha_larga}")
    print(f"Tipo de día: {sistema.contexto.get('tipo_dia')}")
    print(f"Turno SERPAT: {sistema.contexto.get('turno_serpat')}")
    print(f"Excel: {sistema.excel.get('archivo')} | Hojas: {sistema.excel.get('hojas')}")
    print(f"Recursos: {sistema.recursos.get('total_archivos')} archivos")
    print(f"Alertas: {len(sistema.alertas)}")
    print(f"Pendientes: {len(sistema.pendientes)}")
    print(f"Bloques: {len(sistema.cronograma)}")
    print(f"Centro de Comando: {dashboard}")
    print(f"Word respaldo: {word}")
    print()
    print("==============================================")
    print("Proceso terminado.")
    print("==============================================")


if __name__ == "__main__":
    main()
