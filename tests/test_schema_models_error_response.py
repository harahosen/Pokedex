import pytest

# internal dependencies
from app.models.error_response import ErrorDetail, ErrorResponse

@pytest.mark.schema
def test_error_response_model_ok():
    detail = ErrorDetail(type="ExternalAPIError", message="API error", status_code=502, details="Timeout")
    resp = ErrorResponse(error=detail)
    d = resp.dict()
    assert "error" in d and d["error"]["type"] == "ExternalAPIError"
