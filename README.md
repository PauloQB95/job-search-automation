# Automated International Development Job Opportunity Aggregator

## Project Overview

This project collects current job opportunities from selected international
development organizations through their official employment platforms. It
standardizes the available information and generates a consolidated Excel
workbook for easier review.

The project is designed as a practical job-discovery tool. It does not replace
the organizations' official career websites, and it does not guarantee that
every available vacancy is captured.

## Current Data Sources

The project currently collects opportunities from:

- Inter-American Development Bank (IDB)
- World Bank

## Main Features

- Automated collection from multiple official employment platforms
- Independent execution of each scraper so one source can succeed if another
  fails
- Consolidated Excel output
- A standardized English column structure across all sources
- Daily execution through GitHub Actions
- Publication of successful outputs through GitHub Releases
- A public GitHub Pages download page
- Preservation of the latest valid Excel file and Release when an update fails

## Architecture

The automated publishing flow is:

```text
GitHub Actions
    → Python scrapers
    → Consolidated Excel workbook
    → GitHub Release
    → GitHub Pages download link
```

The IDB scraper requests job data directly from the organization's employment
API. The World Bank scraper uses Playwright to open the official careers portal,
capture the authorization header used by the portal, and then request job data
from the employment API.

`main.py` runs both scrapers independently, combines valid results, and writes
the consolidated workbook.

## Repository Structure

```text
job-search-automation/
├── .github/
│   └── workflows/
│       └── actualizar_trabajos.yml   # Daily and manual automation
├── docs/
│   ├── index.html                    # GitHub Pages download page
│   └── styles.css                    # Public website styles
├── results/                          # Generated Excel output
│   └── consolidated_jobs.xlsx        # Created at runtime; not tracked
├── autenticacion_bm.py               # World Bank token capture
├── buscar_bid.py                     # IDB job scraper
├── buscar_bm.py                      # World Bank job scraper
├── main.py                           # Application entry point
├── requirements.txt                  # Python dependencies
├── .gitignore
└── README.md
```

The `results/` directory is created automatically when the application
successfully produces output. Generated `.xlsx` files are excluded from version
control.

## Excel Output

The application writes the consolidated workbook to:

```text
results/consolidated_jobs.xlsx
```

The workbook uses the following columns in this exact order:

1. `Organization`
2. `Job Title`
3. `Location`
4. `Country`
5. `Posting Date`
6. `Closing Date`
7. `Job Type`
8. `Job ID`
9. `Description`
10. `Application URL`
11. `Source`

Values are preserved from the official source data used by each scraper.
Fields that are not available from a source may be empty.

## Failure Protection

The application is designed to avoid replacing a valid workbook with an empty
or failed result:

- Each scraper runs independently.
- One scraper may return valid results even if another scraper fails.
- A new workbook is generated when at least one scraper returns a valid,
  non-empty result list.
- If no scraper returns valid results, the application exits with a non-zero
  status code.
- The previous local workbook, if present, remains unchanged when no valid
  results are returned.
- GitHub Actions stops after a failed application run and does not publish a new
  Release.
- The most recent valid GitHub Release therefore remains available.

The application first writes a temporary workbook and replaces the final file
only after the temporary file has been created successfully.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/PauloQB95/job-search-automation.git
cd job-search-automation
```

### 2. Create and activate a Python environment

Creating an isolated environment is recommended.

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Install Chromium for Playwright

```bash
python -m playwright install chromium
```

On supported Linux environments where Playwright must also install system
packages, use:

```bash
python -m playwright install --with-deps chromium
```

No API token or private environment configuration is required by the current
application.

## Local Execution

Run the application from the repository root:

```bash
python main.py
```

When at least one scraper returns valid results, the workbook will appear at:

```text
results/consolidated_jobs.xlsx
```

A run depends on access to the organizations' external employment platforms and
may take additional time while Playwright opens the World Bank careers portal.

## Automated Execution

The GitHub Actions workflow runs once per day. It can also be started manually
from the repository's **Actions** tab using the `workflow_dispatch` trigger.

On a successful run, the workflow verifies that
`results/consolidated_jobs.xlsx` exists and publishes it in a new GitHub
Release. If the application exits with a failure status, the workflow stops
before creating a Release.

## Public Website

The public download page is available at:

<https://pauloqb95.github.io/job-search-automation/>

Visitors can download the latest valid Excel workbook without installing
software or creating an account.

## Direct Download

The latest valid Release asset is available through this permanent URL:

<https://github.com/PauloQB95/job-search-automation/releases/latest/download/consolidated_jobs.xlsx>

## Technologies

- Python
- Requests
- Pandas
- OpenPyXL
- Playwright
- HTML and CSS
- GitHub Actions
- GitHub Releases
- GitHub Pages

## Limitations

- Availability depends on the external employment platforms.
- Source APIs, authentication behavior, or page structures may change without
  notice and can interrupt collection.
- Job information should always be verified in the official posting.
- The project does not guarantee that every available vacancy is captured.
- Fields unavailable from a source may be empty in the workbook.
- Updates occur on a daily schedule, not in real time.
- This project is independent and is not affiliated with or endorsed by the
  Inter-American Development Bank or the World Bank.

## Roadmap

Possible future improvements include:

- Support for additional international development organizations
- Metadata showing the last successful update
- Filters by location, organization, or job type
- Automated validation and broader test coverage
- Improved monitoring and reporting of scraper failures

These items are possibilities rather than committed delivery dates.

## Disclaimer

Job data originates from the organizations' official employment platforms.
Users should verify titles, locations, deadlines, requirements, and other
details in the official job posting and apply through the official application
link.
