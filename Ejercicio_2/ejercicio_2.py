import json
from pathlib import Path

# ---------------------------------------------------------
# PUNTO A: CLASES, HERENCIA Y VALIDACIÓN
# ---------------------------------------------------------

# Excepción personalizada
class StockInvalidoError(Exception):
    """
    Excepción que se produce cuando se intenta
    asignar un stock negativo.
    """
    pass


# Clase padre
class DispositivoEcologico:
    """
    Representa un dispositivo ecológico del catálogo.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        stock: int
    ):

        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio

        # Encapsulamiento explícito del stock
        self.__stock = 0

        # Asignar el stock mediante el método de validación
        self.asignar_stock(stock)

    def asignar_stock(self, nuevo_stock: int):
        """
        Modifica el stock si el valor es válido.
        Lanza StockInvalidoError si es negativo.
        """

        if nuevo_stock < 0:
            raise StockInvalidoError(
                "El stock no puede ser negativo."
            )

        self.__stock = nuevo_stock

    def obtener_stock(self) -> int:
        """
        Retorna el stock actual del dispositivo.
        """

        return self.__stock

    def ficha_tecnica(self) -> str:
        """
        Retorna la ficha técnica del dispositivo.
        """

        return (
            f"Código: {self.codigo}\n"
            f"Nombre: {self.nombre}\n"
            f"Precio: ${self.precio:.2f}\n"
            f"Stock: {self.obtener_stock()}"
        )


# Clase hija
class PanelSolar(DispositivoEcologico):
    """
    Representa un panel solar.

    Hereda las características de DispositivoEcologico
    y agrega potencia y eficiencia.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        stock: int,
        potencia_watts: float,
        eficiencia: float
    ):

        # Inicializar los atributos heredados
        super().__init__(codigo, nombre, precio, stock)

        # Atributos propios de PanelSolar
        self.potencia_watts = potencia_watts
        self.eficiencia = eficiencia

    def ficha_tecnica(self) -> str:
        """
        Sobrescribe el método de la clase padre.

        Agrega los datos específicos del panel solar.
        """

        return (
            f"{super().ficha_tecnica()}\n"
            f"Potencia: {self.potencia_watts} W\n"
            f"Eficiencia: {self.eficiencia}%"
        )


# ---------------------------------------------------------
# PUNTO B: PERSISTENCIA EN JSON
# ---------------------------------------------------------

class GestorInventario:
    """
    Administra la exportación de dispositivos
    ecológicos a un archivo JSON.
    """

    def guardar_catalogo_json(
        self,
        lista_dispositivos: list,
        ruta_archivo: str
    ):
        """
        Convierte los dispositivos a diccionarios
        y los almacena en un archivo JSON.
        """

        catalogo = []

        # Recorrer los dispositivos
        for dispositivo in lista_dispositivos:

            # Crear un diccionario con los datos generales
            producto = {
                "codigo": dispositivo.codigo,
                "nombre": dispositivo.nombre,
                "precio": dispositivo.precio,
                "stock": dispositivo.obtener_stock()
            }

            # Agregar los atributos específicos de PanelSolar
            if type(dispositivo) == PanelSolar:

                producto["potencia_watts"] = (
                    dispositivo.potencia_watts
                )

                producto["eficiencia"] = (
                    dispositivo.eficiencia
                )

            # Agregar el producto al catálogo
            catalogo.append(producto)

        # Guardar el catálogo en formato JSON
        with open(
            ruta_archivo,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                catalogo,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        print(f"Catálogo guardado correctamente en {ruta_archivo}")


# ---------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------

if __name__ == "__main__":

    print("==========================================")
    print("       INVENTARIO ECOTECH SOLUTIONS")
    print("==========================================")

    # Crear diferentes dispositivos
    panel_1 = PanelSolar(
        "SOL001",
        "Panel Solar Residencial",
        250000,
        15,
        450,
        21.5
    )

    panel_2 = PanelSolar(
        "SOL002",
        "Panel Solar Industrial",
        480000,
        8,
        800,
        23.0
    )

    dispositivo_1 = DispositivoEcologico(
        "ECO001",
        "Controlador de Carga",
        85000,
        5
    )

    # Probar la excepción al crear un dispositivo
    print("\nPRUEBA DE STOCK INVÁLIDO")
    print("------------------------------------------")

    try:

        panel_invalido = PanelSolar(
            "SOL003",
            "Panel Solar Defectuoso",
            150000,
            -5,
            300,
            18.5
        )

    except StockInvalidoError as error:

        print(f"Error controlado: {error}")

    # Probar la excepción al modificar el stock
    print("\nPRUEBA DE MODIFICACIÓN DE STOCK")
    print("------------------------------------------")

    try:

        panel_1.asignar_stock(-10)

    except StockInvalidoError as error:

        print(f"Error controlado: {error}")

    # Crear una lista con los dispositivos válidos
    dispositivos = [
        panel_1,
        panel_2,
        dispositivo_1
    ]

    # Mostrar las fichas técnicas
    print("\nFICHAS TÉCNICAS")
    print("------------------------------------------")

    for dispositivo in dispositivos:

        print(dispositivo.ficha_tecnica())
        print("------------------------------------------")

    # Crear el gestor de inventario
    gestor = GestorInventario()

    # Definir la ruta del archivo
    ruta_archivo = Path(__file__).resolve().parent / "catalogo_ecotech.json"

    # Guardar los dispositivos válidos
    print("\nEXPORTACIÓN DEL CATÁLOGO")
    print("------------------------------------------")

    gestor.guardar_catalogo_json(
        dispositivos,
        ruta_archivo
    )