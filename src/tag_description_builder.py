from typing import List, Dict
from src.lipopulate.core.static_values import CENTER_OF_INTEREST_LIST

def build_interest_and_description(profile_text: str) -> Dict[str, object]:
    """
    Extracts interest tags and a short description from a LinkedIn profile text.

    Args:
        profile_text (str): Concatenated text from a LinkedIn profile.

    Returns:
        dict: Dictionary with keys 'Intérêt' (list of tags) and 'Description' (short summary).
    """
    # Naive keyword-based detection of interests (case-insensitive)
    interests = []
    text_norm = profile_text.lower()
    for tag in CENTER_OF_INTEREST_LIST:
        if tag is not None:
            tag_norm = tag.lower()
            if tag_norm in text_norm:
                interests.append(tag)

    # Manual placeholder for description generation
    description = "Auto-generated summary to be completed."
    return {"Intérêt": ", ".join(interests), "Description": description}