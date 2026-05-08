# ==============================================================
# MÓDULO: asesoria.py
# DESCRIPCIÓN: Asesorías especializadas (legal, financiera, etc.).
# ==============================================================

from __future__ import annotations

from typing import Optional

from excepciones.excepciones_custom import ServicioInvalidoError
from servicios.servicio import Servicio


TIPOS_ASESORIA = frozenset(
    {
        "legal",
        "financiera",
        "tecnologia",
        "marketing",
        "contabilidad",
    }
)

# Tarifas base por hora por área de asesoría.
_TARIFAS_ASESORIA: dict[str, float] = {
    "legal": 95_000.0,
    "financiera": 110_000.0,
    "tecnologia": 100_000.0,
    "marketing": 85_000.0,
    "contabilidad": 90_000.0,
}

# Catálogo de rangos permitidos del asesor.
# Si no se indica rango, el sistema asume `senior` (tarifa base).
RANGOS_ASESOR = frozenset({"junior", "senior", "experto"})

# junior: −10 % | senior: tarifa base | experto: +50 %
_MULTIPLICADOR_RANGO: dict[str, float] = {
    "junior": 0.9,
    "senior": 1.0,
    "experto": 1.5,
}


class Asesoria(Servicio):
    """
    Servicio concreto de asesorías.

    Se compone de:
    - **tipo_asesoria**: área (legal, financiera, etc.)
    - **rango_asesor**: nivel del asesor (junior/senior/experto)

    Regla de negocio del rango:
    - junior: 10% menos sobre la tarifa base del tipo
    - senior: tarifa base
    - experto: 50% más sobre la tarifa base del tipo

    Errores:
    - `ServicioInvalidoError` si el tipo o el rango no pertenecen al catálogo permitido.
    """

    def __init__(
        self,
        nombre: str,
        tipo_asesoria: str,
        rango_asesor: Optional[str] = None,
    ):
        super().__init__(nombre)
        self._tipo_asesoria = self._normalizar_tipo(tipo_asesoria)
        self._rango_asesor = self._normalizar_rango(rango_asesor)

    @staticmethod
    def _normalizar_tipo(tipo: str) -> str:
        """
        Normaliza y valida el tipo de asesoría.

        Retorna:
        - `str`: clave normalizada en minúsculas.
        """
        if tipo is None or not str(tipo).strip():
            raise ServicioInvalidoError(
                "El tipo de asesoría es obligatorio.", servicio="Asesoria"
            )
        clave = str(tipo).strip().lower()
        if clave not in TIPOS_ASESORIA:
            raise ServicioInvalidoError(
                f"Tipo de asesoría no permitido: '{tipo}'. "
                f"Válidos: {', '.join(sorted(TIPOS_ASESORIA))}",
                servicio="Asesoria",
            )
        return clave

    @staticmethod
    def _normalizar_rango(rango: Optional[str]) -> str:
        """
        Normaliza y valida el rango del asesor.

        Si el rango no se indica (`None` o vacío), se usa `senior`.

        Retorna:
        - `str`: 'junior' | 'senior' | 'experto'
        """
        if rango is None or not str(rango).strip():
            return "senior"
        clave = str(rango).strip().lower()
        if clave not in RANGOS_ASESOR:
            raise ServicioInvalidoError(
                f"Rango de asesor no permitido: '{rango}'. "
                f"Válidos: {', '.join(sorted(RANGOS_ASESOR))}",
                servicio="Asesoria",
            )
        return clave

    @property
    def tipo_asesoria(self) -> str:
        return self._tipo_asesoria

    @tipo_asesoria.setter
    def tipo_asesoria(self, valor: str) -> None:
        self._tipo_asesoria = self._normalizar_tipo(valor)

    @property
    def rango_asesor(self) -> str:
        return self._rango_asesor

    @rango_asesor.setter
    def rango_asesor(self, valor: Optional[str]) -> None:
        self._rango_asesor = self._normalizar_rango(valor)

    def obtener_tarifa_hora(self) -> float:
        """
        Retorna la tarifa/hora considerando:
        - tarifa base por `tipo_asesoria`
        - multiplicador por `rango_asesor`

        Retorna:
        - `float` (COP/hora)
        """
        base = _TARIFAS_ASESORIA[self._tipo_asesoria]
        factor = _MULTIPLICADOR_RANGO[self._rango_asesor]
        return round(base * factor, 2)

    def validar(self) -> bool:
        """
        Valida el servicio:
        - tipo_asesoria permitido
        - rango_asesor permitido (o default senior)
        - reglas base del servicio (nombre y disponibilidad)

        Retorna:
        - `True`
        """
        self._normalizar_tipo(self._tipo_asesoria)
        self._rango_asesor = self._normalizar_rango(self._rango_asesor)
        return super().validar()

    def describir(self) -> str:
        """
        Devuelve una descripción legible de la asesoría.

        Retorna:
        - `str`
        """
        return (
            f"Asesoría '{self.nombre}' — área: {self._tipo_asesoria} | "
            f"rango: {self._rango_asesor} | "
            f"tarifa/hora: {self.obtener_tarifa_hora():,.0f}"
        )
