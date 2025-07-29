import pandas as pd
from lipopulate.src.pipeline import process_profile
from lipopulate.utils.linkedin_scrapper_adapter import scrape_linkedin_profile

INPUT_CSV = "data/airtable_export.csv"
OUTPUT_CSV = "data/enriched_output.csv"
METHOD = "llm"  # or "manual"

def is_row_already_enriched(row) -> bool:
    """Check if the row already contains both 'Intérêt' and 'Description'."""
    return bool(str(row.get("Intérêt", "")).strip()) and bool(str(row.get("Description", "")).strip())

def build_profile_dict(row) -> dict:
    """
    Build the minimal profile dictionary expected by LinkedInProfile.
    """
    linkedin_url = str(row.get("Linkedin", "")).strip()
    job_title = str(row.get("Métier", "")).strip()
    domain = str(row.get("Domain", "")).strip()

    if not linkedin_url and not (job_title or domain):
        raise ValueError("Insufficient data to build profile input.")

    if linkedin_url:
        profile_dict = scrape_linkedin_profile(linkedin_url)

        # 💡 Optionally enrich summary
        enriched_summary = profile_dict.get("summary", "")
        if job_title or domain:
            enriched_summary += f" {job_title} {domain}".strip()

        return {
            "summary": enriched_summary,
            "headline": profile_dict.get("headline", job_title),
            "experience": profile_dict.get("experience", [])
        }
    else:
        return {
            "summary": f"{job_title}. Domain: {domain}",
            "headline": job_title,
            "experience": []
        }


def main():
    df = pd.read_csv(INPUT_CSV)

    descriptions = []
    interets = []

    for index, row in df.iterrows():
        if is_row_already_enriched(row):
            descriptions.append(row["Description"])
            interets.append(row["Intérêt"])
            continue

        try:
            profile_dict = build_profile_dict(row)
            result = process_profile(profile_dict, method=METHOD)
            descriptions.append(result["Description"])
            interets.append(result["Intérêt"])
        except Exception as e:
            print(f"[Row {index}] Error: {e}")
            descriptions.append("")
            interets.append("")

    df["Description"] = descriptions
    df["Intérêt"] = interets

    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Enriched file saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
