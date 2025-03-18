from functools import wraps

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError


class ErrorHandler:
    """Класс для обработки ошибок."""

    @staticmethod
    def coiled_steel_not_found():
        """Возвращает исключение если рулон не найден.

        status code: HTTP_404_NOT_FOUND
        """
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Рулон не найден в БД.'
        )

    @staticmethod
    def coiled_steel_already_been_removed():
        """Возвращает исключение если рулон уже удалён со склада.

        status code: HTTP_400_BAD_REQUEST
        """
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Рулон уже удалён со склада.'
        )


def handle_errors(func):
    """Декоратор для обработки ошибок, при работе с БД, в async функциях."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Ошибка базы данных: {str(err)}'
            ) from err
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Неизвестная ошибка: {str(err)}'
            ) from err
    return wrapper
