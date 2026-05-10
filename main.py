# ========================================================================
# MODULO: main.py
# DESCRIPCION: Punto de entrada principal del sistema Software FJ.
#              Ejecuta las pruebas base y la simulacion de reservas.
# ========================================================================

import os
import sys


# Agrega la carpeta src al path para encontrar los modulos del sistema.
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "src")
))

# Agrega tests al path para usar las simulaciones academicas.
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "tests")
))

from simulacion import ejecutar_simulacion
from simulacion_reservas import ejecutar_simulacion_reservas
from utils.logger import registrar_error, registrar_info


def main():
    """Funcion principal del sistema Software FJ."""
    try:
        registrar_info("=" * 50)
        registrar_info("INICIANDO SISTEMA SOFTWARE FJ")
        registrar_info("=" * 50)

        # Primero se ejecutan las pruebas que ya validan clientes y servicios.
        ejecutar_simulacion()

        # Luego se ejecuta la parte de reservas y operaciones completas.
        ejecutar_simulacion_reservas()

    except Exception as error:
        registrar_error("Error critico en el sistema", error)
        print(f"\nError critico: {error}")
        sys.exit(1)

    finally:
        registrar_info("Sistema Software FJ finalizado")


if __name__ == "__main__":
    main()
