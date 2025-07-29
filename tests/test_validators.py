import pytest
from src.lipopulate.core.schema import GeneratedProfileResult

def test_valid_interest_tags_pass():
    result = GeneratedProfileResult(
        Intérêt="MLOps, Data Engineering, Machine Learning",
        Description="Profil senior avec expertise sur la mise en production de modèles."
    )
    assert "Data Engineering" in result.Intérêt
    assert isinstance(result.Intérêt, str)

def test_invalid_interest_tags_filtered():
    result = GeneratedProfileResult(
        Intérêt="MLOps, Blockchain, Pizza AI",
        Description="Expert MLOps avec des projets complexes."
    )
    assert result.Intérêt == "MLOps"

def test_no_valid_tags_raises():
    with pytest.raises(ValueError, match="Aucun tag valide"):
        GeneratedProfileResult(
            Intérêt="Inconnu, Autre",
            Description="Texte valable"
        )
