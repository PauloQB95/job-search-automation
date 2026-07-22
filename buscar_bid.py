import math
import requests

# ============================================================
# CONFIGURACIÓN
# ============================================================

def buscar_trabajos_bid():
    
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

    lista_trabajos = []

    # ============================================================
    # FUNCIÓN PARA PROCESAR UNA PÁGINA
    # ============================================================

    def agregar_trabajos(datos_pagina):

        trabajos = datos_pagina["jobSearchResult"]

        for trabajo in trabajos:

            detalle = trabajo["response"]

            nuevo_trabajo = {
                "organizacion": "IDB",
                "titulo": detalle["unifiedStandardTitle"],
                "ubicacion": "; ".join(
                    ubicacion.strip()
                    for ubicacion in detalle["jobLocationShort"]
                ),
                "fecha_limite": detalle["unifiedStandardEnd"],
                "url": f"https://jobs.iadb.org/job/{detalle['unifiedUrlTitle']}/{detalle['id']}-en_US",
            "fuente": "API"
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

    # Devolvemos la lista completa de trabajos al programa principal
    return lista_trabajos

