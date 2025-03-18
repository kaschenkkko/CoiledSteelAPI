import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_coiled_steel_err422_no_param(async_client: AsyncClient):
    """Тестируем роутер для добавления рулона на склад.

    Не передаём обязательный параметр «length» и ожидаем
    получить ошибку 422.
    """
    request_data = {
        'weight': 500
    }
    response = await async_client.post(
        '/api/v1/coiled_steel',
        json=request_data
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_add_coiled_steel_err422_wrong_format(async_client: AsyncClient):
    """Тестируем роутер для добавления рулона на склад.

    Передаём данные в неправильном формате и ожидаем получить ошибку 422.
    """
    request_data = {
        'length': 'not_an_int',
        'weight': 500
    }
    response = await async_client.post(
        '/api/v1/coiled_steel',
        json=request_data
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_del_coiled_steel_err404(async_client: AsyncClient):
    """Тестируем роутер для удаления рулона со склада.

    Передаём несуществующий ID и ожидаем получить ошибку 404.
    """
    steel_id = 9
    response = await async_client.delete(
        f'/api/v1/coiled_steel/{steel_id}',
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_del_coiled_steel_err422_wrong_format(async_client: AsyncClient):
    """Тестируем роутер для удаления рулона со склада.

    Передаём ID в неправильном формате и ожидаем получить ошибку 422.
    """
    steel_id = 'not_an_int'
    response = await async_client.delete(
        f'/api/v1/coiled_steel/{steel_id}',
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_filtered_coiled_steel_err422_wrong_format(async_client: AsyncClient):
    """Тестируем роутер для получения списка рулонов по заданным параметрам.

    Передаём данные в неправильном формате и ожидаем получить ошибку 422.
    """
    query_params = {'min_id': 'not_an_int', 'max_id': 2}
    response = await async_client.get(
        '/api/v1/coiled_steel',
        params=query_params
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_filtered_coiled_steel_err422_many_param(async_client: AsyncClient):
    """Тестируем роутер для получения списка рулонов по заданным параметрам.

    Передаём несколько параметров для фильтрации и ожидаем получить ошибку 422.
    """
    query_params = {'min_id': 1, 'max_id': 2, 'min_length': 4, 'max_length': 8}
    response = await async_client.get(
        '/api/v1/coiled_steel',
        params=query_params
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_stats_coiled_steel_err422_min_greater_max(async_client: AsyncClient):
    """Тестируем роутер для получения статистики по рулонам.

    Передаём даты в неправильном порядке и ожидаем получить ошибку 422.
    """
    query_params = {'start_date': '3025-03-17', 'end_date': '2025-03-17'}
    response = await async_client.get(
        '/api/v1/coiled_steel/stats',
        params=query_params
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
