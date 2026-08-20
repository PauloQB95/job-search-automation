import math

import requests

from job_schema import create_job


# ============================================================
# CONFIGURATION
# ============================================================

def fetch_united_nations_jobs():
    """Retrieve all available jobs from the United Nations System portal."""

    UNITED_NATIONS_JOBS_URL = "https://onehr.un.org/ja/api/JobData/list"
    JOBS_PER_PAGE = 20

    payload = {
        "filter": "",
        "filterAttributes": {
            "dutyStation": []
        },
        "sortByTitle": {
            "name": "Title Ascending",
            "value": "Title",
            "order": 1
        },
        "pagination": {
            "page": 0,
            "itemPerPage": JOBS_PER_PAGE,
            "sortBy": "startDate",
            "sortDirection": -1
        }
    }

    jobs = []

    def request_page(page_number):
        """Request and validate one page of United Nations job data."""

        payload["pagination"]["page"] = page_number

        response = requests.post(UNITED_NATIONS_JOBS_URL, json=payload)
        response.raise_for_status()

        try:
            page_data = response.json()
        except ValueError as error:
            raise RuntimeError(
                "The United Nations jobs endpoint returned invalid JSON."
            ) from error

        if not isinstance(page_data, dict):
            raise RuntimeError(
                "The United Nations jobs endpoint returned an invalid response."
            )

        if not isinstance(page_data.get("result"), list):
            raise RuntimeError(
                "The United Nations jobs endpoint did not return a job list."
            )

        return page_data

    def append_jobs(page_data):
        """Map one page of United Nations jobs to the shared Excel schema."""

        for job_data in page_data["result"]:
            organization_name = job_data.get("Department", "")

            job = create_job(
                organization=(
                    f"UN - {organization_name}"
                    if organization_name
                    else ""
                ),
                job_title=job_data.get("Title", ""),
                location=job_data.get("DutyStation", ""),
                posting_date=job_data.get("InsertDate", ""),
                closing_date=job_data.get("EndDate", ""),
                job_type=job_data.get("Level", ""),
                job_id=job_data.get("JobId", ""),
                application_url=job_data.get("Link", ""),
                source="United Nations System website"
            )

            jobs.append(job)

    # ============================================================
    # DOWNLOAD THE FIRST PAGE
    # ============================================================

    first_page_data = request_page(page_number=0)
    total_jobs = first_page_data.get("count")

    if not isinstance(total_jobs, int) or isinstance(total_jobs, bool):
        raise RuntimeError(
            "The United Nations jobs endpoint returned an invalid job count."
        )

    total_pages = math.ceil(total_jobs / JOBS_PER_PAGE)

    print(f"Found {total_jobs} jobs.")
    print(f"Downloading {total_pages} pages.\n")

    append_jobs(first_page_data)

    # ============================================================
    # DOWNLOAD THE REMAINING PAGES
    # ============================================================

    for page_number in range(1, total_pages):
        page_data = request_page(page_number)

        print(f"Downloading page {page_number + 1}...")

        append_jobs(page_data)

    return jobs
