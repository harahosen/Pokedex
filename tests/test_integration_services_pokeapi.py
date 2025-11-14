import pytest
from fastapi.testclient import TestClient

# internal dependencies
from app.main import app
from app.services import pokeapi

client = TestClient(app)

# --- mock data shared with your unit test ---
sample_response = {
    "name": "mew",
    "flavor_text_entries": [
        {"flavor_text": "Cute Pokémon", "language": {"name": "en"}},
        {"flavor_text": "Otro", "language": {"name": "es"}},
    ],
    "habitat": {"name": "cave"},
    "is_legendary": True
}

class DummyResp:
    status_code = 200
    def json(self): return sample_response

class DummyFail:
    status_code = 404
    def json(self): return {}

@pytest.mark.integration
def test_pokemon_get_success(monkeypatch):
    """Integration: full flow for GET /pokemon/{name} (OK case)"""

    monkeypatch.setattr(pokeapi.requests, "get", lambda url: DummyResp())

    resp = client.get("/pokemon/mew")
    assert resp.status_code == 200

    data = resp.json()
    assert data["name"] == "mew"
    assert data["habitat"] == "cave"
    assert data["isLegendary"] is True
    assert "Cute" in data["description"]


@pytest.mark.integration
def test_pokemon_get_not_found(monkeypatch):
    """Integration: full flow for GET /pokemon/{name} (KO case)"""
    monkeypatch.setattr(pokeapi.requests, "get", lambda url: DummyFail())

    resp = client.get("/pokemon/missingno")
    # should trigger ExternalAPIError → 502 via handler
    assert resp.status_code == 502

    body = resp.json()
    assert "error" in body
    assert body["error"]["status_code"] == 404
    assert "PokeAPI" in body["error"]["message"]
