from pathlib import Path
import sys

import pandas as pd

from buscar_bid import buscar_trabajos_bid
from buscar_bm import buscar_trabajos_bm


# ============================================================
# CONFIGURACIÓN
# ============================================================

CARPETA_RESULTADOS = Path("resultados")
RUTA_EXCEL = CARPETA_RESULTADOS / "trabajos_consolidados.xlsx"


# ============================================================
# EJECUTAR UN SCRAPER DE FORMA SEGURA
# ============================================================

def ejecutar_scraper(nombre, funcion_scraper):
    """
    Ejecuta un scraper sin permitir que un error detenga
    inmediatamente todo el programa.

    Parámetros
    ----------
    nombre : str
        Nombre de la organización.

    funcion_scraper : function
        Función que ejecuta el scraper.

    Retorna
    -------
    list
        Lista de trabajos encontrados.

        Si el scraper falla o devuelve un valor inválido,
        retorna una lista vacía.
    """

    print("\n" + "=" * 60)
    print(f"Iniciando scraper: {nombre}")
    print("=" * 60)

    try:
        trabajos = funcion_scraper()

        if not isinstance(trabajos, list):
            print(
                f"Advertencia: {nombre} no devolvió una lista válida."
            )
            return []

        print(
            f"{nombre}: se encontraron "
            f"{len(trabajos)} trabajos."
        )

        return trabajos

    except Exception as error:
        print(f"El scraper de {nombre} falló.")
        print(f"Tipo de error: {type(error).__name__}")
        print(f"Detalle: {error}")
        print("El programa continuará con las demás fuentes.")

        return []


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    """
    Ejecuta todos los scrapers, combina los resultados
    y crea el archivo Excel consolidado.

    Retorna
    -------
    int
        0 si se creó correctamente el Excel.
        1 si no se obtuvo ningún trabajo.
    """

    # Ejecutar los scrapers independientemente.
    trabajos_bid = ejecutar_scraper(
        nombre="BID",
        funcion_scraper=buscar_trabajos_bid
    )

    trabajos_bm = ejecutar_scraper(
        nombre="Banco Mundial",
        funcion_scraper=buscar_trabajos_bm
    )

    # Combinar resultados.
    trabajos = []

    trabajos.extend(trabajos_bid)
    trabajos.extend(trabajos_bm)

    # --------------------------------------------------------
    # Si ambos scrapers fallan o no producen resultados
    # --------------------------------------------------------

    if not trabajos:
        print("\n" + "=" * 60)
        print("NO SE GENERÓ UN NUEVO ARCHIVO")
        print("=" * 60)

        print("Ningún scraper produjo resultados.")
        print(
            "El Excel anterior, si existe, se conservará "
            "sin modificaciones."
        )

        # Código 1: GitHub Actions debe considerar
        # esta ejecución como fallida.
        return 1

    # --------------------------------------------------------
    # Crear el nuevo Excel
    # --------------------------------------------------------

    CARPETA_RESULTADOS.mkdir(
        parents=True,
        exist_ok=True
    )

    df = pd.DataFrame(trabajos)

    # Primero creamos un archivo temporal.
    ruta_temporal = (
        CARPETA_RESULTADOS /
        "trabajos_consolidados_temporal.xlsx"
    )

    df.to_excel(
        ruta_temporal,
        index=False
    )

    # Solamente después de crear correctamente el archivo
    # temporal reemplazamos el Excel anterior.
    ruta_temporal.replace(RUTA_EXCEL)

    print("\n" + "=" * 60)
    print("DESCARGA TERMINADA")
    print("=" * 60)

    print(f"Total: {len(df)} trabajos.")
    print(f"BID: {len(trabajos_bid)} trabajos.")
    print(f"Banco Mundial: {len(trabajos_bm)} trabajos.")
    print(f"Archivo creado en: {RUTA_EXCEL}")

    return 0


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    codigo_salida = main()
    sys.exit(codigo_salida)