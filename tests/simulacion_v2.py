# ==============================================================
# MODULO: simulacion_v2.py
# DESCRIPCION: Simulacion integral del sistema Software FJ.
# ==============================================================

import os
import sys


# Permite ejecutar este archivo directamente desde la terminal.
RUTA_PROYECTO = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(RUTA_PROYECTO, "src"))

from clientes.cliente import Cliente
from entidades.entidad_base import EntidadBase
from excepciones.excepciones_custom import ErrorSistemaFJ
from reservas.reserva import Reserva
from servicios.alquiler_equipo import AlquilerEquipo
from servicios.asesoria import Asesoria
from servicios.reserva_sala import ReservaSala
from utils.logger import registrar_advertencia, registrar_error, registrar_info


def _mostrar_titulo() -> None:
    """Imprime el encabezado de la simulacion en consola."""
    print("\n========== SIMULACION V2 SOFTWARE FJ ==========")
    print("Se ejecutan 15 operaciones con casos validos e invalidos.")
    registrar_info("Inicio de simulacion integral V2")


def _ejecutar_operacion(numero: int, descripcion: str, accion):
    """
    Ejecuta una operacion sin detener todo el programa.

    La idea es parecida a un entorno real: si una operacion falla, se registra
    el error, se informa en pantalla y el sistema continua con la siguiente.
    """
    print(f"\nOperacion {numero}: {descripcion}")
    registrar_info(f"Simulacion V2 - Operacion {numero}: {descripcion}")

    try:
        resultado = accion()

    except ErrorSistemaFJ as error:
        registrar_error(f"Operacion {numero} controlada por excepcion del sistema", error)
        print(f"Resultado: error controlado -> {error}")
        return None
    except Exception as error:
        registrar_error(f"Operacion {numero} genero una excepcion no esperada", error)
        print(f"Resultado: error inesperado -> {error}")
        return None
    else:
        print(f"Resultado: {resultado}")
        registrar_info(f"Operacion {numero} finalizada correctamente")
        return resultado
    finally:
        registrar_info(f"Cierre de operacion {numero}")


def ejecutar_simulacion_v2() -> bool:
    """
    Ejecuta 15 simulaciones sobre todos los modulos principales.

    Modulos cubiertos:
    - clientes
    - entidades
    - servicios
    - reservas
    - excepciones
    - utils/logger
    """
    _mostrar_titulo()

    clientes = {}
    servicios = {}
    reservas = {}

    clientes["ana"] = _ejecutar_operacion(
        1,
        "Registrar cliente valido y validar sus datos",
        lambda: _crear_cliente_valido(),
    )

    _ejecutar_operacion(
        2,
        "Intentar registrar cliente con telefono invalido",
        lambda: Cliente("Luis Rojas", "luis@softwarefj.com", "300ABC123", "10101010"),
    )

    _ejecutar_operacion(
        3,
        "Consultar informacion base heredada de EntidadBase",
        lambda: clientes["ana"].obtener_info_base(),
    )

    servicios["sala"] = _ejecutar_operacion(
        4,
        "Crear servicio de reserva de sala",
        lambda: ReservaSala("Sala Ejecutiva Norte", 8),
    )

    _ejecutar_operacion(
        5,
        "Intentar crear sala con capacidad invalida",
        lambda: ReservaSala("Sala sin aforo", 0),
    )

    servicios["equipo"] = _ejecutar_operacion(
        6,
        "Crear servicio de alquiler de equipo",
        lambda: AlquilerEquipo("Kit de presentacion", "proyector"),
    )

    _ejecutar_operacion(
        7,
        "Intentar crear equipo fuera del catalogo",
        lambda: AlquilerEquipo("Equipo no permitido", "drone"),
    )

    servicios["asesoria"] = _ejecutar_operacion(
        8,
        "Crear servicio de asesoria especializada",
        lambda: Asesoria("Asesoria financiera empresarial", "financiera", "experto"),
    )

    _ejecutar_operacion(
        9,
        "Calcular costo de asesoria con IVA y descuento",
        lambda: servicios["asesoria"].calcular_costo(
            2,
            porcentaje_iva=19,
            porcentaje_descuento=5,
        ),
    )

    reservas["sala"] = _ejecutar_operacion(
        10,
        "Crear y procesar reserva valida de sala",
        lambda: _crear_y_procesar_reserva(
            clientes["ana"],
            servicios["sala"],
            horas=3,
            iva=19,
            descuento=10,
        ),
    )

    reservas["equipo"] = _ejecutar_operacion(
        11,
        "Crear reserva de equipo y cancelarla",
        lambda: _crear_y_cancelar_reserva(
            clientes["ana"],
            servicios["equipo"],
            horas=2,
            motivo="El cliente cambio la fecha de la presentacion",
        ),
    )

    _ejecutar_operacion(
        12,
        "Intentar procesar una reserva cancelada",
        lambda: reservas["equipo"].procesar(),
    )

    reservas["asesoria"] = _ejecutar_operacion(
        13,
        "Crear reserva de asesoria y confirmarla",
        lambda: _crear_y_confirmar_reserva(
            clientes["ana"],
            servicios["asesoria"],
            horas=1.5,
        ),
    )

    _ejecutar_operacion(
        14,
        "Intentar confirmar dos veces la misma reserva",
        lambda: reservas["asesoria"].confirmar(),
    )

    _ejecutar_operacion(
        15,
        "Procesar reserva con servicio no disponible y registrar advertencia",
        lambda: _procesar_reserva_con_servicio_no_disponible(clientes["ana"]),
    )

    print("\n========== FIN DE SIMULACION V2 ==========")
    registrar_info("Fin de simulacion integral V2")
    return True


def _crear_cliente_valido() -> Cliente:
    """Crea un cliente valido para usarlo en las siguientes operaciones."""
    cliente = Cliente("Ana Lopez", "ana@softwarefj.com", "3001234567", "1098765432")
    cliente.validar()
    return cliente


def _crear_y_procesar_reserva(cliente, servicio, horas: float, iva: float, descuento: float) -> str:
    """Crea una reserva valida, la procesa y devuelve el resumen."""
    reserva = Reserva(cliente, servicio, horas)
    total = reserva.procesar(porcentaje_iva=iva, porcentaje_descuento=descuento)
    return f"{reserva.describir()} | Costo procesado: {total:,.2f}"


def _crear_y_cancelar_reserva(cliente, servicio, horas: float, motivo: str) -> Reserva:
    """Crea una reserva y la cancela para probar cambios de estado."""
    reserva = Reserva(cliente, servicio, horas)
    reserva.cancelar(motivo)
    return reserva


def _crear_y_confirmar_reserva(cliente, servicio, horas: float) -> Reserva:
    """Crea una reserva y la deja confirmada."""
    reserva = Reserva(cliente, servicio, horas)
    reserva.confirmar()
    return reserva


def _procesar_reserva_con_servicio_no_disponible(cliente) -> str:
    """
    Genera un caso fallido realista usando advertencia, logs y excepciones.

    Se crea una sala valida, luego se marca como no disponible antes de procesar
    la reserva. Asi se demuestra que el sistema controla el error y continua.
    """
    servicio = ReservaSala("Sala de respaldo", 4)
    reserva = Reserva(cliente, servicio, 1)
    registrar_advertencia("La sala de respaldo entra en mantenimiento antes de procesar")
    servicio.marcar_no_disponible("Mantenimiento de ultima hora")
    reserva.procesar()
    return reserva.describir()


def validar_clase_abstracta() -> None:
    """
    Funcion auxiliar para demostrar que EntidadBase no debe instanciarse.

    No se usa en las 15 operaciones porque el modulo de entidades ya queda
    evidenciado con obtener_info_base(), pero se deja documentado por claridad.
    """
    EntidadBase("Entidad generica")


if __name__ == "__main__":
    ejecutar_simulacion_v2()
