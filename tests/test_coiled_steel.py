import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_coiled_steel(async_client: AsyncClient):
    """Тестируем роутер для добавления рулона на склад."""
    request_data = {
        'length': 1000,
        'weight': 500
    }
    response = await async_client.post(
        '/api/v1/coiled_steel',
        json=request_data
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert 'id' in response_data
    assert 'length' in response_data
    assert 'weight' in response_data
    assert 'created_at' in response_data
    assert 'deleted_at' in response_data
    assert response_data['length'] == request_data['length']
    assert response_data['weight'] == request_data['weight']


@pytest.mark.asyncio
async def test_del_coiled_steel(async_client: AsyncClient):
    """Тестируем роутер для удаления рулона со склада."""
    steel_id = 1
    response = await async_client.delete(
        f'/api/v1/coiled_steel/{steel_id}',
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert 'id' in response_data
    assert 'length' in response_data
    assert 'weight' in response_data
    assert 'created_at' in response_data
    assert 'deleted_at' in response_data


@pytest.mark.asyncio
async def test_filtered_coiled_steel(async_client: AsyncClient):
    """Тестируем роутер для получения списка рулонов по заданным параметрам."""
    query_params = {'min_id': 1, 'max_id': 2}
    response = await async_client.get(
        '/api/v1/coiled_steel',
        params=query_params
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert 'id' in response_data[0]
    assert 'length' in response_data[0]
    assert 'weight' in response_data[0]
    assert 'created_at' in response_data[0]
    assert 'deleted_at' in response_data[0]


@pytest.mark.asyncio
async def test_stats_coiled_steel(async_client: AsyncClient):
    """Тестируем роутер для получения статистики по рулонам."""
    query_params = {'start_date': '2025-03-17', 'end_date': '3025-03-17'}
    response = await async_client.get(
        '/api/v1/coiled_steel/stats',
        params=query_params
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert 'number_of_added' in response_data
    assert 'number_of_deleted' in response_data
    assert 'avg_length' in response_data
    assert 'avg_weight' in response_data
    assert 'max_length' in response_data
    assert 'min_length' in response_data
    assert 'max_weight' in response_data
    assert 'min_weight' in response_data
    assert 'sum_weight' in response_data
    assert 'max_interval_between_del' in response_data
    assert 'min_interval_between_del' in response_data
