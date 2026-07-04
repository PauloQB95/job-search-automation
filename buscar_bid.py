import math
import requests
import pandas as pd

# ============================================================
# CONFIGURACIÓN
# ============================================================

URL = "https://jobs.iadb.org/services/recruiting/v1/jobs"

TRABAJOS_POR_PAGINA = 10

payload = {
    "locale": "en_US",
    "pageNumber": 0,
    "sortBy": "",
    "keywords": "",
    "location": "",
    "facetFilters": {},
    "brand": "",
    "categoryId": 0,
    "alertId": "",
    "rcmCandidateId": "",
    "skills": []
}

# Lista donde guardaremos todos los trabajos
lista_trabajos = []


# ============================================================
# FUNCIÓN PARA PROCESAR UNA PÁGINA
# ============================================================

def agregar_trabajos(datos_pagina):

    trabajos = datos_pagina["jobSearchResult"]

    for trabajo in trabajos:

        detalle = trabajo["response"]

        nuevo_trabajo = {
            "titulo": detalle["unifiedStandardTitle"],
            "ubicacion": detalle["jobLocationShort"][0],
            "id": detalle["id"],
            "fecha_limite": detalle["unifiedStandardEnd"]
        }

        lista_trabajos.append(nuevo_trabajo)


# ============================================================
# DESCARGAR LA PRIMERA PÁGINA
# ============================================================

respuesta = requests.post(URL, json=payload)

datos = respuesta.json()

total_trabajos = datos["totalJobs"]

total_paginas = math.ceil(total_trabajos / TRABAJOS_POR_PAGINA)

print(f"Se encontraron {total_trabajos} trabajos.")
print(f"Se descargarán {total_paginas} páginas.\n")

# Procesamos inmediatamente la primera página
agregar_trabajos(datos)


# ============================================================
# DESCARGAR EL RESTO DE LAS PÁGINAS
# ============================================================

for pagina in range(1, total_paginas):

    payload["pageNumber"] = pagina

    respuesta = requests.post(URL, json=payload)

    datos = respuesta.json()

    print(f"Descargando página {pagina + 1}...")

    agregar_trabajos(datos)


# ============================================================
# CREAR EL DATAFRAME
# ============================================================

df = pd.DataFrame(lista_trabajos)

print(f"\nTotal de trabajos descargados: {len(df)}")


# ============================================================
# EXPORTAR A EXCEL
# ============================================================

df.to_excel("trabajos_bid.xlsx", index=False)

print("Archivo trabajos_bid.xlsx creado correctamente.")
