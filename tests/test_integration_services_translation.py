import pytest
from fastapi.testclient import TestClient

# internal dependencies
from app.main import app
from app.services import pokeapi, translation

client = TestClient(app)

sample_legendary = {
    "name": "mew",
    "flavor_text_entries": [
        {"flavor_text": "Cute Pokémon", "language": {"name": "en"}},
        {"flavor_text": "Otro", "language": {"name": "es"}},
    ],
    "habitat": {"name": "cave"},
    "is_legendary": True
}

sample_not_legendary = {
    "name": "pikachu",
    "flavor_text_entries": [
        {"flavor_text": "Electric mouse Pokémon", "language": {"name": "en"}},
    ],
    "habitat": {"name": "forest"},
    "is_legendary": False
}

class DummyLegendaryPoke:
    status_code = 200
    def json(self): return sample_legendary

class DummyNotLegendaryPoke:
    status_code = 200
    def json(self): return sample_not_legendary

class DummyYoda:
    status_code = 200
    def json(self):
        return {"contents": {"translated": "Translated Yoda text"}}

class DummyShakespeare:
    status_code = 200
    def json(self):
        return {"contents": {"translated": "Translated Shakespeare text"}}

class DummyUndescribedPoke:
    status_code = 200
    def json(self):
        return {
            "name": "unknownmon",
            "flavor_text_entries": [],
            "habitat": {"name": "forest"},
            "is_legendary": False
        }

class DummyFail:
    status_code = 500
    def json(self): return {}

@pytest.mark.integration
def test_translated_pokemon_yoda(monkeypatch):
    """Integration: cave or legendary Pokémon -> Yoda translation"""

    # Mock Translation API (Yoda success)
    monkeypatch.setattr(pokeapi.requests, "get", lambda url: DummyLegendaryPoke())
    monkeypatch.setattr(translation.requests, "post", lambda url, data, timeout: DummyYoda())

    resp = client.get("/pokemon/translated/mew")
    assert resp.status_code == 200
    body = resp.json()
    assert "Translated" in body["description"]

@pytest.mark.integration
def test_translated_pokemon_shakespeare(monkeypatch):
    """Integration: non-cave, non-legendary Pokémon -> Shakespeare translation"""

    monkeypatch.setattr(pokeapi.requests, "get", lambda url: DummyNotLegendaryPoke())
    monkeypatch.setattr(translation.requests, "post", lambda url, data, timeout: DummyShakespeare())

    resp = client.get("/pokemon/translated/pikachu")
    assert resp.status_code == 200
    data = resp.json()
    assert "Shakespeare" in data["description"]


@pytest.mark.integration
def test_translated_pokemon_fallback_empty_description(monkeypatch):
    """Integration: fallback when no description is available"""
    monkeypatch.setattr(pokeapi.requests, "get", lambda url: DummyUndescribedPoke())

    resp = client.get("/pokemon/translated/unknownmon")
    assert resp.status_code == 200
    data = resp.json()
    assert "description" in data["description"].lower()

@pytest.mark.integration
def test_translated_pokemon_fallback_api_not_sucess(monkeypatch):
    """Integration: fallback to original when translation fails"""

    monkeypatch.setattr(pokeapi.requests, "get", lambda url: DummyLegendaryPoke())
    monkeypatch.setattr(translation.requests, "post", lambda url, data, timeout: DummyFail())

    resp = client.get("/pokemon/translated/mew")
    assert resp.status_code == 200
    body = resp.json()
    assert "Cute Pokémon" in body["description"]

@pytest.mark.integration
def test_translated_pokemon_fallback_api_down(monkeypatch):
    """Integration: Translation API request failure -> fallback to original"""

    def fail_post(*args, **kwargs):
        raise translation.requests.RequestException("Simulated connection error")

    monkeypatch.setattr(pokeapi.requests, "get", lambda url: DummyNotLegendaryPoke())
    monkeypatch.setattr(translation.requests, "post", fail_post)

    resp = client.get("/pokemon/translated/pikachu")
    assert resp.status_code == 200
    data = resp.json()
    assert "Electric mouse" in data["description"]