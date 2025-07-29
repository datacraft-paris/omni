import pytest
from src.lipopulate.llm_interface import generate_interest_and_description
from src.lipopulate.core.static_values import CENTER_OF_INTEREST_LIST

@pytest.mark.skip(reason="Requires OpenAI API access")
def test_generate_interest_and_description_live():
    profile_text = "Expert en MLOps, Machine Learning et Data Engineering. A dirigé des projets chez BigDataCorp."
    result = generate_interest_and_description(profile_text, CENTER_OF_INTEREST_LIST)

    assert "Description" in result
    assert "Intérêt" in result
    assert isinstance(result["Intérêt"], str)
    assert isinstance(result["Description"], str)
    assert len(result["Description"]) > 20
