# Quick documentation for using tag_description_builder and main.py

## Goal
Automatically extract interest tags ("Intérêt") and a short description ("Description") from a LinkedIn profile, to populate Airtable.

## Main function
- `build_interest_and_description(profile_text: str) -> dict`
  - Input: a raw concatenated text (LinkedIn profile)
  - Output: a dictionary `{ "Intérêt": [tags], "Description": "..." }`

## Usage via main.py
- The script `main.py` simulates fetching a LinkedIn profile in JSON format (see example below).
- It concatenates text fields from the JSON to generate a `profile_text` string for the function.
- Later, adapt the construction of `profile_text` according to the actual scraping API format.

## To do
- Adapt JSON parsing as soon as the scraping API is available.
- Improve description generation (LLM or prompt engineering).
- Add tests for various profiles.

## Example of simulated JSON
```json
{
  "summary": "Expert in Data Engineering and Machine Learning. Passionate about MLOps.",
  "headline": "Lead Data Scientist",
  "experience": [
    {"title": "Data Engineer", "company": "BigDataCorp"},
    {"title": "ML Engineer", "company": "AIStartup"}
  ]
}
```

## How to test
```bash
python3 src/lipopulate/main.py
$PROFILE_TAG_METHOD python3 src/lipopulate/main.py
```
