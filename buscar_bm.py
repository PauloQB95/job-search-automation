import math
import requests

from autenticacion_bm import get_world_bank_token
from job_schema import create_job

# ============================================================
# CONFIGURATION
# ============================================================

def fetch_world_bank_jobs():
    print("Entered fetch_world_bank_jobs")
    
    WORLD_BANK_JOBS_URL = "https://us.api.csod.com/rec-job-search/external/jobs"

    JOBS_PER_PAGE = 25

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
      
    jobs = []

    # ============================================================
    # PROCESS ONE PAGE
    # ============================================================

    def append_jobs(page_data):

        requisitions = page_data["data"]["requisitions"]

        for requisition in requisitions:

            locations = requisition.get("locations", [])

            if len(locations) > 0:
                primary_location = locations[0]
                city = primary_location.get("city", "")
                country = primary_location.get("country", "")
                location = f"{city}, {country}".strip(", ")
            else:
                country = ""
                location = ""

            requisition_id = requisition["requisitionId"]

            job_url = (
                "https://worldbankgroup.csod.com/ux/ats/careersite/1/home/"
                f"requisition/{requisition_id}?c=worldbankgroup"
            )

            job = create_job(
                organization="World Bank",
                job_title=requisition["displayJobTitle"],
                location=location,
                country=country,
                closing_date=requisition["postingExpirationDate"],
                job_id=requisition_id,
                application_url=job_url,
                source="API"
            )

            jobs.append(job)


    # ============================================================
    # DOWNLOAD THE FIRST PAGE
    # ============================================================

    # Automatically retrieve the token used by the World Bank careers portal.
    try:
        world_bank_token = get_world_bank_token()

    except RuntimeError as error:
        print(error)
        return []

    headers = {
        "Authorization": world_bank_token,
        "Content-Type": "application/json"
    }
      
    response = requests.post(
        WORLD_BANK_JOBS_URL,
        json=payload,
        headers=headers
    )

    data = response.json()

    total_jobs = data["data"]["totalCount"]
    total_pages = math.ceil(total_jobs / JOBS_PER_PAGE)

    print(f"Found {total_jobs} jobs.")
    print(f"Downloading {total_pages} pages.\n")

    # Process the first page immediately.
    append_jobs(data)

    # ============================================================
    # DOWNLOAD THE REMAINING PAGES
    # ============================================================

    for page_number in range(2, total_pages + 1):

        payload["pageNumber"] = page_number

        response = requests.post(
            WORLD_BANK_JOBS_URL,
            json=payload,
            headers=headers
        )

        data = response.json()

        print(f"Downloading page {page_number}...")

        append_jobs(data)

    # Return the complete job list to the main program.
    return jobs

