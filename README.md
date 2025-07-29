# Omni LinkedIn Enrichment Pipeline

This project enriches people data from a CSV (e.g. Airtable export) using LinkedIn profiles and LLM-generated summaries & interests. It supports scrapers like **BrightData**, includes local caching to reduce costs, and allows LLM or manual processing.

---

## ⚙️ Setup

### 1. Install dependencies

Install via [`uv`](https://github.com/astral-sh/uv):

```bash
uv sync
source .venv/bin/activate
```

> 💡 Make sure your `.venv` is already created (`uv venv` not required in this repo).

---

### 2. Configure your environment

Copy the `.env` example and edit it with your API keys:

```bash
cp .env.example .env
```

You’ll need to set your **scraper** (e.g. BrightData), your **OpenAI/Gemini keys**, and optionally Airtable parameters (not yet used automatically).

See `.env.example` for all fields.

---

### 3. Prepare your CSV input

Export your Airtable manually to:

```
data/airtable_export.csv
```

The file should look like:

```csv
Prénom,Nom,Email,Organisation,Titre,Métier,Intérêt,Domain,Tags,Statut,Description,Linkedin
Alice,Dupont,alice@example.com,Acme Corp,Lead AI,data scientist,,Tech,,Member,,https://www.linkedin.com/in/alice-dupont/
Bob,Martin,bob@example.org,Omnitech,ML Ops Engineer,mlops engineer,,Tech,,Pending,,https://www.linkedin.com/in/bob-martin/
```

✅ **If `Linkedin` URL is missing**, the script will fall back to job title/domain for enrichment only.

---

## 🚀 Enrichment Options

### Option 1 – Full batch CSV enrichment

```bash
python src/enrich_from_csv.py
```

This will:

* Read `data/airtable_export.csv`
* Scrape and cache LinkedIn data
* Generate `Intérêt` and `Description` using manual or LLM-based logic
* Output to `data/enriched_output.csv`
* Cache raw LinkedIn JSON to `data/fetched_json/`

---

### Option 2 – Try the flow manually

```bash
python src/main.py [manual|llm]
```

Run a single test profile through the logic:

```bash
python src/main.py llm
```

Uses a hardcoded profile with `"summary"`, `"headline"`, and `"experience"` to demonstrate tag extraction & description generation.

---

## 📁 Project Structure

```
data/
  airtable_export.csv             ← CSV input (manual download from Airtable)
  enriched_output.csv             ← Enriched output
  fetched_json/                   ← Cached LinkedIn snapshot data (JSON)

src/
  enrich_from_csv.py              ← Main pipeline runner
  main.py                         ← Manual test run for a single profile
  adapters/
    linkedin_scraper_adapter.py   ← Dynamic scraper loader
  scrapers/
    brightdata_scraper.py         ← BrightData implementation
  core/
    pipeline.py                   ← LLM logic and tag generation
    schema.py                     ← Pydantic validation schemas
    static_values.py              ← Constants and allowed interest tags
  services/
    llm_interface.py              ← Interface for OpenAI or Gemini
    tag_description_builder.py    ← Manual rule-based tag system
  utils/
    crud.py                       ← Helper to flatten LinkedIn data
```

---

## 💡 Features

* 🔀 **LLM or manual tag extraction** (`llm` or `manual` via env or CLI)
* 🚫 **Tag validation & cleaning** (invalid tags are logged and ignored)
* 💾 **Local cache** of scraped data (avoids redundant API calls)
* 🔌 **BrightData support** (snapshot polling and JSON saving)

---

## 📌 .env.example overview

```dotenv
# Select scraper
SCRAPER_TYPE=brightdata

# BrightData
BRIGHTDATA_API_KEY=your_key
BRIGHTDATA_DATASET_ID=your_dataset_id
BRIGHTDATA_TIMEOUT=120
BRIGHTDATA_POLL_INTERVAL=5

# Proxycurl (optional)
PROXYCURL_API_KEY=your_key

# LLM Providers
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key

# Output
OUTPUT_DIRECTORY=./data/profiles
LOG_DIRECTORY=./data/logs
BATCH_LIMIT=5
```

---

## 🛑 Disclaimer

This tool fetches public LinkedIn data using external APIs. You must comply with the terms of service of BrightData, LinkedIn, OpenAI, and other services used.

---

## 📆 Roadmap

* [ ] 🔌 Add automatic Airtable sync
* [ ] 🧠 Add smarter tag suggestion (embeddings / clustering)
* [ ] 🔁 Enable retry queue for failed fetches

---