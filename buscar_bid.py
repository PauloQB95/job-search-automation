import math
import requests

from job_schema import create_job

# ============================================================
# CONFIGURATION
# ============================================================

def fetch_idb_jobs():
    
    IDB_JOBS_URL = "https://jobs.iadb.org/services/recruiting/v1/jobs"

    JOBS_PER_PAGE = 10

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

    jobs = []

    # ============================================================
    # PROCESS ONE PAGE
    # ============================================================

    def append_jobs(page_data):

        job_results = page_data["jobSearchResult"]

        for job_result in job_results:

            job_details = job_result["response"]

            job = create_job(
                organization="IDB",
                job_title=job_details["unifiedStandardTitle"],
                location="; ".join(
                    location.strip()
                    for location in job_details["jobLocationShort"]
                ),
                closing_date=job_details["unifiedStandardEnd"],
                job_id=job_details["id"],
                application_url=(
                    "https://jobs.iadb.org/job/"
                    f"{job_details['unifiedUrlTitle']}/"
                    f"{job_details['id']}-en_US"
                ),
                source="API - IDB"
            )

            jobs.append(job)


    # ============================================================
    # DOWNLOAD THE FIRST PAGE
    # ============================================================

    response = requests.post(IDB_JOBS_URL, json=payload)

    data = response.json()

    total_jobs = data["totalJobs"]

    total_pages = math.ceil(total_jobs / JOBS_PER_PAGE)

    print(f"Found {total_jobs} jobs.")
    print(f"Downloading {total_pages} pages.\n")

    # Process the first page immediately.
    append_jobs(data)

    # ============================================================
    # DOWNLOAD THE REMAINING PAGES
    # ============================================================

    for page_number in range(1, total_pages):

        payload["pageNumber"] = page_number

        response = requests.post(IDB_JOBS_URL, json=payload)

        data = response.json()

        print(f"Downloading page {page_number + 1}...")

        append_jobs(data)

    # Return the complete job list to the main program.
    return jobs

