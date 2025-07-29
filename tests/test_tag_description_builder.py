from lipopulate.tag_description_builder import build_interest_and_description

import sys
import os
import pytest

def test_basic_profile():
    text = "Expert en Data Engineering et Machine Learning. Passionné par le MLOps."
    result = build_interest_and_description(text)
    assert "Data Engineering" in result["Intérêt"]
    assert "Machine Learning" in result["Intérêt"]
    assert "MLOps" in result["Intérêt"]
    assert isinstance(result["Description"], str)
    assert "Description" in result
    assert "Intérêt" in result

def test_no_interest():
    text = "Consultant généraliste sans spécialité data."
    result = build_interest_and_description(text)
    assert result["Intérêt"] == ""
    assert isinstance(result["Description"], str)
