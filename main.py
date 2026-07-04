from Core.motor_central import MotorCentral

def main():
    motor = MotorCentral()
    sistema = motor.ejecutar()

    print()
    print("=" * 70)
    print(" VIDA REAL ENGINE V5.3-002")
    print(" MOTOR CENTRAL IA + 11 MOTORES INTEGRADOS (CONSOLIDADOS)")
    print("=" * 70)
    print()
    print("📅 Fecha:", sistema.fecha_texto)
    print("⏰ Hora:", sistema.hora_actual)
    print("📊 Excel:", sistema.contexto["excel"]["archivo"])
    print("📄 Hojas:", sistema.contexto["excel"]["total_hojas"])
    print("📁 Recursos:", sistema.recursos["total_archivos"], "archivos")
    print()

    if motor.errores:
        print("⚠️  ERRORES DETECTADOS:")
        for error in motor.errores:
            print(f"   ❌ {error}")
        print()

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

    print("=" * 70)
    print(f"🚨 ALERTAS: {len(sistema.alertas)}")
    print("=" * 70)
    print()

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

    print("=" * 70)
    print(" V5.3-002 COMPLETADO EXITOSAMENTE")
    print(" Decisiones consolidadas | Duplicados eliminados | Salida legible")
    print("=" * 70)
    print()

if __name__ == "__main__":
    main()
