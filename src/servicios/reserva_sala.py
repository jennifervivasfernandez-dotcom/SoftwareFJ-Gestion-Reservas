# ==============================================================
# MÓDULO: reserva_sala.py
# DESCRIPCIÓN: Servicio de reserva de sala con tarifa según aforo.
# ==============================================================

from excepciones.excepciones_custom import ServicioInvalidoError
from servicios.servicio import Servicio


class ReservaSala(Servicio):
    """
    Tarifas por hora (COP):
    - hasta 5 personas: 50_000
    - hasta 10 personas: 80_000
    - más de 10: 120_000

    Responsabilidades:
    - Encapsular la **capacidad** (aforo) de la sala.
    - Determinar la tarifa/hora a partir del aforo.

    Errores:
    - `ServicioInvalidoError` si la capacidad es inválida.
    """

    def __init__(self, nombre: str, capacidad: int):
        super().__init__(nombre)
        self._capacidad = capacidad
        self._validar_capacidad()

    def _validar_capacidad(self) -> None:
        """
        Valida la capacidad de la sala.

        Regla:
        - Entero >= 1
        """
        if not isinstance(self._capacidad, int) or self._capacidad < 1:
            raise ServicioInvalidoError(
                "La capacidad debe ser un entero mayor o igual a 1.",
                servicio="ReservaSala",
            )

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor: int) -> None:
        self._capacidad = valor
        self._validar_capacidad()

    def obtener_tarifa_hora(self) -> float:
        """
        Retorna la tarifa/hora según el aforo.

        Retorna:
        - `float` (COP/hora)
        """
        c = self._capacidad
        if c <= 5:
            return 50_000.0
        if c <= 10:
            return 80_000.0
        return 120_000.0

    def validar(self) -> bool:
        """
        valida la sala (capacidad + reglas base del servicio).

        Retorna:
        - `True` si está válido.
        """
        self._validar_capacidad()
        return super().validar()

    def describir(self) -> str:
        """
        Devuelve descripción legible del servicio de sala.

        Retorna:
        - `str`
        """
        return (
            f"Reserva de sala '{self.nombre}' — capacidad: {self._capacidad} pers. | "
            f"tarifa/hora: {self.obtener_tarifa_hora():,.0f}"
        )
