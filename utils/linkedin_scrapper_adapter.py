from lipopulate.utils.proxy_utils import fetch_profile, make_api_request, fetch_profile_by_details
from typing import Dict
import os

def scrape_linkedin_profile(linkedin_url: str) -> Dict:
    headers = {"Authorization": f"Bearer {os.getenv('PROXYCURL_API_KEY')}"}
    raw_data = fetch_profile(linkedin_url, headers)
    
    if not raw_data:
        raise ValueError("LinkedIn scraping failed or profile not found.")

    # Adapt to your LinkedInProfile schema
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
