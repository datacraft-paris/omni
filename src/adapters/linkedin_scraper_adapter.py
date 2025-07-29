# src/adapters/linkedin_scrapper_adapter.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

SCRAPER_TYPE = os.getenv("SCRAPER_TYPE", "mock")

if SCRAPER_TYPE == "proxycurl":
    from scrapers.proxycurl_scraper import ProxycurlScraper as ActiveScraper
    scraper = ActiveScraper()
    def format_url(linkedin_url: str) -> str:
        return linkedin_url.rstrip("/").split("/")[-1]  # public_id

elif SCRAPER_TYPE == "linkedin_api":
    from scrapers.linkedin_api_scraper import LinkedInApiScraper as ActiveScraper
    li_at_cookie = os.getenv("LINKEDIN_LI_AT")
    scraper = ActiveScraper(li_at_cookie)
    def format_url(linkedin_url: str) -> str:
        return linkedin_url.rstrip("/").split("/")[-1]  # public_id

elif SCRAPER_TYPE == "brightdata":
    from scrapers.brightdata_scraper import BrightDataScraper as ActiveScraper
    scraper = ActiveScraper()
    def format_url(linkedin_url: str) -> str:
        return linkedin_url.strip()  # full URL, no transformation

else:
    from scrapers.mock_scraper import MockScraper as ActiveScraper
    scraper = ActiveScraper()
    def format_url(linkedin_url: str) -> str:
        return linkedin_url.rstrip("/").split("/")[-1]  # fallback to ID


def scrape_linkedin_profile(linkedin_url: str):
    formatted = format_url(linkedin_url)
    return scraper.scrape(formatted)
