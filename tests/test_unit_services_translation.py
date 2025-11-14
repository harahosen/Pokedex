import pytest

# internal dependencies
from app.services import translation
from app.exceptions.handlers import TranslationError

class DummySuccess:
    status_code = 200
    def json(self):
        return {"contents": {"translated": "Translated text"}}

class DummyFail:
    status_code = 500
    def json(self):
        return {}

# test for an OK from the Yoda translation service
@pytest.mark.unit
def test_translation_Yoda(monkeypatch):
    # Test Yoda chosen for cave or legendary
    monkeypatch.setattr(translation.requests, "post", lambda url, data, timeout: DummySuccess())
    translated = translation.translate_description("Original", "cave", False)
    assert translated == "Translated text"

# test for an OK from the Shakespeare translation service
@pytest.mark.unit
def test_translation_Shakespeare(monkeypatch):
    monkeypatch.setattr(translation.requests, "post", lambda url, data, timeout: DummySuccess())
    translated = translation.translate_description("Original", "forest", False)
    assert translated == "Translated text"

# test for an OK from the fallback escape calling the translation service
@pytest.mark.unit
def test_translation_back_to_original(monkeypatch):
    # Test fallback on bad status code (should return original)
    monkeypatch.setattr(translation.requests, "post", lambda url, data, timeout: DummyFail())
    translated = translation.translate_description("Original", "forest", False)
    assert translated == "Original"
