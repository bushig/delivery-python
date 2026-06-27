from __future__ import annotations

from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from src.core.application.queries.get_all_couriers import CourierResponseDTO
from src.core.application.queries.get_not_completed_orders import NotCompletedOrderResponseDTO
from src.core.domain.model.location import Location
from src.libs.errs.exceptions import DomainInvariantException, NotFoundException
from src.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_order_201(client: AsyncClient) -> None:
    order_id = uuid4()
    payload = {
        "id": str(order_id),
        "address": {
            "country": "Russia",
            "city": "Moscow",
            "street": "Tverskaya",
            "house": "1",
            "apartment": "1",
        },
        "volume": 5,
    }

    with patch(
        "src.adapters.in_.http.routers.create_order.create_order_use_case",
        new_callable=AsyncMock,
    ):
        response = await client.post("/api/v1/orders", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert "orderId" in data
        assert data["orderId"] == str(order_id)


@pytest.mark.asyncio
async def test_create_order_default_volume(client: AsyncClient) -> None:
    order_id = uuid4()
    payload = {
        "id": str(order_id),
        "address": {
            "country": "Russia",
            "city": "Moscow",
            "street": "Tverskaya",
            "house": "1",
            "apartment": "1",
        },
    }

    with patch(
        "src.adapters.in_.http.routers.create_order.create_order_use_case",
        new_callable=AsyncMock,
    ):
        response = await client.post("/api/v1/orders", json=payload)

        assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_order_validation_empty_body(client: AsyncClient) -> None:
    response = await client.post("/api/v1/orders", json={})

    assert response.status_code == 400
    data = response.json()
    assert data["code"] == "validation_error"


@pytest.mark.asyncio
async def test_complete_order_200(client: AsyncClient) -> None:
    courier_id = uuid4()
    order_id = uuid4()

    with patch(
        "src.adapters.in_.http.routers.complete_order.complete_order_use_case",
        new_callable=AsyncMock,
    ):
        response = await client.post(
            f"/api/v1/couriers/{courier_id}/orders/{order_id}/complete"
        )

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_complete_order_not_found_404(client: AsyncClient) -> None:
    courier_id = uuid4()
    order_id = uuid4()

    with patch(
        "src.adapters.in_.http.routers.complete_order.complete_order_use_case",
        new_callable=AsyncMock,
    ) as mock_handler:
        mock_handler.side_effect = NotFoundException(
            MagicMock(code="not_found", message="Courier not found")
        )

        response = await client.post(
            f"/api/v1/couriers/{courier_id}/orders/{order_id}/complete"
        )
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_complete_order_domain_error_409(client: AsyncClient) -> None:
    courier_id = uuid4()
    order_id = uuid4()

    with patch(
        "src.adapters.in_.http.routers.complete_order.complete_order_use_case",
        new_callable=AsyncMock,
    ) as mock_handler:
        mock_handler.side_effect = DomainInvariantException(
            MagicMock(
                code="assignment_not_found", message="Assignment not found"
            )
        )

        response = await client.post(
            f"/api/v1/couriers/{courier_id}/orders/{order_id}/complete"
        )
        assert response.status_code == 409


@pytest.mark.asyncio
async def test_move_courier_200(client: AsyncClient) -> None:
    courier_id = uuid4()
    payload = {"x": 5, "y": 8}

    with patch(
        "src.adapters.in_.http.routers.move_courier.move_courier_use_case",
        new_callable=AsyncMock,
    ):
        response = await client.post(f"/api/v1/couriers/{courier_id}/move", json=payload)

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_move_courier_not_found_404(client: AsyncClient) -> None:
    courier_id = uuid4()
    payload = {"x": 5, "y": 8}

    with patch(
        "src.adapters.in_.http.routers.move_courier.move_courier_use_case",
        new_callable=AsyncMock,
    ) as mock_handler:
        mock_handler.side_effect = NotFoundException(
            MagicMock(code="not_found", message="Courier not found")
        )

        response = await client.post(f"/api/v1/couriers/{courier_id}/move", json=payload)
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_orders_200(client: AsyncClient) -> None:
    order_id = uuid4()

    with patch(
        "src.adapters.in_.http.routers.get_orders.get_not_completed_orders_use_case",
        new_callable=AsyncMock,
    ) as mock_handler:
        mock_handler.return_value = [
            NotCompletedOrderResponseDTO(
                id=order_id, location=Location(x=5, y=8)
            )
        ]

        response = await client.get("/api/v1/orders/active")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == str(order_id)
        assert data[0]["location"]["x"] == 5
        assert data[0]["location"]["y"] == 8


@pytest.mark.asyncio
async def test_get_orders_empty(client: AsyncClient) -> None:
    with patch(
        "src.adapters.in_.http.routers.get_orders.get_not_completed_orders_use_case",
        new_callable=AsyncMock,
    ) as mock_handler:
        mock_handler.return_value = []

        response = await client.get("/api/v1/orders/active")
        assert response.status_code == 200
        data = response.json()
        assert data == []


@pytest.mark.asyncio
async def test_create_courier_201(client: AsyncClient) -> None:
    payload = {"name": "John"}
    courier_id = uuid4()

    mock_courier = MagicMock()
    mock_courier.id = courier_id

    with patch(
        "src.adapters.in_.http.routers.create_courier.create_courier_use_case",
        new_callable=AsyncMock,
    ) as mock_handler:
        mock_handler.return_value = mock_courier

        response = await client.post("/api/v1/couriers", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "courierId" in data


@pytest.mark.asyncio
async def test_get_couriers_200(client: AsyncClient) -> None:
    courier_id = uuid4()

    with patch(
        "src.adapters.in_.http.routers.get_couriers.get_all_couriers_use_case",
        new_callable=AsyncMock,
    ) as mock_handler:
        mock_handler.return_value = [
            CourierResponseDTO(
                id=courier_id, name="John", location=Location(x=5, y=6)
            )
        ]

        response = await client.get("/api/v1/couriers")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == str(courier_id)
        assert data[0]["name"] == "John"
        assert data[0]["location"]["x"] == 5
        assert data[0]["location"]["y"] == 6
