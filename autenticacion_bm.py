from playwright.sync_api import sync_playwright


# ============================================================
# OBTENER AUTOMÁTICAMENTE EL TOKEN DEL BANCO MUNDIAL
# ============================================================

def obtener_token_bm():

    # Página pública del portal de empleos del Banco Mundial.
    URL_PORTAL = (
        "https://worldbankgroup.csod.com/"
        "ux/ats/careersite/1/home"
        "?c=worldbankgroup"
    )

    # Parte de la dirección de la API que queremos detectar.
    ENDPOINT_TRABAJOS = (
        "us.api.csod.com/rec-job-search/external/jobs"
    )

    # Aquí se guardará el encabezado Authorization
    # cuando Playwright lo encuentre.
    token_encontrado = None

    print("Abriendo el portal de empleos del Banco Mundial...")

    with sync_playwright() as playwright:

        navegador = playwright.chromium.launch(
            headless=True
        )

        contexto = navegador.new_context()

        pagina = contexto.new_page()

        # Esta función se ejecutará cada vez que la página
        # envíe una solicitud a Internet.
        def revisar_solicitud(solicitud):

            nonlocal token_encontrado

            # Solo nos interesa la solicitud que consulta
            # las vacantes del Banco Mundial.
            if ENDPOINT_TRABAJOS in solicitud.url:

                encabezados = solicitud.all_headers()

                authorization = encabezados.get("authorization")

                if authorization:
                    token_encontrado = authorization

        # Empezamos a observar todas las solicitudes
        # realizadas por la página.
        pagina.on("request", revisar_solicitud)

        try:
            pagina.goto(
                URL_PORTAL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            # Damos tiempo al portal para ejecutar JavaScript
            # y consultar la API de vacantes.
            pagina.wait_for_timeout(15000)

        finally:
            navegador.close()

    if not token_encontrado:
        raise RuntimeError(
            "No se pudo obtener automáticamente el token "
            "del Banco Mundial. Es posible que el portal "
            "haya cambiado o que la solicitud de vacantes "
            "no se haya ejecutado."
        )

    print("Token del Banco Mundial obtenido correctamente.")

    return token_encontrado