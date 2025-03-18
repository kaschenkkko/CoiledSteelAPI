from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .api.coiled_steel import coiled_steel_router
from .exceptions.validation_exception_handler import (
    custom_validation_exception_handler,
)

app = FastAPI(
    title='Coiled Steel API',
    description='Минимальный REST API сервис для работы со складом рулонной стали.',
)

app.include_router(coiled_steel_router)
app.add_exception_handler(
    RequestValidationError, custom_validation_exception_handler
)
