import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

# internal dependencies
from app.routes import pokemon as pokemon_routes

app = FastAPI()
app.include_router(pokemon_routes.router)
client = TestClient(app)


@pytest.mark.unit
def test_get_pokemon_route(monkeypatch):
    # Mock pokeapi.get_pokemon_data
    monkeypatch.setattr("services.pokeapi.get_pokemon_data", lambda name: {
        "name": name,
        "description": "Original text",
        "habitat": "cave",
        "isLegendary": False,
    })

@pytest.mark.unit
def test_get_translation_route(monkeypatch):
    # Mock translation.translate_description to return a translation
    monkeypatch.setattr("services.translation.translate_description", lambda desc, hab, isleg: "Yoda-ish")

    r = client.get("/pokemon/translated/mew")
    assert r.status_code == 200
    j = r.json()
    assert j["description"] == "Yoda-ish"
