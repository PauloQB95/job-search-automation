from pathlib import Path
import sys

import pandas as pd

from buscar_bid import fetch_idb_jobs
from buscar_bm import fetch_world_bank_jobs
from buscar_un import fetch_united_nations_jobs
from buscar_adb import fetch_asian_development_bank_jobs


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

    # Run the scrapers independently.
    idb_jobs = run_scraper_safely(
        organization_name="IDB",
        scraper_function=fetch_idb_jobs
    )

    world_bank_jobs = run_scraper_safely(
        organization_name="World Bank",
        scraper_function=fetch_world_bank_jobs
    )

    united_nations_jobs = run_scraper_safely(
        organization_name="United Nations System",
        scraper_function=fetch_united_nations_jobs
    )

    asian_development_bank_jobs = run_scraper_safely(
        organization_name="Asian Development Bank",
        scraper_function=fetch_asian_development_bank_jobs
    )

    # Combine results.
    jobs = []

    jobs.extend(idb_jobs)
    jobs.extend(world_bank_jobs)
    jobs.extend(united_nations_jobs)
    jobs.extend(asian_development_bank_jobs)

    # --------------------------------------------------------
    # Both scrapers failed or returned no results
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

    jobs_dataframe = pd.DataFrame(jobs)

    # Create a temporary file first.
    temporary_excel_path = (
        OUTPUT_DIRECTORY /
        "consolidated_jobs_temporary.xlsx"
    )

    jobs_dataframe.to_excel(
        temporary_excel_path,
        index=False
    )

    # Replace the previous Excel file only after creating the temporary file.
    temporary_excel_path.replace(EXCEL_OUTPUT_PATH)

    print("\n" + "=" * 60)
    print("DOWNLOAD COMPLETE")
    print("=" * 60)

    print(f"Total: {len(jobs_dataframe)} jobs.")
    print(f"IDB: {len(idb_jobs)} jobs.")
    print(f"World Bank: {len(world_bank_jobs)} jobs.")
    print(f"United Nations System: {len(united_nations_jobs)} jobs.")
    print(f"Asian Development Bank: {len(asian_development_bank_jobs)} jobs.")
    print(f"File created at: {EXCEL_OUTPUT_PATH}")

    return 0


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
