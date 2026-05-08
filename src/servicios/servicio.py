# ==============================================================
# MÓDULO: servicio.py
# DESCRIPCIÓN: Clase abstracta base para todos los servicios FJ.
# ==============================================================

from abc import abstractmethod
from typing import Optional

from entidades.entidad_base import EntidadBase
from excepciones.excepciones_custom import (
    CostoInvalidoError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)
from utils.logger import registrar_debug


class Servicio(EntidadBase):
    """
    Clase abstracta base para cualquier servicio ofrecido por Software FJ.

    Responsabilidades:
    - Mantener el estado de disponibilidad del servicio.
    - Proveer una API común para calcular costos por horas con:
      - descuento (%)
      - IVA (%)

    Polimorfismo:
    - Cada servicio concreto implementa `obtener_tarifa_hora()` (su propia regla de tarifa).
    - La lógica de costo se reutiliza para todos los servicios.
    """

    def __init__(self, nombre: str):
        super().__init__(nombre)
        self._disponible = True
        registrar_debug(f"Servicio inicializado: {nombre}")

    @property
    def disponible(self) -> bool:
        return self._disponible

    def marcar_disponible(self) -> None:
        self._disponible = True

    def marcar_no_disponible(self, motivo: Optional[str] = None) -> None:
        """
        Marca el servicio como no disponible.

        Parámetros:
        - `motivo`: texto opcional para registrar en debug.
        """
        self._disponible = False
        if motivo:
            registrar_debug(f"Servicio '{self.nombre}' no disponible: {motivo}")

    @abstractmethod
    def obtener_tarifa_hora(self) -> float:
        """
        Tarifa base por hora del servicio.

        Retorna:
        - `float`: valor monetario por 1 hora.

        Nota:
        - Cada subclase define su tarifa (por capacidad, tipo, rango, etc.).
        """

    def validar(self) -> bool:
        """
        Valida condiciones mínimas del servicio.

        Reglas:
        - nombre no vacío
        - servicio disponible

        Retorna:
        - `True` si está válido.

        Errores:
        - `ServicioInvalidoError` si el nombre es inválido
        - `ServicioNoDisponibleError` si está marcado como no disponible
        """
        if not self.nombre or not str(self.nombre).strip():
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacío.")
        if not self._disponible:
            raise ServicioNoDisponibleError(self.nombre, motivo="Marcado como no disponible")
        return True

    def calcular_costo(
        self,
        horas: float,
        *,
        porcentaje_iva: float = 0.0,
        porcentaje_descuento: float = 0.0,
    ) -> float:
        """
        Calcula el costo total del servicio.

        Fórmula (regla de negocio):
        - subtotal = tarifa_hora * horas
        - neto = subtotal - (subtotal * descuento%)
        - total = neto * (1 + iva%)

        Parámetros:
        - `horas`: duración (debe ser > 0)
        - `porcentaje_iva`: 0..100 (ej. 19)
        - `porcentaje_descuento`: 0..100 (ej. 15)

        Retorna:
        - `float`: total redondeado a 2 decimales.

        Errores:
        - `CostoInvalidoError` si horas/iva/descuento son inválidos.
        - `ServicioNoDisponibleError` si el servicio no está disponible.
        """
        self.validar()
        if horas <= 0:
            raise CostoInvalidoError(horas, motivo="La duración en horas debe ser mayor a cero")
        if porcentaje_iva < 0 or porcentaje_iva > 100:
            raise CostoInvalidoError(
                porcentaje_iva, motivo="El porcentaje de IVA debe estar entre 0 y 100"
            )
        if porcentaje_descuento < 0 or porcentaje_descuento > 100:
            raise CostoInvalidoError(
                porcentaje_descuento,
                motivo="El porcentaje de descuento debe estar entre 0 y 100",
            )
        subtotal = self.obtener_tarifa_hora() * horas
        monto_desc = subtotal * (porcentaje_descuento / 100.0)
        neto = subtotal - monto_desc
        if neto < 0:
            raise CostoInvalidoError(neto, motivo="El neto tras descuento no puede ser negativo")
        total = neto * (1.0 + porcentaje_iva / 100.0)
        return round(total, 2)

    def calcular_costo_sin_impuesto(self, horas: float) -> float:
        """
        Atajo para el caso más común: costo solo con horas (sin IVA ni descuento).

        Retorna:
        - `float`
        """
        return self.calcular_costo(horas, porcentaje_iva=0.0, porcentaje_descuento=0.0)
