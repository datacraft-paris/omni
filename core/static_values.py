import os
from dotenv import load_dotenv
import re

# Necessary for loading environment variables (.env) with os.getenv()
load_dotenv(override=True)

def is_env_true(varname: str) -> bool:
    return os.getenv(varname, "").strip().lower() in ["true", "1", "yes"]

AIRTABLE_TEST_TABLES = is_env_true("AIRTABLE_TEST_TABLES")

### STATIC VARIABLES ###
# Formats connus dans l'écosystème Airtable CSV
KNOWN_DATE_FORMATS = [
        "%Y-%m-%dT%H:%M:%S.%fZ",  # Airtable API
        "%Y-%m-%dT%H:%M:%S",      # ISO sans Z
        "%Y-%m-%d %H:%M:%S",      # Supabase
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y %I:%M%p",
        "%d/%m/%Y",
        "%m/%d/%Y",               # fallback pour CSV US
]

AIRTABLE_API_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"


### LIST OF VALID VALUES FOR DATABASE FIELDS ###

TAG_LIST = ['#CONTACT',"Blacklist","ClubCDO","Star",None]
JOB_CATEGORY_LIST = ["data scientist","data analyst","data engineer","data architect","data manager","consultant data","CDO/head data","gouvernance data","data owner","transformation data","developer","data/tech/IT/digital manager","freelance","manager","chercheur","consultant","CEO","chief officer","marketing/CRM","professeur","direction","business development","laws & ethics","étudiant","autre","unknown","gestion de projets","engineer",None]
CENTER_OF_INTEREST_LIST = ["Data Engineering","Data Gouvernance","Data Analytics","Data Infrastructure","MLOps","DevOps","Web","Machine Learning","Time Series","NLP","Computer Vision","Frugal AI","Ethical/Green AI","Explicability","Privacy/Safety","Generative AI (images)","Generative AI (text)", None]
DOMAIN_LIST = ["Health", "Insurance", "Transportation", "Sports", "Marketing", "Environment", "Human Resources", "Tech", "Biology", "Aerospace", "Ocean", "Military", "Finance", "Food", "Supply Chain / Retail", "Cyber", "Creative Industry", "Archives", "Beauty", "Luxury", "Construction", "Audiovisual", "Video Games", "Education", "Management", "Telecom", "Energy", "IT", "Events / Hotels", "Industry", "Automobile", "Media"]
STATUS_LIST = ["Full Membership","Corporate Membership","Chercheur en résidence","Freelance en résidence","Etudiant en résidence","Ancien membre","Board Member","Partenaire","Journaliste","Prospect","CDO Membership","Contributeur en résidence","Autre",None]
SLACK_LIST = ["Invité","Accepté","Désinscrit","A inviter","Ne pas inviter","Invité-WIP", None]
# NEWSLETTER_STATUS = ["Subscribed", "Unsubscribed", None] # transformed to boolean in cleaning.py directly

COMPANY_STATUS_LIST = ["Full Membership","Individual Membership","Not Member","Old Member","Undefined",None]
COMPANY_GROUP_LIST = ["Crédit Agricole - Group","Bouygues - Group","Accuracy - Group","Air France KLM - Group","Airbus - Group","Test Group",None]

WORKSHOP_TYPE_LIST = ["Atelier","Atelier *","État de l'art","REX","Expert Q&A","Découverte","Formation","Benchaton","Soirée CDO & HR","Data Gouv","Mindshaketime","Masterclass","Hackaton","Meet-up","Focus","Acculturation","Formation","Autre",None]
WORKSHOP_FORMAT_LIST = ["En ligne","En présentiel","Hybride",None]
WORKSHOP_REQUIRED_PYTHON_LEVEL_LIST = ["Tout public","Connaissances de base en Python","Bonnes connaissances en Python","Connaissances avancées en Python",None]
WORKSHOP_REQUIRED_ML_LEVEL_LIST = ["Tout public","Connaissances de base en ML/Data/IA","Bonnes connaissances en ML/Data/IA","Connaissances avancées en ML/Data/IA",None]
WORKSHOP_STAFF_MEMBER_LIST = ["Xavier Lioneton","Marc de Vaugiraud","Isabelle Hilali","Caroline Daudeteau","Thaïs Denoyelle","Raphael Vienne",None]
WORKSHOP_STATUS_LIST = ["À planifier","Confirmé","À confirmer","Inscription","Passé","Idée","Annulé","Reporté",None]
WORKSHOP_PUBLISHING_STATUS_LIST = ["Fait","À faire","Mettre à jour","No need",None]
WORKSHOP_LANGUAGE_LIST = ["Français","Anglais",None]

PARTICIPANT_STATUS_LIST = ["Inscrit","Vérification","Validé","Refus","Annulation",None]
PARTICIPANT_SOURCE_LIST = ["Eventbrite","Wordpress","Manuelle",None]
PARTICIPATION_TYPE_LIST = ["En ligne","Présentiel",None]

# Airtable API Configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
HEADERS = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}

# Local CSV Option
USE_LOCAL_CSV = os.getenv("USE_LOCAL_CSV")

# Folder to place raw csv. In .gitignore
RAW_CSV_DIR = "./raw_csv"
RAW_MOCK_DIR = "./mocked_csv/Airtable"
RAW_MOCK_PYTEST_DIR = "./mocked_csv/Airtable_pytest"

# CSV paths
CSV_PATHS = {
    "Company": os.getenv("COMPANIES_CSV_PATH"),
    "User": os.getenv("USERS_CSV_PATH"),
    "Workshop": os.getenv("WORKSHOPS_CSV_PATH"),
    "Participant": os.getenv("PARTICIPANTS_CSV_PATH"),
}

# Airtable table URLs, switching between prod and test depending on ENV
AIRTABLE_URLS = {
    "Company": os.getenv("AIRTABLE_COMPANY_TEST_URL") if AIRTABLE_TEST_TABLES else os.getenv("AIRTABLE_COMPANY_URL"),
    "User": os.getenv("AIRTABLE_USER_TEST_URL") if AIRTABLE_TEST_TABLES else os.getenv("AIRTABLE_USER_URL"),
    "Workshop": os.getenv("AIRTABLE_WORKSHOP_TEST_URL") if AIRTABLE_TEST_TABLES else os.getenv("AIRTABLE_WORKSHOP_URL"),
    "Participant": os.getenv("AIRTABLE_PARTICIPANT_TEST_URL") if AIRTABLE_TEST_TABLES else os.getenv("AIRTABLE_PARTICIPANT_URL"),
}

def get_view_mapping() -> dict:
    test_mode = is_env_true("AIRTABLE_TEST_TABLES")
    return {
        "Company": os.getenv("COMPANIES_TEST_TARGET_VIEW") if test_mode else os.getenv("COMPANIES_TARGET_VIEW"),
        "User": os.getenv("USERS_TEST_TARGET_VIEW") if test_mode else os.getenv("USERS_TARGET_VIEW"),
        "Workshop": os.getenv("WORKSHOPS_TEST_TARGET_VIEW") if test_mode else os.getenv("WORKSHOPS_TARGET_VIEW"),
        "Participant": os.getenv("PARTICIPANTS_TEST_TARGET_VIEW") if test_mode else os.getenv("PARTICIPANTS_TARGET_VIEW"),
    }

### Mapping columns for object (row) creation

CREATE_ROW_COLUMNS = {
    "Company": {
        "name": "Raison sociale",
        "status": "Statut",
        "description": "Description",
        "group": "Test Group",
        "comments": "Commentaires",
        "interests": "Centres d'intérêt",
        "topics": "Enjeux",
        "country": "Pays",
        "city": "Ville",
        "creation_date": "Date création",
        "onboarding_date": "Date onboarding"
    },
    "User": {
        "name": "Prénom",
        "lastname": "Nom",
        "email": "Email",
        "company_name": "Organisation",
        "job": "Titre",
        "job_category": "Métier",
        "interests": "Intérêt",
        "domains": "Domain",
        "tags": "Tags",
        "status": "Statut",
        "description": "Description",
        "comments": "Commentaire",
        "newsletter": "Marc dev - Newsletter",
        "slack": "Slack",
        "linkedin": "Linkedin",
        "wordpress": "Compte Wordpress",
        "onboarding_date": "Date d'entrée",
        "token": "token",
        "password": "password"
    },
    "Workshop": {
        "nomenclature": "Nomenclature",
        "name": "Titre",
        "workshop_type": "Type Event (dev Marc)",
        "description": "Description de l'atelier",
        "date": "Date",
        "start_time": "Start time",
        "end_time": "End time",
        "address": "Adress",
        "format": "Format",
        "tags": "Tags (Marc dev)",
        "required_python_level": "Niveau Python",
        "required_ml_level": "Niveau ML",
        "dataset_description": "Description du jeu de données",
        "common_approaches": "Approche algo",
        "useful_links": "Liens",
        "language": "Langue",
        "staff_member_in_charge": "Resp. Prog",
        "status": "Statut Prog",
        "website_publishing_status": "Site web",
        "eventbrite_publishing_status": "Eventbrite",
        "calendar_publishing_status": "Calendrier",
        "slack_publishing_status": "Slack",
        "zoom_conference_status": "Zoom",
        "room_reservation_status": "salle",
        "comments": "Commentaire"
    },
    "Participant": {
        "user_email": "Email",
        "name": "Prénom",
        "lastname": "Nom",
        "company_name": "Company",
        "job": "Poste",
        "linkedin": "Linkedin",
        "workshop_nomenclature": "Nomenclature",
        "register_date": "Date d'inscription",  # Already cleaned
        "type_of_participation": "Type de particip",
        "status": "Statut",
        "confirmation_email_send_date": "Confirmation mail",  # Already cleaned
        "source": "Source",
        "has_participated": "Présent à l'évènement ?",  # Already cleaned
        "follow_email": "Suivi mail"  # Already cleaned
    }
}

