import os
import time
import json
import hashlib
import requests
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv
from scrapers.scrapper_interface import LinkedInScraper

load_dotenv()

class BrightDataScraper(LinkedInScraper):
    def __init__(self):
        self.api_key = os.getenv("BRIGHTDATA_API_KEY")
        self.dataset_id = os.getenv("BRIGHTDATA_DATASET_ID")
        self.polling_interval = int(os.getenv("BRIGHTDATA_POLL_INTERVAL", 3))
        self.max_timeout = int(os.getenv("BRIGHTDATA_TIMEOUT", 120))
        self.cache_dir = os.getenv("BRIGHTDATA_CACHE_DIR", "data/fetched_json")

        if not self.api_key or not self.dataset_id:
            raise EnvironmentError("BRIGHTDATA_API_KEY or BRIGHTDATA_DATASET_ID is missing")

        self.trigger_endpoint = "https://api.brightdata.com/datasets/v3/trigger"
        self.progress_endpoint_template = "https://api.brightdata.com/datasets/v3/progress/{snapshot_id}"
        self.data_url_template = "https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format=json"

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        os.makedirs(self.cache_dir, exist_ok=True)

    def scrape(self, linkedin_url: str) -> Dict:
        if not linkedin_url or "linkedin.com/in/" not in linkedin_url:
            raise ValueError(f"Invalid LinkedIn URL: '{linkedin_url}'")

        cache_path = self._url_to_cache_path(linkedin_url)

        if os.path.exists(cache_path):
            print(f"📁 Using cached data for {linkedin_url}")
            with open(cache_path, "r", encoding="utf-8") as f:
                cached = json.load(f)
                profile = cached.get("data", {})
        else:
            snapshot_id = self._trigger_snapshot(linkedin_url)
            self._wait_until_snapshot_ready(snapshot_id)
            profile = self._fetch_snapshot_data(snapshot_id)

            cached = {
                "scraper": "brightdata",
                "fetched_at": datetime.utcnow().isoformat() + "Z",
                "url": linkedin_url,
                "data": profile
            }

            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cached, f, ensure_ascii=False, indent=2)
            print(f"✅ Cached snapshot JSON: {cache_path}")

        return self._extract_profile(profile)

    def _url_to_cache_path(self, linkedin_url: str) -> str:
        slug = hashlib.md5(linkedin_url.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"brightdata_{slug}.json")

    def _trigger_snapshot(self, linkedin_url: str) -> str:
        params = {"dataset_id": self.dataset_id, "include_errors": "true"}
        data = [{"url": linkedin_url}]
        resp = requests.post(self.trigger_endpoint, headers=self.headers, params=params, json=data)
        resp.raise_for_status()
        snapshot_id = resp.json().get("snapshot_id")
        if not snapshot_id:
            raise ValueError(f"No snapshot_id returned: {resp.json()}")
        print(f"⏳ Snapshot triggered: {snapshot_id}")
        return snapshot_id

    def _wait_until_snapshot_ready(self, snapshot_id: str):
        url = self.progress_endpoint_template.format(snapshot_id=snapshot_id)
        start = time.time()
        while True:
            elapsed = time.time() - start
            if elapsed > self.max_timeout:
                raise TimeoutError(f"⏱️ Timeout: snapshot {snapshot_id} not ready after {self.max_timeout} seconds")
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                state = resp.json().get("status")
                print(f"📶 Snapshot {snapshot_id} status: {state} (after {int(elapsed)}s)")
                if state == "ready":
                    return
            elif resp.status_code == 202:
                print(f"⌛ Waiting... ({int(elapsed)}s)")
            else:
                print(f"⚠️ Unexpected polling response: {resp.status_code}")
            time.sleep(self.polling_interval)
    """
    def _fetch_snapshot_data(self, snapshot_id: str) -> Dict:
        url = self.data_url_template.format(snapshot_id=snapshot_id)
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            batch = data[0] if data and isinstance(data[0], list) else data
            if batch and isinstance(batch[0], dict):
                print(f"✅ Data received from snapshot {snapshot_id}")
                return batch[0]
        raise ValueError(f"❌ Unexpected snapshot format for {snapshot_id}")
    """
    def _fetch_snapshot_data(self, snapshot_id: str) -> Dict:
        url = self.data_url_template.format(snapshot_id=snapshot_id)
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and data and isinstance(data[0], dict):
            print(f"✅ Data received from snapshot {snapshot_id}")
            return data[0]
        raise ValueError(f"❌ Unexpected snapshot format for {snapshot_id}: {type(data)}")

    def _extract_profile(self, profile: Dict) -> Dict:
        summary = (
            profile.get("about")
            or (profile.get("recommendations") or [None])[0]
            or ""
        )

        current = profile.get("current_company", {})
        title = current.get("title", "")
        company = current.get("name", "")
        headline = f"{title} at {company}".strip() if title or company else ""

        return {
            "summary": summary,
            "headline": headline,
            "experience": []
        }
