from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

# internal dependencies
from utils.logger import logger
from models.error_response import ErrorResponse, ErrorDetail

# Exception for API failure
class ExternalAPIError(Exception):
    def __init__(self, source: str, status_code: int, detail: str):
        self.source = source
        self.status_code = status_code
        self.detail = detail

# Exception for translation failure
class TranslationError(Exception):
    def __init__(self, message: str):
        self.message = message

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ExternalAPIError)
    def external_api_error_handler(request: Request, exc: ExternalAPIError):
        logger.error(f"[{request.url.path}] {exc.source} API failed ({exc.status_code}): {exc.detail}")

        error_response = ErrorResponse(
            error=ErrorDetail(
                type=exc.__class__.__name__,
                message=f"{exc.source} API error",
                status_code=exc.status_code,
                details=exc.detail
            )
        )
        return JSONResponse(status_code=502, content=error_response.dict())

    @app.exception_handler(TranslationError)
    def translation_error_handler(request: Request, exc: TranslationError):
        logger.warning(f"[{request.url.path}] Translation failed: {exc.message}")

        error_response = ErrorResponse(
            error=ErrorDetail(
                type=exc.__class__.__name__,
                message="Translation unavailable, returning original text.",
                status_code=200,
                details=exc.message
            )
        )
        return JSONResponse(status_code=200, content=error_response.dict())

    @app.exception_handler(Exception)
    def generic_exception_handler(request: Request, exc: Exception):
        logger.error(f"[{request.url.path}] Unhandled exception: {exc}")

        error_response = ErrorResponse(
            error=ErrorDetail(
                type=exc.__class__.__name__,
                message="Internal Server Error",
                status_code=500,
                details=str(exc)
            )
        )
        return JSONResponse(status_code=500, content=error_response.dict())
