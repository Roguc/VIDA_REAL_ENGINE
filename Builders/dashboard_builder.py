from __future__ import annotations

import re
from pathlib import Path

from Models.sistema_dia import SistemaDia


def e(value):
    if value is None:
        return ""
    text = str(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


class DashboardBuilder:
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        self.out_dir = self.root_dir / "Salidas" / "Dashboard"
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def build(self, sistema: SistemaDia, motor_data: dict | None = None) -> Path:
        motor_data = motor_data or {}
        sistema.cronograma = self._generar_cronograma_especifico(sistema, motor_data)

        fecha_str = sistema.fecha_texto or ""
        hora_str = sistema.hora_actual or ""
        tipo_dia = sistema.tipo_dia or "Día operativo"
        turno_serpat = sistema.turno_serpat or "N/A"
        fecha_iso = getattr(sistema, "fecha_iso", fecha_str.replace("-", ""))

        area_universidad = self._decision(sistema, "Universidad")
        area_finanzas = self._decision(sistema, "Finanzas")
        area_empresas = self._decision(sistema, "Empresas")
        area_salud = self._decision(sistema, "Salud")
        area_serpat = self._decision(sistema, "SERPAT")
        area_ancla = self._decision(sistema, "Ancla")
        if not area_ancla:
            area_ancla = self._decision(sistema, "Ancla Mental")

        identidad = sistema.identidad or {}
        recursos = sistema.recursos or {}
        contexto_excel = sistema.contexto.get("excel", {}) if isinstance(sistema.contexto, dict) else {}
        total_archivos = recursos.get("total_archivos", 0)
        total_hojas = contexto_excel.get("total_hojas", 0)
        vision_items = getattr(sistema, "vision_board", []) or []

        cronograma_html = self._cronograma_bloques_html(sistema.cronograma)
        cronograma_tabla = self._cronograma_tabla_html(sistema.cronograma)
        alertas_html = self._alertas_mini(sistema.alertas)
        pendientes_html = self._pendientes_html(sistema)
        vision_card_inicio = self._vision_inicio_card()
        vision_quote = self._vision_quote_strip()
        capital_map_html = self._capital_map_html()
        vision_decisions_html = self._vision_decisions_html(sistema)
        vision_today_html = self._vision_today_html(sistema)
        vision_progress_html = self._vision_progress_html(sistema)
        vision_detectado_html = self._vision_detectado_html(vision_items)
        vision_hero_html = self._vision_hero_html()

        word_path = f"../Word/VIDA_REAL_ENGINE_V5_{fecha_iso}.docx"
        vision_pdf_raw = "../../Recursos/09_PANEL_VISION/CARTEL DE ATRACCION VISUAL (1).pdf"
        dashboard_path = self.out_dir / f"CENTRO_COMANDO_V5.4.3_{fecha_str.replace('-', '')}.html"

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VIDA REAL ENGINE V5.4.3 FINAL</title>
    <style>
        :root {{
            --bg: #050b14;
            --bg-2: #091423;
            --panel: rgba(12, 26, 43, 0.94);
            --panel-2: rgba(16, 34, 56, 0.95);
            --line: rgba(78, 126, 178, 0.42);
            --line-strong: rgba(255, 196, 46, 0.6);
            --text: #edf4ff;
            --muted: #9cb6d1;
            --accent: #ffc62c;
            --accent-2: #6aa9ff;
            --good: #46d17a;
            --warn: #ffb24d;
            --danger: #ff6b7f;
        }}

        * {{ box-sizing: border-box; }}

        html, body {{ height: 100%; }}

        body {{
            margin: 0;
            font-family: "Segoe UI", Arial, sans-serif;
            color: var(--text);
            overflow: hidden;
            background:
                radial-gradient(circle at 10% 0%, rgba(255, 196, 46, 0.12), transparent 35%),
                radial-gradient(circle at 90% 8%, rgba(106, 169, 255, 0.14), transparent 30%),
                linear-gradient(145deg, var(--bg) 0%, #08111c 45%, #07131f 100%);
        }}

        body::before {{
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
                linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 42px 42px;
            mask-image: linear-gradient(180deg, rgba(0,0,0,0.85), rgba(0,0,0,0.45));
            opacity: 0.6;
        }}

        .topbar {{
            position: sticky;
            top: 0;
            z-index: 40;
            padding: 10px 18px 9px;
            background: linear-gradient(180deg, rgba(5, 11, 20, 0.96), rgba(7, 18, 30, 0.92));
            border-bottom: 1px solid rgba(255, 196, 46, 0.35);
            box-shadow: 0 14px 28px rgba(0, 0, 0, 0.38);
            backdrop-filter: blur(8px);
        }}

        .hero {{
            display: grid;
            grid-template-columns: 1.4fr 1fr;
            gap: 14px;
            align-items: center;
        }}

        .hero-title h1 {{
            margin: 0;
            font-size: 20px;
            line-height: 1.05;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #f6fbff;
        }}

        .hero-title .eyebrow {{
            margin-top: 2px;
            color: var(--accent);
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.6px;
            text-transform: uppercase;
        }}

        .hero-title .tagline {{
            margin-top: 4px;
            color: var(--muted);
            font-size: 10px;
        }}

        .header-metrics {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 8px;
        }}

        .metric {{
            min-height: 50px;
            padding: 8px 10px;
            border-radius: 12px;
            background: linear-gradient(145deg, rgba(16, 34, 56, 0.95), rgba(12, 26, 43, 0.9));
            border: 1px solid var(--line);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        }}

        .metric small {{
            display: block;
            color: #87b2d8;
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}

        .metric strong {{
            display: block;
            margin-top: 2px;
            font-size: 12px;
            color: #f3f8ff;
        }}

        .metric span {{
            display: block;
            margin-top: 1px;
            color: var(--muted);
            font-size: 10px;
        }}

        .command-bar {{
            position: sticky;
            top: 80px;
            z-index: 39;
            display: grid;
            grid-template-columns: repeat(13, minmax(0, 1fr));
            gap: 8px;
            padding: 8px 18px 10px;
            border-bottom: 1px solid rgba(255, 196, 46, 0.16);
            background: rgba(7, 17, 27, 0.92);
            backdrop-filter: blur(10px);
        }}

        .nav-btn {{
            border: 1px solid rgba(121, 170, 226, 0.45);
            border-radius: 999px;
            padding: 10px 12px;
            background: linear-gradient(180deg, rgba(20, 40, 66, 0.96), rgba(11, 25, 41, 0.98));
            color: var(--text);
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            cursor: pointer;
            transition: transform .16s ease, box-shadow .16s ease, border-color .16s ease;
        }}

        .nav-btn:hover {{
            transform: translateY(-1px);
            border-color: rgba(255, 196, 46, 0.8);
            box-shadow: 0 10px 18px rgba(0, 0, 0, 0.3);
        }}

        .nav-btn.primary {{
            background: linear-gradient(180deg, #ffd86e, #f5b91c);
            color: #122033;
            border-color: #f2c63d;
        }}

        .workspace {{
            display: grid;
            grid-template-columns: 290px minmax(0, 1fr) 305px;
            gap: 14px;
            padding: 14px 16px 18px;
            max-width: 1760px;
            margin: 0 auto;
            height: calc(100vh - 148px);
            overflow: hidden;
        }}

        .sidebar {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            align-self: start;
            height: 100%;
            max-height: 100%;
            overflow: auto;
            padding-right: 2px;
        }}

        .panel {{
            background: linear-gradient(145deg, rgba(17, 34, 54, 0.96), rgba(11, 24, 40, 0.92));
            border: 1px solid var(--line);
            border-radius: 16px;
            box-shadow: 0 12px 26px rgba(0, 0, 0, 0.34);
        }}

        .side-card {{ padding: 14px; }}

        .side-card h3 {{
            margin: 0 0 10px;
            color: var(--accent);
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .side-card p {{
            margin: 6px 0;
            color: var(--muted);
            font-size: 12px;
            line-height: 1.45;
        }}

        .left-plan-item {{
            padding: 8px 10px;
            margin-bottom: 8px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.05);
            background: rgba(255,255,255,0.03);
        }}

        .left-plan-item strong {{ display: block; font-size: 12px; color: #f4f8ff; }}
        .left-plan-item span {{ display: block; margin-top: 3px; font-size: 11px; color: var(--muted); }}

        .badge-row {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
        .badge {{
            padding: 5px 8px;
            border-radius: 999px;
            border: 1px solid rgba(255, 196, 46, 0.35);
            background: rgba(255, 196, 46, 0.08);
            color: #ffe4a1;
            font-size: 10px;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }}

        .command-box {{
            border-radius: 14px;
            padding: 12px;
            background: linear-gradient(180deg, rgba(17, 35, 56, 0.98), rgba(10, 21, 34, 0.96));
            border: 1px solid rgba(255, 196, 46, 0.2);
        }}

        .command-box h4 {{
            margin: 0 0 10px;
            color: var(--accent-2);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 12px;
        }}

        .quick-actions {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }}

        .quick-actions button, .quick-actions a {{
            border: 1px solid rgba(121, 170, 226, 0.44);
            border-radius: 10px;
            padding: 10px 10px;
            background: rgba(15, 32, 52, 0.95);
            color: var(--text);
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            text-align: center;
            cursor: pointer;
            text-decoration: none;
        }}

        .quick-actions button.primary, .quick-actions a.primary {{
            background: linear-gradient(180deg, #ffd86e, #f5b91c);
            color: #122033;
            border-color: #f2c63d;
        }}

        .stage {{
            min-height: 100%;
            height: 100%;
            padding: 0;
            overflow: hidden;
            border-radius: 18px;
        }}

        .screen {{
            display: none;
            padding: 18px;
            min-height: 100%;
            height: 100%;
            overflow: auto;
            animation: fadeIn .2s ease;
        }}

        .screen.active {{ display: block; }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .screen-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 14px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255, 196, 46, 0.28);
        }}

        .screen-header h2 {{
            margin: 0;
            font-size: 22px;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .screen-header p {{ margin: 5px 0 0; color: var(--muted); font-size: 12px; line-height: 1.4; }}

        .ghost-btn {{
            border: 1px solid rgba(255, 196, 46, 0.45);
            background: rgba(255, 196, 46, 0.08);
            color: #ffe39c;
            border-radius: 10px;
            padding: 10px 12px;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            cursor: pointer;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 10px;
            margin-bottom: 12px;
        }}

        .kpi-card {{
            padding: 12px;
            border-radius: 14px;
            background: linear-gradient(145deg, rgba(17, 37, 60, 0.98), rgba(12, 24, 39, 0.94));
            border: 1px solid rgba(121, 170, 226, 0.35);
            border-top: 2px solid var(--accent);
        }}

        .kpi-card small {{ display: block; color: #87b1d8; font-size: 10px; letter-spacing: 1px; text-transform: uppercase; font-weight: 800; }}
        .kpi-card strong {{ display: block; margin-top: 5px; color: #f6fbff; font-size: 16px; }}
        .kpi-card span {{ display: block; margin-top: 2px; color: var(--muted); font-size: 11px; }}

        .layout-grid {{
            display: grid;
            grid-template-columns: 1.12fr 0.88fr;
            gap: 12px;
            margin-bottom: 12px;
        }}

        .stack-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
            margin-bottom: 12px;
        }}

        .tile {{
            padding: 12px;
            border-radius: 14px;
            background: linear-gradient(180deg, rgba(12, 25, 42, 0.96), rgba(10, 20, 33, 0.96));
            border: 1px solid rgba(121, 170, 226, 0.28);
        }}

        .tile h3 {{
            margin: 0 0 8px;
            color: #ffd86e;
            text-transform: uppercase;
            letter-spacing: 0.9px;
            font-size: 12px;
        }}

        .tile p {{ margin: 0; color: #b8cce0; font-size: 12px; line-height: 1.45; }}

        .mini-list {{ display: flex; flex-direction: column; gap: 8px; }}

        .mini-item {{
            padding: 10px 12px;
            border-radius: 12px;
            background: rgba(255,255,255,0.03);
            border-left: 3px solid var(--accent-2);
        }}

        .mini-item strong {{ display: block; font-size: 12px; color: #f6fbff; }}
        .mini-item span {{ display: block; margin-top: 3px; color: var(--muted); font-size: 11px; line-height: 1.35; }}

        .table-card {{
            margin-bottom: 12px;
            padding: 12px;
            border-radius: 14px;
            background: rgba(7, 17, 28, 0.75);
            border: 1px solid rgba(121, 170, 226, 0.3);
        }}

        .table-card h3 {{
            margin: 0 0 10px;
            color: var(--accent);
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.9px;
        }}

        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ text-align: left; padding: 9px 8px; border-bottom: 1px solid rgba(121, 170, 226, 0.2); font-size: 12px; }}
        th {{ color: #ffd86e; font-size: 10px; text-transform: uppercase; letter-spacing: 0.9px; }}
        td {{ color: #e7f0fb; }}
        tr:hover td {{ background: rgba(255, 196, 46, 0.05); }}

        .actions-row {{ display: flex; flex-wrap: wrap; gap: 8px; }}

        .action-btn {{
            border: 1px solid rgba(255, 196, 46, 0.45);
            border-radius: 10px;
            padding: 10px 12px;
            background: linear-gradient(180deg, rgba(255, 216, 110, 0.2), rgba(255, 196, 46, 0.08));
            color: #ffe39c;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            cursor: pointer;
        }}

        .alert-list {{ display: flex; flex-direction: column; gap: 8px; max-height: 230px; overflow: auto; }}
        .alert-item {{
            padding: 9px 10px;
            border-radius: 10px;
            background: rgba(255,255,255,0.04);
            border-left: 3px solid var(--good);
            color: #f0f7ff;
            font-size: 12px;
        }}
        .alert-item strong {{ display: block; margin-bottom: 3px; }}
        .alert-item span {{ color: var(--muted); }}

        .clock-card {{
            padding: 12px;
            border-radius: 14px;
            background: linear-gradient(180deg, rgba(11, 25, 42, 0.96), rgba(7, 16, 27, 0.96));
            border: 1px solid rgba(255, 196, 46, 0.25);
        }}

        .clock-card .time {{ font-size: 25px; font-weight: 800; color: #f7fbff; }}
        .clock-card .meta {{ margin-top: 4px; color: var(--muted); font-size: 12px; line-height: 1.45; }}

        .footer-note {{
            margin-top: 12px;
            padding: 12px;
            border-radius: 14px;
            border: 1px solid rgba(255, 196, 46, 0.28);
            background: rgba(255, 196, 46, 0.06);
            color: #ffe5a0;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 800;
        }}

        .status-line {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }}

        .status-pill {{
            padding: 5px 9px;
            border-radius: 999px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(121, 170, 226, 0.32);
            color: #cfe3f7;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }}

        .print-panel {{
            border: 1px dashed rgba(255, 196, 46, 0.35);
            border-radius: 14px;
            padding: 14px;
            background: rgba(255,255,255,0.03);
        }}

        .screen-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}

        .image-card {{
            min-height: 160px;
            display: flex;
            align-items: flex-end;
            justify-content: flex-start;
            padding: 14px;
            border-radius: 16px;
            background:
                linear-gradient(180deg, rgba(7, 12, 18, 0.05), rgba(7, 12, 18, 0.5)),
                linear-gradient(135deg, rgba(32, 49, 76, 0.75), rgba(15, 24, 36, 0.92));
            border: 1px solid rgba(121, 170, 226, 0.25);
        }}

        .image-card .caption {{
            max-width: 75%;
            color: #f7fbff;
            font-size: 12px;
            line-height: 1.45;
            font-weight: 700;
            text-shadow: 0 2px 8px rgba(0,0,0,0.4);
        }}

        .screen-standalone {{
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
            gap: 12px;
        }}

        .screen-standalone .box {{
            padding: 12px;
            border-radius: 14px;
            border: 1px solid rgba(121, 170, 226, 0.26);
            background: rgba(11, 22, 36, 0.88);
        }}

        .screen-standalone .box h3 {{ margin: 0 0 8px; color: var(--accent); font-size: 13px; text-transform: uppercase; letter-spacing: 0.8px; }}
        .screen-standalone .box p {{ margin: 0; color: #b9cce0; font-size: 12px; line-height: 1.45; }}

        .schedule-list {{ display: flex; flex-direction: column; gap: 8px; }}

        .schedule-item {{
            display: grid;
            grid-template-columns: 112px 1fr;
            gap: 10px;
            padding: 10px 12px;
            border-radius: 12px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(121, 170, 226, 0.18);
        }}

        .schedule-time {{ color: #ffd86e; font-weight: 800; font-size: 12px; }}
        .schedule-meta {{ color: var(--muted); font-size: 11px; margin-top: 3px; }}
        .schedule-item strong {{ display: block; color: #f7fbff; font-size: 12px; }}
        .schedule-item span {{ display: block; color: #a8bfd6; font-size: 11px; margin-top: 3px; line-height: 1.35; }}

        .right-statement {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .vision-card {{
            position: relative;
            overflow: hidden;
            background:
                linear-gradient(135deg, rgba(255, 196, 46, 0.12), rgba(106, 169, 255, 0.06)),
                linear-gradient(180deg, rgba(18, 35, 58, 0.98), rgba(8, 20, 33, 0.96));
        }}

        .vision-card::after {{
            content: "2042";
            position: absolute;
            right: 14px;
            bottom: 10px;
            font-size: 34px;
            font-weight: 900;
            color: rgba(255, 255, 255, 0.06);
            letter-spacing: 2px;
        }}

        .vision-card p {{ position: relative; z-index: 1; }}

        .vision-pillars {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
        }}

        .capital-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
            margin-bottom: 12px;
        }}

        .capital-card {{
            padding: 12px;
            border-radius: 14px;
            background: linear-gradient(145deg, rgba(17, 37, 60, 0.98), rgba(12, 24, 39, 0.94));
            border: 1px solid rgba(255, 196, 46, 0.18);
            border-top: 2px solid rgba(106, 169, 255, 0.8);
        }}

        .capital-card h4 {{ margin: 0 0 6px; color: #ffd86e; font-size: 12px; text-transform: uppercase; letter-spacing: 0.8px; }}
        .capital-card p {{ margin: 0; color: #b9cde1; font-size: 11px; line-height: 1.45; }}

        .vision-hero {{
            padding: 8px;
            border-radius: 14px;
            border: 1px solid rgba(121, 170, 226, 0.28);
            background: linear-gradient(180deg, rgba(18, 37, 58, 0.98), rgba(7, 15, 25, 0.98));
        }}

        .vision-board-poster {{
            display: grid;
            gap: 2px;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(4, 9, 16, 0.96);
        }}

        .vision-row {{
            position: relative;
            min-height: 138px;
            padding: 14px 16px;
            display: grid;
            align-content: start;
            gap: 10px;
            overflow: hidden;
        }}

        .vision-row h4 {{
            margin: 0;
            color: #f7fbff;
            text-shadow: 0 4px 14px rgba(0, 0, 0, 0.48);
            line-height: 1.05;
            font-weight: 900;
            letter-spacing: 0.4px;
        }}

        .vision-row-top {{
            min-height: 300px;
            background:
                radial-gradient(circle at 50% 67%, rgba(255, 197, 95, 0.82), rgba(255, 184, 63, 0.12) 8%, transparent 12%),
                linear-gradient(180deg, rgba(127, 173, 196, 0.62) 0%, rgba(127, 173, 196, 0.4) 34%, rgba(243, 168, 88, 0.92) 58%, rgba(76, 110, 50, 0.96) 78%, rgba(52, 92, 39, 0.98) 100%);
        }}

        .vision-row-top h4 {{ font-size: 70px; max-width: 760px; }}

        .vision-row-house {{
            min-height: 184px;
            background: linear-gradient(180deg, rgba(24, 41, 27, 0.78), rgba(13, 22, 16, 0.93));
        }}

        .vision-row-cars {{
            min-height: 168px;
            background: linear-gradient(180deg, rgba(60, 117, 156, 0.84), rgba(35, 76, 108, 0.95));
        }}

        .vision-row-travel {{
            min-height: 168px;
            background: linear-gradient(180deg, rgba(65, 136, 194, 0.88), rgba(39, 85, 120, 0.96));
        }}

        .vision-row-business {{
            min-height: 188px;
            background: linear-gradient(180deg, rgba(70, 145, 205, 0.86), rgba(43, 90, 129, 0.96));
        }}

        .vision-row-house h4,
        .vision-row-cars h4,
        .vision-row-travel h4,
        .vision-row-business h4 {{ font-size: 54px; max-width: 1120px; }}

        .vision-gallery {{
            margin-top: auto;
            display: grid;
            gap: 2px;
        }}

        .vision-gallery.cols-2 {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
        .vision-gallery.cols-3 {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
        .vision-gallery.cols-4 {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}

        .vision-photo {{
            min-height: 96px;
            border-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background-size: cover;
            background-position: center;
            box-shadow: inset 0 0 0 999px rgba(0, 0, 0, 0.08);
        }}

        .vision-photo.house-1 {{ background-image: linear-gradient(145deg, rgba(94, 138, 183, 0.82), rgba(77, 56, 34, 0.74)); }}
        .vision-photo.house-2 {{ background-image: linear-gradient(145deg, rgba(139, 116, 83, 0.85), rgba(60, 79, 98, 0.76)); }}
        .vision-photo.house-3 {{ background-image: linear-gradient(145deg, rgba(166, 156, 139, 0.86), rgba(103, 117, 110, 0.78)); }}

        .vision-photo.car-1 {{ background-image: linear-gradient(145deg, rgba(37, 49, 67, 0.88), rgba(78, 88, 101, 0.78)); }}
        .vision-photo.car-2 {{ background-image: linear-gradient(145deg, rgba(42, 58, 78, 0.88), rgba(95, 117, 137, 0.76)); }}
        .vision-photo.car-3 {{ background-image: linear-gradient(145deg, rgba(176, 184, 190, 0.9), rgba(112, 119, 125, 0.8)); }}
        .vision-photo.car-4 {{ background-image: linear-gradient(145deg, rgba(56, 65, 75, 0.9), rgba(123, 105, 75, 0.8)); }}

        .vision-photo.travel-1 {{ background-image: linear-gradient(145deg, rgba(154, 176, 199, 0.9), rgba(82, 101, 121, 0.8)); }}
        .vision-photo.travel-2 {{ background-image: linear-gradient(145deg, rgba(88, 170, 212, 0.9), rgba(57, 107, 142, 0.82)); }}
        .vision-photo.travel-3 {{ background-image: linear-gradient(145deg, rgba(122, 176, 224, 0.88), rgba(80, 131, 179, 0.82)); }}

        .vision-photo.biz-1 {{ background-image: linear-gradient(145deg, rgba(83, 143, 185, 0.9), rgba(64, 96, 132, 0.82)); }}
        .vision-photo.biz-2 {{ background-image: linear-gradient(145deg, rgba(165, 147, 118, 0.9), rgba(91, 86, 75, 0.82)); }}
        .vision-photo.biz-3 {{ background-image: linear-gradient(145deg, rgba(188, 160, 122, 0.9), rgba(102, 89, 72, 0.84)); }}

        .quote-list {{ display: flex; flex-direction: column; gap: 8px; }}

        .quote-item {{
            padding: 10px 12px;
            border-radius: 12px;
            background: rgba(255,255,255,0.05);
            border-left: 3px solid var(--accent);
            color: #f7fbff;
            font-size: 12px;
            line-height: 1.45;
        }}

        .progress-stack {{ display: flex; flex-direction: column; gap: 10px; }}

        .progress-row {{
            display: grid;
            grid-template-columns: 132px 1fr 48px;
            gap: 10px;
            align-items: center;
        }}

        .progress-row label {{ color: #d9e8f8; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; }}
        .progress-row span {{ color: #ffd86e; font-size: 11px; font-weight: 800; text-align: right; }}

        .progress-bar {{
            height: 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            overflow: hidden;
            border: 1px solid rgba(121, 170, 226, 0.18);
        }}

        .progress-fill {{
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #f5b91c, #6aa9ff);
        }}

        .vision-cta {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-top: 10px;
            padding: 10px 12px;
            border-radius: 10px;
            border: 1px solid rgba(255, 196, 46, 0.42);
            background: rgba(255, 196, 46, 0.08);
            color: #ffe39c;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.7px;
            cursor: pointer;
        }}

        .vision-poster-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
        }}

        .vision-poster-block {{
            min-height: 92px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.08);
            background: linear-gradient(160deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
            padding: 10px;
            display: flex;
            align-items: flex-end;
            color: #f6fbff;
            font-size: 11px;
            font-weight: 700;
            line-height: 1.35;
        }}

        .vision-poster-block.luxury {{ background: linear-gradient(145deg, rgba(235, 237, 243, 0.95), rgba(142, 150, 169, 0.55)); color: #172434; }}
        .vision-poster-block.cars {{ background: linear-gradient(145deg, rgba(30, 33, 42, 0.95), rgba(94, 124, 178, 0.45)); }}
        .vision-poster-block.travel {{ background: linear-gradient(145deg, rgba(82, 168, 235, 0.92), rgba(23, 76, 122, 0.85)); }}
        .vision-poster-block.business {{ background: linear-gradient(145deg, rgba(36, 63, 99, 0.98), rgba(102, 154, 230, 0.42)); }}
        .vision-poster-block.abundance {{ background: linear-gradient(145deg, rgba(101, 71, 32, 0.92), rgba(213, 164, 84, 0.72)); color: #1d1d14; }}

        @media (max-width: 1280px) {{
            .hero, .workspace, .layout-grid, .screen-standalone, .screen-grid {{ grid-template-columns: 1fr; }}
            .header-metrics {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
            .command-bar {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
            .kpi-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
            .stack-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
            .capital-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
            .vision-gallery.cols-4 {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
            .workspace {{ height: auto; overflow: visible; }}
            .sidebar {{ position: static; max-height: none; height: auto; }}
            body {{ overflow: auto; }}
        }}

        @media (max-width: 780px) {{
            .topbar {{ padding: 14px 14px 10px; }}
            .hero-title h1 {{ font-size: 22px; }}
            .workspace {{ padding: 12px; }}
            .command-bar {{ grid-template-columns: repeat(2, minmax(0, 1fr)); padding: 10px 12px 12px; }}
            .header-metrics {{ grid-template-columns: 1fr; }}
            .kpi-grid, .stack-grid, .capital-grid, .vision-pillars, .vision-gallery {{ grid-template-columns: 1fr; }}
            .schedule-item {{ grid-template-columns: 1fr; }}
            .progress-row {{ grid-template-columns: 1fr; }}
            .vision-row-top h4 {{ font-size: 38px; }}
            .vision-row-house h4,
            .vision-row-cars h4,
            .vision-row-travel h4,
            .vision-row-business h4 {{ font-size: 28px; }}
        }}

        @media print {{
            body {{ background: #fff; color: #000; overflow: visible; }}
            body::before, .command-bar, .sidebar, .ghost-btn, .nav-btn, .action-btn {{ display: none !important; }}
            .workspace {{ display: block; padding: 0; max-width: none; height: auto; overflow: visible; }}
            .panel, .screen, .tile, .kpi-card, .table-card {{ box-shadow: none !important; }}
            .stage {{ min-height: auto; height: auto; }}
            .screen {{ display: none !important; min-height: auto; height: auto; overflow: visible; }}
            .screen.active {{ display: block !important; }}
            .topbar {{ position: static; box-shadow: none; border-bottom: 1px solid #ddd; background: #fff; }}
            .hero-title h1, .screen-header h2, .kpi-card strong, .metric strong, td, th, p, span {{ color: #000 !important; }}
        }}
    </style>
</head>
<body data-fecha="{e(fecha_iso)}" data-word-path="{e(word_path)}">
    <header class="topbar">
        <div class="hero">
            <div class="hero-title">
                <h1>VIDA REAL ENGINE V5.4.2</h1>
                <div class="eyebrow">Director Ejecutivo Digital</div>
                <div class="tagline">Centro de comando oscuro, ejecutivo y navegable para operar tu día con foco, continuidad y disciplina.</div>
            </div>
            <div class="header-metrics">
                <div class="metric"><small>Fecha</small><strong>{e(fecha_str)}</strong><span>Actualización del sistema</span></div>
                <div class="metric"><small>Hora</small><strong>{e(hora_str)}</strong><span>Hora de inicio del tablero</span></div>
                <div class="metric"><small>Tipo de día</small><strong>{e(tipo_dia)}</strong><span>Lectura operativa del día</span></div>
                <div class="metric"><small>Turno SERPAT</small><strong>{e(turno_serpat)}</strong><span>Ritmo laboral activo</span></div>
            </div>
        </div>
    </header>

    <nav class="command-bar" aria-label="Navegación principal">
        <button class="nav-btn primary" data-screen="inicio">Inicio</button>
        <button class="nav-btn" data-screen="universidad">Universidad</button>
        <button class="nav-btn" data-screen="finanzas">Finanzas</button>
        <button class="nav-btn" data-screen="empresas">Empresas</button>
        <button class="nav-btn" data-screen="salud">Salud</button>
        <button class="nav-btn" data-screen="serpat">SERPAT</button>
        <button class="nav-btn" data-screen="ancla">Ancla</button>
        <button class="nav-btn" data-screen="recursos">Recursos</button>
        <button class="nav-btn" data-screen="vision-board">Vision Board</button>
        <button class="nav-btn" data-screen="word">Word</button>
        <button class="nav-btn" data-screen="pdf">PDF</button>
        <button class="nav-btn" data-screen="imprimir">Imprimir</button>
        <button class="nav-btn primary" data-screen="inicio" data-action="back-home">Volver al inicio</button>
    </nav>

    <div class="workspace">
        <aside class="sidebar">
            <section class="panel side-card">
                <h3>Plan de desarrollo</h3>
                <div class="left-plan-item">
                    <strong>Semana 1 - Activar</strong>
                    <span>Montar el centro de comando, validar fuentes y dejar el sistema estable.</span>
                </div>
                <div class="left-plan-item">
                    <strong>Semana 2 - Corregir</strong>
                    <span>Ajustar lo necesario, limpiar pendientes y reforzar rutinas de control.</span>
                </div>
                <div class="left-plan-item">
                    <strong>Semana 3 - Consolidar</strong>
                    <span>Dejar el tablero operando con continuidad, orden y ejecución diaria.</span>
                </div>
                <div class="badge-row">
                    <span class="badge">3 semanas clave</span>
                    <span class="badge">Cockpit ejecutivo</span>
                </div>
            </section>

            <section class="panel side-card">
                <h3>Regla maestra</h3>
                <p><strong>Ley 001:</strong> Nunca romper la cadena.</p>
                <p>Si no puedes avanzar 100%, avanza 20%. Si no puedes 20%, avanza 5%. Pero nunca cero.</p>
            </section>

            <section class="panel side-card">
                <h3>Identidad</h3>
                <p><strong>Robinson</strong></p>
                <p>{e(identidad.get('proposito') or 'Constructor de futuro con disciplina, propósito y visión de largo plazo.')}</p>
                <p>{e(identidad.get('vision') or 'Convertir la realidad diaria en una plataforma de crecimiento sostenido.')}</p>
                <div class="status-line">
                    <span class="status-pill">Ley 001 activa</span>
                    <span class="status-pill">Continuidad protegida</span>
                </div>
            </section>

            <section class="panel side-card">
                <h3>Recursos</h3>
                <p><strong>{e(total_archivos)}</strong> archivos indexados</p>
                <p><strong>{e(total_hojas)}</strong> hojas Excel detectadas</p>
                <p>Word, PDF y dashboard central listos para uso diario.</p>
            </section>

            <section class="panel side-card">
                <h3>Estado del sistema</h3>
                <div class="clock-card">
                    <div class="time">{e(hora_str)}</div>
                    <div class="meta">{e(fecha_str)}<br>{e(tipo_dia)}<br>SERPAT: {e(turno_serpat)}</div>
                </div>
                <div class="status-line">
                    <span class="status-pill">Alertas: {len(sistema.alertas)}</span>
                    <span class="status-pill">Decisiones: {len(sistema.decisiones)}</span>
                </div>
            </section>

            <section class="panel side-card">
                <h3>Accesos</h3>
                <div class="command-box">
                    <h4>Exportación y navegación</h4>
                    <div class="quick-actions">
                        <button class="primary" data-screen="vision-board">Vision Board</button>
                        <button class="primary" data-screen="word">Word</button>
                        <button class="primary" data-screen="pdf">PDF</button>
                        <button class="primary" data-screen="imprimir">Imprimir</button>
                        <button data-screen="inicio">Inicio</button>
                    </div>
                </div>
            </section>
        </aside>

        <main class="panel stage" id="stage">
            <section class="screen active" id="screen-inicio">
                <div class="screen-header">
                    <div>
                        <h2>Buenos días, Robinson</h2>
                        <p>Hoy eres el Director Ejecutivo del Robinson 2042. El tablero resume tu realidad, ordena el día y protege la continuidad.</p>
                    </div>
                    <button class="ghost-btn" data-screen="inicio">Volver al inicio</button>
                </div>

                <div class="kpi-grid">
                    <div class="kpi-card"><small>Energía</small><strong>7/10</strong><span>Listo para ejecutar</span></div>
                    <div class="kpi-card"><small>Sueño</small><strong>6h 40m</strong><span>Recuperación aceptable</span></div>
                    <div class="kpi-card"><small>Continuidad</small><strong>{len(sistema.cronograma)}</strong><span>Bloques del día</span></div>
                    <div class="kpi-card"><small>Identidad</small><strong>{e(identidad.get('mision') or 'Constructor')}</strong><span>Nivel de enfoque</span></div>
                    <div class="kpi-card"><small>Foco</small><strong>{e(area_ancla.get('prioridad', 'Alto') if area_ancla else 'Alto')}</strong><span>Prioridad única</span></div>
                </div>

                <div class="layout-grid">
                    <section class="tile">
                        <h3>Propósito del día</h3>
                        <p>{e((identidad.get('proposito') or 'Salir hoy siendo una versión superior del Robinson de ayer.'))}</p>
                        <div class="badge-row">
                            <span class="badge">Disciplina</span>
                            <span class="badge">Ejecución</span>
                            <span class="badge">Orden</span>
                        </div>
                    </section>
                    <section class="tile">
                        <h3>Identidad que construyes hoy</h3>
                        <div class="mini-list">
                            <div class="mini-item"><strong>Capital intelectual</strong><span>Aprender, resolver y dejar evidencia útil.</span></div>
                            <div class="mini-item"><strong>Capital financiero</strong><span>Registrar, corregir y sostener control visible.</span></div>
                            <div class="mini-item"><strong>Capital biológico</strong><span>Proteger sueño, salud y energía física.</span></div>
                            <div class="mini-item"><strong>Capital relacional</strong><span>Ordenar compromisos, comunicación y contexto.</span></div>
                        </div>
                    </section>
                </div>

                <div class="layout-grid">
                    <section class="tile">
                        <h3>Visualización</h3>
                        <div class="image-card">
                            <div class="caption">Holdings, casa central y operación ordenada. El sistema se ve limpio, estable y preparado para crecer.</div>
                        </div>
                    </section>
                    <section class="tile">
                        <h3>Pendientes críticos</h3>
                        {pendientes_html}
                    </section>
                </div>

                <section class="tile vision-card">
                    <h3>Vision Board 2042</h3>
                    {vision_card_inicio}
                </section>

                <div class="stack-grid">
                    <section class="tile">
                        <h3>Alertas y recordatorios</h3>
                        <div class="alert-list">{alertas_html}</div>
                    </section>
                    <section class="tile">
                        <h3>Prioridades del día</h3>
                        <div class="mini-list">
                            <div class="mini-item"><strong>Universidad</strong><span>{e(area_universidad.get('accion', 'Revisar evaluaciones y resolver bloque académico.'))}</span></div>
                            <div class="mini-item"><strong>Finanzas</strong><span>{e(area_finanzas.get('accion', 'Actualizar registros y validar caja.'))}</span></div>
                            <div class="mini-item"><strong>Empresas</strong><span>{e(area_empresas.get('accion', 'Mantener el CRM y la continuidad de negocios.'))}</span></div>
                            <div class="mini-item"><strong>Salud</strong><span>{e(area_salud.get('accion', 'Cuidar cuerpo y registrar capital biológico.'))}</span></div>
                        </div>
                    </section>
                    <section class="tile">
                        <h3>Capital actual</h3>
                        <div class="mini-list">
                            <div class="mini-item"><strong>Biológico</strong><span>{e(area_salud.get('registro', 'H02_Registro_Salud'))}</span></div>
                            <div class="mini-item"><strong>Financiero</strong><span>{e(area_finanzas.get('registro', '11_Ingresos; 12_Gastos'))}</span></div>
                            <div class="mini-item"><strong>Empresarial</strong><span>{e(area_empresas.get('registro', '30_MGC_CRM'))}</span></div>
                            <div class="mini-item"><strong>Reputacional</strong><span>{e(area_serpat.get('registro', '06_TRABAJO_SERPAT'))}</span></div>
                        </div>
                    </section>
                </div>

                <section class="table-card">
                    <h3>Cronograma completo del día</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Hora</th>
                                <th>Actividad</th>
                                <th>Objetivo</th>
                                <th>Registro</th>
                                <th>Capital</th>
                            </tr>
                        </thead>
                        <tbody>
                            {cronograma_tabla}
                        </tbody>
                    </table>
                </section>

                <section class="tile">
                    <h3>Cronograma ejecutivo</h3>
                    <div class="schedule-list">{cronograma_html}</div>
                </section>
            </section>

            <section class="screen" id="screen-universidad">
                <div class="screen-header">
                    <div>
                        <h2>Universidad</h2>
                        <p>Vista académica ejecutiva para organizar ramos, evaluaciones, errores y recursos de estudio.</p>
                    </div>
                    <button class="ghost-btn" data-screen="inicio">Volver al inicio</button>
                </div>
                <div class="kpi-grid">
                    <div class="kpi-card"><small>Estado</small><strong>Activo</strong><span>Ramos priorizados</span></div>
                    <div class="kpi-card"><small>Acción IA</small><strong>Estudio</strong><span>{e(area_universidad.get('accion', 'Revisar evaluaciones'))}</span></div>
                    <div class="kpi-card"><small>Registro</small><strong>Académico</strong><span>{e(area_universidad.get('registro', '62_T2_Evaluaciones'))}</span></div>
                    <div class="kpi-card"><small>Objetivo</small><strong>Avanzar</strong><span>Sin perder continuidad</span></div>
                    <div class="kpi-card"><small>Meta</small><strong>Claridad</strong><span>Menos ruido, más entrega</span></div>
                </div>
                <div class="screen-standalone">
                    <div class="box">
                        <h3>Prioridad universitaria</h3>
                        <p>{e(area_universidad.get('motivo', 'Resuelve primero lo que más mueve el avance académico.'))}</p>
                    </div>
                    <div class="box">
                        <h3>Bloque activo</h3>
                        <p>Lectura, ejercicios, dudas, evaluación y registro disciplinado del avance académico.</p>
                    </div>
                </div>
                <div class="table-card">
                    <h3>Seguimiento académico</h3>
                    <table>
                        <thead><tr><th>Ramo</th><th>Estado</th><th>Próxima acción</th><th>Registro</th></tr></thead>
                        <tbody>
                            <tr><td>Calculo II</td><td>En curso</td><td>Resolver guía y consolidar unidad</td><td>04_UNIVERSIDAD</td></tr>
                            <tr><td>Fisica Mecanica</td><td>En revisión</td><td>Repasar lo crítico y corregir errores</td><td>04_UNIVERSIDAD</td></tr>
                            <tr><td>Probabilidad y Estadística</td><td>Pendiente</td><td>Ejercicios y control de avance</td><td>04_UNIVERSIDAD</td></tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <section class="screen" id="screen-finanzas">
                <div class="screen-header">
                    <div>
                        <h2>Finanzas</h2>
                        <p>Centro de control para ingresos, gastos, caja, conciliación y decisiones de rentabilidad.</p>
                    </div>
                    <button class="ghost-btn" data-screen="inicio">Volver al inicio</button>
                </div>
                <div class="kpi-grid">
                    <div class="kpi-card"><small>Capital financiero</small><strong>Vivo</strong><span>Registro del día</span></div>
                    <div class="kpi-card"><small>Acción IA</small><strong>{e(area_finanzas.get('accion', 'Registrar movimientos'))}</strong><span>Prioridad máxima</span></div>
                    <div class="kpi-card"><small>Registro</small><strong>{e(area_finanzas.get('registro', '11_Ingresos; 12_Gastos'))}</strong><span>Fuentes contables</span></div>
                    <div class="kpi-card"><small>Control</small><strong>Conciliación</strong><span>Visibilidad total</span></div>
                    <div class="kpi-card"><small>Riesgo</small><strong>Monitoreado</strong><span>Evitar fuga de caja</span></div>
                </div>
                <div class="stack-grid">
                    <section class="tile"><h3>Cash</h3><p>Liquidez y caja al día.</p></section>
                    <section class="tile"><h3>Ingresos</h3><p>{e(area_finanzas.get('motivo', 'Mantener trazabilidad y orden financiero.'))}</p></section>
                    <section class="tile"><h3>Gastos</h3><p>Clasificación y recorte de ruido financiero.</p></section>
                </div>
                <div class="table-card">
                    <h3>Control financiero</h3>
                    <table>
                        <thead><tr><th>Bloque</th><th>Estado</th><th>Objetivo</th><th>Registro</th></tr></thead>
                        <tbody>
                            <tr><td>Ingresos</td><td>Activo</td><td>Consolidar entradas</td><td>11_Ingresos</td></tr>
                            <tr><td>Gastos</td><td>Activo</td><td>Reducir fugas</td><td>12_Gastos</td></tr>
                            <tr><td>Conciliación</td><td>Programado</td><td>Verificar caja</td><td>18_Conciliacion_Bancaria_V3</td></tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <section class="screen" id="screen-empresas">
                <div class="screen-header">
                    <div>
                        <h2>Empresas</h2>
                        <p>Vista para continuidad comercial, CRM, holdings y capital empresarial.</p>
                    </div>
                    <button class="ghost-btn" data-screen="inicio">Volver al inicio</button>
                </div>
                <div class="kpi-grid">
                    <div class="kpi-card"><small>Acción IA</small><strong>{e(area_empresas.get('accion', 'Mantener seguimiento comercial'))}</strong><span>Bloque empresarial</span></div>
                    <div class="kpi-card"><small>Registro</small><strong>{e(area_empresas.get('registro', '30_MGC_CRM'))}</strong><span>CRM y seguimiento</span></div>
                    <div class="kpi-card"><small>Estado</small><strong>Operativo</strong><span>Holding y mercado</span></div>
                    <div class="kpi-card"><small>Objetivo</small><strong>Continuidad</strong><span>Negocio sin ruido</span></div>
                    <div class="kpi-card"><small>Visión</small><strong>Holding</strong><span>Escala y orden</span></div>
                </div>
                <div class="layout-grid">
                    <section class="tile"><h3>MGC</h3><p>CRM, oportunidades, seguimiento y pipeline.</p></section>
                    <section class="tile"><h3>Holding</h3><p>Latitud Norte Real Estate y Latutud Norte Holding operando con disciplina.</p></section>
                </div>
                <div class="table-card">
                    <h3>Control empresarial</h3>
                    <table>
                        <thead><tr><th>Unidad</th><th>Estado</th><th>Objetivo</th><th>Registro</th></tr></thead>
                        <tbody>
                            <tr><td>MGC</td><td>Activo</td><td>Dar seguimiento</td><td>30_MGC_CRM</td></tr>
                            <tr><td>Latitud Norte</td><td>Activo</td><td>Consolidar estructura</td><td>05_EMPRESAS</td></tr>
                            <tr><td>CaptaPropIA</td><td>En desarrollo</td><td>Captar oportunidades</td><td>05_EMPRESAS</td></tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <section class="screen" id="screen-salud">
                <div class="screen-header">
                    <div>
                        <h2>Salud</h2>
                        <p>Capital biológico, sueño, medicación, energía y control del cuerpo como base de ejecución.</p>
                    </div>
                    <button class="ghost-btn" data-screen="inicio">Volver al inicio</button>
                </div>
                <div class="kpi-grid">
                    <div class="kpi-card"><small>Acción IA</small><strong>{e(area_salud.get('accion', 'Cuidar cuerpo y mente'))}</strong><span>Prioridad biológica</span></div>
                    <div class="kpi-card"><small>Registro</small><strong>{e(area_salud.get('registro', 'H02_Registro_Salud'))}</strong><span>Control diario</span></div>
                    <div class="kpi-card"><small>Sueño</small><strong>6h 40m</strong><span>Recuperación aceptable</span></div>
                    <div class="kpi-card"><small>Energía</small><strong>7/10</strong><span>Arranque listo</span></div>
                    <div class="kpi-card"><small>Estado</small><strong>Vigilado</strong><span>Presión y medicación</span></div>
                </div>
                <div class="layout-grid">
                    <section class="tile"><h3>Presión</h3><p>Registrar al comenzar el día y seguir el control indicado.</p></section>
                    <section class="tile"><h3>Medicación</h3><p>Tomar y registrar lo que corresponda sin saltarse el horario.</p></section>
                </div>
                <div class="table-card">
                    <h3>Seguimiento de salud</h3>
                    <table>
                        <thead><tr><th>Elemento</th><th>Estado</th><th>Objetivo</th><th>Registro</th></tr></thead>
                        <tbody>
                            <tr><td>Presión</td><td>Pendiente</td><td>Medir y registrar</td><td>H03_Presión_Log</td></tr>
                            <tr><td>Medicamento</td><td>Programado</td><td>No olvidar toma</td><td>H02_Registro_Salud</td></tr>
                            <tr><td>Ejercicio</td><td>Planificado</td><td>Caminar o activar cuerpo</td><td>H02_Registro_Salud</td></tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <section class="screen" id="screen-serpat">
                <div class="screen-header">
                    <div>
                        <h2>SERPAT</h2>
                        <p>Turno, calendario laboral y control de continuidad en el trabajo.</p>
                    </div>
                    <button class="ghost-btn" data-screen="inicio">Volver al inicio</button>
                </div>
                <div class="kpi-grid">
                    <div class="kpi-card"><small>Tipo de día</small><strong>{e(tipo_dia)}</strong><span>Clasificación operativa</span></div>
                    <div class="kpi-card"><small>Turno</small><strong>{e(turno_serpat)}</strong><span>Bloque laboral</span></div>
                    <div class="kpi-card"><small>Acción IA</small><strong>{e(area_serpat.get('accion', 'Gestionar turno y continuidad'))}</strong><span>Orden laboral</span></div>
                    <div class="kpi-card"><small>Registro</small><strong>{e(area_serpat.get('registro', '06_TRABAJO_SERPAT'))}</strong><span>Contexto de trabajo</span></div>
                    <div class="kpi-card"><small>Estado</small><strong>Activo</strong><span>Preparación y cierre</span></div>
                </div>
                <div class="screen-standalone">
                    <div class="box"><h3>Preparación</h3><p>Checklist, salida y llegada con foco en continuidad y disciplina.</p></div>
                    <div class="box"><h3>Continuidad</h3><p>El día se coordina con universidad, salud y finanzas para no romper la cadena.</p></div>
                </div>
            </section>

            <section class="screen" id="screen-ancla">
                <div class="screen-header">
                    <div>
                        <h2>Ancla Mental</h2>
                        <p>La capa de identidad, criterio y continuidad diaria.</p>
                    </div>
                    <button class="ghost-btn" data-screen="inicio">Volver al inicio</button>
                </div>
                <div class="kpi-grid">
                    <div class="kpi-card"><small>Ley 001</small><strong>Activa</strong><span>Nunca romper la cadena</span></div>
                    <div class="kpi-card"><small>Identidad</small><strong>{e(identidad.get('mision') or 'Constructor')}</strong><span>Construir, corregir, avanzar</span></div>
                    <div class="kpi-card"><small>Continuidad</small><strong>Protegida</strong><span>Sin cero</span></div>
                    <div class="kpi-card"><small>Acción IA</small><strong>{e(area_ancla.get('accion', 'Revisar identidad y reflexionar'))}</strong><span>Autoevaluación</span></div>
                    <div class="kpi-card"><small>Registro</small><strong>{e(area_ancla.get('registro', 'Ancla Mental; 21_KPI_Diario'))}</strong><span>Cierre de día</span></div>
                </div>
                <div class="layout-grid">
                    <section class="tile"><h3>Propósito</h3><p>{e(identidad.get('proposito') or 'Construir un sistema de vida real con continuidad y propósito.')}</p></section>
                    <section class="tile"><h3>Misión</h3><p>{e(identidad.get('mision') or 'Dirigir la realidad diaria con orden, enfoque y disciplina.')}</p><button class="vision-cta" data-screen="vision-board">Abrir Vision Board 2042</button></section>
                </div>
            </section>

            <section class="screen" id="screen-recursos">
                <div class="screen-header">
                    <div>
                        <h2>Recursos</h2>
                        <p>Archivo operativo, documentos, Excel, Word, PDF e información del sistema.</p>
                    </div>
                    <button class="ghost-btn" data-screen="inicio">Volver al inicio</button>
                </div>
                <div class="kpi-grid">
                    <div class="kpi-card"><small>Archivos</small><strong>{e(total_archivos)}</strong><span>Indexados</span></div>
                    <div class="kpi-card"><small>Excel</small><strong>{e(contexto_excel.get('archivo', 'N/D'))}</strong><span>Libro activo</span></div>
                    <div class="kpi-card"><small>Hojas</small><strong>{e(total_hojas)}</strong><span>Detectadas</span></div>
                    <div class="kpi-card"><small>Word</small><strong>Disponible</strong><span>Salida diaria</span></div>
                    <div class="kpi-card"><small>PDF</small><strong>Disponible</strong><span>Vía impresión</span></div>
                </div>
                <div class="table-card">
                    <h3>Fuentes y carpetas</h3>
                    <table>
                        <thead><tr><th>Fuente</th><th>Estado</th><th>Uso</th></tr></thead>
                        <tbody>
                            <tr><td>04_UNIVERSIDAD</td><td>Activa</td><td>Estudio y evaluación</td></tr>
                            <tr><td>03_FINANZAS</td><td>Activa</td><td>Control financiero</td></tr>
                            <tr><td>05_EMPRESAS</td><td>Activa</td><td>CRM y continuidad</td></tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <section class="screen" id="screen-vision-board">
                <div class="screen-header">
                    <div>
                        <h2>Vision Board 2042</h2>
                        <p>Cartel de atracción visual convertido en módulo vivo: visión, capitales, decisiones del día y construcción concreta del Robinson 2042.</p>
                    </div>
                    <button class="ghost-btn" data-screen="inicio">Volver al inicio</button>
                </div>

                <div class="kpi-grid">
                    <div class="kpi-card"><small>Mantra central</small><strong>Mi Divina Obsesión</strong><span>Visión directiva permanente</span></div>
                    <div class="kpi-card"><small>Capitales</small><strong>8</strong><span>Mapa integral 2042</span></div>
                    <div class="kpi-card"><small>Decisiones conectadas</small><strong>{len(sistema.decisiones)}</strong><span>Hoy construyes la visión</span></div>
                    <div class="kpi-card"><small>Referencia</small><strong>PDF oficial</strong><span>CARTEL DE ATRACCION VISUAL</span></div>
                    <div class="kpi-card"><small>Lema</small><strong>2042</strong><span>No son tareas. Es construcción.</span></div>
                </div>

                <div class="layout-grid">
                    <section class="tile">
                        <h3>Cartel visual</h3>
                        {vision_hero_html}
                    </section>
                    <section class="tile">
                        <h3>Frases principales</h3>
                        <div class="quote-list">{vision_quote}</div>
                    </section>
                </div>

                <section class="table-card">
                    <h3>Mapa de capitales 2042</h3>
                    <div class="capital-grid">{capital_map_html}</div>
                </section>

                <div class="layout-grid">
                    <section class="tile">
                        <h3>Conexión con decisiones del día</h3>
                        <div class="mini-list">{vision_decisions_html}</div>
                    </section>
                    <section class="tile">
                        <h3>Progreso simbólico</h3>
                        <div class="progress-stack">{vision_progress_html}</div>
                    </section>
                </div>

                <div class="layout-grid">
                    <section class="tile">
                        <h3>Hoy construyes 2042</h3>
                        <div class="mini-list">{vision_today_html}</div>
                    </section>
                    <section class="tile">
                        <h3>Panel detectado por el sistema</h3>
                        <div class="mini-list">{vision_detectado_html}</div>
                    </section>
                </div>
            </section>

            <section class="screen" id="screen-word">
                <div class="screen-header">
                    <div>
                        <h2>Word</h2>
                        <p>Enlace diario para abrir el documento Word si existe.</p>
                    </div>
                    <button class="ghost-btn" data-screen="inicio">Volver al inicio</button>
                </div>
                <div class="screen-grid">
                    <div class="tile">
                        <h3>Documento diario</h3>
                        <p>Ruta prevista: {e(word_path)}</p>
                        <div class="actions-row" style="margin-top: 10px;">
                            <button class="action-btn" data-action="open-word">Abrir Word diario</button>
                        </div>
                    </div>
                    <div class="tile">
                        <h3>Estado</h3>
                        <p>Si el archivo existe, el navegador intentará abrirlo en una pestaña nueva.</p>
                    </div>
                </div>
            </section>

            <section class="screen" id="screen-pdf">
                <div class="screen-header">
                    <div>
                        <h2>PDF</h2>
                        <p>La exportación se realiza mediante la impresión del navegador.</p>
                    </div>
                    <button class="ghost-btn" data-screen="inicio">Volver al inicio</button>
                </div>
                <div class="print-panel">
                    <div class="actions-row">
                        <button class="action-btn" data-action="print-pdf">Imprimir / Guardar como PDF</button>
                        <button class="action-btn" data-action="print-view">Abrir vista de impresión</button>
                    </div>
                    <div class="footer-note">Usa la opción "Guardar como PDF" del diálogo de impresión del navegador.</div>
                </div>
            </section>

            <section class="screen" id="screen-imprimir">
                <div class="screen-header">
                    <div>
                        <h2>Imprimir</h2>
                        <p>Impresión del panel activo con salida limpia para papel o PDF.</p>
                    </div>
                    <button class="ghost-btn" data-screen="inicio">Volver al inicio</button>
                </div>
                <div class="print-panel">
                    <div class="actions-row">
                        <button class="action-btn" data-action="print-now">window.print()</button>
                    </div>
                    <div class="footer-note">La impresión respeta el panel activo visible en pantalla.</div>
                </div>
            </section>
        </main>

        <aside class="sidebar right-statement">
            <section class="panel side-card">
                <h3>Resultado final</h3>
                <div class="mini-list">
                    <div class="mini-item"><strong>Analiza tu realidad completa</strong><span>Captura fecha, hora, turno, alertas y estado operativo.</span></div>
                    <div class="mini-item"><strong>Piensa y decide por ti</strong><span>Convierte decisiones en prioridades visibles del día.</span></div>
                    <div class="mini-item"><strong>Entrega plan por horas</strong><span>Cada bloque del cronograma ya queda expuesto en el tablero.</span></div>
                    <div class="mini-item"><strong>Te recuerda lo importante</strong><span>El foco de salud, universidad, finanzas y empresa queda presente.</span></div>
                    <div class="mini-item"><strong>Te protege con Ley 001</strong><span>Nunca romper la cadena.</span></div>
                </div>
            </section>

            <section class="panel side-card">
                <h3>Salidas automáticas</h3>
                <div class="mini-list">
                    <div class="mini-item"><strong>Word</strong><span>{e(word_path)}</span></div>
                    <div class="mini-item"><strong>PDF</strong><span>Salida desde impresión del navegador</span></div>
                    <div class="mini-item"><strong>Dashboard</strong><span>{e(dashboard_path.as_posix())}</span></div>
                    <div class="mini-item"><strong>Excel</strong><span>{e(contexto_excel.get('archivo', 'Libro no detectado'))}</span></div>
                    <div class="mini-item"><strong>Vision Board</strong><span>{e(vision_pdf_raw)}</span></div>
                </div>
            </section>

            <section class="panel side-card">
                <h3>Fuentes de información</h3>
                <div class="mini-list">
                    <div class="mini-item"><strong>Excel CRONOGRAMA</strong><span>Todos los datos</span></div>
                    <div class="mini-item"><strong>Ancla Mental</strong><span>Capitales y reflejo diario</span></div>
                    <div class="mini-item"><strong>Vision Board 2042</strong><span>Cartel de atracción visual y obsesión directiva</span></div>
                    <div class="mini-item"><strong>Universidad</strong><span>Evaluaciones y recursos</span></div>
                    <div class="mini-item"><strong>Finanzas y empresas</strong><span>Control, continuidad y CRM</span></div>
                </div>
            </section>

            <section class="panel side-card">
                <h3>Misión del sistema</h3>
                <p>Impedir que vuelvas a ser el Robinson del pasado y construir cada día al Robinson de 2042.</p>
                <div class="footer-note">Continuidad &gt; Intensidad</div>
            </section>
        </aside>
    </div>

    <script>
        const stage = document.getElementById('stage');
        const screens = Array.from(document.querySelectorAll('.screen'));
        const navButtons = Array.from(document.querySelectorAll('[data-screen]'));

        function setActiveScreen(name) {{
            screens.forEach((screen) => screen.classList.toggle('active', screen.id === 'screen-' + name));
            screens.forEach((screen) => {{
                screen.scrollTop = 0;
            }});
            if (stage) {{
                stage.scrollTop = 0;
            }}
            window.scrollTo({{ top: 0, behavior: 'auto' }});
        }}

        function openWord() {{
            const path = document.body.dataset.wordPath || '';
            if (path) {{
                window.open(path, '_blank');
            }}
        }}

        function printNow() {{
            window.print();
        }}

        navButtons.forEach((button) => {{
            button.addEventListener('click', () => {{
                const target = button.dataset.screen;
                if (target) {{
                    setActiveScreen(target);
                }}
            }});
        }});

        document.querySelectorAll('[data-action="open-word"]').forEach((button) => button.addEventListener('click', openWord));
        document.querySelectorAll('[data-action="print-pdf"]').forEach((button) => button.addEventListener('click', printNow));
        document.querySelectorAll('[data-action="print-view"]').forEach((button) => button.addEventListener('click', printNow));
        document.querySelectorAll('[data-action="print-now"]').forEach((button) => button.addEventListener('click', printNow));

        setActiveScreen('inicio');
    </script>
</body>
</html>"""

        dashboard_path.write_text(html, encoding="utf-8")
        return dashboard_path

    def _decision(self, sistema: SistemaDia, area: str) -> dict:
        for decision in sistema.decisiones:
            if decision.get("area") == area:
                return decision
        return {}

    def _alertas_mini(self, alertas):
        if not alertas:
            return '<div class="alert-item"><strong>Sin alertas</strong><span>El sistema está limpio.</span></div>'

        html = []
        for alerta in alertas[:6]:
            titulo = e(alerta.get("titulo", "Alerta"))
            detalle = e(alerta.get("detalle", ""))
            html.append(f'<div class="alert-item"><strong>{titulo}</strong><span>{detalle}</span></div>')
        return "".join(html)

    def _pendientes_html(self, sistema: SistemaDia):
        items = []
        if sistema.alertas:
            for alerta in sistema.alertas[:5]:
                items.append(
                    f'<div class="mini-item"><strong>{e(alerta.get("area", "Sistema"))}</strong>'
                    f'<span>{e(alerta.get("titulo", "Pendiente crítico"))} - {e(alerta.get("detalle", ""))}</span></div>'
                )
        else:
            items.append('<div class="mini-item"><strong>Sin pendientes críticos</strong><span>El tablero está estable por ahora.</span></div>')
        return "".join(items)

    def _vision_frases(self) -> list[str]:
        return [
            "Mi Divina Obsesión.",
            "Yo ya vivo en mi campo de abundancia.",
            "Mi hogar es mi templo de lujo y armonía.",
            "Me muevo con estilo, poder y libertad.",
            "Viajo por el mundo haciendo negocios y disfrutando la vida.",
            "Mis negocios prosperan y multiplican millones cada mes.",
            "Soy abundancia que impacta vidas, doy trabajo y bienestar a miles.",
            "Soy millonario en expansión constante.",
            "Mis negocios prosperan cada día.",
        ]

    def _vision_quote_strip(self) -> str:
        return "".join(f'<div class="quote-item">{e(frase)}</div>' for frase in self._vision_frases())

    def _vision_hero_html(self) -> str:
        return (
            '<div class="vision-hero">'
            '<div class="vision-board-poster">'
            '<section class="vision-row vision-row-top"><h4>Yo ya vivo en mi campo de abundancia</h4></section>'
            '<section class="vision-row vision-row-house">'
            '<h4>Mi hogar es mi templo de lujo y armonía</h4>'
            '<div class="vision-gallery cols-3">'
            '<div class="vision-photo house-1"></div><div class="vision-photo house-2"></div><div class="vision-photo house-3"></div>'
            '</div>'
            '</section>'
            '<section class="vision-row vision-row-cars">'
            '<h4>Me muevo con estilo, poder y libertad</h4>'
            '<div class="vision-gallery cols-4">'
            '<div class="vision-photo car-1"></div><div class="vision-photo car-2"></div><div class="vision-photo car-3"></div><div class="vision-photo car-4"></div>'
            '</div>'
            '</section>'
            '<section class="vision-row vision-row-travel">'
            '<h4>Viajo el mundo haciendo negocios y disfrutando la vida</h4>'
            '<div class="vision-gallery cols-3">'
            '<div class="vision-photo travel-1"></div><div class="vision-photo travel-2"></div><div class="vision-photo travel-3"></div>'
            '</div>'
            '</section>'
            '<section class="vision-row vision-row-business">'
            '<h4>Mis negocios prosperan y multiplican millones cada mes</h4>'
            '<div class="vision-gallery cols-3">'
            '<div class="vision-photo biz-1"></div><div class="vision-photo biz-2"></div><div class="vision-photo biz-3"></div>'
            '</div>'
            '</section>'
            '</div>'
            '</div>'
        )

    def _vision_inicio_card(self) -> str:
        return (
            '<p>Hoy no estás haciendo tareas. Estás construyendo 2042.</p>'
            '<div class="badge-row"><span class="badge">Mi Divina Obsesión</span><span class="badge">Campo de abundancia</span></div>'
            '<button class="vision-cta" data-screen="vision-board">Abrir módulo vivo</button>'
        )

    def _capital_meta(self) -> list[tuple[str, str]]:
        return [
            ("Capital financiero", "Caja, inversiones, patrimonio y control de abundancia."),
            ("Capital empresarial", "Negocios, CRM, ventas, holdings y expansión."),
            ("Capital intelectual", "Universidad, estudio, criterio y aprendizaje superior."),
            ("Capital biológico", "Salud, sueño, energía y resistencia sostenida."),
            ("Capital relacional", "Confianza, redes, alianzas y comunicación efectiva."),
            ("Capital espiritual", "Sentido, fe, propósito y dirección interna."),
            ("Capital familiar", "Hogar, armonía, contención y legado íntimo."),
            ("Capital reputacional", "SERPAT, disciplina, profesionalismo y credibilidad visible."),
        ]

    def _capital_map_html(self) -> str:
        cards = []
        for nombre, detalle in self._capital_meta():
            cards.append(f'<article class="capital-card"><h4>{e(nombre)}</h4><p>{e(detalle)}</p></article>')
        return "".join(cards)

    def _capital_por_area(self, area: str) -> str:
        mapping = {
            "Universidad": "Capital intelectual",
            "Finanzas": "Capital financiero",
            "Empresas": "Capital empresarial",
            "Salud": "Capital biológico",
            "Ancla": "Capital espiritual / psicológico",
            "Ancla Mental": "Capital espiritual / psicológico",
            "SERPAT": "Capital reputacional",
            "Pendientes": "Capital de continuidad",
            "Sistema": "Capital de dirección",
            "Continuidad": "Capital relacional",
        }
        return mapping.get(area, "Capital de continuidad")

    def _objetivo_2042_por_area(self, area: str) -> str:
        mapping = {
            "Universidad": "Dominar conocimiento para dirigir con inteligencia superior.",
            "Finanzas": "Soy millonario en expansión constante.",
            "Empresas": "Mis negocios prosperan y multiplican millones cada mes.",
            "Salud": "Me muevo con estilo, poder y libertad.",
            "Ancla": "Yo ya vivo en mi campo de abundancia.",
            "Ancla Mental": "Yo ya vivo en mi campo de abundancia.",
            "SERPAT": "Viajo por el mundo haciendo negocios y disfrutando la vida.",
            "Pendientes": "Mis negocios prosperan cada día.",
            "Sistema": "Hoy no estás haciendo tareas. Estás construyendo 2042.",
            "Continuidad": "Soy abundancia que impacta vidas, doy trabajo y bienestar a miles.",
        }
        return mapping.get(area, "Construir 2042 con continuidad real.")

    def _vision_decisions_html(self, sistema: SistemaDia) -> str:
        items = []
        for decision in sistema.decisiones:
            area = decision.get("area", "Sistema")
            items.append(
                f'<div class="mini-item"><strong>{e(area)} -> {e(self._capital_por_area(area))}</strong>'
                f'<span>{e(decision.get("accion", ""))} | Fortalece: {e(self._objetivo_2042_por_area(area))}</span></div>'
            )
        return "".join(items) or '<div class="mini-item"><strong>Sin decisiones</strong><span>El motor aún no produjo decisiones conectables.</span></div>'

    def _vision_today_html(self, sistema: SistemaDia) -> str:
        rows = []
        for decision in sistema.decisiones:
            area = decision.get("area", "Sistema")
            rows.append(
                f'<div class="mini-item"><strong>{e(decision.get("accion", ""))}</strong>'
                f'<span>{e(self._capital_por_area(area))} | Objetivo 2042: {e(self._objetivo_2042_por_area(area))} | Evidencia: {e(decision.get("registro", "Sin registro"))}</span></div>'
            )
        return "".join(rows) or '<div class="mini-item"><strong>Sin acciones</strong><span>El tablero no tiene acciones para proyectar hoy.</span></div>'

    def _progress_value(self, decision: dict, default: int) -> int:
        if not decision:
            return default
        prioridad = int(decision.get("prioridad", default) or default)
        return max(25, min(100, prioridad))

    def _vision_progress_html(self, sistema: SistemaDia) -> str:
        bloques = [
            ("Finanzas", self._progress_value(self._decision(sistema, "Finanzas"), 74)),
            ("Empresas", self._progress_value(self._decision(sistema, "Empresas"), 72)),
            ("Universidad", self._progress_value(self._decision(sistema, "Universidad"), 88)),
            ("Salud", self._progress_value(self._decision(sistema, "Salud"), 80)),
            ("Identidad", self._progress_value(self._decision(sistema, "Ancla") or self._decision(sistema, "Ancla Mental"), 85)),
            ("Continuidad", min(100, 45 + len(sistema.cronograma) * 3)),
        ]
        html = []
        for nombre, valor in bloques:
            html.append(
                f'<div class="progress-row"><label>{e(nombre)}</label><div class="progress-bar"><div class="progress-fill" style="width: {valor}%;"></div></div><span>{valor}%</span></div>'
            )
        return "".join(html)

    def _vision_detectado_html(self, vision_items) -> str:
        if not vision_items:
            return (
                '<div class="mini-item"><strong>Referencia oficial</strong><span>PDF detectado en Recursos/09_PANEL_VISION.</span></div>'
                '<div class="mini-item"><strong>Fallback HTML activo</strong><span>Se renderizan frases, capitales y decisiones aunque el PDF no se incruste.</span></div>'
                '<div class="mini-item"><strong>Estado</strong><span>Módulo Vision Board 2042 operativo dentro del Centro de Comando.</span></div>'
            )

        items = []
        for item in vision_items[:4]:
            categoria = item.get("categoria", "Vision")
            texto = item.get("texto", item.get("objetivo", "Elemento detectado"))
            items.append(f'<div class="mini-item"><strong>{e(categoria)}</strong><span>{e(texto)}</span></div>')
        return "".join(items)

    def _to_minutes(self, hhmm: str) -> int:
        try:
            hh, mm = (hhmm or "00:00").split(":")
            return max(0, min(23, int(hh))) * 60 + max(0, min(59, int(mm)))
        except Exception:
            return 0

    def _to_hhmm(self, minutes: int) -> str:
        m = int(minutes) % (24 * 60)
        return f"{m // 60:02d}:{m % 60:02d}"

    def _duracion_min(self, inicio: str, fin: str) -> int:
        a = self._to_minutes(inicio)
        b = self._to_minutes(fin)
        if b >= a:
            return b - a
        return (24 * 60 - a) + b

    def _cronograma_item(
        self,
        hora_inicio: str,
        hora_fin: str,
        area: str,
        actividad: str,
        objetivo: str,
        registro: str,
        *,
        motivo: str = "",
        prioridad: int = 70,
        evidencia_requerida: str = "",
        hoja_excel: str = "",
        documento_relacionado: str = "",
        objetivo_2042: str = "",
    ) -> dict:
        duracion = self._duracion_min(hora_inicio, hora_fin)
        capital = self._capital_por_area(area)
        return {
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "duracion": f"{duracion} min",
            "area": area,
            "capital": capital,
            "capital_construido": capital,
            "titulo": actividad,
            "actividad": actividad,
            "actividad_exacta": actividad,
            "objetivo": objetivo,
            "motivo": motivo or objetivo,
            "prioridad": prioridad,
            "evidencia_requerida": evidencia_requerida or registro,
            "hoja_excel": hoja_excel or registro,
            "documento_relacionado": documento_relacionado or "Sin documento explícito",
            "objetivo_2042_asociado": objetivo_2042 or self._objetivo_2042_por_area(area),
            "registro": registro,
        }

    def _detectar_turno_info(self, sistema: SistemaDia) -> dict:
        tipo = " ".join(
            str(valor or "")
            for valor in (
                sistema.tipo_dia,
                sistema.contexto.get("tipo_dia") if isinstance(sistema.contexto, dict) else "",
            )
        ).lower()
        turno_txt = " ".join(
            str(valor or "")
            for valor in (
                sistema.turno_serpat,
                sistema.contexto.get("turno_serpat") if isinstance(sistema.contexto, dict) else "",
                sistema.serpat.get("turno_serpat") if isinstance(sistema.serpat, dict) else "",
            )
        ).lower().replace("—", "-").replace("–", "-")

        ingreso = str(sistema.serpat.get("ingreso") or "").strip() if isinstance(sistema.serpat, dict) else ""
        salida = str(sistema.serpat.get("salida") or "").strip() if isinstance(sistema.serpat, dict) else ""
        if not ingreso or not salida:
            match = re.search(r"(\d{1,2}:\d{2}).*?(\d{1,2}:\d{2})", turno_txt)
            if match:
                ingreso = ingreso or match.group(1)
                salida = salida or match.group(2)

        if "libre" in tipo or "libre" in turno_txt:
            return {"tipo": "libre", "ingreso": "", "salida": "", "activo": False}
        if "noche" in tipo:
            return {"tipo": "noche", "ingreso": ingreso or "21:00", "salida": salida or "08:00", "activo": True}
        if "tarde" in tipo:
            return {"tipo": "tarde", "ingreso": ingreso or "12:30", "salida": salida or "21:00", "activo": True}
        if "mañana" in tipo or "manana" in tipo or ingreso:
            return {"tipo": "mañana", "ingreso": ingreso or "08:00", "salida": salida or "16:30", "activo": True}
        return {"tipo": "libre", "ingreso": "", "salida": "", "activo": False}

    def _area_hoja_excel(self, area: str, registro: str) -> str:
        mapping = {
            "Universidad": "61_T2_Ramos; 62_T2_Evaluaciones; 63_T2_Bloques; 64_T2_Errores",
            "Finanzas": "11_Ingresos; 12_Gastos; 13_Deudas; 18_Conciliacion_Bancaria_V3",
            "Empresas": "30_MGC_CRM; 33_Seguimientos; 70_Mercado_MGC; 76_CaptaPropIA",
            "Salud": "H02_Registro_Salud; H03_Presion_Log; H00_Dashboard_Health",
            "SERPAT": "SERPAT TURNOS",
            "Ancla": "Ancla Mental; 21_KPI_Diario",
            "Ancla Mental": "Ancla Mental; 21_KPI_Diario",
            "Desarrollo personal": "DESARROLLO_PERSONAL; 21_KPI_Diario",
            "Pendientes": "PENDIENTES; 90_Alertas_Correcciones",
            "Sistema": "00_GENERADOR_DIA; 20_Registro_Diario; 21_KPI_Diario",
        }
        return registro or mapping.get(area, "20_Registro_Diario")

    def _documento_relacionado(self, sistema: SistemaDia, area: str) -> str:
        categorias = (sistema.recursos or {}).get("categorias", {}) if isinstance(sistema.recursos, dict) else {}
        if not categorias:
            return "Recursos sin índice"

        claves = {
            "Universidad": ["04_UNIVERSIDAD"],
            "Salud": ["02_SALUD"],
            "Finanzas": ["03_FINANZAS"],
            "Empresas": ["05_EMPRESAS"],
            "SERPAT": ["06_TRABAJO_SERPAT"],
            "Ancla": ["07_ANCLA_MENTAL", "08_LECTURA_CRECIIMIENTO"],
            "Ancla Mental": ["07_ANCLA_MENTAL", "08_LECTURA_CRECIIMIENTO"],
            "Sistema": ["09_PANEL_VISION", "99_HISTORIAL_RESPALDOS"],
            "Pendientes": ["99_HISTORIAL_RESPALDOS"],
        }.get(area, ["09_PANEL_VISION"])

        for clave in claves:
            info = categorias.get(clave)
            if info and info.get("archivos"):
                return Path(info["archivos"][0]).name
        return "Sin documento específico"

    def _historial_ref(self) -> str:
        logs = sorted((self.root_dir / "Salidas" / "Logs").glob("*.log"))
        dashboards = sorted((self.root_dir / "Salidas" / "Dashboard").glob("CENTRO_COMANDO*.html"))
        ref_logs = logs[-1].name if logs else "Sin logs previos"
        ref_dash = dashboards[-1].name if dashboards else "Sin dashboards previos"
        return f"Historial: {ref_logs} | {ref_dash}"

    def _duracion_objetivo(self, prioridad: int, area: str, carga_alertas: int) -> int:
        base = 25 + int(prioridad * 0.55)
        if area in {"Universidad", "Empresas", "Finanzas"}:
            base += 10
        if area == "Salud":
            base = max(30, base)
        if carga_alertas > 6 and area in {"Pendientes", "Sistema"}:
            base += 10
        return max(25, min(120, base))

    def _es_domingo(self, sistema: SistemaDia) -> bool:
        fecha = getattr(sistema, "fecha", None)
        try:
            return bool(fecha) and fecha.weekday() == 6
        except Exception:
            return False

    def _extraer_hojas_fuente(self, sistema: SistemaDia) -> dict:
        contexto = sistema.contexto if isinstance(sistema.contexto, dict) else {}
        excel = contexto.get("excel", {}) if isinstance(contexto.get("excel", {}), dict) else {}
        hojas = excel.get("hojas", [])
        hojas = [str(h).strip() for h in hojas if str(h).strip()]

        kpi = [h for h in hojas if "kpi" in h.lower()]
        registro = [
            h for h in hojas
            if "registro" in h.lower() or h.strip().upper() in {"20_REGISTRO_DIARIO", "21_KPI_DIARIO"}
        ]
        historial = [h for h in hojas if "historial" in h.lower() or "respaldo" in h.lower()]
        return {
            "hojas": hojas,
            "kpi": kpi,
            "registro": registro,
            "historial": historial,
        }

    def _es_solapado(self, ini_a: int, fin_a: int, ini_b: int, fin_b: int) -> bool:
        return max(ini_a, ini_b) < min(fin_a, fin_b)

    def _texto_reagendada(self, tarea: dict) -> tuple[str, str]:
        actividad = tarea.get("actividad", "Actividad")
        objetivo = tarea.get("objetivo", "Avance diario")
        return (
            f"REAGENDADA - {actividad}",
            f"{objetivo}. Reagendada por falta de tiempo fuera del bloque SERPAT.",
        )

    def _agregar_reagendada(self, agenda: list[dict], tarea: dict, hora_ref: str) -> None:
        actividad, objetivo = self._texto_reagendada(tarea)
        agenda.append(
            self._cronograma_item(
                hora_ref,
                hora_ref,
                tarea.get("area", "Sistema"),
                actividad,
                objetivo,
                tarea.get("registro", "20_Registro_Diario"),
                motivo=f"{tarea.get('motivo', 'Sin motivo')} | Estado: reagendada.",
                prioridad=int(tarea.get("prioridad", 70) or 70),
                evidencia_requerida=f"Reagendar en 20_Registro_Diario: {tarea.get('evidencia', tarea.get('registro', 'Registro diario'))}",
                hoja_excel=tarea.get("hoja_excel", tarea.get("registro", "20_Registro_Diario")),
                documento_relacionado=tarea.get("documento", "Sin documento específico"),
                objetivo_2042=tarea.get("objetivo_2042", self._objetivo_2042_por_area(tarea.get("area", "Sistema"))),
            )
        )

    def _bloque_desde_tarea(self, sistema: SistemaDia, tarea: dict, ini: str, fin: str, area_default: str, actividad_default: str, objetivo_default: str, registro_default: str) -> dict:
        area = tarea.get("area", area_default) if tarea else area_default
        actividad = tarea.get("actividad", actividad_default) if tarea else actividad_default
        objetivo = tarea.get("objetivo", objetivo_default) if tarea else objetivo_default
        registro = tarea.get("registro", registro_default) if tarea else registro_default
        motivo = tarea.get("motivo", objetivo_default) if tarea else objetivo_default
        prioridad = int(tarea.get("prioridad", 80) or 80) if tarea else 80
        evidencia = tarea.get("evidencia", registro) if tarea else registro
        hoja_excel = tarea.get("hoja_excel", registro_default) if tarea else registro_default
        documento = tarea.get("documento", self._documento_relacionado(sistema, area)) if tarea else self._documento_relacionado(sistema, area)
        objetivo_2042 = tarea.get("objetivo_2042", self._objetivo_2042_por_area(area)) if tarea else self._objetivo_2042_por_area(area)

        return self._cronograma_item(
            ini,
            fin,
            area,
            actividad,
            objetivo,
            registro,
            motivo=motivo,
            prioridad=prioridad,
            evidencia_requerida=evidencia,
            hoja_excel=hoja_excel,
            documento_relacionado=documento,
            objetivo_2042=objetivo_2042,
        )

    def _asignar_turno_manana_base(self, sistema: SistemaDia, tareas: list[dict], turno_info: dict, cierre_dia: int) -> tuple[list[dict], list[dict], list[tuple[int, int]], int]:
        agenda = []
        restantes = list(tareas)

        def pull_area(area: str):
            for i, t in enumerate(restantes):
                if t.get("area") == area:
                    return restantes.pop(i)
            return None

        t_salud = pull_area("Salud")
        t_uni = pull_area("Universidad")
        t_fin = pull_area("Finanzas")
        t_emp = pull_area("Empresas")
        t_dev = pull_area("Desarrollo personal")
        t_ancla = pull_area("Ancla") or pull_area("Ancla Mental")

        serpat_decision = self._decision(sistema, "SERPAT")

        agenda.append(
            self._bloque_desde_tarea(
                sistema,
                t_salud,
                "06:00",
                "06:30",
                "Salud",
                "Salud / presion / hidratacion",
                "Preparar capital biologico antes de SERPAT.",
                "H02_Registro_Salud; H03_Presion_Log",
            )
        )
        agenda.append(
            self._cronograma_item(
                "06:30",
                "07:00",
                "Salud",
                "Desayuno / preparacion",
                "Asegurar energia estable y alistamiento personal.",
                "H02_Registro_Salud; 20_Registro_Diario",
                motivo="Rutina pre-turno para llegar estable a SERPAT.",
                prioridad=max(82, int((t_salud or {}).get("prioridad", 82) or 82)),
                evidencia_requerida="Desayuno y preparacion registrados.",
                hoja_excel="H02_Registro_Salud; 20_Registro_Diario",
                documento_relacionado=self._documento_relacionado(sistema, "Salud"),
                objetivo_2042=self._objetivo_2042_por_area("Salud"),
            )
        )
        agenda.append(
            self._cronograma_item(
                "07:00",
                "07:30",
                "SERPAT",
                "Traslado / alistamiento SERPAT",
                "Llegar puntual y operativo al turno.",
                "SERPAT TURNOS",
                motivo="Bloque obligatorio de traslado y preparacion pre-turno.",
                prioridad=max(90, int(serpat_decision.get("prioridad", 92) or 92)),
                evidencia_requerida="Ingreso puntual y checklist operativo previo.",
                hoja_excel="SERPAT TURNOS",
                documento_relacionado=self._documento_relacionado(sistema, "SERPAT"),
                objetivo_2042=self._objetivo_2042_por_area("SERPAT"),
            )
        )

        agenda.append(
            self._cronograma_item(
                turno_info.get("ingreso", "08:00"),
                turno_info.get("salida", "16:30"),
                "SERPAT",
                "SERPAT - bloque laboral",
                serpat_decision.get("accion", "Cumplir turno SERPAT"),
                serpat_decision.get("registro", "SERPAT TURNOS"),
                motivo=serpat_decision.get("motivo", "Turno laboral confirmado por SERPAT."),
                prioridad=int(serpat_decision.get("prioridad", 92) or 92),
                evidencia_requerida="Turno cumplido, novedades registradas y cierre operativo",
                hoja_excel="SERPAT TURNOS",
                documento_relacionado=self._documento_relacionado(sistema, "SERPAT"),
                objetivo_2042=self._objetivo_2042_por_area("SERPAT"),
            )
        )

        agenda.append(
            self._cronograma_item(
                "16:30",
                "17:15",
                "Salud",
                "Retorno / recuperacion",
                "Bajar carga del turno y recuperar energia.",
                "H02_Registro_Salud; 20_Registro_Diario",
                motivo="Transicion post-turno para proteger continuidad.",
                prioridad=84,
                evidencia_requerida="Recuperacion y estado fisico registrados.",
                hoja_excel="H02_Registro_Salud; 20_Registro_Diario",
                documento_relacionado=self._documento_relacionado(sistema, "Salud"),
                objetivo_2042=self._objetivo_2042_por_area("Salud"),
            )
        )
        agenda.append(
            self._bloque_desde_tarea(
                sistema,
                t_uni,
                "17:15",
                "18:30",
                "Universidad",
                "Universidad critica",
                "Resolver evaluacion critica y evitar riesgo academico.",
                "61_T2_Ramos; 62_T2_Evaluaciones; 64_T2_Errores",
            )
        )
        agenda.append(
            self._cronograma_item(
                "18:30",
                "19:00",
                "Salud",
                "Salud / alimentacion / presion",
                "Reponer energia y registrar estado biologico.",
                "H02_Registro_Salud; H03_Presion_Log",
                motivo="Bloque de recuperacion para sostener turno extendido.",
                prioridad=83,
                evidencia_requerida="Alimentacion, hidratacion y presion registradas.",
                hoja_excel="H02_Registro_Salud; H03_Presion_Log",
                documento_relacionado=self._documento_relacionado(sistema, "Salud"),
                objetivo_2042=self._objetivo_2042_por_area("Salud"),
            )
        )
        agenda.append(
            self._bloque_desde_tarea(
                sistema,
                t_fin,
                "19:00",
                "19:45",
                "Finanzas",
                "Finanzas",
                "Actualizar control financiero diario.",
                "11_Ingresos; 12_Gastos; 13_Deudas; 18_Conciliacion_Bancaria_V3",
            )
        )
        agenda.append(
            self._bloque_desde_tarea(
                sistema,
                t_emp,
                "19:45",
                "20:30",
                "Empresas",
                "Empresas",
                "Ejecutar accion real de continuidad empresarial.",
                "30_MGC_CRM; 33_Seguimientos; 70_Mercado_MGC; 76_CaptaPropIA",
            )
        )
        agenda.append(
            self._bloque_desde_tarea(
                sistema,
                t_dev,
                "20:30",
                "21:00",
                "Desarrollo personal",
                "Desarrollo Personal / Vision Board",
                "Conectar decisiones del dia con Vision Board y crecimiento personal.",
                "DESARROLLO_PERSONAL; VISION_BOARD; 21_KPI_Diario",
            )
        )
        agenda.append(
            self._bloque_desde_tarea(
                sistema,
                t_ancla,
                "21:00",
                "21:30",
                "Ancla Mental",
                "Ancla / cierre",
                "Cerrar identidad y definir continuidad para manana.",
                "Ancla Mental; 21_KPI_Diario; 90_Alertas_Correcciones",
            )
        )

        ventanas_restantes = []
        final_base = self._to_minutes("21:30")
        if cierre_dia > final_base:
            ventanas_restantes.append((final_base, cierre_dia))

        return agenda, restantes, ventanas_restantes, final_base

    def _validar_bloqueo_serpat(self, agenda: list[dict], turno_info: dict, cierre_dia: int) -> tuple[list[dict], list[str]]:
        if not turno_info.get("activo"):
            return agenda, []

        t_ini = self._to_minutes(turno_info.get("ingreso", "08:00"))
        t_fin = self._to_minutes(turno_info.get("salida", "16:30"))
        if t_fin <= t_ini:
            return agenda, []

        warnings = []
        corregida = []
        cola = []
        cursor_post = t_fin

        for bloque in sorted(agenda, key=lambda b: self._to_minutes(b.get("hora_inicio", "00:00"))):
            area = str(bloque.get("area", ""))
            b_ini = self._to_minutes(bloque.get("hora_inicio", "00:00"))
            b_fin = self._to_minutes(bloque.get("hora_fin", "00:00"))

            if area == "SERPAT":
                corregida.append(bloque)
                continue

            if self._es_solapado(b_ini, b_fin, t_ini, t_fin):
                warnings.append(
                    f"Solapamiento detectado y corregido: {bloque.get('actividad', 'Actividad')} ({bloque.get('hora_inicio')}-{bloque.get('hora_fin')}) con SERPAT {turno_info.get('ingreso')}-{turno_info.get('salida')}"
                )
                cola.append(bloque)
            else:
                corregida.append(bloque)

        for bloque in cola:
            dur = self._duracion_min(bloque.get("hora_inicio", "00:00"), bloque.get("hora_fin", "00:00"))
            dur = max(20, dur)
            nuevo_ini = max(cursor_post, t_fin)
            nuevo_fin = nuevo_ini + dur

            if nuevo_fin <= cierre_dia:
                bloque["hora_inicio"] = self._to_hhmm(nuevo_ini)
                bloque["hora_fin"] = self._to_hhmm(nuevo_fin)
                bloque["duracion"] = f"{dur} min"
                bloque["motivo"] = f"{bloque.get('motivo', '')} | Reubicada por bloqueo SERPAT."
                cursor_post = nuevo_fin
                corregida.append(bloque)
            else:
                bloque["hora_inicio"] = self._to_hhmm(cierre_dia)
                bloque["hora_fin"] = self._to_hhmm(cierre_dia)
                bloque["duracion"] = "0 min"
                bloque["actividad"] = f"REAGENDADA - {bloque.get('actividad', 'Actividad')}"
                bloque["actividad_exacta"] = bloque["actividad"]
                bloque["objetivo"] = f"{bloque.get('objetivo', '')}. Reagendada por bloqueo SERPAT y falta de ventana."
                bloque["motivo"] = f"{bloque.get('motivo', '')} | Estado: reagendada por bloqueo SERPAT."
                bloque["evidencia_requerida"] = f"Reagendar y ejecutar en siguiente ventana: {bloque.get('evidencia_requerida', bloque.get('registro', 'Registro diario'))}"
                corregida.append(bloque)

        corregida.sort(key=lambda b: self._to_minutes(b.get("hora_inicio", "00:00")))
        return corregida, warnings

    def _construir_tareas_dinamicas(self, sistema: SistemaDia, motor_data: dict) -> list[dict]:
        decisiones = sorted(sistema.decisiones or [], key=lambda x: int(x.get("prioridad", 0)), reverse=True)
        alertas = sistema.alertas or []
        pendientes = sistema.pendientes or []
        vision = getattr(sistema, "vision_board", []) or []
        desarrollo = getattr(sistema, "desarrollo_personal", {}) or {}
        universidad = getattr(sistema, "universidad", {}) or {}
        historial = self._historial_ref()
        fuentes_excel = self._extraer_hojas_fuente(sistema)
        es_domingo = self._es_domingo(sistema)
        serpat_activo = self._detectar_turno_info(sistema).get("activo", False)

        hojas_excel = len(fuentes_excel.get("hojas", []))
        recursos_total = int((sistema.recursos or {}).get("total_archivos", 0)) if isinstance(sistema.recursos, dict) else 0
        fuentes_texto = (
            "Excel Maestro, Recursos, SERPAT, Universidad, Salud, Finanzas, Empresas, Desarrollo Personal, "
            "Vision Board, Pendientes, Alertas, KPI, Registro Diario, Historial y Objetivos 2026-2042"
        )

        tareas = [
            {
                "area": "Sistema",
                "prioridad": 100,
                "duracion": 35 + min(20, len(alertas) * 2),
                "actividad": "Apertura EDE 360 y agenda ejecutiva",
                "objetivo": "Sincronizar estado real del dia y establecer orden de ejecucion",
                "motivo": f"Consolidar {hojas_excel} hojas Excel, {recursos_total} recursos, {len(alertas)} alertas y {len(pendientes)} pendientes.",
                "registro": "20_Registro_Diario; 21_KPI_Diario; 90_Alertas_Correcciones",
                "hoja_excel": "00_GENERADOR_DIA; 20_Registro_Diario; 21_KPI_Diario",
                "documento": historial,
                "evidencia": "Checklist EDE completo, prioridad unica definida y cronograma confirmado",
                "objetivo_2042": "Hoy no estas haciendo tareas. Estas construyendo 2042.",
                "fuentes": fuentes_texto,
            }
        ]

        areas_usadas = {"SERPAT"}
        for d in decisiones:
            area = d.get("area", "Sistema")
            if area in areas_usadas:
                continue

            prioridad = int(d.get("prioridad", 70) or 70)
            duracion = self._duracion_objetivo(prioridad, area, len(alertas))

            if es_domingo and not serpat_activo:
                if area == "Universidad":
                    tiene_critica = bool(universidad.get("critica"))
                    if not tiene_critica:
                        prioridad = min(prioridad, 78)
                        duracion = max(35, duracion - 20)
                elif area in {"Empresas", "Finanzas", "Pendientes"}:
                    prioridad = max(60, prioridad - 8)
                    duracion = max(30, duracion - 18)
                elif area == "Salud":
                    prioridad = max(prioridad, 90)
                    duracion = min(120, duracion + 20)

            registro = d.get("registro", "")
            tareas.append(
                {
                    "area": area,
                    "prioridad": prioridad,
                    "duracion": duracion,
                    "actividad": d.get("accion", f"Ejecutar bloque de {area}"),
                    "objetivo": d.get("motivo", f"Construir continuidad en {area}"),
                    "motivo": d.get("motivo", "Decisión priorizada por EDE."),
                    "registro": registro,
                    "hoja_excel": self._area_hoja_excel(area, registro),
                    "documento": self._documento_relacionado(sistema, area),
                    "evidencia": f"Evidencia operativa en {registro or 'registro diario'}.",
                    "objetivo_2042": self._objetivo_2042_por_area(area),
                    "fuentes": fuentes_texto,
                }
            )
            areas_usadas.add(area)

        if "Desarrollo personal" not in areas_usadas:
            libro = desarrollo.get("libro") if isinstance(desarrollo, dict) else ""
            capitulo = desarrollo.get("capitulo") if isinstance(desarrollo, dict) else ""
            ley = desarrollo.get("ley") if isinstance(desarrollo, dict) else ""
            tareas.append(
                {
                    "area": "Desarrollo personal",
                    "prioridad": 92 if es_domingo and not serpat_activo else 83,
                    "duracion": 55 if es_domingo and not serpat_activo else 35,
                    "actividad": "Bloque de desarrollo personal y refuerzo identitario",
                    "objetivo": "Consolidar criterio directivo y continuidad de la Ley 001.",
                    "motivo": f"Lectura activa: {libro or 'lectura estratégica'} | Capítulo: {capitulo or 'pendiente'} | Ley: {ley or 'Ley 001 activa'}.",
                    "registro": "DESARROLLO_PERSONAL; 20_Registro_Diario; 21_KPI_Diario",
                    "hoja_excel": "DESARROLLO_PERSONAL; 21_KPI_Diario",
                    "documento": self._documento_relacionado(sistema, "Ancla"),
                    "evidencia": "Insight aplicado por escrito, ajuste conductual y prioridad de continuidad definida.",
                    "objetivo_2042": self._objetivo_2042_por_area("Ancla"),
                    "fuentes": fuentes_texto,
                }
            )
            areas_usadas.add("Desarrollo personal")

        tareas.append(
            {
                "area": "Sistema",
                "prioridad": 89,
                "duracion": 30,
                "actividad": "Cierre KPI y Registro Diario",
                "objetivo": "Dejar trazabilidad cuantitativa y cualitativa del dia.",
                "motivo": (
                    f"Hojas KPI detectadas: {', '.join(fuentes_excel.get('kpi', [])[:3]) or 'ninguna'} | "
                    f"Registro diario: {', '.join(fuentes_excel.get('registro', [])[:3]) or 'ninguno'}"
                ),
                "registro": "20_Registro_Diario; 21_KPI_Diario; 90_Alertas_Correcciones",
                "hoja_excel": "20_Registro_Diario; 21_KPI_Diario",
                "documento": "Registro Diario y KPI del libro maestro",
                "evidencia": "KPI del día actualizados, decisión final registrada y correcciones anotadas.",
                "objetivo_2042": "Medir y corregir cada día para construir capital acumulado.",
                "fuentes": fuentes_texto,
            }
        )

        tareas.append(
            {
                "area": "Sistema",
                "prioridad": 76,
                "duracion": 25,
                "actividad": "Revisión de historial operativo",
                "objetivo": "Aprender del último cierre y evitar repetir errores.",
                "motivo": f"Referencias activas: {historial}.",
                "registro": "99_HISTORIAL_RESPALDOS; Salidas/Logs",
                "hoja_excel": "; ".join(fuentes_excel.get("historial", [])[:3]) or "99_HISTORIAL_RESPALDOS",
                "documento": historial,
                "evidencia": "Lección concreta del historial aplicada en el plan de hoy.",
                "objetivo_2042": "Escalar con memoria operativa, no por improvisación.",
                "fuentes": fuentes_texto,
            }
        )

        if pendientes:
            top = pendientes[0]
            tareas.append(
                {
                    "area": "Pendientes",
                    "prioridad": 92,
                    "duracion": 35,
                    "actividad": f"Cerrar pendiente critico: {top.get('tarea', 'Pendiente estrategico')}",
                    "objetivo": f"Resolver riesgo abierto en area {top.get('area', 'General')}",
                    "motivo": f"Pendiente activo con prioridad {top.get('prioridad', 'alta')} y estado {top.get('estado', 'abierto')}.",
                    "registro": "PENDIENTES; 90_Alertas_Correcciones",
                    "hoja_excel": "PENDIENTES; 20_Registro_Diario",
                    "documento": self._documento_relacionado(sistema, "Pendientes"),
                    "evidencia": "Pendiente actualizado, comentario de avance y siguiente accion",
                    "objetivo_2042": self._objetivo_2042_por_area("Pendientes"),
                    "fuentes": fuentes_texto,
                }
            )

        if vision or desarrollo:
            vision_txt = vision[0].get("objetivo", "objetivo 2042 activo") if vision else "objetivo 2042 activo"
            lectura = desarrollo.get("libro", "lectura estrategica") if isinstance(desarrollo, dict) else "lectura estrategica"
            tareas.append(
                {
                    "area": "Ancla",
                    "prioridad": 85,
                    "duracion": 30,
                    "actividad": "Ancla, visualizacion y cierre de identidad",
                    "objetivo": "Conectar decisiones del dia con la vision 2042",
                    "motivo": f"Vision activa: {vision_txt}. Refuerzo de desarrollo personal: {lectura}.",
                    "registro": "Ancla Mental; 21_KPI_Diario",
                    "hoja_excel": "DESARROLLO_PERSONAL; VISION_BOARD; 21_KPI_Diario",
                    "documento": self._documento_relacionado(sistema, "Ancla"),
                    "evidencia": "Reflexion escrita, capital construido y prioridad de manana",
                    "objetivo_2042": self._objetivo_2042_por_area("Ancla"),
                    "fuentes": fuentes_texto,
                }
            )

        tareas.sort(key=lambda t: int(t.get("prioridad", 0)), reverse=True)
        return tareas

    def _asignar_horario_dinamico(self, sistema: SistemaDia, tareas: list[dict], turno_info: dict) -> list[dict]:
        agenda = []
        warnings = []
        es_domingo = self._es_domingo(sistema)
        if es_domingo and not turno_info.get("activo"):
            inicio_dia = self._to_minutes("07:30")
            cierre_dia = self._to_minutes("21:00")
        else:
            inicio_dia = self._to_minutes("06:00")
            cierre_dia = self._to_minutes("22:30")

        ventanas = [(inicio_dia, cierre_dia)]
        if turno_info.get("activo"):
            t_ini = self._to_minutes(turno_info.get("ingreso", "08:00"))
            t_fin = self._to_minutes(turno_info.get("salida", "16:30"))
            cruza = t_fin <= t_ini

            if cruza:
                ventanas = [(max(inicio_dia, t_fin), min(cierre_dia, t_ini))]
                agenda.append(
                    self._cronograma_item(
                        turno_info.get("ingreso", "21:00"),
                        turno_info.get("salida", "08:00"),
                        "SERPAT",
                        "SERPAT - bloque laboral",
                        self._decision(sistema, "SERPAT").get("accion", "Cumplir turno SERPAT"),
                        self._decision(sistema, "SERPAT").get("registro", "SERPAT TURNOS"),
                        motivo=self._decision(sistema, "SERPAT").get("motivo", "Turno laboral confirmado por SERPAT."),
                        prioridad=int(self._decision(sistema, "SERPAT").get("prioridad", 92) or 92),
                        evidencia_requerida="Turno cumplido, novedades registradas y cierre operativo",
                        hoja_excel="SERPAT TURNOS",
                        documento_relacionado=self._documento_relacionado(sistema, "SERPAT"),
                        objetivo_2042=self._objetivo_2042_por_area("SERPAT"),
                    )
                )
            else:
                serpat_ya_insertado = False
                if turno_info.get("tipo") == "mañana":
                    agenda, tareas, ventanas, _ = self._asignar_turno_manana_base(sistema, tareas, turno_info, cierre_dia)
                    serpat_ya_insertado = True
                else:
                    ventanas = []
                    if t_ini > inicio_dia:
                        ventanas.append((inicio_dia, t_ini))
                    if t_fin < cierre_dia:
                        ventanas.append((t_fin, cierre_dia))
                    ventanas = sorted({v for v in ventanas if v[1] > v[0]})
                if not serpat_ya_insertado:
                    agenda.append(
                        self._cronograma_item(
                            turno_info.get("ingreso", "08:00"),
                            turno_info.get("salida", "16:30"),
                            "SERPAT",
                            "SERPAT - bloque laboral",
                            self._decision(sistema, "SERPAT").get("accion", "Cumplir turno SERPAT"),
                            self._decision(sistema, "SERPAT").get("registro", "SERPAT TURNOS"),
                            motivo=self._decision(sistema, "SERPAT").get("motivo", "Turno laboral confirmado por SERPAT."),
                            prioridad=int(self._decision(sistema, "SERPAT").get("prioridad", 92) or 92),
                            evidencia_requerida="Turno cumplido, novedades registradas y cierre operativo",
                            hoja_excel="SERPAT TURNOS",
                            documento_relacionado=self._documento_relacionado(sistema, "SERPAT"),
                            objetivo_2042=self._objetivo_2042_por_area("SERPAT"),
                        )
                    )

        disponibles = sum(v[1] - v[0] for v in ventanas)
        requeridos = sum(int(t.get("duracion", 30)) for t in tareas)
        escala = 1.0 if requeridos <= 0 else min(1.0, disponibles / max(requeridos, 1))

        idx = 0
        for inicio, fin in ventanas:
            cursor = inicio
            while idx < len(tareas) and cursor < fin:
                t = tareas[idx]
                dur = max(20, int(int(t.get("duracion", 30)) * escala))
                end = min(fin, cursor + dur)
                if end - cursor < 20:
                    break

                agenda.append(
                    self._cronograma_item(
                        self._to_hhmm(cursor),
                        self._to_hhmm(end),
                        t.get("area", "Sistema"),
                        t.get("actividad", "Accion ejecutiva"),
                        t.get("objetivo", "Avance diario"),
                        t.get("registro", "20_Registro_Diario"),
                        motivo=t.get("motivo", "Priorizacion EDE"),
                        prioridad=int(t.get("prioridad", 70) or 70),
                        evidencia_requerida=t.get("evidencia", t.get("registro", "Registro diario")),
                        hoja_excel=t.get("hoja_excel", t.get("registro", "20_Registro_Diario")),
                        documento_relacionado=t.get("documento", "Sin documento específico"),
                        objetivo_2042=t.get("objetivo_2042", self._objetivo_2042_por_area(t.get("area", "Sistema"))),
                    )
                )
                cursor = end
                idx += 1

            if idx >= len(tareas):
                break

        if idx < len(tareas):
            for t in tareas[idx:]:
                self._agregar_reagendada(agenda, t, self._to_hhmm(cierre_dia))

        agenda, warnings = self._validar_bloqueo_serpat(agenda, turno_info, cierre_dia)
        if warnings:
            for msg in warnings:
                print(f"[ADVERTENCIA EDE] {msg}")

        agenda.sort(key=lambda b: self._to_minutes(b.get("hora_inicio", "00:00")))
        return agenda

    def _generar_cronograma_especifico(self, sistema: SistemaDia, motor_data: dict) -> list[dict]:
        turno_info = self._detectar_turno_info(sistema)
        tareas = self._construir_tareas_dinamicas(sistema, motor_data)
        agenda = self._asignar_horario_dinamico(sistema, tareas, turno_info)
        return agenda or [
            self._cronograma_item(
                "06:00",
                "06:40",
                "Sistema",
                "Apertura EDE de contingencia",
                "No hubo datos suficientes para agenda completa, activar verificacion de fuentes",
                "20_Registro_Diario; 90_Alertas_Correcciones",
                motivo="Falta de datos en entradas primarias del sistema.",
                prioridad=99,
                evidencia_requerida="Checklist de fuentes ejecutado y alerta registrada",
                hoja_excel="00_GENERADOR_DIA; 20_Registro_Diario",
                documento_relacionado=self._historial_ref(),
                objetivo_2042=self._objetivo_2042_por_area("Sistema"),
            )
        ]

    def _cronograma_bloques_html(self, cronograma):
        partes = []
        for bloque in cronograma:
            rango = f"{bloque['hora_inicio']} - {bloque['hora_fin']}"
            partes.append(
                f'<div class="schedule-item"><div><div class="schedule-time">{e(rango)}</div><div class="schedule-meta">{e(bloque.get("capital", ""))}</div></div>'
                f'<div><strong>{e(bloque.get("actividad", ""))}</strong><span>{e(bloque.get("objetivo", ""))}</span></div></div>'
            )
        return "".join(partes)

    def _cronograma_tabla_html(self, cronograma):
        filas = []
        for bloque in cronograma:
            rango = f"{bloque['hora_inicio']} - {bloque['hora_fin']}"
            filas.append(
                f"<tr><td>{e(rango)}</td><td>{e(bloque.get('actividad', ''))}</td><td>{e(bloque.get('objetivo', ''))}</td><td>{e(bloque.get('registro', ''))}</td><td>{e(bloque.get('capital', ''))}</td></tr>"
            )
        return "".join(filas)