from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_session
from ..crud.coiled_steel import (
    add_deleted_at,
    create_coiled_steel,
    get_coiled_steel_by_id,
    get_list_coiled_steel,
    get_stats_coiled_steel,
)
from ..exceptions.custom_error_handler import ErrorHandler
from ..schemas.coiled_steel import (
    CoiledSteelAddDOT,
    CoiledSteelDOT,
    CoiledSteelFilterDOT,
    CoiledSteelStatsDOT,
    CoiledSteelStatsGetDOT,
)

coiled_steel_router = APIRouter()


@coiled_steel_router.post(
        '/api/v1/coiled_steel',
        response_model=CoiledSteelDOT,
        status_code=status.HTTP_201_CREATED,
        summary='Добавление нового рулона на склад',
)
async def add_coiled_steel(
    session: Annotated[AsyncSession, Depends(get_session)],
    request: CoiledSteelAddDOT,
):
    """Добавляем новый рулон на склад, принимая параметры рулона в теле запроса."""
    new_coiled_steel = await create_coiled_steel(
        session, request.length, request.weight
    )
    return new_coiled_steel


@coiled_steel_router.delete(
        '/api/v1/coiled_steel/{steel_id}',
        response_model=CoiledSteelDOT,
        status_code=status.HTTP_200_OK,
        summary='Удаление рулона со склада',
)
async def del_coiled_steel(
    session: Annotated[AsyncSession, Depends(get_session)],
    steel_id: int = Path(..., description='ID рулона'),
):
    """Удаляем рулон со склада, изменяя поле «deleted_at» в БД."""
    coiled_steel = await get_coiled_steel_by_id(session, steel_id)

    if coiled_steel is None:
        ErrorHandler.coiled_steel_not_found()
    if coiled_steel.deleted_at is not None:
        ErrorHandler.coiled_steel_already_been_removed()

    await add_deleted_at(session, coiled_steel)

    return coiled_steel


@coiled_steel_router.get(
        '/api/v1/coiled_steel',
        response_model=List[Optional[CoiledSteelDOT]],
        status_code=status.HTTP_200_OK,
        summary='Получение списка рулонов со склада',
)
async def filtered_coiled_steel(
    session: Annotated[AsyncSession, Depends(get_session)],
    filter_query: Annotated[CoiledSteelFilterDOT, Query()],
):
    """Получаем список рулонов по заданным параметрам запроса.

    Фильтрация работает с комбинациями нескольких диапазонов сразу.
    Если параметры не переданы, то результатом будет список со всеми объектами
    рулонов из БД.

    Примеры запросов:

    - api/v1/coiled_steel
    - api/v1/coiled_steel?min_id=2&max_id=7
    - api/v1/coiled_steel?min_created_at=2025-03-17&max_created_at=2025-03-30

    Пример комбинации нескольких диапазонов сразу:
    - api/v1/coiled_steel?min_id=2&max_id=4&min_id=7&max_id=9
    """
    list_coiled_steel = await get_list_coiled_steel(session, filter_query)
    return list_coiled_steel


@coiled_steel_router.get(
        '/api/v1/coiled_steel/stats',
        response_model=CoiledSteelStatsDOT,
        status_code=status.HTTP_200_OK,
        summary='Cтатистика по рулонам за определённый период',
)
async def stats_coiled_steel(
    session: Annotated[AsyncSession, Depends(get_session)],
    range_query: Annotated[CoiledSteelStatsGetDOT, Query()],
):
    """Получаем статистику по рулонам за определённый период.

    Пример запроса:

    - api/v1/coiled_steel/stats?start_date=2025-03-17&end_date=2025-03-30
    """
    stats = await get_stats_coiled_steel(session, range_query)

    return stats
