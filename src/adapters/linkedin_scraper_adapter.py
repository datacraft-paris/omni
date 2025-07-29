# src/adapters/linkedin_scrapper_adapter.py
import os

SCRAPER_TYPE = os.getenv("SCRAPER_TYPE", "mock")

if SCRAPER_TYPE == "proxycurl":
    from scrapers.proxycurl_scraper import ProxycurlScraper as ActiveScraper
    scraper = ActiveScraper()

elif SCRAPER_TYPE == "linkedin_api":
    from scrapers.linkedin_api_scraper import LinkedInApiScraper as ActiveScraper
    li_at_cookie = os.getenv("LINKEDIN_LI_AT")
    scraper = ActiveScraper(li_at_cookie)

else:
    from scrapers.mock_scraper import MockScraper as ActiveScraper
    scraper = ActiveScraper()


def scrape_linkedin_profile(linkedin_url: str):
    # Extract public identifier from LinkedIn URL
    public_id = linkedin_url.rstrip("/").split("/")[-1]
    return scraper.scrape(public_id)
