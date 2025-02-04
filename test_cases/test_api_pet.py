import pytest
import json
import os

from api_requests.api_methods import PetstoreApi

pa = PetstoreApi()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.mark.parametrize("pet_id, category_id, category_name, name, photo_urls, tag_id, tag_name, status", [
    (30, 5, "cats", "mayo", ["https://disk.yandex.ru/i/_ImUt2Rkl1KH6ghttps://disk.yandex.ru/i/_ImUt2Rkl1KH6g"], 5,
     "cat", "available"),
    (31, 6, "dogs", "buddy", ["https://disk.yandex.ru/i/_ImUt2Rkl1KH6ghttps://disk.yandex.ru/i/_ImUt2Rkl1KH6g"], 6,
     "dog", "pending"),
    (32, 7, "birds", "song", ["https://disk.yandex.ru/i/_ImUt2Rkl1KH6ghttps://disk.yandex.ru/i/_ImUt2Rkl1KH6g"], 7,
     "bird", "sold")
])
def test_create_pet_positive(pet_id, category_id, category_name, name, photo_urls, tag_id, tag_name, status):
    response = pa.create_pet(pet_id, category_id, category_name, name, photo_urls, tag_id, tag_name, status)
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"

    response_data = response.json()
    assert "name" in response_data, "Ключ 'name' отсутствует в ответе"
    assert "status" in response_data, "Ключ 'status' отсутствует в ответе"
    assert response_data["name"] == name, "Имя питомца не совпадает."
    assert response_data["status"] == status, "Статус питомца некорректен."


@pytest.mark.parametrize("pet_id, category_id, category_name, name, photo_urls, tag_id, tag_name, status", [
    ("", "", "", "", [""], "", "", ""),
    ("a", 2, 4444, "", ["^&^%$%"], 6, ".......", ""),
    (None, None, None, None, [None], None, None, None)
])
def test_create_pet_negative(pet_id, category_id, category_name, name, photo_urls, tag_id, tag_name, status):
    response = pa.create_pet(pet_id, category_id, category_name, name, photo_urls, tag_id, tag_name, status)
    assert response.status_code in [400, 404], f"Некорректный статус ответа: {response.status_code}"


@pytest.mark.parametrize("pet_id, meta_data, photo_path", [
    (31, "test_meta_data", os.path.join(BASE_DIR, "test_photo.jpg"))
])
def test_post_pet_image_positive(pet_id, meta_data, photo_path):
    assert os.path.exists(photo_path), f"Файл {photo_path} не существует"
    response = pa.post_pet_image(pet_id, meta_data, photo_path)
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"

    response_data = response.json()
    assert "message" in response_data, "Ключ 'message' отсутствует в ответе"


@pytest.mark.parametrize("pet_id, expected_name", [
    (30, "mayo"),
    (31, "buddy"),
    (32, "song")
])
def test_get_pet_id_positive(pet_id, expected_name):
    response = pa.get_pet_id(pet_id)
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"

    response_data = response.json()
    assert response_data["name"] == expected_name, "Имя питомца не совпадает."


@pytest.mark.parametrize("pet_id", [
    (-1),
    (999),
    (0),
    (None),
    (""),
    ("abc"),
    ("123abc"),
    ("@#$%"),
])
def test_get_pet_id_negative(pet_id):
    response = pa.get_pet_id(pet_id)
    assert response.status_code in [400, 404], f"Некорректный статус ответа: {response.status_code}"

    response_data = response.json()
    assert response_data["message"] == "Pet not found"


@pytest.mark.parametrize("status", [
    ("available"),
    ("pending"),
    ("sold")
])
def test_get_pet_by_status_positive(status):
    response = pa.get_pet_by_status(status)
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"

    response_data = response.json()
    assert isinstance(response_data, list), "Ответ API должен быть списком"
    for pet in response_data:
        assert pet.get("status") == status


@pytest.mark.parametrize("status", [
    (""),
    ("nonexisting status"),
    ("%^$%$%$")
])
def test_get_pet_by_status_negative(status):
    response = pa.get_pet_by_status(status)
    assert response.status_code in [400, 404], f"Некорректный статус ответа: {response.status_code}"


@pytest.mark.parametrize("pet_id, category_id, category_name, name, photo_urls, tag_id, tag_name, status", [
    (30, 5, "cats", "bean", ["https://disk.yandex.ru/i/_ImUt2Rkl1KH6ghttps://disk.yandex.ru/i/_ImUt2Rkl1KH6g"], 5,
     "cat", "pending"),
    (31, 6, "dogs", "ben", ["https://disk.yandex.ru/i/_ImUt2Rkl1KH6ghttps://disk.yandex.ru/i/_ImUt2Rkl1KH6g"], 6,
     "dog", "available"),
    (32, 7, "birds", "whiskey", ["https://disk.yandex.ru/i/_ImUt2Rkl1KH6ghttps://disk.yandex.ru/i/_ImUt2Rkl1KH6g"], 7,
     "bird", "pending")
])
def test_update_pet_info_positive(pet_id, category_id, category_name, name, photo_urls, tag_id, tag_name, status):
    response = pa.update_pet_info(pet_id, category_id, category_name, name, photo_urls, tag_id, tag_name, status)
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"

    response_data = response.json()
    assert "name" in response_data, "Ключ 'name' отсутствует в ответе"
    assert "status" in response_data, "Ключ 'status' отсутствует в ответе"
    assert response_data["name"] == name, "Имя питомца не совпадает."
    assert response_data["status"] == status, "Статус питомца некорректен."


@pytest.mark.parametrize("pet_id, category_id, category_name, name, photo_urls, tag_id, tag_name, status", [
    ("", "", "", "", [""], "", "", ""),
    ("a", 2, 4444, "", ["^&^%$%"], 6, ".......", ""),
    (None, None, None, None, [None], None, None, None)
])
def test_update_pet_info_negative(pet_id, category_id, category_name, name, photo_urls, tag_id, tag_name, status):
    response = pa.update_pet_info(pet_id, category_id, category_name, name, photo_urls, tag_id, tag_name, status)
    assert response.status_code in [400, 404], f"Некорректный статус ответа: {response.status_code}"


@pytest.mark.parametrize("pet_id", [
    (30),
    (31),
    (32)
])
def test_delete_pet_positive(pet_id):
    response = pa.delete_pet(pet_id)
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"


@pytest.mark.parametrize("pet_id", [
    (-1),
    (999),
    (0),
    (None),
    (""),
    ("abc"),
    ("123abc"),
    ("@#$%"),
])
def test_delete_pet_negative(pet_id):
    response = pa.delete_pet(pet_id)
    assert response.status_code in [400, 404], f"Некорректный статус ответа: {response.status_code}"
