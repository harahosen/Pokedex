import pytest
import json

# internal dependencies
from app.services import pokeapi
from exceptions.handlers import ExternalAPIError

sample_response = {
    "name": "mew",
    "flavor_text_entries": [
        {"flavor_text": "Cute\\n", "language": {"name": "en"}},
        {"flavor_text": "Otro", "language": {"name": "es"}}
    ],
    "habitat": {"name": "cave"},
    "is_legendary": True
}

class DummyResp:
    status_code = 200
    def json(self):
        return sample_response

class DummyFail:
    status_code = 404
    def json(self): return {}

# test for an OK from the pokeapi service 
@pytest.mark.unit
def test_get_pokemon_data_ok(monkeypatch):
    monkeypatch.setattr(pokeapi.requests, "get", lambda url: DummyResp())
    result = pokeapi.get_pokemon_data("mew")
    assert isinstance(result, dict)
    assert result["name"] == "mew"
    assert "Cute" in result["description"]
    assert result["habitat"] == "cave"
    assert result["isLegendary"] is True

# test for an KO from the pokeapi service
@pytest.mark.unit
def test_get_pokemon_data_ko(monkeypatch):
    monkeypatch.setattr(pokeapi.requests, "get", lambda url: DummyFail())
    
    with pytest.raises(ExternalAPIError):
        pokeapi.get_pokemon_data("missingno")