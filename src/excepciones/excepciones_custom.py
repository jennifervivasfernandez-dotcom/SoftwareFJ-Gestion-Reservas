# =============================================================
# MÓDULO: excepciones_custom.py
# DESCRIPCIÓN: Define todas las excepciones personalizadas del 
#              sistemaSoftware FJ. Cada excepcion representa 
#              un tipo de error específico del negocio. 
# =============================================================



# -------------------------------------------------------------
# CLASE BASE: ErrorSistemaFJ
# Todas las excepciones del sistema heredaro de esta clase.
# Esto permite capturar cualquier error del sistema con un 
# solo bloque except ErrorSistemaFJ.
# -------------------------------------------------------------
class ErrorSistemaFJ (Exception):
    """Excepción base para todos los errores del sistema FJ."""


    def __init__(self, mensaje, codigo=None):
        # Llamamos al constructor de Excepcion (clase padre)
        super().__init__(mensaje)
        self.mensaje = mensaje
        # Código opcional para identificar el tipo de error
        self.codigo = codigo

    def __str__(self):
        # Define cómo se muestra el error al imprimirlo
        if self.codigo:
            return f"[Error {self.codigo}] {self.mensaje}"
        return f"[Error] {self.mensaje}"    
    
    
# -------------------------------------------------------------
# EXCEPCIONES DE CLIENTE
# Se lanza cuando hay problemas con los datos de un cliente
# -------------------------------------------------------------
class ClienteInvalidoError (ErrorSistemaFJ):
    """ Se lanza cuando los datos de un cliente son inválidos.
     Ejemplo: nombre vacío, email sin @, teléfono con letras. """
    
    def __init__(self, mensaje, campo=None):
        # Llamamos al constructor de la clase padre ErrorSistemaFJ
        super().__init__(mensaje, codigo="CLI-001")
        # Campo indica qué dato específico es inválido 
        self.campo = campo

    def __str__(self):
        if self.campo:
            return f"[Error CLI-001] campo '{self.campo}': {self.mensaje}"
        return f"[Error CLI-001] {self.mensaje}"


class ClienteNoEncontradoError (ErrorSistemaFJ):
    """ Se lanza cuando se busca un cliente que no existe en el sistema. """

    def __init__(self, id_cliente):
        mensaje = f"No se encontró el cliente con ID: {id_cliente}"
        super().__init__(mensaje, codigo="CLI-002")
        self.id_cliente = id_cliente


# -------------------------------------------------------------
# EXCEPCIONES DE SERVICIO
# Se lanza cuando hay problemas con los servicios ofrecidos
# -------------------------------------------------------------
class ServicioInvalidoError (ErrorSistemaFJ):
    """ Se lanza cuando los parámetros de un servicio son
    incorrectos o están incompletos."""

    def __init__(self, mensaje, servicio=None):
        super().__init__(mensaje, codigo="SRV-001")
        self.servicio = servicio

    def __str__(self):
        if self. servicio:
            return f"[Error SRV-001] '{self.mensaje}' : {self.mensaje}"
        return f"[Error SVR-001] {self.mensaje}"


class ServicioNoDisponibleError (ErrorSistemaFJ):
    """ Se lanza cuando un servicio no está disponible en 
    la fecha o condiciones solicitadas. """

    def __init__(self, nombre_servicio, motivo=None):
        mensaje = f"El servicio '{nombre_servicio}' no estás disponible"
        if motivo:
            mensaje += f". Motivo:{motivo}"
            super().__init__(mensaje, codigo="SRV-002")
            self.nombre_servicio = nombre_servicio


class CostoInvalidoError (ErrorSistemaFJ):
    """ Se lanza cuando el cálculo de un costo resulta
    inválido (negativo, cero, o inconsistente)."""

    def __init__(self, valor, motivo=None):
        mensaje = f"Costo inválido: {valor}"
        if motivo:
            mensaje += f".{motivo}"
        super().__init__(mensaje, codigo="SRV-003")
        self.valor = valor          


# ----------------------------------------------------------------              
# EXCEPCIONES DE RESERVA
# Se lanza cuando hay problemas al crear o gestionar reservas 
# ----------------------------------------------------------------
class ReservaInvalidaError (ErrorSistemaFJ):
    """ Se lanza cuando los datos de una reserva son inválidos.
    Ejemplo: duración negativa, fecha pasada, cliente nulo."""

    def __init__(self, mensaje, id_reserva=None):
        super().__init__(mensaje, codigo="RES-001")
        self.id_reserva = id_reserva

    def __str__(self):
        if self.id_reserva:
            return f"[Error RES-001] Reserva '{self.id_reserva}': {self.mensaje}"
        return f"[Error RES-001] {self.mensaje}"


class ReservaNoEncontradaError (ErrorSistemaFJ):
    """ Se lanza cuando se busca una reserva que no existe."""

    def __init__(self, id_reserva):
        mensaje = f"No se encontró la reserva con ID: {id_reserva}"
        super().__init__(mensaje, codigo="RES-002")
        self.id_reserva = id_reserva


class ReservaCanceladaError (ErrorSistemaFJ):
    """ Se lanza cuando se intenta operar sobre una reserva 
    que ya fue cancelada previamente."""

    def __init__(self, id_reserva):
        mensaje = f"La reserva '{id_reserva}' ya fue cancelada"
        super().__init__(mensaje, codigo="RES-003")
        self.id_reserva = id_reserva


class ReservaYaConfirmadaError (ErrorSistemaFJ):
    """ Se lanza cuando se intenta confirmar una reserva que 
    ya estaba confirmada. """ 

    def __init__(self, id_reserva):
        mensaje = f"La reserva '{id_reserva}' ya estaba confirmada"
        super().__init__(mensaje, codigo="RES-004")
        self.id_reserva = id_reserva



             


             