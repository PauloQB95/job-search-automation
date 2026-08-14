"""Ordered scraper configuration used by the application entry point."""

from buscar_adb import fetch_asian_development_bank_jobs
from buscar_bid import fetch_idb_jobs
from buscar_bm import fetch_world_bank_jobs
from buscar_un import fetch_united_nations_jobs


SCRAPERS = (
    ("IDB", fetch_idb_jobs),
    ("World Bank", fetch_world_bank_jobs),
    ("United Nations System", fetch_united_nations_jobs),
    ("Asian Development Bank", fetch_asian_development_bank_jobs),
)
