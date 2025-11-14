import pytest
from fastapi.testclient import TestClient

# internal dependencies
from app.main import app

client = TestClient(app)

@pytest.mark.e2e
def test_real_pokemon_translation_e2e():
    """End-to-End: call the real PokéAPI + FunTranslations"""
    resp = client.get("/pokemon/translated/charizard")
    assert resp.status_code == 200
    data = resp.json()
    assert "charizard" in data["name"]
    assert isinstance(data["description"], str)
    # Usually one of Yoda or Shakespeare translation depending on habitat/legendary
    assert len(data["description"]) > 10
