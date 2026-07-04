from datetime import datetime
from pathlib import Path


def log(root_dir: Path, mensaje: str) -> None:
    logs = root_dir / "Salidas" / "Logs"
    logs.mkdir(parents=True, exist_ok=True)
    with open(logs / "vida_real_engine_v5.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensaje}\n")
