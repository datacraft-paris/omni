"""
Neutral LLM interface for generating interest tags and description from a profile text.
Supports multiple providers (OpenAI, Gemini, etc.).

Example usage:
    from llm_interface import generate_interest_and_description
    from src.lipopulate.core.static_values import CENTER_OF_INTEREST_LIST

    profile_text = "..."  # Your LinkedIn profile text
    result = generate_interest_and_description(
        profile_text,
        CENTER_OF_INTEREST_LIST,
        provider="openai"
    )
    print(result)
"""
from typing import List, Dict, Optional
from openai import OpenAI
import os

# Import provider SDKs as needed
'''
try:
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except ImportError:
    client = None
'''

# Add more imports for other providers as needed

class LLMProviderNotAvailable(Exception):
    pass

def generate_interest_and_description(
    profile_text: str,
    tags_list: List[str],
    provider: str = "openai",
    api_key: Optional[str] = None,
    language: str = "fr"
) -> Dict[str, object]:
    """
    Neutral interface for LLM-based tag and description generation.
    Args:
        profile_text (str): The input profile text.
        tags_list (List[str]): List of allowed tags.
        provider (str): LLM provider ("openai", "gemini", ...).
        api_key (str, optional): API key for the provider.
        language (str): Output language for the description.
    Returns:
        dict: {"Intérêt": [tags], "Description": str}
    """
    if provider == "openai":
        return _openai_generate(profile_text, tags_list, api_key, language)
    elif provider == "gemini":
        raise NotImplementedError("Gemini backend not implemented yet.")
    else:
        raise ValueError(f"Unknown provider: {provider}")

def _openai_generate(profile_text, tags_list, api_key, language):

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not provided.")

    client = OpenAI(api_key=api_key)

    if client is None:
        raise LLMProviderNotAvailable("openai package is not installed.")

    # Prompt for tags
    tags_prompt = (
        f"Les informations suivantes sont issues d'un profil LinkedIn d’un professionnel de la data.\n"
        f"Attribue à ce profil les labels les plus pertinents parmi :\n"
        + ", ".join([tag for tag in tags_list if tag])
        + "\nRéponds uniquement par une chaîne de texte contenant les tags séparés par des virgules, par exemple : 'Data Engineering, MLOps'"
    )
    '''
    tags_prompt = (
        f"Les informations suivantes sont issues d'un profil LinkedIn. "
        f"Ce profil appartient à un professionnel de la data.\n"
        f"Attribue à ce profil les labels qui correspondent parmi les suivants :\n"
        + "\n".join(f"- {tag}" for tag in tags_list if tag)
        + "\nRéponds uniquement par une liste Python, par exemple : ['Data Engineering', 'MLOps']"
    )'''
    # Prompt for description
    desc_prompt = (
        "A partir des informations suivantes issues d'un profil LinkedIn, je souhaite faire un résumé impersonnel en 150 mots du profil de la personne. "
        "Ce résumé doit mettre l'accent sur l'expérience de la personne et ses capacités/savoir-faires techniques. "
        "Ce résumé doit rapidement permettre de savoir ce que sais faire la personne, en quoi elle est experte. "
        "Ce résumé doit être précis, et ne pas utiliser de termes vagues comme 'des compétences variées' ou 'une expérience solide'. Il ne doit contenir que de l'information factuelle. "
        "Ce résumé doit être en français. "
        "Ce résumé ne doit pas décrire les activités des entreprises, mais doit vraiment se concentrer sur les expériences et compétences de la personne."
    )
    # Compose full prompts
    tags_full_prompt = f"{tags_prompt}\n\n{profile_text}"
    desc_full_prompt = f"{desc_prompt}\n\n{profile_text}"

    # Call OpenAI for tags
    tags_response = client.completions.create(model="gpt-3.5-turbo-instruct",
        prompt=tags_full_prompt,
        max_tokens=100)
    tags_output = tags_response.choices[0].text.strip()
    tags_cleaned = [t.strip() for t in tags_output.split(",") if t.strip()]
    tags_string = ", ".join(tags_cleaned)

    # Call OpenAI for description
    desc_response = client.completions.create(model="gpt-3.5-turbo-instruct",
        prompt=desc_full_prompt,
        max_tokens=500)
    description = desc_response.choices[0].text.strip()

    return {"Intérêt": tags_string, "Description": description}
