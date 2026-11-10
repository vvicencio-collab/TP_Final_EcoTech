from django.test import TestCase

import unittest

from .emisiones import (
    calcular_emisiones_carbono,
    obtener_metricas_consumo
)


# PUNTO A: Auditoría del cálculo de emisiones

class TestCalculoEmisiones(unittest.TestCase):

    def test_consumo_normal(self):
        """
        Verificar el cálculo con un consumo normal.
        """

        resultado = calcular_emisiones_carbono(100)

        self.assertAlmostEqual(resultado, 40.0)

    def test_consumo_cero(self):
        """
        Verificar que un consumo cero genere cero emisiones.
        """

        resultado = calcular_emisiones_carbono(0)

        self.assertAlmostEqual(resultado, 0.0)

    def test_factor_personalizado(self):
        """
        Verificar el cálculo con otro factor de emisión.
        """

        resultado = calcular_emisiones_carbono(100, 0.5)

        self.assertAlmostEqual(resultado, 50.0)

    def test_consumo_decimal(self):
        """
        Verificar la precisión con valores decimales.
        """

        resultado = calcular_emisiones_carbono(25.5)

        self.assertAlmostEqual(resultado, 10.2)

    def test_consumo_negativo(self):
        """
        Verificar que un consumo negativo genere ValueError.
        """

        with self.assertRaises(ValueError):

            calcular_emisiones_carbono(-10)


# PRUEBAS ADICIONALES: Procesamiento de métricas

class TestMetricasConsumo(unittest.TestCase):

    def test_metricas_consumo(self):
        """
        Verificar las emisiones globales y la planta
        con mayor consumo.
        """

        registros = [
            {"planta": "Planta Norte", "consumo_kwh": 1200},
            {"planta": "Planta Sur", "consumo_kwh": 1800},
            {"planta": "Planta Este", "consumo_kwh": 950}
        ]

        resultado = obtener_metricas_consumo(registros)

        self.assertAlmostEqual(
            resultado["total_emisiones"],
            1580.0
        )

        self.assertEqual(
            resultado["planta_mayor_consumo"],
            "Planta Sur"
        )

    def test_lista_vacia(self):
        """
        Verificar el comportamiento cuando no hay registros.
        """

        resultado = obtener_metricas_consumo([])

        self.assertEqual(resultado["total_emisiones"], 0)

        self.assertIsNone(resultado["planta_mayor_consumo"])

    def test_registro_consumo_negativo(self):
        """
        Verificar que las métricas rechacen consumos negativos.
        """

        registros = [
            {"planta": "Planta Norte", "consumo_kwh": -100}
        ]

        with self.assertRaises(ValueError):

            obtener_metricas_consumo(registros)