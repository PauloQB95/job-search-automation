# Job Search Automation

## Overview

Job Search Automation is a Python project that automatically collects job opportunities from international organizations through their public APIs or career portals.

The project is designed with a modular architecture so that new organizations can be incorporated without modifying the main workflow.

Current implementation includes the Inter-American Development Bank (IDB), with future support planned for organizations such as the World Bank, CAF, the United Nations, and other institutions.

The project exports the collected information into Excel files for further analysis and filtering.

---

## Motivation

Searching for opportunities across multiple international organizations is a repetitive and time-consuming process.

This project automates that workflow by retrieving vacancies directly from official sources and consolidating them into a structured dataset.

Besides its practical purpose, the project serves as an exercise in software design, API consumption, data processing, and Python programming.

---

## Current Features

- Retrieve job vacancies from the IDB Careers API.
- Automatically download all available pages.
- Extract relevant vacancy information.
- Export results to Excel.
- Modular project structure.
- Version controlled with Git.

---

## Project Structure

```text
Job_Search_Project/

│

├── main.py                 # Main application

├── buscar_bid.py           # IDB job collector

├── README.md

├── requirements.txt

├── .gitignore

│

├── datos/

└── resultados/
```

---

## Technologies

- Python
- Requests
- Pandas
- OpenPyXL
- Git

---

## Installation

Clone the repository:

```bash
git clone <repository_url>
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the main application:

```bash
python main.py
```

The program will download all available IDB vacancies and generate an Excel file inside the `resultados/` directory.

---

## Roadmap

Current progress:

- ✅ IDB
- ⬜ World Bank
- ⬜ CAF
- ⬜ United Nations
- ⬜ OECD
- ⬜ Custom keyword filters
- ⬜ Job relevance scoring
- ⬜ Configuration file
- ⬜ Automatic scheduled execution

---

## Learning Goals

This project is being developed as part of a structured learning process focused on:

- Python programming
- API integration
- Data processing
- Software architecture
- Version control with Git
- GitHub workflow

---

## Author

Paulo Quequezana