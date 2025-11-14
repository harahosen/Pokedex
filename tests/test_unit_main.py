import pytest
from fastapi.testclient import TestClient

# internal dependencies
from app import main

@pytest.mark.unit
def test_app_runs_and_docs_available():
    client = TestClient(main.app)
    # health-check via docs (FastAPI auto)
    r = client.get("/docs")
    assert r.status_code == 200
    # endpoint prefix exists
    r2 = client.get("/openapi.json")
    assert r2.status_code == 200
    o = r2.json()
    assert "paths" in o
    assert any(p.startswith("/pokemon") for p in o["paths"].keys())
