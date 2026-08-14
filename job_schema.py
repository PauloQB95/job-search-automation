"""Shared job record structure for every organization scraper."""

JOB_COLUMNS = (
    "Organization",
    "Job Title",
    "Location",
    "Country",
    "Posting Date",
    "Closing Date",
    "Job Type",
    "Job ID",
    "Description",
    "Application URL",
    "Source",
)


def create_job(
    organization,
    job_title,
    location="",
    country="",
    posting_date="",
    closing_date="",
    job_type="",
    job_id="",
    description="",
    application_url="",
    source=""
):
    """Build a job record using the shared Excel schema and column order."""

    return {
        "Organization": organization,
        "Job Title": job_title,
        "Location": location,
        "Country": country,
        "Posting Date": posting_date,
        "Closing Date": closing_date,
        "Job Type": job_type,
        "Job ID": job_id,
        "Description": description,
        "Application URL": application_url,
        "Source": source,
    }
