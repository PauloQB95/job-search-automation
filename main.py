from pathlib import Path
import sys

import pandas as pd

from job_schema import JOB_COLUMNS
from output_generator import WEBSITE_DATA_PATH, write_excel_workbook, write_website_data
from scraper_registry import SCRAPERS


# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_DIRECTORY = Path("results")
EXCEL_OUTPUT_PATH = OUTPUT_DIRECTORY / "consolidated_jobs.xlsx"


# ============================================================
# RUN A SCRAPER SAFELY
# ============================================================

def run_scraper_safely(organization_name, scraper_function):
    """
    Run a scraper without allowing an error to stop the entire program.

    Parameters
    ----------
    organization_name : str
        Name of the organization.

    scraper_function : function
        Function that runs the scraper.

    Returns
    -------
    list
        List of jobs found.

        If the scraper fails or returns an invalid value, return an empty list.
    """

    print("\n" + "=" * 60)
    print(f"Starting scraper: {organization_name}")
    print("=" * 60)

    try:
        jobs = scraper_function()

        if not isinstance(jobs, list):
            print(
                f"Warning: {organization_name} did not return a valid list."
            )
            return []

        print(
            f"{organization_name}: found "
            f"{len(jobs)} jobs."
        )

        return jobs

    except Exception as error:
        print(f"The {organization_name} scraper failed.")
        print(f"Error type: {type(error).__name__}")
        print(f"Details: {error}")
        print("The program will continue with the remaining sources.")

        return []


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():
    """
    Run all scrapers, combine their results, and create the consolidated Excel file.

    Returns
    -------
    int
        0 if the Excel file was created successfully.
        1 if no jobs were retrieved.
    """

    # Run scrapers independently and combine their results in registry order.
    jobs = []
    scraper_results = {}

    for organization_name, scraper_function in SCRAPERS:
        organization_jobs = run_scraper_safely(
            organization_name=organization_name,
            scraper_function=scraper_function
        )
        scraper_results[organization_name] = organization_jobs
        jobs.extend(organization_jobs)

    # --------------------------------------------------------
    # No scraper returned results
    # --------------------------------------------------------

    if not jobs:
        print("\n" + "=" * 60)
        print("NO NEW FILE WAS GENERATED")
        print("=" * 60)

        print("No scraper returned any results.")
        print(
            "The previous Excel file, if it exists, will remain unchanged."
        )

        # Exit code 1 makes GitHub Actions treat this run as failed.
        return 1

    # --------------------------------------------------------
    # Create the new Excel file
    # --------------------------------------------------------

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    jobs_dataframe = pd.DataFrame(jobs, columns=JOB_COLUMNS)

    # Create a temporary file first.
    temporary_excel_path = (
        OUTPUT_DIRECTORY /
        "consolidated_jobs_temporary.xlsx"
    )

    write_excel_workbook(jobs_dataframe, temporary_excel_path)

    temporary_website_data_path = WEBSITE_DATA_PATH.with_name(
        "job_data_temporary.json"
    )
    WEBSITE_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_website_data(scraper_results, temporary_website_data_path)

    # Replace the previous Excel file only after creating the temporary file.
    temporary_excel_path.replace(EXCEL_OUTPUT_PATH)
    temporary_website_data_path.replace(WEBSITE_DATA_PATH)

    print("\n" + "=" * 60)
    print("DOWNLOAD COMPLETE")
    print("=" * 60)

    print(f"Total: {len(jobs_dataframe)} jobs.")

    for organization_name, _ in SCRAPERS:
        print(
            f"{organization_name}: "
            f"{len(scraper_results[organization_name])} jobs."
        )

    print(f"File created at: {EXCEL_OUTPUT_PATH}")

    return 0


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
