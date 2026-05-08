# ==============================================================
# MÓDULO: simulacion.py
# DESCRIPCIÓN: Pruebas unitarias para cliente y servicios (sin las 10 operaciones de demo).
# ==============================================================

import unittest

from clientes.cliente import Cliente
from excepciones.excepciones_custom import (
    ClienteInvalidoError,
    CostoInvalidoError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)
from servicios.asesoria import Asesoria, TIPOS_ASESORIA
from servicios.alquiler_equipo import AlquilerEquipo, TIPOS_EQUIPO
from servicios.reserva_sala import ReservaSala
from servicios.servicio import Servicio
from utils.logger import registrar_error

"""
Este archivo contiene pruebas unitarias (unittest) para validar:
- Cliente (`Cliente`)
- Servicios (`ReservaSala`, `AlquilerEquipo`, `Asesoria`)
- Cálculo de costos y manejo de errores del dominio (excepciones custom)

Importante:
- Estas pruebas **no** son la "simulación de 10 operaciones" de la rúbrica.
- Su objetivo es comprobar que los módulos implementados:
  - validan correctamente entradas válidas/ inválidas
  - lanzan excepciones personalizadas cuando corresponde
  - calculan tarifas/costos según reglas de negocio
"""

def _loggear_excepcion_prueba(contexto: str, exc: Exception) -> None:
    """
    Helper para la rúbrica: si en una prueba provocamos un error "a propósito",
    lo registramos en el log y aun así seguimos con la ejecución.
    """
    registrar_error(f"Prueba (caso inválido) detectó error en: {contexto}", exc)


# Test de Jaime
class TestCliente(unittest.TestCase):
    def test_cliente_valido(self):
        """Caso feliz: construye un cliente válido y verifica getters/validar/describir."""
        c = Cliente(
            "Ana López",
            "ana@softwarefj.com",
            "3001234567",
            "1098765432",
        )
        self.assertIn("@", c.email)
        self.assertTrue(c.validar())
        self.assertIn("Ana", c.describir())

    def test_email_sin_arroba(self):
        """Caso inválido: email sin '@' debe lanzar `ClienteInvalidoError` con campo=email."""
        try:
            Cliente("Bob", "bobinvalido.com", "3001234567", "123")
            self.fail("Se esperaba ClienteInvalidoError")
        except ClienteInvalidoError as e:
            _loggear_excepcion_prueba("Cliente.email sin '@'", e)
            self.assertEqual(e.campo, "email")

    def test_telefono_con_letras(self):
        """Caso inválido: teléfono con letras debe lanzar `ClienteInvalidoError` con campo=telefono."""
        try:
            Cliente("Carla", "c@mail.com", "300abc1234", "12345678")
            self.fail("Se esperaba ClienteInvalidoError")
        except ClienteInvalidoError as e:
            _loggear_excepcion_prueba("Cliente.telefono con letras", e)
            self.assertEqual(e.campo, "telefono")

    def test_documento_no_numerico(self):
        """Caso inválido: documento no numérico debe lanzar `ClienteInvalidoError` con campo=documento."""
        try:
            Cliente("Dana", "d@mail.com", "3001234567", "ABC123")
            self.fail("Se esperaba ClienteInvalidoError")
        except ClienteInvalidoError as e:
            _loggear_excepcion_prueba("Cliente.documento no numérico", e)
            self.assertEqual(e.campo, "documento")


class TestReservaSala(unittest.TestCase):
    def test_tarifas_por_capacidad(self):
        """Verifica la regla de negocio de tarifas por capacidad (5/10/11)."""
        self.assertEqual(ReservaSala("Sala A", 5).obtener_tarifa_hora(), 50_000.0)
        self.assertEqual(ReservaSala("Sala B", 10).obtener_tarifa_hora(), 80_000.0)
        self.assertEqual(ReservaSala("Sala C", 11).obtener_tarifa_hora(), 120_000.0)

    def test_capacidad_invalida(self):
        """Capacidad 0 debe lanzar `ServicioInvalidoError`."""
        try:
            ReservaSala("Sala X", 0)
            self.fail("Se esperaba ServicioInvalidoError")
        except ServicioInvalidoError as e:
            _loggear_excepcion_prueba("ReservaSala.capacidad inválida", e)


class TestAlquilerEquipo(unittest.TestCase):
    def test_tipos_permitidos(self):
        """Itera el catálogo `TIPOS_EQUIPO` y comprueba que cada tipo funciona con tarifa > 0."""
        for tipo in TIPOS_EQUIPO:
            eq = AlquilerEquipo(f"Equipo {tipo}", tipo)
            self.assertEqual(eq.tipo_equipo, tipo)
            self.assertGreater(eq.obtener_tarifa_hora(), 0)

    def test_tipo_invalido(self):
        """Tipo de equipo fuera del catálogo debe lanzar `ServicioInvalidoError`."""
        try:
            AlquilerEquipo("X", "tractor")
            self.fail("Se esperaba ServicioInvalidoError")
        except ServicioInvalidoError as e:
            _loggear_excepcion_prueba("AlquilerEquipo.tipo inválido", e)


class TestAsesoria(unittest.TestCase):
    def test_tipos_permitidos(self):
        """Para cada tipo permitido, el rango por defecto debe ser senior y la tarifa debe ser > 0."""
        for tipo in TIPOS_ASESORIA:
            a = Asesoria(f"Asesoría {tipo}", tipo)
            self.assertEqual(a.tipo_asesoria, tipo)
            self.assertEqual(a.rango_asesor, "senior")
            self.assertGreater(a.obtener_tarifa_hora(), 0)

    def test_rango_predeterminado_senior(self):
        """Si el rango viene None o vacío, el sistema debe usar 'senior' (tarifa base)."""
        a = Asesoria("Consulta", "legal", None)
        self.assertEqual(a.rango_asesor, "senior")
        self.assertEqual(a.obtener_tarifa_hora(), 95_000.0)
        b = Asesoria("Consulta B", "legal", "")
        self.assertEqual(b.rango_asesor, "senior")

    def test_rango_junior_diez_porciento_descuento(self):
        """Rango junior aplica 10% de descuento sobre la tarifa base."""
        a = Asesoria("Jr", "legal", "junior")
        self.assertEqual(a.obtener_tarifa_hora(), 85_500.0)

    def test_rango_experto_cincuenta_porciento_mas(self):
        """Rango experto aplica 50% adicional sobre la tarifa base."""
        a = Asesoria("Exp", "legal", "experto")
        self.assertEqual(a.obtener_tarifa_hora(), 142_500.0)

    def test_rango_invalido(self):
        """Rango no permitido debe lanzar `ServicioInvalidoError`."""
        try:
            Asesoria("X", "legal", "ninja")
            self.fail("Se esperaba ServicioInvalidoError")
        except ServicioInvalidoError as e:
            _loggear_excepcion_prueba("Asesoria.rango inválido", e)

    def test_tipo_invalido(self):
        """Tipo de asesoría no permitido debe lanzar `ServicioInvalidoError`."""
        try:
            Asesoria("Pack", "cocina")
            self.fail("Se esperaba ServicioInvalidoError")
        except ServicioInvalidoError as e:
            _loggear_excepcion_prueba("Asesoria.tipo inválido", e)


class TestServicio(unittest.TestCase):
    def test_no_instanciar_clase_abstracta(self):
        """`Servicio` es abstracta: intentar instanciar debe producir TypeError."""
        with self.assertRaises(TypeError):
            Servicio("Genérico")

    def test_calcular_con_iva_y_descuento(self):
        """Valida fórmula de costo total: descuento sobre subtotal y luego IVA."""
        s = ReservaSala("Sala test", 5)
        # 50_000 * 2h = 100_000; 15% dto = 85_000; IVA 19% = 101_150
        total = s.calcular_costo(2, porcentaje_iva=19.0, porcentaje_descuento=15.0)
        self.assertAlmostEqual(total, 101_150.0, places=2)

    def test_calcular_sin_impuesto_metodo_acortado(self):
        """Atajo `calcular_costo_sin_impuesto`: equivalente a costo con IVA=0 y descuento=0."""
        s = ReservaSala("Sala", 5)
        self.assertEqual(s.calcular_costo_sin_impuesto(1), 50_000.0)

    def test_horas_negativas(self):
        """Horas <= 0 deben lanzar `CostoInvalidoError`."""
        s = ReservaSala("Sala", 5)
        try:
            s.calcular_costo(-1)
            self.fail("Se esperaba CostoInvalidoError")
        except CostoInvalidoError as e:
            _loggear_excepcion_prueba("Servicio.calcular_costo horas inválidas", e)

    def test_servicio_no_disponible(self):
        """Si el servicio está marcado no disponible, calcular costo debe lanzar `ServicioNoDisponibleError`."""
        s = ReservaSala("Sala", 4)
        s.marcar_no_disponible()
        try:
            s.calcular_costo(1)
            self.fail("Se esperaba ServicioNoDisponibleError")
        except ServicioNoDisponibleError as e:
            _loggear_excepcion_prueba("Servicio no disponible al calcular costo", e)
#Fin de pruebas de Jaime

def ejecutar_simulacion() -> bool:
    """
    Ejecuta la suite de pruebas y falla de forma controlada si algo no pasa.

    Retorna:
    - `True` si todas las pruebas pasaron.

    Lanza:
    - `RuntimeError` si hubo fallas/errores, para que `main.py` lo registre en logs.
    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in (
        TestCliente,
        TestReservaSala,
        TestAlquilerEquipo,
        TestAsesoria,
        TestServicio,
    ):
        suite.addTests(loader.loadTestsFromTestCase(cls))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        raise RuntimeError(
            f"Pruebas fallidas: {len(result.failures)} fallo(s), "
            f"{len(result.errors)} error(es)"
        )
    return True


if __name__ == "__main__":
    ejecutar_simulacion()
