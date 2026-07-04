from __future__ import annotations
from pathlib import Path
from datetime import datetime
from Models.sistema_dia import SistemaDia


def e(x):
    """Escape HTML special characters"""
    if x is None:
        return ""
    x = str(x)
    return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


class DashboardBuilder:
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        self.out_dir = self.root_dir / "Salidas" / "Dashboard"
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def build(self, sistema: SistemaDia, motor_data: dict = None) -> Path:
        """Genera Centro de Comando HTML con todos los paneles V5.4"""
        
        motor_data = motor_data or {}
        fecha_str = sistema.fecha_texto
        hora_str = sistema.hora_actual
        tipo_dia = sistema.tipo_dia or "No definido"
        turno_serpat = sistema.turno_serpat or "N/A"
        
        # Panel Universidad
        decisiones_universidad = [d for d in sistema.decisiones if d.get('area') == 'Universidad']
        universidad_html = self._panel_universidad(decisiones_universidad, motor_data)
        
        # Panel Finanzas
        decisiones_finanzas = [d for d in sistema.decisiones if d.get('area') == 'Finanzas']
        finanzas_html = self._panel_finanzas(decisiones_finanzas)
        
        # Panel Salud
        decisiones_salud = [d for d in sistema.decisiones if d.get('area') == 'Salud']
        salud_html = self._panel_salud(decisiones_salud)
        
        # Panel Empresas
        decisiones_empresas = [d for d in sistema.decisiones if d.get('area') == 'Empresas']
        empresas_html = self._panel_empresas(decisiones_empresas)
        
        # Panel SERPAT
        serpat_html = self._panel_serpat(tipo_dia, turno_serpat, sistema.serpat or {})
        
        # Panel Ancla/Continuidad
        ancla_html = self._panel_ancla_continuidad(sistema.decisiones)
        
        # Panel Decisiones
        decisiones_html = self._panel_decisiones(sistema.decisiones)
        
        # Panel Alertas
        alertas_html = self._panel_alertas(sistema.alertas)
        
        # Panel Motores Activos
        motores_html = self._panel_motores(motor_data.get('motores_activos', []))
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VIDA REAL ENGINE V5.4 - Centro de Comando</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a1428 0%, #0d1b2a 100%);
            color: #e8f1f8;
            line-height: 1.6;
        }}
        
        header {{
            background: linear-gradient(135deg, #0f2642 0%, #1a3a52 100%);
            padding: 30px;
            border-bottom: 3px solid #ffc107;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        }}
        
        h1 {{ color: #ffc107; margin-bottom: 10px; font-size: 28px; }}
        .header-info {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 15px; }}
        .info-item {{
            background: rgba(255, 193, 7, 0.1);
            padding: 12px;
            border-left: 3px solid #ffc107;
            border-radius: 4px;
        }}
        .info-item strong {{ color: #ffc107; display: block; font-size: 12px; text-transform: uppercase; }}
        .info-item span {{ font-size: 16px; color: #e8f1f8; }}
        
        nav {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 15px;
            justify-content: center;
        }}
        
        nav button {{
            background: #ffc107;
            color: #0a1428;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        nav button:hover {{
            background: #ffeb3b;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(255, 193, 7, 0.3);
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 15px;
        }}
        
        .panel {{
            background: linear-gradient(135deg, #0f2642 0%, #1a3a52 100%);
            border: 1px solid #2d5a7b;
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 30px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }}
        
        .panel h2 {{
            color: #ffc107;
            margin-bottom: 20px;
            font-size: 22px;
            border-bottom: 2px solid #ffc107;
            padding-bottom: 10px;
        }}
        
        .panel h3 {{
            color: #64b5f6;
            margin-top: 15px;
            margin-bottom: 10px;
            font-size: 16px;
        }}
        
        .decision-item {{
            background: rgba(255, 193, 7, 0.05);
            padding: 15px;
            margin-bottom: 12px;
            border-left: 4px solid #ffc107;
            border-radius: 4px;
        }}
        
        .decision-item .area {{
            color: #ffc107;
            font-weight: bold;
            font-size: 14px;
            text-transform: uppercase;
        }}
        
        .decision-item .prioridad {{
            color: #90caf9;
            font-size: 12px;
            margin-left: 10px;
        }}
        
        .decision-item .accion {{
            margin-top: 8px;
            color: #e8f1f8;
            font-size: 15px;
        }}
        
        .decision-item .motivo {{
            margin-top: 5px;
            color: #b0bec5;
            font-size: 13px;
            font-style: italic;
        }}
        
        .alert-item {{
            background: rgba(244, 67, 54, 0.1);
            padding: 15px;
            margin-bottom: 12px;
            border-left: 4px solid #ff6b6b;
            border-radius: 4px;
        }}
        
        .alert-item .titulo {{
            color: #ff6b6b;
            font-weight: bold;
        }}
        
        .alert-item .detalle {{
            margin-top: 5px;
            color: #b0bec5;
            font-size: 13px;
        }}
        
        .motor-badge {{
            display: inline-block;
            background: #4caf50;
            color: white;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-right: 8px;
            margin-bottom: 8px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        table th {{
            background: rgba(255, 193, 7, 0.2);
            color: #ffc107;
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid #ffc107;
        }}
        
        table td {{
            padding: 12px;
            border-bottom: 1px solid #2d5a7b;
        }}
        
        table tr:hover {{
            background: rgba(255, 193, 7, 0.05);
        }}
        
        .back-to-top {{
            display: flex;
            justify-content: center;
            margin: 40px 0;
        }}
        
        .back-to-top a {{
            background: #ffc107;
            color: #0a1428;
            padding: 12px 24px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
        }}
        
        .back-to-top a:hover {{
            background: #ffeb3b;
            transform: translateY(-2px);
        }}
        
        footer {{
            background: #0f2642;
            padding: 20px;
            text-align: center;
            color: #90caf9;
            border-top: 1px solid #2d5a7b;
            margin-top: 40px;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        
        .grid-item {{
            background: rgba(255, 193, 7, 0.05);
            padding: 15px;
            border-left: 3px solid #ffc107;
            border-radius: 4px;
        }}
        
        .hidden {{ display: none; }}
    </style>
</head>
<body>
    <header id="inicio">
        <h1>VIDA REAL ENGINE V5.4 FINAL</h1>
        <p>Centro de Comando Inteligente • Motor Central IA + 11 Motores Integrados</p>
        
        <div class="header-info">
            <div class="info-item">
                <strong>Fecha</strong>
                <span>{e(fecha_str)}</span>
            </div>
            <div class="info-item">
                <strong>Hora</strong>
                <span>{e(hora_str)}</span>
            </div>
            <div class="info-item">
                <strong>Tipo de Día</strong>
                <span>{e(tipo_dia)}</span>
            </div>
            <div class="info-item">
                <strong>Turno SERPAT</strong>
                <span>{e(turno_serpat)}</span>
            </div>
        </div>
        
        <nav>
            <button onclick="document.getElementById('decisiones').scrollIntoView();">Decisiones</button>
            <button onclick="document.getElementById('alertas').scrollIntoView();">Alertas</button>
            <button onclick="document.getElementById('motores').scrollIntoView();">Motores</button>
            <button onclick="document.getElementById('universidad').scrollIntoView();">Universidad</button>
            <button onclick="document.getElementById('finanzas').scrollIntoView();">Finanzas</button>
            <button onclick="document.getElementById('salud').scrollIntoView();">Salud</button>
            <button onclick="document.getElementById('empresas').scrollIntoView();">Empresas</button>
            <button onclick="document.getElementById('serpat').scrollIntoView();">SERPAT</button>
            <button onclick="document.getElementById('ancla').scrollIntoView();">Ancla</button>
        </nav>
    </header>
    
    <div class="container">
        <!-- DECISIONES -->
        <div id="decisiones" class="panel">
            {decisiones_html}
        </div>
        
        <!-- ALERTAS -->
        <div id="alertas" class="panel">
            {alertas_html}
        </div>
        
        <!-- MOTORES ACTIVOS -->
        <div id="motores" class="panel">
            {motores_html}
        </div>
        
        <!-- UNIVERSIDAD -->
        <div id="universidad" class="panel">
            {universidad_html}
        </div>
        
        <!-- FINANZAS -->
        <div id="finanzas" class="panel">
            {finanzas_html}
        </div>
        
        <!-- SALUD -->
        <div id="salud" class="panel">
            {salud_html}
        </div>
        
        <!-- EMPRESAS -->
        <div id="empresas" class="panel">
            {empresas_html}
        </div>
        
        <!-- SERPAT -->
        <div id="serpat" class="panel">
            {serpat_html}
        </div>
        
        <!-- ANCLA/CONTINUIDAD -->
        <div id="ancla" class="panel">
            {ancla_html}
        </div>
        
        <div class="back-to-top">
            <a href="#inicio">Volver al inicio</a>
        </div>
    </div>
    
    <footer>
        <p>VIDA REAL ENGINE V5.4 FINAL • Centro de Comando Inteligente</p>
        <p>Ejecutado: {e(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))}</p>
    </footer>
</body>
</html>"""
        
        # Guardar archivo
        out = self.out_dir / f"CENTRO_COMANDO_V5.4_{fecha_str.replace('-', '')}.html"
        out.write_text(html, encoding="utf-8")
        return out
    
    def _panel_decisiones(self, decisiones):
        """Panel de decisiones consolidadas"""
        html = "<h2>Decisiones del Motor Central IA</h2>"
        if decisiones:
            for i, d in enumerate(decisiones, 1):
                area = e(d.get('area', 'Sistema'))
                prioridad = d.get('prioridad', 0)
                accion = e(d.get('accion', ''))
                motivo = e(d.get('motivo', ''))
                html += f"""
                <div class="decision-item">
                    <div>
                        <span class="area">{area}</span>
                        <span class="prioridad">Prioridad {prioridad:03d}</span>
                    </div>
                    <div class="accion">{accion}</div>
                    {f'<div class="motivo">{motivo}</div>' if motivo else ''}
                </div>"""
        else:
            html += "<p>No hay decisiones disponibles.</p>"
        return html
    
    def _panel_alertas(self, alertas):
        """Panel de alertas"""
        html = "<h2>Alertas del Sistema</h2>"
        if alertas:
            for a in alertas:
                area = e(a.get('area', 'General'))
                titulo = e(a.get('titulo', ''))
                detalle = e(a.get('detalle', ''))
                html += f"""
                <div class="alert-item">
                    <div class="titulo">{titulo}</div>
                    <div class="detalle">{area} • {detalle}</div>
                </div>"""
        else:
            html += "<p>Sin alertas activas.</p>"
        return html
    
    def _panel_motores(self, motores_activos):
        """Panel de motores activos"""
        html = "<h2>Motores Activos: 11</h2>"
        motores_default = [
            "MotorUniversidad",
            "MotorSerpat",
            "MotorPendientes",
            "MotorVisionBoard",
            "MotorDesarrolloPersonal",
            "MotorSalud",
            "MotorFinanzas",
            "MotorEmpresas",
            "MotorAncla",
            "MotorContinuidad",
            "MotorCentral"
        ]
        for motor in motores_default:
            html += f'<span class="motor-badge">✓ {motor}</span>'
        return html
    
    def _panel_universidad(self, decisiones, motor_data):
        """Panel Universidad"""
        html = "<h2>Universidad</h2>"
        html += "<h3>Análisis de Evaluaciones</h3>"
        
        if decisiones:
            for d in decisiones:
                accion = e(d.get('accion', ''))
                motivo = e(d.get('motivo', ''))
                html += f"""
                <div class="grid-item">
                    <strong>{accion[:80]}</strong>
                    <p style="margin-top: 8px; color: #b0bec5; font-size: 13px;">{motivo[:150]}</p>
                </div>"""
        else:
            html += "<p>No hay decisiones de Universidad.</p>"
        
        # Información de recursos
        html += "<h3>Recursos Disponibles</h3>"
        html += "<p>• 115 archivos en Recursos/04_UNIVERSIDAD</p>"
        html += "<p>• 36 registros de errores/dudas</p>"
        html += "<h3>Acción Recomendada</h3>"
        html += "<p>Revisar evaluaciones críticas, resolver ejercicios, registrar errores.</p>"
        
        return html
    
    def _panel_finanzas(self, decisiones):
        """Panel Finanzas"""
        html = "<h2>Finanzas</h2>"
        html += "<h3>Capital Financiero</h3>"
        
        if decisiones:
            for d in decisiones:
                accion = e(d.get('accion', ''))
                html += f"<p>• {accion}</p>"
        else:
            html += "<p>No hay decisiones de Finanzas.</p>"
        
        html += "<h3>Registros Sugeridos</h3>"
        html += "<p>• 11_Ingresos</p>"
        html += "<p>• 12_Gastos</p>"
        html += "<p>• 13_Deudas</p>"
        html += "<p>• 18_Conciliacion_Bancaria_V3</p>"
        html += "<h3>Objetivo</h3>"
        html += "<p>Construir capital financiero mediante visibilidad, control y decisión patrimonial.</p>"
        
        return html
    
    def _panel_salud(self, decisiones):
        """Panel Salud"""
        html = "<h2>Salud</h2>"
        html += "<h3>Capital Biológico</h3>"
        
        if decisiones:
            for d in decisiones:
                accion = e(d.get('accion', ''))
                html += f"<p>• {accion}</p>"
        else:
            html += "<p>No hay decisiones de Salud.</p>"
        
        html += "<h3>Registros Sugeridos</h3>"
        html += "<p>• H02_Registro_Salud</p>"
        html += "<p>• H03_Presión_Log</p>"
        html += "<p>• H00_Dashboard_Health</p>"
        html += "<h3>Objetivo</h3>"
        html += "<p>Construir capital biológico para sostener 15 años de crecimiento.</p>"
        
        return html
    
    def _panel_empresas(self, decisiones):
        """Panel Empresas"""
        html = "<h2>Empresas</h2>"
        html += "<h3>Capital Empresarial</h3>"
        
        if decisiones:
            for d in decisiones:
                accion = e(d.get('accion', ''))
                html += f"<p>• {accion}</p>"
        else:
            html += "<p>No hay decisiones de Empresas.</p>"
        
        html += "<h3>Registros Sugeridos</h3>"
        html += "<p>• 30_MGC_CRM</p>"
        html += "<p>• 33_Seguimientos</p>"
        html += "<p>• 70_Mercado_MGC</p>"
        html += "<p>• 71_Mercado_LNR</p>"
        html += "<h3>Objetivo</h3>"
        html += "<p>Ejecutar una acción concreta, registrable y acumulativa cada día.</p>"
        
        return html
    
    def _panel_serpat(self, tipo_dia, turno_serpat, datos_serpat):
        """Panel SERPAT"""
        html = "<h2>SERPAT - Calendario Laboral</h2>"
        html += f"<h3>Tipo de Día: {e(tipo_dia)}</h3>"
        html += f"<h3>Turno: {e(turno_serpat)}</h3>"
        
        if "Libre" in str(tipo_dia):
            html += "<p style='color: #4caf50; font-weight: bold;'>Día libre disponible — Usar para avance estratégico sin restricción horaria.</p>"
        else:
            ingreso = datos_serpat.get('ingreso', '?')
            salida = datos_serpat.get('salida', '?')
            html += f"<p>Horario: {e(ingreso)} a {e(salida)}</p>"
        
        html += "<h3>Observaciones</h3>"
        html += "<p>• Revisar SERPAT TURNOS para adaptar el día.</p>"
        html += "<p>• Registrar cambios en 09_PANEL_VISION.</p>"
        
        return html
    
    def _panel_ancla_continuidad(self, decisiones):
        """Panel Ancla Mental y Continuidad"""
        html = "<h2>Ancla Mental & Continuidad</h2>"
        
        decisiones_ancla = [d for d in decisiones if d.get('area') == 'Ancla Mental']
        decisiones_continuidad = [d for d in decisiones if d.get('area') == 'Continuidad']
        
        html += "<h3>Ley 001 (Cadena de Continuidad)</h3>"
        html += "<p><strong>'Nunca romper la cadena. Si no puedes avanzar al 100%, avanza al 20%; si no puedes al 20%, avanza al 5%; nunca cero.'</strong></p>"
        
        if decisiones_ancla:
            html += "<h3>Preguntas de Identidad</h3>"
            for d in decisiones_ancla:
                accion = e(d.get('accion', ''))
                html += f"<p>• {accion}</p>"
        
        html += "<h3>Capitales en Construcción</h3>"
        html += "<p>• Capital Biológico (Salud)</p>"
        html += "<p>• Capital Financiero (Finanzas)</p>"
        html += "<p>• Capital Empresarial (Empresas)</p>"
        html += "<p>• Capital Educativo (Universidad)</p>"
        html += "<p>• Capital Mental (Ancla)</p>"
        
        html += "<h3>Objetivo Diario</h3>"
        html += "<p>Evitar volver al Robinson anterior y preparar la continuidad de mañana.</p>"
        
        return html
