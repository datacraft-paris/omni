# utils/linkedin_scrapper_adapter.py
import os

SCRAPER_TYPE = os.getenv("SCRAPER_TYPE", "mock")  # 'mock' ou 'proxycurl'

if SCRAPER_TYPE == "proxycurl":
    from utils.proxycurl_scraper import ProxycurlScraper as ActiveScraper
else:
    from utils.mock_scraper import MockScraper as ActiveScraper

scraper = ActiveScraper()

def scrape_linkedin_profile(linkedin_url: str):
    return scraper.scrape(linkedin_url)
