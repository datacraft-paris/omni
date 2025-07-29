import os
import sys
from src.tag_description_builder import build_interest_and_description
from utils.llm_interface import generate_interest_and_description
from core.static_values import CENTER_OF_INTEREST_LIST
from core.schema import GeneratedProfileResult, LinkedInProfile
from utils.crud import get_profile_text
from pydantic import ValidationError

if __name__ == "__main__":
    """
    Main script for generating interests and descriptions from a LinkedIn profile JSON.

    Usage:
        python3 src/lipopulate/main.py [manual|llm]

    Arguments:
        manual   Use manual keyword-based generation (default if no argument or PROFILE_TAG_METHOD is not set)
        llm      Use LLM-based generation (requires OpenAI API access)

    Environment Variables:
        PROFILE_TAG_METHOD   If set to "manual" or "llm", overrides the default method unless a CLI argument is provided.

    Example:
        python3 src/lipopulate/main.py llm

    This will use the LLM-based method to generate interests and descriptions from the example profile.
    """
    # TODO Example LinkedIn profile JSON (to be adapted to real API)
    example_profile = {
        "summary": "Expert en Data Engineering et Machine Learning. Passionné par le MLOps.",
        "headline": "Lead Data Scientist",
        "experience": [
            {"title": "Data Engineer", "company": "BigDataCorp"},
            {"title": "ML Engineer", "company": "AIStartup"}
        ]
    }

    try:
        validated_profile = LinkedInProfile(**example_profile)
    except ValidationError as e:
        print("Erreur de validation du profil LinkedIn :", e)
        sys.exit(1)

    profile_text = get_profile_text(validated_profile.model_dump())

    # CLI override: python3 src/lipopulate/main.py [manual|llm]
    if len(sys.argv) > 1 and sys.argv[1] in {"manual", "llm"}:
        method = sys.argv[1]
    else:
        method = os.getenv("PROFILE_TAG_METHOD", "manual")

    if method == "llm":
        # Use LLM-based generation (OpenAI)
        print("Using LLM-based generation...")
        result = generate_interest_and_description(
            profile_text,
            CENTER_OF_INTEREST_LIST,
            provider="openai"
        )
    else:
        # Use manual keyword-based generation
        print("Using manual keyword-based generation...")
        result = build_interest_and_description(profile_text)

    #print(result)

    try:
        validated = GeneratedProfileResult(**result)
        print(validated.model_dump_json(indent=2))
    except ValidationError as e:
        print("Erreur de validation du résultat généré :", e)