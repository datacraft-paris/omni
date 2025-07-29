def get_profile_text(profile_json):
    """
    Concatenate relevant fields from a LinkedIn profile JSON to a single text string.
    """
    text = profile_json.get("summary", "") + " " + profile_json.get("headline", "")
    for exp in profile_json.get("experience", []):
        text += f" {exp.get('title', '')} {exp.get('company', '')}"
    return text.strip()