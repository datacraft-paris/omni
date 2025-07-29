from lipopulate.core.schema import LinkedInProfile, GeneratedProfileResult
from lipopulate.src.tag_description_builder import build_interest_and_description
from lipopulate.src.llm_interface import generate_interest_and_description
from lipopulate.core.static_values import CENTER_OF_INTEREST_LIST
from lipopulate.utils.crud import get_profile_text
from pydantic import ValidationError

def process_profile(profile_dict: dict, method: str = "llm") -> dict:
    """
    Process a LinkedIn profile dictionary to generate interests and descriptions.
    Args:
        profile_dict (dict): LinkedIn profile data.
        method (str): Method to use for generation ("manual" or "llm").
    Returns:
        dict: Generated interests and descriptions.
    """
    
    try:
        validated_profile = LinkedInProfile(**profile_dict)
    except ValidationError as e:
        raise ValueError(f"Profil invalide : {e}")

    profile_text = get_profile_text(validated_profile.model_dump())

    if method == "llm":
        result = generate_interest_and_description(
            profile_text, CENTER_OF_INTEREST_LIST, provider="openai"
        )
    else:
        result = build_interest_and_description(profile_text)

    try:
        validated_result = GeneratedProfileResult(**result)
    except ValidationError as e:
        raise ValueError(f"Résultat invalide : {e}")

    return validated_result.model_dump()
