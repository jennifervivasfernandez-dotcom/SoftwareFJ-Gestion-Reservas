# ==============================================================
# MODULO: simulacion_reservas.py
# DESCRIPCION: Simulacion principal de reservas para Software FJ.
# ==============================================================

import os
import sys


# Permite ejecutar este archivo directamente sin depender solo de main.py.
RUTA_PROYECTO = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(RUTA_PROYECTO, "src"))

from clientes.cliente import Cliente
from excepciones.excepciones_custom import ErrorSistemaFJ
from reservas.reserva import Reserva
from servicios.alquiler_equipo import AlquilerEquipo
from servicios.asesoria import Asesoria
from servicios.reserva_sala import ReservaSala
from utils.logger import registrar_error, registrar_info


def _ejecutar_operacion(numero: int, descripcion: str, accion):
    """
    Ejecuta una operacion de la simulacion sin detener todo el programa.

    Esta funcion representa la idea principal de la guia: si ocurre un error,
    el sistema lo registra, muestra un mensaje controlado y continua con la
    siguiente operacion.
    """
    print(f"\nOperacion {numero}: {descripcion}")
    registrar_info(f"Operacion {numero}: {descripcion}")

    try:
        resultado = accion()

    except ErrorSistemaFJ as error:
        registrar_error(f"Operacion {numero} controlada con excepcion del sistema", error)
        print(f"Resultado: error controlado -> {error}")
        return None
    except Exception as error:
        registrar_error(f"Operacion {numero} genero un error inesperado", error)
        print(f"Resultado: error inesperado -> {error}")
        return None
    else:
        print(f"Resultado: {resultado}")
        registrar_info(f"Operacion {numero} finalizada correctamente")
        return resultado
    finally:
        registrar_info(f"Fin de operacion {numero}")


def ejecutar_simulacion_reservas() -> bool:
    """
    Ejecuta minimo 10 operaciones completas del sistema.

    Se mezclan casos correctos e incorrectos para demostrar validaciones,
    excepciones personalizadas, logs y continuidad del programa.
    """
    print("\n========== SIMULACION SOFTWARE FJ - RESERVAS ==========")
    registrar_info("Inicio de simulacion de reservas")

    clientes = {}
    servicios = {}
    reservas = {}

    clientes["ana"] = _ejecutar_operacion(
        1,
        "Registrar cliente valido",
        lambda: Cliente("Ana Lopez", "ana@softwarefj.com", "3001234567", "1098765432"),
    )

    _ejecutar_operacion(
        2,
        "Intentar registrar cliente con email invalido",
        lambda: Cliente("Carlos Perez", "carlos.softwarefj.com", "3101234567", "1020304050"),
    )

    servicios["sala"] = _ejecutar_operacion(
        3,
        "Crear servicio de reserva de sala",
        lambda: ReservaSala("Sala Ejecutiva Norte", 8),
    )

    _ejecutar_operacion(
        4,
        "Intentar crear sala con capacidad invalida",
        lambda: ReservaSala("Sala sin aforo", 0),
    )

    servicios["equipo"] = _ejecutar_operacion(
        5,
        "Crear servicio de alquiler de equipo",
        lambda: AlquilerEquipo("Kit de presentacion", "proyector"),
    )

    servicios["asesoria"] = _ejecutar_operacion(
        6,
        "Crear servicio de asesoria especializada",
        lambda: Asesoria("Asesoria financiera empresarial", "financiera", "experto"),
    )

    reservas["sala"] = _ejecutar_operacion(
        7,
        "Crear y procesar reserva valida de sala con descuento",
        lambda: _crear_y_procesar_reserva(
            clientes["ana"],
            servicios["sala"],
            horas=3,
            iva=19,
            descuento=10,
        ),
    )

    reservas["equipo"] = _ejecutar_operacion(
        8,
        "Crear reserva de equipo y cancelarla",
        lambda: _crear_y_cancelar_reserva(
            clientes["ana"],
            servicios["equipo"],
            horas=2,
            motivo="El cliente cambio la fecha de la actividad",
        ),
    )

    _ejecutar_operacion(
        9,
        "Intentar procesar una reserva cancelada",
        lambda: reservas["equipo"].procesar(),
    )

    reservas["asesoria"] = _ejecutar_operacion(
        10,
        "Crear reserva de asesoria y confirmarla",
        lambda: _crear_y_confirmar_reserva(
            clientes["ana"],
            servicios["asesoria"],
            horas=1.5,
        ),
    )

    _ejecutar_operacion(
        11,
        "Intentar confirmar dos veces la misma reserva",
        lambda: reservas["asesoria"].confirmar(),
    )

    servicios["temporal"] = _ejecutar_operacion(
        12,
        "Crear servicio temporal para probar disponibilidad",
        lambda: ReservaSala("Sala Temporal", 4),
    )

    reservas["temporal"] = _ejecutar_operacion(
        13,
        "Intentar procesar reserva cuando el servicio deja de estar disponible",
        lambda: _procesar_reserva_con_servicio_no_disponible(
            clientes["ana"],
            servicios["temporal"],
            horas=1,
        ),
    )

    _ejecutar_operacion(
        14,
        "Intentar crear reserva con duracion invalida",
        lambda: Reserva(clientes["ana"], servicios["sala"], 0),
    )

    print("\n========== FIN DE SIMULACION ==========")
    registrar_info("Fin de simulacion de reservas")
    return True


def _crear_y_procesar_reserva(cliente, servicio, horas: float, iva: float, descuento: float) -> str:
    reserva = Reserva(cliente, servicio, horas)
    total = reserva.procesar(porcentaje_iva=iva, porcentaje_descuento=descuento)
    return f"{reserva.describir()} | Costo procesado: {total:,.2f}"


def _crear_y_cancelar_reserva(cliente, servicio, horas: float, motivo: str) -> Reserva:
    reserva = Reserva(cliente, servicio, horas)
    reserva.cancelar(motivo)
    return reserva


def _crear_y_confirmar_reserva(cliente, servicio, horas: float) -> Reserva:
    reserva = Reserva(cliente, servicio, horas)
    reserva.confirmar()
    return reserva


def _procesar_reserva_con_servicio_no_disponible(cliente, servicio, horas: float) -> str:
    reserva = Reserva(cliente, servicio, horas)
    servicio.marcar_no_disponible("Mantenimiento de ultima hora")
    total = reserva.procesar()
    return f"{reserva.describir()} | Total: {total:,.2f}"


if __name__ == "__main__":
    ejecutar_simulacion_reservas()
