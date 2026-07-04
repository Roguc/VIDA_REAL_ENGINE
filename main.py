from Core.motor_central import MotorCentral

def main():
    motor = MotorCentral()
    sistema = motor.ejecutar()

    print()
    print("===================================")
    print(" VIDA REAL ENGINE V5.1")
    print(" MOTOR CENTRAL IA — ACTIVO")
    print("===================================")
    print()
    print("Fecha:", sistema.fecha_texto)
    print("Hora:", sistema.hora_actual)
    print("Excel:", sistema.contexto["excel"]["archivo"])
    print("Hojas:", sistema.contexto["excel"]["total_hojas"])
    print("Recursos:", sistema.recursos["total_archivos"], "archivos")
    print()
    print("DECISIONES DEL MOTOR CENTRAL:")
    print()

    for i, decision in enumerate(sistema.decisiones, start=1):
        print(f"{i}. [{decision['area']}] Prioridad {decision['prioridad']}")
        print("   Acción:", decision["accion"])
        print("   Motivo:", decision["motivo"])
        print("   Registro:", decision["registro"])
        print()

    print("ALERTAS:")
    print()

    for alerta in sistema.alertas:
        print(f"- [{alerta['area']}] {alerta['titulo']}")
        print(" ", alerta["detalle"])
        print()

if __name__ == "__main__":
    main()
