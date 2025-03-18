from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def standard_validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    """Стандартный обработчик ошибок валидации данных."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors(), 'body': exc.body}),
    )


async def custom_validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    """Кастомный обработчик ошибок валидации данных."""
    for error in exc.errors():
        error_loc = error.get('loc')

        if 'body' in error_loc or 'query' in error_loc or 'path' in error_loc:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    'loc': exc.errors()[0].get('loc'),
                    'detail': exc.errors()[0].get('msg')
                }
            )

    return await standard_validation_exception_handler(request, exc)
