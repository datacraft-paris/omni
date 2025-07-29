# utils/proxycurl_scraper.py
import os
from typing import Dict
from utils.proxy_utils import fetch_profile
from utils.scrapper_interface import LinkedInScraper

class ProxycurlScraper(LinkedInScraper):
    def scrape(self, linkedin_url: str) -> Dict:
        headers = {"Authorization": f"Bearer {os.getenv('PROXYCURL_API_KEY')}"}
        raw_data = fetch_profile(linkedin_url, headers)

        if not raw_data:
            raise ValueError("LinkedIn scraping failed or profile not found.")

        summary = raw_data.get("summary", "")
        headline = raw_data.get("occupation", "")
        experiences_raw = raw_data.get("experience", [])

        experience = []
        for exp in experiences_raw:
            if "title" in exp and "company" in exp:
                experience.append({
                    "title": exp["title"],
                    "company": exp["company"].get("name", "")
                })

        return {
            "summary": summary,
            "headline": headline,
            "experience": experience
        }
