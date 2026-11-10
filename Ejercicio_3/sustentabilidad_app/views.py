from django.shortcuts import render

from django.shortcuts import render

from .emisiones import obtener_metricas_consumo


# PUNTO B: Vista del panel de sustentabilidad

def vista_panel_sustentabilidad(request):
    """
    Procesa los consumos industriales y envía
    las métricas a la plantilla HTML.
    """

    # Historial de consumos
    registros = [
        {
            "planta": "Planta Norte",
            "consumo_kwh": 1200
        },
        {
            "planta": "Planta Sur",
            "consumo_kwh": 1800
        },
        {
            "planta": "Planta Este",
            "consumo_kwh": 950
        }
    ]

    # Procesar los registros
    metricas = obtener_metricas_consumo(registros)

    # Crear el contexto
    contexto = {
        "total_emisiones": metricas["total_emisiones"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"]
    }

    # Renderizar la plantilla
    return render(
        request,
        "sustentabilidad/panel.html",
        contexto
    )
