from datetime import datetime
from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..exceptions.custom_error_handler import handle_errors
from ..models.coiled_steel import CoiledSteel


@handle_errors
async def create_coiled_steel(
    db: AsyncSession, length: int, weight: int
) -> CoiledSteel:
    """Функция добавляет объект «CoiledSteel» в БД."""
    async with db.begin():
        new_object: CoiledSteel = CoiledSteel(length=length, weight=weight)
        db.add(new_object)
        return new_object


@handle_errors
async def get_coiled_steel_by_id(db: AsyncSession, id: int) -> Optional[CoiledSteel]:
    """Функция получает объект «CoiledSteel», с заданным параметром «ID», из БД."""
    result = await db.execute(select(CoiledSteel).where(CoiledSteel.id == id))
    return result.scalar_one_or_none()


@handle_errors
async def add_deleted_at(db: AsyncSession, coiled_steel: CoiledSteel) -> CoiledSteel:
    """Функция изменяет поле «deleted_at», записывая в него текущую дату и время."""
    coiled_steel.deleted_at = datetime.now()
    await db.commit()
    await db.refresh(coiled_steel)
    return coiled_steel


@handle_errors
async def get_list_coiled_steel(db: AsyncSession, filters):
    """Получаем список объектов «CoiledSteel» по заданным фильтрам.

    Если фильтры не заданы, получим все объекты «CoiledSteel» из БД.
    """
    query = select(CoiledSteel)
    conditions = []

    filter_map = {
        'id': (CoiledSteel.id, filters.min_id, filters.max_id),
        'length': (CoiledSteel.length, filters.min_length, filters.max_length),
        'weight': (CoiledSteel.weight, filters.min_weight, filters.max_weight),
        'created_at': (
            CoiledSteel.created_at, filters.min_created_at, filters.max_created_at
        ),
        'deleted_at': (
            CoiledSteel.deleted_at, filters.min_deleted_at, filters.max_deleted_at
        ),
    }
    for _, (field, min_values, max_values) in filter_map.items():
        min_values = min_values or []
        max_values = max_values or []
        all_pairs = zip(min_values, max_values, strict=False)

        if min_values and max_values:
            conditions.append(or_(*(
                field.between(min_v, max_v) for min_v, max_v in all_pairs))
            )

    if conditions:
        query = query.where(*conditions)

    result = await db.execute(query)
    return result.scalars().all()


@handle_errors
async def get_stats_coiled_steel(db: AsyncSession, range_query):
    """Функция для получения статистики по рулонам за определённый период."""
    query = select(
        func.count(CoiledSteel.created_at).label('number_of_added'),
        func.count(CoiledSteel.deleted_at).label('number_of_deleted'),
        func.avg(CoiledSteel.length).label('avg_length'),
        func.avg(CoiledSteel.weight).label('avg_weight'),
        func.max(CoiledSteel.length).label('max_length'),
        func.min(CoiledSteel.length).label('min_length'),
        func.max(CoiledSteel.weight).label('max_weight'),
        func.min(CoiledSteel.weight).label('min_weight'),
        func.sum(CoiledSteel.weight).label('sum_weight'),
        func.max(
            CoiledSteel.deleted_at - CoiledSteel.created_at
        ).label('max_interval_between_del'),
        func.min(
            CoiledSteel.deleted_at - CoiledSteel.created_at
        ).label('min_interval_between_del'),
    ).where(
        CoiledSteel.created_at.between(range_query.start_date, range_query.end_date)
    )

    result = await db.execute(query)
    statistics = result.first()
    return statistics
