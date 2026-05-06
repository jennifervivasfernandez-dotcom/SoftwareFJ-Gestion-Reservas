# ========================================================================
# MÓDULO: main.py
# SEACRIPCIÓN: Punto de entrada principal del sistema FJ.
#              Ejecuta la simulación completa del sistema.
# =========================================================================

import sys
import os

# Agrega la carpeta src al path para encontrar los módulos
sys.path.insert(0, os .path.abspath(
    os.path.join(os.path.dirname(__file__), "src")
))

# Agrega tests al path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "tests")
))

from utils.logger import registrar_info, registrar_error
from simulacion import ejecutar_simulacion


def main():
    """Función principal del sistema Software FJ."""
    try:
        registrar_info("="*50)
        registrar_info("INICIANDO SISTEMA SOFTWARE FJ")
        registrar_info("="*50)

        # Ejecuta la simulación completa
        ejecutar_simulacion()

    except Exception as e:
        registrar_error("Error crítico en el sistema", e)
        print(f"\n❌ Error crítico: {e}")
        sys.exit(1)

    finally:
        registrar_info("Sistema Software FJ finalizado")


if __name__ == "__main__":
    main()        
