import pytest
import json

from api_requests.api_methods import PetstoreApi

pa = PetstoreApi()


@pytest.mark.parametrize("order_id, pet_id, quantity, ship_date, status", [
    (50, 1, 1, "2025-02-03T18:35:02.289Z", "placed"),
    (51, 2, 1, "2025-03-03T18:35:02.289Z", "pending")
])
def test_create_oder_positive(order_id, pet_id, quantity, ship_date, status):
    response = pa.create_order(order_id, pet_id, quantity, ship_date, status)
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"


@pytest.mark.parametrize("id, pet_id, quantity, ship_date, status", [
    ("", "", "", "", ""),
    ("%^%%", "$##", "%$%", "#$#$%^^", "^&^^^*"),
    (None, None, None, None, None),
    (-1, -1, -1, "fjhf", "#$#$%^^")
])
def test_create_oder_negative(id, pet_id, quantity, ship_date, status):
    response = pa.create_order(id, pet_id, quantity, ship_date, status)
    assert response.status_code in [400, 404], f"Некорректный статус ответа: {response.status_code}"


def test_get_store_inventory():
    response = pa.get_store_inventory()
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"

    response_data = response.json()
    assert "sold" in response_data, "Ключ 'message' отсутствует в ответе"


@pytest.mark.parametrize("order_id", [
    (50),
    (51)
])
def test_get_order_id_positive(order_id):
    response = pa.get_order_id(order_id)
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"

    response_data = response.json()
    assert "status" in response_data, "Ключ 'message' отсутствует в ответе"


@pytest.mark.parametrize("order_id", [
    (-1),
    (0),
    (999),
    (None),
    (""),
    ("abc"),
    ("123abc"),
    ("@#$%"),
])
def test_get_order_id_negative(order_id):
    response = pa.get_order_id(order_id)
    assert response.status_code in [400, 404], f"Некорректный статус ответа: {response.status_code}"

    response_data = response.json()
    assert response_data["message"] == "Order not found"


@pytest.mark.parametrize("order_id", [
    (50),
    (51)
])
def test_delete_order_positive(order_id):
    response = pa.delete_order(order_id)
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"


@pytest.mark.parametrize("order_id", [
    (0),
    (-1),
    (9999),
    (None),
    (""),
    ("abc"),
    ("123abc"),
    ("@#$%"),
])
def test_delete_order_negative(order_id):
    response = pa.delete_order(order_id)
    assert response.status_code in [400, 404], f"Некорректный статус ответа: {response.status_code}"
