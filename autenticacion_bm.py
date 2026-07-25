from playwright.sync_api import sync_playwright


# ============================================================
# AUTOMATICALLY RETRIEVE THE WORLD BANK TOKEN
# ============================================================

def get_world_bank_token():

    # Public page for the World Bank careers portal.
    WORLD_BANK_CAREERS_URL = (
        "https://worldbankgroup.csod.com/"
        "ux/ats/careersite/1/home"
        "?c=worldbankgroup"
    )

    # Portion of the API address to detect.
    WORLD_BANK_JOBS_ENDPOINT = (
        "us.api.csod.com/rec-job-search/external/jobs"
    )

    # Store the Authorization header when Playwright finds it.
    captured_token = None

    print("Opening the World Bank careers portal...")

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=True
        )

        browser_context = browser.new_context()

        page = browser_context.new_page()

        # Run this function whenever the page sends a request.
        def inspect_request(request):

            nonlocal captured_token

            # Only inspect the request that retrieves World Bank jobs.
            if WORLD_BANK_JOBS_ENDPOINT in request.url:

                headers = request.all_headers()

                authorization = headers.get("authorization")

                if authorization:
                    captured_token = authorization

        # Monitor every request made by the page.
        page.on("request", inspect_request)

        try:
            page.goto(
                WORLD_BANK_CAREERS_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            # Allow the portal to run JavaScript and query the jobs API.
            page.wait_for_timeout(15000)

        finally:
            browser.close()

    if not captured_token:
        raise RuntimeError(
            "The World Bank token could not be retrieved automatically. "
            "The portal may have changed, or the jobs request may not "
            "have been sent."
        )

    print("World Bank token retrieved successfully.")

    return captured_token
