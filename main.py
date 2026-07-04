from Core.motor_central import MotorCentral

def main():
    motor = MotorCentral()
    sistema = motor.ejecutar()

    print()
    print("=" * 60)
    print(" VIDA REAL ENGINE V5.3-001")
    print(" MOTOR CENTRAL IA + 11 MOTORES INTEGRADOS")
    print("=" * 60)
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
            print(f"   - {error}")
        print()

    print("🔧 MOTORES ACTIVOS:")
    motores_activos = [
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
    ]
    for m in motores_activos:
        print(f"   ✓ {m}")
    print()

    print("🎯 DECISIONES DEL MOTOR CENTRAL:")
    print(f"   Total: {len(sistema.decisiones)} decisiones")
    print()

    for i, decision in enumerate(sistema.decisiones, start=1):
        print(f"{i}. [{decision['area']}] Prioridad {decision['prioridad']:03d}")
        print(f"   Acción: {decision['accion'][:80]}")
        if decision['motivo']:
            print(f"   Motivo: {decision['motivo'][:60]}")
        if decision['registro']:
            print(f"   Registro: {decision['registro'][:50]}")
        print()

    print("🚨 ALERTAS:")
    print(f"   Total: {len(sistema.alertas)} alertas")
    print()

    for i, alerta in enumerate(sistema.alertas, start=1):
        print(f"{i}. [{alerta['area']}] Prioridad {alerta['prioridad']}")
        print(f"   {alerta['titulo']}")
        print(f"   → {alerta['detalle']}")
        print()

    print("=" * 60)
    print(" V5.3-001 COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
