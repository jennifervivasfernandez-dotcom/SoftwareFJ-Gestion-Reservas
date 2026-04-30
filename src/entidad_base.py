# ==============================================================
# MÓDULO: entidad_base.py
# DESCRIPCIÓN: Define la clase abstracta base del sistema FJ.
#              Todas las entidades de sistema (Cliente, Servicio, Reserva) heredan de esta clase.
#              Una clase abtracta NO puede instanciarse directamente, solo sirve como plantilla.
# ==============================================================


from abc import ABC, abstractmethod   # ABC = Abstract Base Clase
from datetime import datetime         # Para fecha de creación
import uuid                           # Para generar IDs únicos


# -------------------------------------------------------------
# CLASE ABSTRACTA: EntidadBase
# Define atributos y métodos comunes a todas las entidades
# -------------------------------------------------------------
class EntidadBase(ABC):
    """Clase abstracta base para todas las entidades del 
    sistema Software FJ.
    Proporciona:
    - ID único automático para cada entidad
    - Fecha de creación automática
    - Métodos adstractos que TODAS las clases hijas 
      estaán obligadas a implementar
    """

def __init__(self, nombre):
    # Valida que el nombre no esté vacío
    if not nombre or not nombre.strip():
        raise ValueError("El nombre de la entidad no puede estar vacío")

    # Genera un ID único autométicamente
    # Ejemplo: "a3f8c2d1-4b5e-6f7a-8b9c-0d1e2f3a4b5c"
    self.__id = str (uuid.uuid4())  

    # Guarda el nombre limpio (sin espacios extra)
    self.__nombre = nombre.strip()

    # Registra la fecha y hora exacta de creación
    self.__fecha_creación = datetime.now()

    # Estado activo/inactivo de la entidad
    self.__activo = True


# -----------------------------------------------------------
# PROPIEDADES (getters y settert con encapsulación)
# El doble guion __ hace que los atributos sean privados
# Las @property permiten leerlos desde afuera de forma
# controlada, sin modificarlos directamente
# -----------------------------------------------------------

@property
def id(self):
    """Retorna el ID único de la entidad (solo lectura)."""
    return self.__id

@property 
def nombre(self):
    """Retorna el nombre de la entidad."""
    return self.__nombre

@nombre.satter
def nombre(self, nuevo_nombre):
    """Permite cambiar el nombre con validación."""
    if not nuevo_nombre or not nuevo_nombre.strip():
        raise ValueError("El nombre no puede estar vacío")
    self.__nombre = nuevo_nombre.strip()

@property
def fecha_creacion(self):
    """Retorna la fecha de creación (solo lectura)."""
    return self.__fecha_creacion

@property
def activo(self):
    """Retorna si la entidad está activa o no."""
    return self.__activo

@activo.setter
def activo(self, valor):
    """Permite activar o desactivar la entidad."""
    if not isinstance(valor, bool):
        raise ValueError("El estado activo debe ser True o False")
    self.__activo = valor


# -------------------------------------------------------------------------
# MÉTODOS ABSTRACTOS
# Todas las clases hijas DEBEN implementar estos métodos
# Si no los implementan, Python lanzará un error
# -------------------------------------------------------------------------

@abstractmethod
def describir(self):
    """Retorna una descripción completa de la entidad.
    sean correctos y completos.
    Retorna True si es válida, lanza excepción si no."""
    
    pass

# -------------------------------------------------------------------------
# MÉTODOS CONCRETOS
# Métodos que ya tienen implementación y todas las 
# clases hijas heredan tal cual
# -------------------------------------------------------------------------

def desactivar(self):
    """Desactiva la entidad en el sistema."""
    self.__activo = False

def activar(self):
    """Activa la entidad en el sistema."""
    self.__activo = True

def obtener_info_base(self):
    """Retrona un diccionario con la información
    básica común de cualquier entidad."""
    return{
        "id": self.__id,
        "nombre": self.__nombre,
        "fecha_creación": self.__fecha_creacion.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "activo": self.__activo
    }        

def __str__(self):
    """Define cómo se muestra la entidad al imprimirla."""
    estado = "Activo" if self.__activo else "Inactivo"
    return (f"[{self.__class__.__name__}]"
            f"ID: {self.__id[:8]}... | "
            f"Nombre: {self.__nombre} | "
            f"Estado: {estado}")

def __repr__(self):
    """Representación técnica de la entidad."""
    return (f"{self.__class__.__name__}("
            f"id='{self.__id[:8]}...',"
            f"nombre='{self.__nombre}')")

