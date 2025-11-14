from pydantic import BaseModel
from typing import Optional

class ErrorDetail(BaseModel):
    type: str
    message: str
    status_code: int
    details: Optional[str] = None

class ErrorResponse(BaseModel):
    error: ErrorDetail
