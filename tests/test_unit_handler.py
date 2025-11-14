import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# internal dependencies
from app.exceptions.handlers import register_exception_handlers, ExternalAPIError, TranslationError


@pytest.mark.unit
def test_external_api_error_handler():
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/boom")
    def boom():
        raise ExternalAPIError("PokeAPI", 503, "Timeout")
    client = TestClient(app)
    r = client.get("/boom")
    assert r.status_code == 502
    data = r.json()
    assert data["error"]["type"] == "ExternalAPIError"
    assert "Timeout" in data["error"]["details"]


@pytest.mark.unit
def test_translation_error_handler():
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/translate_fail")
    def tfail():
        raise TranslationError("Rate limited")
    client = TestClient(app)
    r = client.get("/translate_fail")
    # Current refactor returns HTTP 200 with ErrorResponse schema
    assert r.status_code == 200
    data = r.json()
    assert data["error"]["type"] == "TranslationError"
    assert "Rate limited" in data["error"]["details"]

