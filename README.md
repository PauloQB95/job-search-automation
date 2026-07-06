# Job Search Automation

## Overview

Job Search Automation is a Python application that automates the collection of job opportunities from international organizations using their official career APIs.

The project was developed as part of my Python and software engineering learning journey while building a practical tool to support my own international job search in policy analysis, economics, data analysis, infrastructure, and international development.

Rather than manually visiting dozens of career websites every day, the goal is to collect opportunities automatically, standardize the information, and export it into a format that is easy to review.

---

## Current Features

* Retrieve job opportunities from the **Inter-American Development Bank (IDB)** Careers API.
* Retrieve job opportunities from the **World Bank** Careers API.
* Automatic pagination for organizations that publish vacancies across multiple pages.
* Standardized job data model across organizations.
* Export results to Excel.
* Secure credential management using environment variables.
* Modular architecture designed for future expansion.
* Version control using Git and GitHub.

---

## Technologies

* Python
* Requests
* Pandas
* OpenPyXL
* python-dotenv
* Git
* GitHub

---

## Project Structure

```text
job-search-automation/

│
├── buscar_bid.py          # IDB job scraper
├── buscar_bm.py           # World Bank job scraper
├── main.py                # Main execution script
│
├── resultados/            # Generated Excel files
│
├── .env.example           # Example environment variables
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/PauloQB95/job-search-automation.git
```

Move into the project folder:

```bash
cd job-search-automation
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```text
.env
```

Copy the contents of:

```text
.env.example
```

into:

```text
.env
```

and replace the placeholder values with your own credentials.

Run the project:

```bash
python main.py
```

---

## Security

Sensitive credentials are **not stored in the repository**.

The project uses environment variables (`.env`) to securely manage authentication tokens required by some APIs.

---

## Current Architecture

Each organization is implemented as an independent module.

Each scraper is responsible for:

1. Connecting to its API.
2. Downloading all available pages.
3. Converting the organization's JSON structure into a standardized Python dictionary.
4. Returning a list of job postings.

This architecture allows new organizations to be incorporated with minimal changes to the rest of the project.

---

## Roadmap

### Completed

* ✅ IDB scraper
* ✅ World Bank scraper
* ✅ Automatic pagination
* ✅ Excel export
* ✅ GitHub integration
* ✅ Environment variable support

### Planned

* ⬜ Refactor common API functionality
* ⬜ CAF scraper
* ⬜ United Nations scraper
* ⬜ OECD scraper
* ⬜ Keyword-based filtering
* ⬜ Job relevance scoring
* ⬜ Automated daily execution
* ⬜ Email notifications

---

## What I Learned

This project has allowed me to strengthen practical software engineering skills, including:

* Working with REST APIs
* Processing JSON responses
* Handling API authentication
* Managing pagination
* Designing modular Python applications
* Managing dependencies
* Using Git and GitHub
* Debugging real-world software issues

---

## Motivation

As a public policy graduate interested in economic development, infrastructure, data analysis, and evidence-based policymaking, I wanted to build a practical application that solves a real problem while strengthening my programming skills.

This project combines both goals: improving my software engineering abilities while creating a tool that supports my own international job search.

## Author

Paulo Quequezana
