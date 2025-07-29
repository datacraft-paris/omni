import requests
import os
from typing import Optional, Dict, Any
from loguru import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration des chemins
LOG_DIRECTORY = os.getenv("LOG_DIRECTORY", "./data/logs")
os.makedirs(LOG_DIRECTORY, exist_ok=True)

# Configuration du logger
log_path = os.path.join(LOG_DIRECTORY, "api_calls.log")
logger.add(log_path, rotation="1 MB", level="INFO", backtrace=True, diagnose=True)

def make_api_request(
    api_endpoint: str,
    headers: Dict[str, str],
    params: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Effectue une requête API générique, gère les erreurs et retourne la réponse JSON si disponible.
    
    Args:
        api_endpoint (str): URL de l'API à appeler.
        headers (Dict[str, str]): En-têtes HTTP pour la requête.
        params (Dict[str, Any]): Paramètres de la requête.
    
    Returns:
        Optional[Dict[str, Any]]: La réponse JSON si la requête réussit, None en cas d'erreur.
    """
    try:
        response = requests.get(api_endpoint, headers=headers, params=params)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        logger.info("Requête réussie.")
        return response.json()  # Parse la réponse JSON
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de l'appel à l'API : {e}")
        return None

def fetch_profile_by_details(
    headers: Dict[str, str],
    first_name: str,
    last_name: str,
    company_domain: Optional[str] = None,
    title: Optional[str] = None,
    location: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Récupère les informations du profil LinkedIn à partir de plusieurs détails.
    
    Args:
        first_name (str): Prénom de la personne.
        last_name (str): Nom de la personne.
        company_domain (str): Domaine de l'entreprise.
        title (str, optional): Titre ou poste de la personne. Default is None.
        location (str, optional): Localisation de la personne. Default is None.
    
    Returns:
        dict: Données du profil LinkedIn si trouvé.
        None: En cas d'erreur ou si le profil n'est pas trouvé.
    """
    API_ENDPOINT = "https://nubela.co/proxycurl/api/linkedin/profile/resolve"

    params = {
        'first_name': first_name,
        'last_name': last_name,
        'similarity_checks': 'include',
        'enrich_profile': 'enrich',
    }
    if company_domain:
        params['company_domain'] = company_domain
    if title:
        params['title'] = title
    if location:
        params['location'] = location

    logger.info(f"Paramètres envoyés : {params}")
    return make_api_request(API_ENDPOINT, headers, params)

def fetch_profile(linkedin_profile_url: str, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    Récupère les informations du profil LinkedIn via l'API Proxycurl.
    Les paramètres nécessaires sont définis directement dans cette fonction.
    
    Args:
        linkedin_profile_url (str): URL du profil LinkedIn.
        headers (Dict[str, str]): En-têtes pour l'appel API.
    
    Returns:
        dict: Données du profil LinkedIn si trouvé.
        None: En cas d'erreur ou si le profil n'est pas trouvé.
    """
    API_ENDPOINT = "https://nubela.co/proxycurl/api/v2/linkedin"

    params = {
        'url': linkedin_profile_url,
        'extra': 'include',
        'skills': 'include',
        'inferred_salary': 'include',
        'use_cache': 'if-present',
        'fallback_to_cache': 'on-error',
    }

    logger.info(f"Paramètres envoyés pour l'URL LinkedIn : {params}")
    return make_api_request(API_ENDPOINT, headers, params)