import math
from httpcore import URL
import requests
import os
from dotenv import load_dotenv

# ============================================================
# CONFIGURACIÓN
# ============================================================

def buscar_trabajos_bm():
    print("Entré a buscar_trabajos_bm")
    
    URL = "https://us.api.csod.com/rec-job-search/external/jobs"

    TRABAJOS_POR_PAGINA = 25

    payload = {
        "careerSiteId": 1,
        "careerSitePageId": 1,
        "cities": [],
        "countryCodes": [],
        "cultureId": 1,
        "cultureName": "en-US",
        "customFieldCheckboxKeys": [],
        "customFieldDropdowns": [],
        "customFieldRadios": [],
        "pageNumber": 1,
        "pageSize": 25,
        "placeID": "",
        "postingsWithinDays": None,
        "radius": None,
        "searchText": "",
        "states": []
    }
      
    lista_trabajos = []

    # ============================================================
    # FUNCIÓN PARA PROCESAR UNA PÁGINA
    # ============================================================

    def agregar_trabajos(datos_pagina):

        trabajos = datos_pagina["data"]["requisitions"]

        for trabajo in trabajos:

            locations = trabajo.get("locations", [])

            if len(locations) > 0:
                primera_ubicacion = locations[0]
                ciudad = primera_ubicacion.get("city", "")
                pais = primera_ubicacion.get("country", "")
                ubicacion = f"{ciudad}, {pais}".strip(", ")
            else:
                ubicacion = ""

            requisition_id = trabajo["requisitionId"]

            url_trabajo = (
                "https://worldbankgroup.csod.com/ux/ats/careersite/1/home/"
                f"requisition/{requisition_id}?c=worldbankgroup"
            )

            nuevo_trabajo = {
                "organizacion": "World Bank",
                "titulo": trabajo["displayJobTitle"],
                "ubicacion": ubicacion,
                "fecha_limite": trabajo["postingExpirationDate"],
                "url": url_trabajo,
                "fuente": "API"
            }

            lista_trabajos.append(nuevo_trabajo)


    # ============================================================
    # DESCARGAR LA PRIMERA PÁGINA
    # ============================================================

    load_dotenv()

    world_bank_token = os.getenv("WORLD_BANK_TOKEN")

    headers = {
        "Authorization": world_bank_token,
        "Content-Type": "application/json"
    }
      
    respuesta = requests.post(URL, json=payload, headers=headers)

    print("Status code:", respuesta.status_code)
    print("Respuesta:", respuesta.text[:300])

    if respuesta.status_code != 200:
        print("La API no respondió correctamente. Revisa el Authorization header.")
        return []

    datos = respuesta.json()

    total_trabajos = datos["data"]["totalCount"]
    total_paginas = math.ceil(total_trabajos / TRABAJOS_POR_PAGINA)

    print(f"Se encontraron {total_trabajos} trabajos.")
    print(f"Se descargarán {total_paginas} páginas.\n")

    # Procesamos inmediatamente la primera página
    agregar_trabajos(datos)

    # ============================================================
    # DESCARGAR EL RESTO DE LAS PÁGINAS
    # ============================================================

    for pagina in range(2, total_paginas + 1):

        payload["pageNumber"] = pagina

        respuesta = requests.post(
            URL,
            json=payload,
            headers=headers
        )

        print("Status code:", respuesta.status_code)
        print("Respuesta:", respuesta.text[:300])

        if respuesta.status_code != 200:
            print(f"No se pudo descargar la página {pagina}.")
            continue

        datos = respuesta.json()

        print(f"Descargando página {pagina}...")

        agregar_trabajos(datos)

    # Devolvemos la lista completa de trabajos al programa principal
    return lista_trabajos

