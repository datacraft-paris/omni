from enum import Enum
from pydantic import BaseModel, Field, field_validator, ValidationInfo
import re

class InterestTag(str, Enum):
    DATA_ENGINEERING = "Data Engineering"
    DATA_GOUVERNANCE = "Data Gouvernance"
    DATA_ANALYTICS = "Data Analytics"
    DATA_INFRASTRUCTURE = "Data Infrastructure"
    MLOPS = "MLOps"
    DEVOPS = "DevOps"
    WEB = "Web"
    MACHINE_LEARNING = "Machine Learning"
    TIME_SERIES = "Time Series"
    NLP = "NLP"
    COMPUTER_VISION = "Computer Vision"
    FRUGAL_AI = "Frugal AI"
    ETHICAL_GREEN_AI = "Ethical/Green AI"
    EXPLICABILITY = "Explicability"
    PRIVACY_SAFETY = "Privacy/Safety"
    GEN_AI_IMAGE = "Generative AI (images)"
    GEN_AI_TEXT = "Generative AI (text)"


class GeneratedProfileResult(BaseModel):
    Intérêt: str = Field(default_factory=str)
    Description: str = Field(..., min_length=10)
        
    @field_validator("Intérêt")
    @classmethod
    def filter_valid_tags(cls, tags: str, info: ValidationInfo) -> str:
        allowed = {tag.value for tag in InterestTag}
        raw_tags = [tag.strip() for tag in tags.split(",")]

        cleaned_tags = []
        for tag in raw_tags:
            # Supprimer tout préfixe du style "s :" ou autre
            tag = re.sub(r"^\w\s*[:\-–]", "", tag).strip()
            # Supprimer les caractères spéciaux en fin (., ;, etc.)
            tag = tag.rstrip(".;: ")
            cleaned_tags.append(tag)

        valid = [tag for tag in cleaned_tags if tag in allowed]
        invalid = [tag for tag in cleaned_tags if tag not in allowed]

        if invalid:
            print(f"[INFO] Tags ignorés car non valides : {invalid}")
        if not valid:
            raise ValueError("Aucun tag valide trouvé dans la liste fournie.")

        return ", ".join(valid)

#TODO    
class LinkedInExperience(BaseModel):
    title: str = Field(..., min_length=1)
    company: str = Field(..., min_length=1)

#TODO
class LinkedInProfile(BaseModel):
    summary: str = ""
    headline: str = ""
    experience: list[LinkedInExperience] = Field(default_factory=list)
