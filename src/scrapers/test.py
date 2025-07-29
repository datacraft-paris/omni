import os
import requests
from dotenv import load_dotenv

load_dotenv()  # ⬅️ Obligatoire pour charger .env dans os.environ

print("API KEY from env:", os.getenv("BRIGHTDATA_API_KEY"))

headers = {
    "Authorization": f"Bearer {os.getenv('BRIGHTDATA_API_KEY')}",
    "Content-Type": "application/json",
}

payload = {"input": [{"url": "https://www.linkedin.com/in/arthurcornelio/"}]}
res = requests.post("https://api.brightdata.com/datasets/v3/scrape", headers=headers, json=payload)

print("Response status:", res.status_code)
print("Response text:", res.text)

###

import requests

url = "https://api.brightdata.com/datasets/v3/trigger"
headers = {
	"Authorization": "Bearer a2335020549d122ce38a71be8e5ba44283ced3ae94c8f90fd6fe567ad969a0f2",
	"Content-Type": "application/json",
}
params = {
	"dataset_id": "gd_l1viktl72bvl7bjuj0",
	"include_errors": "true",
}
data = [
	{"url":"https://www.linkedin.com/in/elad-moshe-05a90413/"},
	{"url":"https://www.linkedin.com/in/jonathan-myrvik-3baa01109"},
	{"url":"https://www.linkedin.com/in/aviv-tal-75b81/"},
	{"url":"https://www.linkedin.com/in/bulentakar/"},
]

response = requests.post(url, headers=headers, params=params, json=data)
print(response.json())