# utils/mock_scraper.py
from utils.scrapper_interface import LinkedInScraper

class MockScraper(LinkedInScraper):
    def scrape(self, linkedin_url: str):
        return {
            "summary": f"Mock summary for {linkedin_url}",
            "headline": "Senior Software Engineer",
            "experience": [
                {"title": "Software Engineer", "company": "MockCorp"},
                {"title": "Tech Lead", "company": "Example Inc."}
            ]
        }
