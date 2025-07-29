# src/scrapers/linkedin_api_scraper.py
from linkedin_api import Linkedin
from scrapers.scrapper_interface import LinkedInScraper

class LinkedInApiScraper(LinkedInScraper):
    def __init__(self, li_at_cookie: str):
        if not li_at_cookie:
            raise ValueError("Missing LinkedIn session cookie (li_at).")

        try:
            self.api = Linkedin(cookie_li_at=li_at_cookie)
        except Exception as e:
            raise RuntimeError(f"Failed to authenticate with LinkedIn using cookie: {e}")

    def scrape(self, public_identifier: str):
        try:
            profile = self.api.get_profile(public_identifier)

            experiences = profile.get("experience", []) or []
            formatted_exp = [
                {
                    "title": exp.get("title", ""),
                    "company": exp.get("companyName", "")
                }
                for exp in experiences
                if exp.get("title") and exp.get("companyName")
            ]

            return {
                "summary": profile.get("summary", ""),
                "headline": profile.get("headline", ""),
                "experience": formatted_exp
            }

        except Exception as e:
            raise ValueError(f"Failed to fetch profile for '{public_identifier}': {e}")
