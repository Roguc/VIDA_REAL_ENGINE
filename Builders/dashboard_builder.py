from __future__ import annotations

from pathlib import Path

from Models.sistema_dia import SistemaDia


def e(x):
    x = "" if x is None else str(x)
    return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


class DashboardBuilder:
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        self.out_dir = self.root_dir / "Salidas" / "Dashboard"
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def build(self, s: SistemaDia) -> Path:
        rows = ""
        for b in s.cronograma:
            rows += f"""
            <tr>
              <td><b>{e(b['hora_inicio'])}–{e(b['hora_fin'])}</b></td>
              <td><b>{e(b['titulo'])}</b><br><small>{e(b['actividad'])}</small></td>
              <td>{e(b['registro'])}</td>
              <td>{e(b['capital'])}</td>
            </tr>"""
        alertas = "".join(f"<li><b>{e(a['nivel'])}</b> · {e(a['area'])}: {e(a['mensaje'])}<br><small>{e(a.get('accion',''))}</small></li>" for a in s.alertas)
        decisiones = "".join(f"<li><b>{e(d['area'])}</b>: {e(d['decision'])}<br><small>{e(d.get('motivo',''))}</small></li>" for d in s.decisiones)
        pendientes = "".join(f"<li><b>{e(p.get('prioridad'))}</b> · {e(p.get('area'))} · {e(p.get('subarea'))}: {e(p.get('tarea'))}</li>" for p in s.pendientes[:12])
        vision = "".join(f"<li><b>{e(v.get('categoria'))}</b>: {e(v.get('objetivo'))}</li>" for v in s.vision_board[:12])
        recursos = "".join(f"<li>{e(c.get('categoria'))}: {e(c.get('archivos'))} archivo(s)</li>" for c in s.recursos.get('categorias', []))

        html = f"""<!doctype html>
<html lang='es'><head><meta charset='utf-8'><title>Vida Real Engine V5</title>
<style>
html{{scroll-behavior:smooth}}body{{margin:0;font-family:Arial;background:#07111f;color:#eef6ff}}header{{padding:24px;background:linear-gradient(90deg,#07111f,#102a44);position:sticky;top:0;border-bottom:1px solid #25486a}}h1{{margin:0}}h2{{color:#ffd166}}.grid{{display:grid;grid-template-columns:1fr 2fr 1fr;gap:16px;padding:16px}}.card{{background:#0c1c2e;border:1px solid #25486a;border-radius:14px;padding:16px}}.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:16px}}.kpi{{background:#102a44;border-radius:12px;padding:12px;border:1px solid #315a7e}}.kpi strong{{display:block;color:#ffd166}}table{{width:100%;border-collapse:collapse;font-size:13px}}th,td{{border-bottom:1px solid #25486a;padding:8px;vertical-align:top}}th{{color:#ffd166;text-align:left}}small{{color:#b8c7d9}}a.btn{{display:block;text-align:center;text-decoration:none;color:#06101c;background:#ffd166;border-radius:10px;padding:12px;margin:6px 0;font-weight:bold}}.section{{margin:16px}}ul{{padding-left:20px}}
</style></head><body>
<header id='inicio'><h1>VIDA REAL ENGINE V5.0 — BACKEND CORE</h1><p>Buenos días, Robinson. El backend integrado ya construyó el SistemaDia.</p><div class='kpis'>
<div class='kpi'><strong>Fecha</strong>{e(s.fecha_larga)}</div><div class='kpi'><strong>Tipo día</strong>{e(s.contexto.get('tipo_dia'))}</div><div class='kpi'><strong>Turno</strong>{e(s.contexto.get('turno_serpat'))}</div><div class='kpi'><strong>Excel</strong>{e(s.excel.get('hojas'))} hojas</div></div></header>
<div class='grid'><section class='card'><h2>Identidad</h2><p><b>{e(s.identidad.get('rol'))}</b></p><p>{e(s.identidad.get('ley_001'))}</p><h2>Estado</h2><p>Energía: {e(s.contexto.get('energia'))}</p><p>Salud: {e(s.contexto.get('salud_alerta'))}</p><p>Recursos: {e(s.recursos.get('total_archivos'))} archivos</p></section>
<section class='card'><h2>Cronograma</h2><table><tr><th>Hora</th><th>Actividad</th><th>Registro</th><th>Capital</th></tr>{rows}</table></section>
<section class='card'><h2>Paneles</h2><a class='btn' href='#alertas'>Alertas</a><a class='btn' href='#decisiones'>Decisiones</a><a class='btn' href='#pendientes'>Pendientes</a><a class='btn' href='#vision'>Vision Board</a><a class='btn' href='#recursos'>Recursos</a><a class='btn' href='#excel'>Excel</a></section></div>
<section id='alertas' class='card section'><h2>Alertas</h2><ul>{alertas}</ul></section>
<section id='decisiones' class='card section'><h2>Decisiones</h2><ul>{decisiones}</ul></section>
<section id='pendientes' class='card section'><h2>Pendientes</h2><ul>{pendientes}</ul></section>
<section id='vision' class='card section'><h2>Vision Board</h2><ul>{vision}</ul></section>
<section id='recursos' class='card section'><h2>Recursos</h2><ul>{recursos}</ul></section>
<section id='excel' class='card section'><h2>Excel</h2><p>Archivo: {e(s.excel.get('archivo'))}</p><p>Hojas detectadas: {e(s.excel.get('hojas'))}</p></section>
<p style='text-align:center'><a href='#inicio' style='color:#ffd166'>Volver arriba</a></p></body></html>"""
        out = self.out_dir / f"CENTRO_COMANDO_V5_{s.fecha_iso}.html"
        out.write_text(html, encoding="utf-8")
        return out
