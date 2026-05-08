# ==============================================================
# MÓDULO: cliente.py
# DESCRIPCIÓN: Gestión de clientes con validaciones estrictas.
# ==============================================================

import re

from entidades.entidad_base import EntidadBase
from excepciones.excepciones_custom import ClienteInvalidoError
from utils.logger import registrar_info


_CLASS_SOLO_DIGITOS = re.compile(r"^\d+$")


class Cliente(EntidadBase):
    """
    Representa un cliente del sistema.

    Responsabilidades:
    - **Encapsular** datos de cliente (nombre, email, teléfono, documento).
    - **Validar estrictamente** esos datos al crear y al modificar.

    Reglas de validación (según rúbrica):
    - **email**: obligatorio y debe contener '@'
    - **teléfono**: solo dígitos, longitud entre 7 y 15
    - **documento**: solo números (sin letras)

    Errores:
    - Lanza `ClienteInvalidoError` indicando el `campo` inválido.
    """

    def __init__(self, nombre: str, email: str, telefono: str, documento: str):
        super().__init__(nombre)
        # Se normaliza y valida al construir para evitar instancias "a medias".
        self._email = self._normalizar_y_validar_email(email)
        self._telefono = self._normalizar_y_validar_telefono(telefono)
        self._documento = self._normalizar_y_validar_documento(documento)
        registrar_info(f"Cliente registrado: {self._nombre} (id {self._id[:8]}…)")

    @staticmethod
    def _normalizar_y_validar_email(email: str) -> str:
        """
        Normaliza/valida email y retorna el valor limpio.

        Retorna:
        - `str`: email sin espacios laterales.
        """
        if email is None or not str(email).strip():
            raise ClienteInvalidoError("El email no puede estar vacío.", campo="email")
        limpio = str(email).strip()
        if "@" not in limpio:
            raise ClienteInvalidoError("El email debe contener el símbolo '@'.", campo="email")
        return limpio

    @staticmethod
    def _normalizar_y_validar_telefono(telefono: str) -> str:
        """
        Normaliza/valida teléfono y retorna el valor limpio.

        Reglas:
        - Solo dígitos
        - Longitud 7..15

        Retorna:
        - `str`: teléfono ya normalizado (sin espacios).
        """
        if telefono is None or not str(telefono).strip():
            raise ClienteInvalidoError("El teléfono no puede estar vacío.", campo="telefono")
        limpio = str(telefono).strip().replace(" ", "")
        if not re.fullmatch(r"\d{7,15}", limpio):
            if not limpio.isdigit():
                raise ClienteInvalidoError(
                    "El teléfono debe consistir solo en dígitos.", campo="telefono"
                )
            raise ClienteInvalidoError(
                "El teléfono debe tener entre 7 y 15 dígitos.", campo="telefono"
            )
        return limpio

    @staticmethod
    def _normalizar_y_validar_documento(documento: str) -> str:
        """
        Normaliza/valida documento y retorna el valor limpio.

        Retorna:
        - `str`: documento sin espacios.
        """
        if documento is None or not str(documento).strip():
            raise ClienteInvalidoError("El documento no puede estar vacío.", campo="documento")
        limpio = re.sub(r"\s", "", str(documento))
        if not _CLASS_SOLO_DIGITOS.match(limpio):
            raise ClienteInvalidoError(
                "El documento debe consistir solo en números.", campo="documento"
            )
        return limpio

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        self._email = self._normalizar_y_validar_email(valor)

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        self._telefono = self._normalizar_y_validar_telefono(valor)

    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str) -> None:
        self._documento = self._normalizar_y_validar_documento(valor)

    def validar(self) -> bool:
        """
        Re-ejecuta todas las validaciones actuales del objeto.

        Retorna:
        - `True` si el objeto está consistente.

        Nota:
        - Si hay un dato inválido, se lanza `ClienteInvalidoError`.
        """
        self._normalizar_y_validar_email(self._email)
        self._normalizar_y_validar_telefono(self._telefono)
        self._normalizar_y_validar_documento(self._documento)
        return True

    def describir(self) -> str:
        """
        Devuelve una descripción legible del cliente (para UI/impresión/logs).

        Retorna:
        - `str`
        """
        return (
            f"Cliente: {self._nombre} | email: {self._email} | "
            f"tel: {self._telefono} | doc: {self._documento}"
        )
