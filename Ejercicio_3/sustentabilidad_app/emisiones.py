"""
Auditoría con Tests Unitarios e Integración Web
"""

# PUNTO A: Cálculo de emisiones de carbono

def calcular_emisiones_carbono(
    consumo_kwh: float,
    factor_emision: float = 0.4
) -> float:
    """
    Calcula las emisiones de carbono según el consumo eléctrico.

    Si el consumo es negativo, genera ValueError.
    """

    if consumo_kwh < 0:
        raise ValueError("El consumo no puede ser negativo.")

    emisiones = consumo_kwh * factor_emision

    return emisiones


# PUNTO B: Procesamiento de métricas

def obtener_metricas_consumo(registros: list) -> dict:
    """
    Procesa los consumos de las plantas industriales.

    Retorna un diccionario con:
    - Total global de emisiones.
    - Planta de mayor consumo.
    """

    total_emisiones = 0
    mayor_consumo = 0
    planta_mayor_consumo = None

    for registro in registros:

        consumo = registro["consumo_kwh"]

        # Reutilizar la función auditada
        emisiones = calcular_emisiones_carbono(consumo)

        # Acumular emisiones
        total_emisiones += emisiones

        # Identificar la planta de mayor consumo
        if planta_mayor_consumo is None or consumo > mayor_consumo:

            mayor_consumo = consumo
            planta_mayor_consumo = registro["planta"]

    # Preparar los resultados
    metricas = {
        "total_emisiones": total_emisiones,
        "planta_mayor_consumo": planta_mayor_consumo
    }

    return metricas