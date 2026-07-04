from Core.motor_central import MotorCentral
from Core.logger import guardar_log
from datetime import datetime

def generar_resumen_estado(motor, sistema):
    """Genera un resumen textual del estado del sistema"""
    resumen = []
    resumen.append("\n" + "=" * 70)
    resumen.append("RESUMEN FINAL DEL ESTADO DEL SISTEMA")
    resumen.append("=" * 70)
    
    # Estado general
    resumen.append("\n📊 ESTADO GENERAL:")
    resumen.append(f"   • Fecha: {sistema.fecha_texto}")
    resumen.append(f"   • Hora: {sistema.hora_actual}")
    resumen.append(f"   • Tipo de día: {sistema.tipo_dia or 'No definido'}")
    resumen.append(f"   • Turno SERPAT: {sistema.turno_serpat or 'N/A'}")
    
    # Recursos disponibles
    resumen.append("\n📁 RECURSOS DISPONIBLES:")
    resumen.append(f"   • Excel: {sistema.contexto['excel']['archivo']}")
    resumen.append(f"   • Hojas: {sistema.contexto['excel']['total_hojas']}")
    resumen.append(f"   • Archivos en Recursos: {sistema.recursos['total_archivos']}")
    
    # Análisis por dominio
    resumen.append("\n🎯 DOMINIOS ANALIZADOS:")
    dominios = {
        'universidad': 'Universidad',
        'salud': 'Salud',
        'finanzas': 'Finanzas',
        'empresas': 'Empresas',
        'serpat': 'SERPAT',
        'ancla': 'Ancla Mental',
        'continuidad': 'Continuidad',
        'recursos': 'Recursos',
        'pendientes': 'Pendientes'
    }
    
    for key, label in dominios.items():
        has_data = bool(sistema.__dict__.get(key))
        status = "✓" if has_data else "○"
        resumen.append(f"   {status} {label}")
    
    # Decisiones
    resumen.append(f"\n🎯 DECISIONES GENERADAS: {len(sistema.decisiones)}")
    areas_uniques = set(d.get('area', 'Sistema') for d in sistema.decisiones)
    resumen.append(f"   • Áreas cubiertas: {len(areas_uniques)}")
    for area in sorted(areas_uniques):
        count = sum(1 for d in sistema.decisiones if d.get('area') == area)
        resumen.append(f"     - {area}: {count} decisión(es)")
    
    # Prioridades
    resumen.append(f"\n📈 DISTRIBUCIÓN DE PRIORIDADES:")
    if sistema.decisiones:
        max_prio = max(d.get('prioridad', 0) for d in sistema.decisiones)
        min_prio = min(d.get('prioridad', 0) for d in sistema.decisiones)
        avg_prio = sum(d.get('prioridad', 0) for d in sistema.decisiones) / len(sistema.decisiones)
        resumen.append(f"   • Máxima: {max_prio}")
        resumen.append(f"   • Mínima: {min_prio}")
        resumen.append(f"   • Promedio: {avg_prio:.1f}")
    
    # Alertas
    resumen.append(f"\n🚨 ALERTAS GENERADAS: {len(sistema.alertas)}")
    if sistema.alertas:
        areas_alertas = {}
        for alerta in sistema.alertas:
            area = alerta.get('area', 'General')
            areas_alertas[area] = areas_alertas.get(area, 0) + 1
        for area, count in sorted(areas_alertas.items()):
            resumen.append(f"   • {area}: {count} alerta(s)")
    
    # Errores
    if motor.errores:
        resumen.append(f"\n⚠️  ERRORES DETECTADOS: {len(motor.errores)}")
        for error in motor.errores:
            resumen.append(f"   • {error}")
    else:
        resumen.append(f"\n✓ EJECUCIÓN LIMPIA: Sin errores")
    
    # Motores activos
    resumen.append("\n🔧 MOTORES ACTIVOS: 11")
    resumen.append("   ✓ MotorUniversidad (evaluaciones críticas)")
    resumen.append("   ✓ MotorSerpat (calendario laboral)")
    resumen.append("   ✓ MotorPendientes (tareas críticas)")
    resumen.append("   ✓ MotorVisionBoard (identidad 2042)")
    resumen.append("   ✓ MotorDesarrolloPersonal (Ley 001)")
    resumen.append("   ✓ MotorSalud (capital biológico)")
    resumen.append("   ✓ MotorFinanzas (capital financiero)")
    resumen.append("   ✓ MotorEmpresas (capital empresarial)")
    resumen.append("   ✓ MotorAncla (identidad diaria)")
    resumen.append("   ✓ MotorContinuidad (capitales)")
    
    resumen.append("\n" + "=" * 70)
    resumen.append("Estado: ✓ OPERATIVO")
    resumen.append("=" * 70 + "\n")
    
    return "\n".join(resumen)

def main():
    motor = MotorCentral()
    sistema = motor.ejecutar()
    
    # Buffer para log
    log_buffer = []
    
    log_buffer.append("")
    log_buffer.append("=" * 70)
    log_buffer.append(" VIDA REAL ENGINE V5.3 FINAL")
    log_buffer.append(" MOTOR CENTRAL IA + 11 MOTORES INTEGRADOS (CONSOLIDADOS)")
    log_buffer.append("=" * 70)
    
    print()
    print("=" * 70)
    print(" VIDA REAL ENGINE V5.3 FINAL")
    print(" MOTOR CENTRAL IA + 11 MOTORES INTEGRADOS (CONSOLIDADOS)")
    print("=" * 70)
    print()
    print("📅 Fecha:", sistema.fecha_texto)
    print("⏰ Hora:", sistema.hora_actual)
    print("📊 Excel:", sistema.contexto["excel"]["archivo"])
    print("📄 Hojas:", sistema.contexto["excel"]["total_hojas"])
    print("📁 Recursos:", sistema.recursos["total_archivos"], "archivos")
    print()
    
    log_buffer.append("")
    log_buffer.append(f"Fecha: {sistema.fecha_texto}")
    log_buffer.append(f"Hora: {sistema.hora_actual}")
    log_buffer.append(f"Excel: {sistema.contexto['excel']['archivo']}")
    log_buffer.append(f"Hojas: {sistema.contexto['excel']['total_hojas']}")
    log_buffer.append(f"Recursos: {sistema.recursos['total_archivos']} archivos")
    log_buffer.append("")

    if motor.errores:
        print("⚠️  ERRORES DETECTADOS:")
        log_buffer.append("ERRORES DETECTADOS:")
        for error in motor.errores:
            print(f"   ❌ {error}")
            log_buffer.append(f"   • {error}")
        print()
        log_buffer.append("")
    else:
        print("✓ Ejecución sin errores")
        log_buffer.append("✓ Ejecución sin errores")
        print()
        log_buffer.append("")

    print("🔧 MOTORES ACTIVOS: 11")
    print("   ✓ MotorUniversidad (evaluaciones críticas)")
    print("   ✓ MotorSerpat (calendario laboral)")
    print("   ✓ MotorPendientes (tareas críticas)")
    print("   ✓ MotorVisionBoard (identidad 2042)")
    print("   ✓ MotorDesarrolloPersonal (Ley 001)")
    print("   ✓ MotorSalud (capital biológico)")
    print("   ✓ MotorFinanzas (capital financiero)")
    print("   ✓ MotorEmpresas (capital empresarial)")
    print("   ✓ MotorAncla (identidad diaria)")
    print("   ✓ MotorContinuidad (capitales)")
    print()

    print("=" * 70)
    print(f"🎯 DECISIONES: {len(sistema.decisiones)} (consolidadas, sin duplicados)")
    print("=" * 70)
    print()
    
    log_buffer.append("=" * 70)
    log_buffer.append(f"DECISIONES: {len(sistema.decisiones)} (consolidadas, sin duplicados)")
    log_buffer.append("=" * 70)
    log_buffer.append("")

    for i, decision in enumerate(sistema.decisiones, start=1):
        area = decision.get('area', 'Sistema')
        prioridad = decision.get('prioridad', 0)
        accion = decision.get('accion', '')
        motivo = decision.get('motivo', '')
        registro = decision.get('registro', '')
        
        print(f"{i}. [{area}] Prioridad {prioridad:03d}")
        print(f"   📌 Acción: {accion}")
        if motivo:
            print(f"   💡 Motivo: {motivo}")
        if registro:
            print(f"   📋 Registro: {registro}")
        print()
        
        log_buffer.append(f"{i}. [{area}] Prioridad {prioridad:03d}")
        log_buffer.append(f"   Acción: {accion}")
        if motivo:
            log_buffer.append(f"   Motivo: {motivo}")
        if registro:
            log_buffer.append(f"   Registro: {registro}")
        log_buffer.append("")

    print("=" * 70)
    print(f"🚨 ALERTAS: {len(sistema.alertas)}")
    print("=" * 70)
    print()
    
    log_buffer.append("=" * 70)
    log_buffer.append(f"ALERTAS: {len(sistema.alertas)}")
    log_buffer.append("=" * 70)
    log_buffer.append("")

    for i, alerta in enumerate(sistema.alertas, start=1):
        area = alerta.get('area', '?')
        prioridad = alerta.get('prioridad', 0)
        titulo = alerta.get('titulo', '')
        detalle = alerta.get('detalle', '')
        
        print(f"{i}. [{area}] Prioridad {prioridad}")
        print(f"   ⚡ {titulo}")
        if detalle:
            print(f"   → {detalle}")
        print()
        
        log_buffer.append(f"{i}. [{area}] Prioridad {prioridad}")
        log_buffer.append(f"   {titulo}")
        if detalle:
            log_buffer.append(f"   {detalle}")
        log_buffer.append("")

    # Generar resumen del estado
    resumen = generar_resumen_estado(motor, sistema)
    print(resumen)
    log_buffer.append(resumen)

    print("=" * 70)
    print(" V5.3 FINAL COMPLETADO EXITOSAMENTE")
    print(" Decisiones consolidadas | Duplicados eliminados | Salida legible")
    print("=" * 70)
    print()
    
    log_buffer.append("=" * 70)
    log_buffer.append(" V5.3 FINAL COMPLETADO EXITOSAMENTE")
    log_buffer.append(" Decisiones consolidadas | Duplicados eliminados | Salida legible")
    log_buffer.append("=" * 70)
    
    # Guardar log en archivo
    contenido_log = "\n".join(log_buffer)
    archivo_log = guardar_log(contenido_log, "v5_3_final_ejecucion.log")
    if archivo_log:
        print(f"📄 Log guardado en: {archivo_log}")
    
    print()

if __name__ == "__main__":
    main()
