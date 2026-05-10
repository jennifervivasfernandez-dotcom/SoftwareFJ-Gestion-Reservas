# ==============================================================
# MODULO: reserva.py
# DESCRIPCION: Gestion de reservas del sistema Software FJ.
# ==============================================================

from datetime import datetime

from clientes.cliente import Cliente
from entidades.entidad_base import EntidadBase
from excepciones.excepciones_custom import (
    ReservaCanceladaError,
    ReservaInvalidaError,
    ReservaYaConfirmadaError,
    ServicioNoDisponibleError,
)
from servicios.servicio import Servicio
from utils.logger import registrar_error, registrar_info


ESTADO_PENDIENTE = "PENDIENTE"
ESTADO_CONFIRMADA = "CONFIRMADA"
ESTADO_CANCELADA = "CANCELADA"
ESTADO_PROCESADA = "PROCESADA"


class Reserva(EntidadBase):
    """
    Representa una reserva hecha por un cliente sobre un servicio.

    Esta clase integra tres partes importantes del proyecto:
    - Cliente: quien solicita la reserva.
    - Servicio: sala, equipo o asesoria que se va a usar.
    - Duracion: cantidad de horas necesarias para calcular el costo.

    La reserva inicia en estado PENDIENTE y luego puede confirmarse,
    cancelarse o procesarse. Cada operacion registra informacion en logs.
    """

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion_horas: float):
        super().__init__(f"Reserva para {servicio.nombre if servicio else 'servicio no definido'}")
        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._estado = ESTADO_PENDIENTE
        self._costo_total = 0.0
        self.validar()
        registrar_info(f"Reserva creada: {self.id[:8]} para {self._cliente.nombre}")

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def duracion_horas(self) -> float:
        return self._duracion_horas

    @duracion_horas.setter
    def duracion_horas(self, valor: float) -> None:
        self._duracion_horas = valor
        self.validar()

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def validar(self) -> bool:
        """
        Valida que la reserva tenga datos completos y coherentes.

        Se valida el tipo de cliente, el tipo de servicio, la duracion y
        tambien se llama la validacion propia del servicio.
        """
        if not isinstance(self._cliente, Cliente):
            raise ReservaInvalidaError("La reserva debe tener un cliente valido.", self.id)
        if not isinstance(self._servicio, Servicio):
            raise ReservaInvalidaError("La reserva debe tener un servicio valido.", self.id)
        if not isinstance(self._duracion_horas, (int, float)):
            raise ReservaInvalidaError("La duracion debe ser un numero.", self.id)
        if self._duracion_horas <= 0:
            raise ReservaInvalidaError("La duracion debe ser mayor a cero.", self.id)

        self._cliente.validar()
        self._servicio.validar()
        return True

    def confirmar(self) -> bool:
        """
        Confirma una reserva pendiente.

        Si la reserva ya esta confirmada o cancelada, se lanza una excepcion
        personalizada para que el sistema pueda manejar el caso sin detenerse.
        """
        if self._estado == ESTADO_CONFIRMADA:
            raise ReservaYaConfirmadaError(self.id)
        if self._estado == ESTADO_CANCELADA:
            raise ReservaCanceladaError(self.id)

        self.validar()
        self._estado = ESTADO_CONFIRMADA
        registrar_info(f"Reserva confirmada: {self.id[:8]}")
        return True

    def cancelar(self, motivo: str = "Cancelacion solicitada") -> bool:
        """
        Cancela una reserva que aun no ha sido procesada.

        El motivo es opcional, pero ayuda a que el log sea mas claro.
        """
        if self._estado == ESTADO_CANCELADA:
            raise ReservaCanceladaError(self.id)
        if self._estado == ESTADO_PROCESADA:
            raise ReservaInvalidaError("No se puede cancelar una reserva procesada.", self.id)

        self._estado = ESTADO_CANCELADA
        registrar_info(f"Reserva cancelada: {self.id[:8]} | Motivo: {motivo}")
        return True

    def calcular_costo(self, porcentaje_iva: float = 19.0, porcentaje_descuento: float = 0.0) -> float:
        """
        Calcula el costo de la reserva usando el polimorfismo del servicio.

        Cada servicio sabe calcular su tarifa por hora, por eso aqui solo se
        delega el calculo y se guarda el resultado en la reserva.
        """
        self.validar()
        self._costo_total = self._servicio.calcular_costo(
            self._duracion_horas,
            porcentaje_iva=porcentaje_iva,
            porcentaje_descuento=porcentaje_descuento,
        )
        return self._costo_total

    def procesar(self, porcentaje_iva: float = 19.0, porcentaje_descuento: float = 0.0) -> float:
        """
        Procesa la reserva completa: confirma si hace falta y calcula costo.

        Aqui se usa try/except/else/finally y encadenamiento de excepciones.
        Si algo falla al procesar, se registra el error y se lanza una
        ReservaInvalidaError conservando la causa original con "from".
        """
        try:
            if self._estado == ESTADO_CANCELADA:
                raise ReservaCanceladaError(self.id)
            if self._estado == ESTADO_PROCESADA:
                raise ReservaInvalidaError("La reserva ya fue procesada.", self.id)
            if self._estado == ESTADO_PENDIENTE:
                self.confirmar()

            total = self.calcular_costo(porcentaje_iva, porcentaje_descuento)

        except ServicioNoDisponibleError as error:
            registrar_error("No fue posible procesar la reserva por servicio no disponible", error)
            raise ReservaInvalidaError(
                "La reserva no pudo procesarse porque el servicio no esta disponible.",
                self.id,
            ) from error
        except (ReservaCanceladaError, ReservaYaConfirmadaError, ReservaInvalidaError):
            raise
        except Exception as error:
            registrar_error("Error inesperado al procesar reserva", error)
            raise ReservaInvalidaError("Error inesperado durante el procesamiento.", self.id) from error
        else:
            self._estado = ESTADO_PROCESADA
            registrar_info(f"Reserva procesada: {self.id[:8]} | Total: {total:,.2f}")
            return total
        finally:
            registrar_info(
                f"Fin de intento de procesamiento reserva {self.id[:8]} | Estado: {self._estado}"
            )

    def describir(self) -> str:
        """
        Devuelve una descripcion corta y legible de la reserva.
        """
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"Reserva {self.id[:8]} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Horas: {self._duracion_horas} | "
            f"Estado: {self._estado} | Total: {self._costo_total:,.2f} | Consulta: {fecha}"
        )

    def __str__(self) -> str:
        """
        Muestra la reserva de forma simple cuando se imprime en consola.
        """
        return (
            f"Reserva {self.id[:8]} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Estado: {self._estado}"
        )
