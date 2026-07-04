from pathlib import Path
from openpyxl import load_workbook

class ExcelManager:
    def __init__(self):
        self.archivo = None
        self.workbook = None
        self.hojas = []

    def buscar_excel(self):
        carpeta = Path("Excel")
        archivos = list(carpeta.glob("*.xlsx"))
        if not archivos:
            raise FileNotFoundError("No se encontró ningún Excel en la carpeta Excel.")
        archivos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        self.archivo = archivos[0]
        return self.archivo

    def cargar(self):
        self.buscar_excel()
        self.workbook = load_workbook(self.archivo, data_only=True)
        self.hojas = self.workbook.sheetnames
        return True

    def existe_hoja(self, nombre: str) -> bool:
        return nombre in self.hojas

    def obtener_hoja(self, nombre: str):
        if self.existe_hoja(nombre):
            return self.workbook[nombre]
        return None

    def leer_celda(self, hoja: str, celda: str):
        ws = self.obtener_hoja(hoja)
        if ws is None:
            return None
        return ws[celda].value

    def resumen(self):
        return {
            "archivo": self.archivo.name if self.archivo else "",
            "total_hojas": len(self.hojas),
            "hojas": self.hojas,
        }
