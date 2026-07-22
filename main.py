from pathlib import Path

import pandas as pd

from buscar_bid import buscar_trabajos_bid
from buscar_bm import buscar_trabajos_bm


# ============================================================
# EJECUTAR UN SCRAPER DE FORMA SEGURA
# ============================================================

def ejecutar_scraper(nombre, funcion_scraper):
    """
    Ejecuta un scraper y evita que un error detenga
    el resto del programa.

    Parámetros:
        nombre:
            Nombre de la fuente. Se utiliza en los mensajes.

        funcion_scraper:
            Función que descarga y devuelve una lista de trabajos.

    Devuelve:
        La lista obtenida por el scraper.

        Si ocurre un error, devuelve una lista vacía para que
        el programa pueda continuar con las demás fuentes.
    """

    print("\n" + "=" * 60)
    print(f"Iniciando scraper: {nombre}")
    print("=" * 60)

    try:
        trabajos = funcion_scraper()

        # Comprobamos que el scraper haya devuelto una lista.
        if not isinstance(trabajos, list):
            print(
                f"Advertencia: el scraper de {nombre} no devolvió "
                "una lista. Se utilizará una lista vacía."
            )
            return []

        print(
            f"Scraper de {nombre} completado correctamente: "
            f"{len(trabajos)} trabajos."
        )

        return trabajos

    except Exception as error:
        print(f"El scraper de {nombre} encontró un error.")
        print(f"Tipo de error: {type(error).__name__}")
        print(f"Detalle: {error}")
        print("El programa continuará con las demás fuentes.")

        return []


# ============================================================
# DESCARGAR TRABAJOS DE CADA FUENTE
# ============================================================

trabajos_bid = ejecutar_scraper(
    nombre="BID",
    funcion_scraper=buscar_trabajos_bid
)

trabajos_bm = ejecutar_scraper(
    nombre="Banco Mundial",
    funcion_scraper=buscar_trabajos_bm
)


# ============================================================
# COMBINAR LOS RESULTADOS
# ============================================================

trabajos = []

trabajos.extend(trabajos_bid)
trabajos.extend(trabajos_bm)


# ============================================================
# CREAR LA CARPETA DE RESULTADOS
# ============================================================

carpeta_resultados = Path("resultados")

# Si la carpeta no existe, Python la crea.
# Si ya existe, no ocurre ningún error.
carpeta_resultados.mkdir(exist_ok=True)


# ============================================================
# EXPORTAR EL ARCHIVO CONSOLIDADO
# ============================================================

if trabajos:

    df = pd.DataFrame(trabajos)

    ruta_salida = carpeta_resultados / "trabajos_consolidados.xlsx"

    df.to_excel(
        ruta_salida,
        index=False
    )

    print("\n" + "=" * 60)
    print("DESCARGA TERMINADA")
    print("=" * 60)

    print(f"Se descargaron {len(df)} trabajos en total.")
    print(f"BID: {len(trabajos_bid)} trabajos.")
    print(f"Banco Mundial: {len(trabajos_bm)} trabajos.")
    print(f"Archivo creado en: {ruta_salida}")

else:
    print("\nNo se descargaron trabajos de ninguna fuente.")
    print("No se creó un archivo Excel vacío.")