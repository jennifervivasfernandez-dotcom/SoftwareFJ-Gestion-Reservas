# ==============================================================
# MÓDULO: alquiler_equipo.py
# DESCRIPCIÓN: Alquiler de equipos (laptop, proyector, cámara, etc.).
# ==============================================================

from excepciones.excepciones_custom import ServicioInvalidoError
from servicios.servicio import Servicio


TIPOS_EQUIPO = frozenset(
    {
        "laptop",
        "proyector",
        "camara",
        "impresora",
        "tablet",
    }
)

# Tarifas por hora (COP) por tipo de equipo.
# Esta tabla es la "fuente de verdad" para `obtener_tarifa_hora()`.
_TARIFAS_EQUIPO: dict[str, float] = {
    "laptop": 35_000.0,
    "proyector": 25_000.0,
    "camara": 45_000.0,
    "impresora": 18_000.0,
    "tablet": 30_000.0,
}


class AlquilerEquipo(Servicio):
    """
    Servicio concreto para alquiler de equipos.

    Responsabilidades:
    - Validar que el `tipo_equipo` esté dentro de `TIPOS_EQUIPO`.
    - Proveer la tarifa/hora en función del tipo de equipo.

    Errores:
    - `ServicioInvalidoError` si el tipo es vacío o no pertenece al catálogo.
    """

    def __init__(self, nombre: str, tipo_equipo: str):
        super().__init__(nombre)
        self._tipo_equipo = self._normalizar_tipo(tipo_equipo)

    @staticmethod
    def _normalizar_tipo(tipo: str) -> str:
        """
        Normaliza/valida el tipo de equipo.

        Retorna:
        - `str`: clave normalizada en minúsculas.
        """
        if tipo is None or not str(tipo).strip():
            raise ServicioInvalidoError(
                "El tipo de equipo es obligatorio.", servicio="AlquilerEquipo"
            )
        clave = str(tipo).strip().lower()
        if clave not in TIPOS_EQUIPO:
            raise ServicioInvalidoError(
                f"Tipo de equipo no permitido: '{tipo}'. "
                f"Válidos: {', '.join(sorted(TIPOS_EQUIPO))}",
                servicio="AlquilerEquipo",
            )
        return clave

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, valor: str) -> None:
        self._tipo_equipo = self._normalizar_tipo(valor)

    def obtener_tarifa_hora(self) -> float:
        """
        Retorna la tarifa por hora del tipo de equipo seleccionado.

        Retorna:
        - `float` (COP/hora)
        """
        return _TARIFAS_EQUIPO[self._tipo_equipo]

    def validar(self) -> bool:
        """
        Valida el servicio:
        - tipo de equipo válido
        - reglas base del servicio (nombre y disponibilidad)

        Retorna:
        - `True`
        """
        self._normalizar_tipo(self._tipo_equipo)
        return super().validar()

    def describir(self) -> str:
        """
        Devuelve descripción legible del alquiler.

        Retorna:
        - `str`
        """
        return (
            f"Alquiler '{self.nombre}' — equipo: {self._tipo_equipo} | "
            f"tarifa/hora: {self.obtener_tarifa_hora():,.0f}"
        )
