from typing import Any

from fastapi.responses import JSONResponse

from database.schemas import ErrorScheme


async def validation_exception_handler(_: Any, exc: Any) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=ErrorScheme(
            code=400, message=f'Validation error: {exc}'
        ).dict(),
    )
