
# PUNTO A: Normalización de lecturas
def limpiar_registro_sensor(registro_raw: dict) -> dict:

    # Limpiar el identificador del sensor
    sensor_id = registro_raw["sensor_id"].strip()

    # Eliminar las unidades de temperatura y los espacios
    temperatura = registro_raw["temperatura"].replace("°C", "").replace("C", "").strip()

    # Convertir la temperatura a float
    temperatura = float(temperatura)

    # Obtener la ubicación
    ubicacion = registro_raw.get("ubicacion", "")

    # Controlar si la ubicación está informada
    if ubicacion is None:
        ubicacion = ""

    ubicacion = ubicacion.strip()

    if ubicacion == "":
        ubicacion = "Ubicación desconocida"

    # Crear un nuevo diccionario con los datos limpios
    registro_limpio = {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion
    }

    return registro_limpio


# PUNTO B: Monitoreo y análisis estadístico

def generar_resumen_sensores(
    lista_sensores_limpios: list,
    umbral_temperatura: float
) -> tuple:

    # Inicializar la lista de alertas
    lista_sensores_alerta = []

    # Inicializar el acumulador de temperaturas
    suma_temperaturas = 0

    # Recorrer todos los sensores
    for sensor in lista_sensores_limpios:

        temperatura = sensor["temperatura"]
        sensor_id = sensor["sensor_id"]

        # Verificar si supera el umbral
        if temperatura > umbral_temperatura:
            lista_sensores_alerta.append(sensor_id)

        # Acumular todas las temperaturas
        suma_temperaturas += temperatura

    # Calcular el promedio evitando dividir por cero
    if len(lista_sensores_limpios) > 0:
        promedio_temperatura = suma_temperaturas / len(lista_sensores_limpios)
    else:
        promedio_temperatura = 0

    # Retornar una tupla
    return lista_sensores_alerta, promedio_temperatura


# BLOQUE PRINCIPAL

if __name__ == "__main__":

    # Registros originales recibidos de los sensores
    sensores_raw = [
        {
            "sensor_id": " SENSOR-001 ",
            "temperatura": "24.5C",
            "ubicacion": " Planta Norte "
        },
        {
            "sensor_id": " SENSOR-002 ",
            "temperatura": "32.8°C",
            "ubicacion": "Planta Sur"
        },
        {
            "sensor_id": " SENSOR-003 ",
            "temperatura": "28.3 C"
        },
        {
            "sensor_id": " SENSOR-004 ",
            "temperatura": "35.2C ",
            "ubicacion": " Planta Este "
        },
        {
            "sensor_id": " SENSOR-005 ",
            "temperatura": "22.0°C",
            "ubicacion": ""
        }
    ]

    # Crear una lista vacía para los sensores normalizados
    sensores_limpios = []

    # Limpiar cada registro
    for registro in sensores_raw:

        registro_limpio = limpiar_registro_sensor(registro)

        sensores_limpios.append(registro_limpio)

    # Definir el umbral de temperatura
    umbral = 30

    # Generar el resumen estadístico
    sensores_alerta, promedio_global = generar_resumen_sensores(
        sensores_limpios,
        umbral
    )

    # Mostrar el reporte final
    print("==========================================")
    print("       REPORTE DE SENSORES ECOTECH")
    print("==========================================")

    print("\nSENSORES PROCESADOS")
    print("------------------------------------------")

    for sensor in sensores_limpios:

        print(f"Sensor: {sensor['sensor_id']}")
        print(f"Temperatura: {sensor['temperatura']} °C")
        print(f"Ubicación: {sensor['ubicacion']}")
        print("------------------------------------------")

    print("\nRESUMEN ESTADÍSTICO")
    print("------------------------------------------")

    print(f"Cantidad de sensores: {len(sensores_limpios)}")
    print(f"Umbral establecido: {umbral} °C")
    print(f"Temperatura promedio: {promedio_global:.2f} °C")

    print("\nSENSORES QUE SUPERAN EL UMBRAL")
    print("------------------------------------------")

    if len(sensores_alerta) > 0:

        for sensor_id in sensores_alerta:
            print(f"- {sensor_id}")

    else:
        print("No se registraron sensores en alerta.")
