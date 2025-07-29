# LiScrape - Projet d'Analyse et Documentation

## 📖 Vue d'ensemble

**LiScrape** est un projet Python qui automatise la récupération d'informations de profils LinkedIn via l'API Proxycurl et la mise à jour de données dans Airtable. Le projet est conçu pour traiter des listes de personnes et enrichir leurs informations avec des données LinkedIn.

## 🏗️ Architecture du Projet

```
liscrape/
├── pyproject.toml          # Configuration du projet Python
├── README.md               # Documentation (actuellement vide)
├── .gitignore             # Fichiers à ignorer (.env, .venv)
└── src/
    └── liscrape/
        ├── find_someone.py       # Module principal de traitement
        ├── proxy_utils.py        # Utilitaires API Proxycurl
        ├── test-api.py          # Test avec URL LinkedIn
        ├── test-without-url.py  # Test sans URL LinkedIn
        └── update_airtable.py   # Intégration Airtable
```

## 🔧 Modules et Fonctionnalités

### 1. `proxy_utils.py` - Utilitaires API Proxycurl

**Rôle**: Module central pour les appels à l'API Proxycurl

**Fonctions principales**:
- `make_api_request()`: Gestionnaire générique des requêtes API avec gestion d'erreurs
- `fetch_profile()`: Récupère un profil LinkedIn via son URL
- `fetch_profile_by_details()`: Recherche un profil par nom, prénom et détails optionnels

**Points clés**:
- Utilise la bibliothèque `requests` pour les appels HTTP
- Intégration du logging avec `loguru`
- Gestion robuste des erreurs HTTP
- Support de paramètres optionnels (entreprise, titre, localisation)

### 2. `find_someone.py` - Module Principal de Traitement

**Rôle**: Orchestrateur principal du processus de recherche

**Fonction principale**:
- `process_person()`: Traite une personne selon les données disponibles
  - Si URL LinkedIn disponible → utilise `fetch_profile()`
  - Sinon → utilise `fetch_profile_by_details()`
  - Retourne des données structurées ou une erreur

**Logique de fallback**:
1. Tentative avec URL LinkedIn si disponible
2. Si échec ou URL absente → recherche par détails personnels
3. Logging détaillé de chaque étape

**Configuration**:
- Variables d'environnement via `python-dotenv`
- Clé API Proxycurl requise
- Exemple de test avec "Raphaël Vienne" de Datacraft

### 3. `update_airtable.py` - Intégration Airtable

**Rôle**: Automatisation complète du workflow avec Airtable

**Fonctionnalités**:
- `get_people_data()`: Récupère les données depuis Airtable
- `get_proxy_columns()`: Identifie les colonnes à remplir (format `*_proxy`)
- `batch_update_airtable()`: Met à jour les enregistrements en lot
- `save_to_json()`: Sauvegarde locale des résultats

**Workflow**:
1. Connexion à Airtable via `pyairtable`
2. Récupération des personnes à traiter
3. Traitement via `process_person()`
4. Sauvegarde JSON locale
5. Mise à jour batch d'Airtable

### 4. Scripts de Test

#### `test-api.py`
- Test simple avec URL LinkedIn fixe
- Exemple: "Eric Gautier"
- Version simplifiée sans logging avancé

#### `test-without-url.py`
- Test de recherche par détails personnels
- Exemple: "Marc de Vaugiraud" chez Datacraft
- Démontre l'API de résolution de profils

## 🔑 Configuration Requise

### Variables d'Environnement (.env)
```env
PROXYCURL_API_KEY=your_proxycurl_api_key
BASE_ID=your_airtable_base_id
TABLE_NAME=your_airtable_table_name
AIRTABLE_API_KEY=your_airtable_api_key
```

### Dépendances Principales
- `requests`: Appels HTTP
- `loguru`: Logging avancé
- `python-dotenv`: Gestion des variables d'environnement
- `pyairtable`: Intégration Airtable

## 🚀 Utilisation

### Cas d'usage 1: Test simple
```python
# Avec URL LinkedIn
python src/liscrape/test-api.py

# Sans URL LinkedIn (recherche par détails)
python src/liscrape/test-without-url.py
```

### Cas d'usage 2: Traitement individuel
```python
from find_someone import process_person

person_data = {
    "first_name": "Prénom",
    "last_name": "Nom",
    "linkedin_url": "URL_optionnelle",
    "company": "entreprise",
    "title": "poste",
    "location": "localisation"
}

result = process_person(person_data, headers)
```

### Cas d'usage 3: Automatisation Airtable
```python
python src/liscrape/update_airtable.py
```

## 📊 Structure des Données

### Entrée (person_row)
```python
{
    "first_name": str,          # Obligatoire
    "last_name": str,           # Obligatoire
    "linkedin_url": str,        # Optionnel
    "company": str,             # Optionnel
    "title": str,               # Optionnel
    "location": str             # Optionnel
}
```

### Sortie (profile_data)
```python
{
    "status": "success",
    "data": {
        # Données complètes du profil LinkedIn
        "public_identifier": str,
        "profile_pic_url": str,
        "background_cover_image_url": str,
        "first_name": str,
        "last_name": str,
        # ... autres champs LinkedIn
    }
}
```

## 🔍 Points d'Attention

### 1. Gestion des Erreurs
- Validation des champs obligatoires (prénom, nom)
- Gestion des erreurs HTTP avec `requests.exceptions.RequestException`
- Logging détaillé pour le debugging

### 2. Optimisations API
- Cache Proxycurl: `use_cache: if-present`
- Fallback: `fallback_to_cache: on-error`
- Enrichissement: `enrich_profile: enrich`

### 3. Logging
- Fichiers de log rotatifs (1 MB)
- Niveaux: INFO, ERROR, WARNING
- Traceback activé pour le debugging

### 4. Traitement par Lots
- Limitation configurable (actuellement 5 personnes)
- Mise à jour batch d'Airtable pour l'efficacité
- Sauvegarde JSON locale pour backup

## 🎯 Cas d'Usage Métier

Ce projet semble conçu pour :
- **Enrichissement de données CRM**: Compléter des bases de données clients/prospects
- **Recherche commerciale**: Identifier et qualifier des contacts LinkedIn
- **Automatisation RH**: Enrichir des profils candidats
- **Veille concurrentielle**: Analyser les profils d'entreprises cibles

## 🔄 Workflow Complet

1. **Préparation**: Configuration des clés API et variables d'environnement
2. **Extraction**: Récupération des données depuis Airtable
3. **Enrichissement**: 
   - Tentative avec URL LinkedIn
   - Fallback sur recherche par détails
4. **Sauvegarde**: Export JSON local des résultats
5. **Intégration**: Mise à jour des colonnes `*_proxy` dans Airtable

## 📈 Améliorations Potentielles

- [ ] Gestion de la pagination Airtable pour de gros volumes
- [ ] Rate limiting pour respecter les quotas API
- [ ] Interface CLI avec arguments configurables
- [ ] Tests unitaires et d'intégration
- [ ] Documentation API automatisée
- [ ] Monitoring et métriques de performance
- [ ] Support de multiples sources de données
