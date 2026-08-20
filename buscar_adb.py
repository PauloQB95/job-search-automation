import re

import requests
from bs4 import BeautifulSoup

from job_schema import create_job


# ============================================================
# CONFIGURATION
# ============================================================

ADB_CURRENT_OPPORTUNITIES_URL = (
    "https://www.adb.org/work-with-us/careers/current-opportunities"
)
REQUEST_TIMEOUT_SECONDS = 30
HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
INCLUDED_TABLE_CAPTIONS = {
    "Managerial International",
    "Technical International",
    "Technical Local (Headquarters)",
    "Technical Local (Field Offices)",
}
JOB_REFERENCE_PATTERN = re.compile(r"\s*/\s*(\d+)\s*$")


def fetch_asian_development_bank_jobs():
    """Retrieve current eligible job opportunities from the ADB careers page."""

    try:
        response = requests.get(
            ADB_CURRENT_OPPORTUNITIES_URL,
            headers=HTTP_HEADERS,
            timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
    except requests.RequestException as error:
        response_status = getattr(error.response, "status_code", None)
        status_details = (
            f" (HTTP status {response_status})"
            if response_status is not None
            else ""
        )

        raise RuntimeError(
            "Could not retrieve the Asian Development Bank careers page"
            f"{status_details}."
        ) from error

    soup = BeautifulSoup(response.text, "html.parser")
    table_captions = {
        caption.get_text(" ", strip=True)
        for caption in soup.find_all("caption")
    }

    if not table_captions.intersection(INCLUDED_TABLE_CAPTIONS):
        raise RuntimeError(
            "The Asian Development Bank careers page did not contain the "
            "expected current-opportunity tables."
        )

    jobs = []
    seen_job_references = set()

    for table in soup.find_all("table"):
        caption = table.find("caption")

        if caption is None:
            continue

        table_caption = caption.get_text(" ", strip=True)

        if table_caption not in INCLUDED_TABLE_CAPTIONS:
            continue

        for row in table.find_all("tr"):
            job_link = row.find("a", href=True)

            if job_link is None:
                continue

            job_title_with_reference = job_link.get_text(" ", strip=True)
            job_reference_match = JOB_REFERENCE_PATTERN.search(
                job_title_with_reference
            )

            if job_reference_match is None:
                continue

            job_reference = job_reference_match.group(1)

            if job_reference in seen_job_references:
                continue

            job_title = JOB_REFERENCE_PATTERN.sub(
                "",
                job_title_with_reference
            ).strip()

            if not job_title:
                continue

            posting_date_element = row.select_one(
                "td.views-field-field-date-content time"
            )
            closing_date_element = row.select_one(
                "td.views-field-field-date-closing time"
            )

            organization_name = get_cell_text(
                row,
                "td.views-field-field-department"
            )

            job = create_job(
                organization=(
                    f"ADB - {organization_name}"
                    if organization_name
                    else ""
                ),
                job_title=job_title,
                location=get_cell_text(
                    row,
                    "td.views-field-field-location"
                ),
                posting_date=get_element_text(posting_date_element),
                closing_date=get_element_text(closing_date_element),
                job_type=get_cell_text(
                    row,
                    "td.views-field-field-position"
                ),
                job_id=job_reference,
                application_url=job_link["href"].strip(),
                source="Asian Development Bank website"
            )

            jobs.append(job)
            seen_job_references.add(job_reference)

    return jobs


def get_cell_text(row, selector):
    """Return normalized text from a table cell, or an empty string."""

    return get_element_text(row.select_one(selector))


def get_element_text(element):
    """Return normalized text from an HTML element, or an empty string."""

    if element is None:
        return ""

    return element.get_text(" ", strip=True)
