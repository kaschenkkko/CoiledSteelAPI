from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field, model_validator
from pydantic.functional_serializers import PlainSerializer
from typing_extensions import Annotated

from ..core.utils import timedelta_to_str
from ..exceptions.pydantic_validators import validate_range_pairs

CustomTimedelta = Annotated[
    timedelta, PlainSerializer(
        lambda x: timedelta_to_str(x), return_type=str, when_used='json'
    )
]

CustomDatetime = Annotated[
    datetime, PlainSerializer(
        lambda x: x.strftime('%d.%m.%Y %H:%M:%S'), return_type=str, when_used='json'
    )
]


class CoiledSteelAddDOT(BaseModel):
    """Pydantic модель для добавления рулона стали."""

    length: int = Field(gt=0, description='Длина рулона в метрах.')
    weight: int = Field(gt=0, description='Вес рулона в кг.')


class CoiledSteelDOT(CoiledSteelAddDOT):
    """Pydantic модель для получения информации о рулоне стали."""

    id: int = Field(description='ID рулона.')
    created_at: CustomDatetime = Field(description='Дата и время добавления рулона.')
    deleted_at: Optional[CustomDatetime] = Field(
        None, description='Дата и время удаления рулона.')


class CoiledSteelFilterDOT(BaseModel):
    """Pydantic модель для параметров запроса при фильтрации рулонов."""

    min_id: Optional[list[int]] = None
    max_id: Optional[list[int]] = None

    min_length: Optional[list[int]] = None
    max_length: Optional[list[int]] = None

    min_weight: Optional[list[int]] = None
    max_weight: Optional[list[int]] = None

    min_created_at: Optional[list[datetime]] = None
    max_created_at: Optional[list[datetime]] = None

    min_deleted_at: Optional[list[datetime]] = None
    max_deleted_at: Optional[list[datetime]] = None

    @model_validator(mode='before')
    def check_range_pairs(cls, values):
        """Вызываем функцию для валидации фильтров."""
        return validate_range_pairs(values)


class CoiledSteelStatsGetDOT(BaseModel):
    """Pydantic модель для получения статистики по рулонам за определённый период."""

    start_date: datetime = Field(description='Начало диапазона для сбора статистики')
    end_date: datetime = Field(description='Конец диапазона для сбора статистики')

    @model_validator(mode='after')
    def check_date_order(cls, values):
        """Валидация данных. Проверяем что start_date <= end_date."""
        start_date = values.start_date
        end_date = values.end_date
        if start_date and start_date > end_date:
            raise ValueError('start_date должен быть меньше или равен end_date')
        return values


class CoiledSteelStatsDOT(BaseModel):
    """Pydantic модель для вывода статистики по рулонам."""

    number_of_added: Optional[int] = Field(
        description='Количество добавленных рулонов за период'
    )
    number_of_deleted: Optional[int] = Field(
        description='Количество удалённых рулонов за период'
    )
    avg_length: Optional[int] = Field(description='Cредняя длина рулонов за период')
    avg_weight: Optional[int] = Field(description='Cредний вес рулонов за период')
    max_length: Optional[int] = Field(
        description='Максимальная длина рулона за период')
    min_length: Optional[int] = Field(
        description='Минимальная длина рулона за период')
    max_weight: Optional[int] = Field(
        description='Максимальный вес рулонов за период')
    min_weight: Optional[int] = Field(
        description='Минимальный вес рулонов за период')
    sum_weight: Optional[int] = Field(description='Cуммарный вес рулонов на складе')
    max_interval_between_del: Optional[CustomTimedelta] = Field(
        description='Максимальный промежуток между добавлением и удалением рулона'
    )
    min_interval_between_del: Optional[CustomTimedelta] = Field(
        description='Минимальный промежуток между добавлением и удалением рулона'
    )
