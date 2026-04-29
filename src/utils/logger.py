# ==============================================================
# MÓDULO: logger.py
# DESCRIPCIÓN: Sistema de registro de eventos y errores del 
#              sistema Software FJ. Guarda todos los eventos
#              en un archivo de texto con fecha y hora.
# ==============================================================

import logging    # Módulo de Python para manejo de logs
import os         # Para manejo de rutas y carpetas
from datetime import datetime   # Para obtener fecha y hora actual



# --------------------------------------------------------------
# CONFIGURACIÓN DE RUTAS
# Calcula automáticamente dónde guardar el archivo de logs
# sin importar desde qué carpeta se ejecute el programa.
# --------------------------------------------------------------

# Obtiene la ruta de la carpeta raíz del proyecto
RUTA_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Construye la ruta completa a la carpeta logs/
RUTA_LOGS = os.path.join(RUTA_RAIZ, "logs")

# Crea la carpeta logs/ si no existe todavía
os.makedirs(RUTA_LOGS, exist_ok=True)

# Nombre del archivo de log con la fecha actual
# Ejemplo: sistema_fj_2026_04_28.log
NOMBRE_ARCHIVO = f"sistema_fj_{datetime.now().strftime('%Y-%m-%d')}.log"

# Ruta completa del archivo de log
RUTA_ARCHIVO_LOG = os.path.join(RUTA_LOGS, NOMBRE_ARCHIVO)


# --------------------------------------------------------------
# CONFIGURACIÓN DEL LOGGER
# Define el formato y destino de los mensajes de log
# --------------------------------------------------------------

# Formato de cada línea del log:
# 2026-04-28 10:30:15 | INFO | cliente.py | Cliente creado OK 
FORMATO_LOG = "%(asctime)s | %(levelname)s | %(module)s | %(message)s"
FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"

# Crea el logger principal del sistema
logger = logging.getLogger("SistemaFJ")

# Establecer el nivel mínimo de mensajes a registrar
# DEBUG = registra absolutamente todo
logger.setLever(logging.DEBUG)

# Evita duplicar mensajes si el logger ya fue configurado
if not logger.handlers:

    # --- HANDLER 1: Guarda los logs en archivo ---
    # Escribe cada mensaje en el archivo .log
    manejador_archivo = logging.FileHandler(
        RUTA_ARCHIVO_LOG,
        encoding="utf-8"   # Para soportar tildes y ñ
    )
    manejador_archivo.satLevel(logging.DEBUG)
    manejador_archivo.setFormatter(
        logging.Formatter(FORMATO_LOG, FORMATO_FECHA)
    )

    # --- HANDLER 2: Muestra los logs en la terminal ---
    # Imprime cada mensaje en la consola mientras se ejecuta
    manejador_consola = logging.StreamHandler()
    manejador_consola.setLevel(logging.INFO)
    manejador_consola.setFormatter(
        logging.Formatter(FORMATO_LOG, FORMATO_FECHA)

    )

    # Agrega ambos manejadores al logger
    logger.addHandler(manejador_archivo)
    logger.addHandler(manejador_consola)


# --------------------------------------------------------------
# FUNCIONES DE REGISTRO
# Funciones simples para usar el logger desde cualquier módulo
# --------------------------------------------------------------

def registrar_ifo(mensaje):
    """Registra un evento informativo normal.
    Ejemplo: cliente creado, reserva confirmada."""
    logger.info(mensaje)


def registrar_advertencia(mensaje):
    """Registra una advertencia - algo inusual pero que
    no detiene el problema.
    Ejemplo: intento de duplicar un cliente."""
    logger.warning(mensaje)


def registrar_error(mensaje, excepcion=None):
    """Registra un error - algo mal pero
    el programa puede continuar.
    Si se pasa la excepción, también registra el detalle."""
    if excepcion:
        logger.error(f"{mensaje} | Detalle: {excepcion}")
    else:
        logger.error(mensaje)


def registrar_critico(mensaje, excepción=None):
    """Registra un error crítico - algo muy grave que
    puede comprometer el sistema."""
    if excepción:
        logger.critical(f"{mensaje} | Detalle: {excepción}")
    else:
        logger.critical(mensaje)


def registrar_debug(mensaje):
    """Registra información de depuración datallada.
    Solo visible en el archivo, no en la consola."""
    logger.debug(mensaje)


    