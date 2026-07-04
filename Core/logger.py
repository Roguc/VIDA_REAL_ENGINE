from datetime import datetime

def log(texto: str) -> None:
    ahora = datetime.now().strftime("%H:%M:%S")
    print(f"[{ahora}] {texto}")
