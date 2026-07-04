from datetime import datetime
from Config.config import DASHBOARD_DIR
import os

def generar_dashboard(resultado):
    d=resultado["dia"]
    os.makedirs(DASHBOARD_DIR,exist_ok=True)
    f=os.path.join(DASHBOARD_DIR,f"CENTRO_COMANDO_{datetime.now().date()}.html")
    html=f"""<!doctype html><html><head><meta charset="utf-8">
<title>VIDA REAL ENGINE V5</title>
<style>
body{{font-family:Arial;background:#13253a;color:white;margin:0}}
header{{position:sticky;top:0;background:#0f1f30;padding:15px;font-size:22px}}
nav{{position:fixed;right:10px;top:80px;width:180px}}
nav a{{display:block;background:#f0b93a;color:black;padding:10px;margin:6px;text-decoration:none;border-radius:8px;text-align:center}}
section{{margin:20px;padding:20px;background:#1d3557;border-radius:10px}}
.top{{position:fixed;left:15px;bottom:15px}}
</style></head><body>
<header>VIDA REAL ENGINE V5 — {datetime.now().strftime("%d-%m-%Y %H:%M")}</header>
<nav>
<a href="#universidad">Universidad</a>
<a href="#finanzas">Finanzas</a>
<a href="#salud">Salud</a>
<a href="#empresas">Empresas</a>
<a href="#serpat">SERPAT</a>
<a href="#ancla">Ancla</a>
<a href="#recursos">Recursos</a>
<a href="javascript:window.print()">PDF / Imprimir</a>
<a href="../Word/VIDA_REAL_ENGINE_{d.get('fecha')}.docx">Word</a>
</nav>
<section id="inicio"><h2>Centro de Comando</h2><p>Esta versión está preparada para cronograma dinámico basado en SERPAT_TURNOS.</p></section>
<section id="universidad"><h2>Universidad</h2><p>Leer tema, ejercicios, dudas y registros desde Excel.</p></section>
<section id="finanzas"><h2>Finanzas</h2><p>KPIs, saldo, pagos y alertas.</p></section>
<section id="salud"><h2>Salud</h2><p>Presión, sueño, medicamentos y energía.</p></section>
<section id="empresas"><h2>Empresas</h2><p>MGC · LNH · CaptaPropIA separados.</p></section>
<section id="serpat"><h2>SERPAT</h2><p>Turno y cronograma dinámico.</p></section>
<section id="ancla"><h2>Ancla Mental</h2></section>
<section id="recursos"><h2>Recursos</h2></section>
<button class="top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑ Arriba</button>
</body></html>"""
    open(f,"w",encoding="utf-8").write(html)
    return f
