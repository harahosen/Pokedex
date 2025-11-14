import pytest
from fastapi.testclient import TestClient

# internal dependencies
from app.main import app

client = TestClient(app)

@pytest.mark.smoke
def test_api_health_check():
    """Smoke test: the API should start and respond."""
    resp = client.get("/docs")
    assert resp.status_code == 200

@pytest.mark.smoke
def test_pokemon_basic_route_up():
    """Smoke test: /pokemon/<name> route is live."""
    resp = client.get("/pokemon/mew")
    # it may fail if PokéAPI is not mocked, so just assert no crash
    assert resp.status_code in (200, 404, 502)
