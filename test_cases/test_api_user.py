import pytest
import json

from api_requests.api_methods import PetstoreApi

pa = PetstoreApi()


@pytest.mark.parametrize("user_id,username,first_name,last_name,email,password,phone,status", [
    (50, "test_1", "john", "smith", "yada@yada.com", "test_pass_1", "9999999999", 1),
    (52, "test_2", "miras", "angel", "yada_1@yada.com", "test_pass_2", "8888888888", 1)
])
def test_create_user_positive(user_id, username, first_name, last_name, email, password, phone, status):
    response = pa.create_user(user_id, username, first_name, last_name, email, password, phone, status)
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"


@pytest.mark.parametrize("user_id,username,first_name,last_name,email,password,phone,status", [
    (None, None, None, None, None, None, None, None),
    ("", "", "", "", "", "", "", ""),
    (1, 1, 1, 1, 1, 1, 1, 1),
    ("%$%$%%", "%%$%$%^", 11111, 5555, "%$%$%", "**&&&&", 000, "&&^^")
])
def test_create_user_negative(user_id, username, first_name, last_name, email, password, phone, status):
    response = pa.create_user(user_id, username, first_name, last_name, email, password, phone, status)
    assert response.status_code in [400, 404], f"Некорректный статус ответа: {response.status_code}"


@pytest.mark.parametrize("username", [
    ("test_1"),
    ("test_2")
])
def test_get_user_by_username_positive(username):
    response = pa.get_user_by_username(username)
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"


@pytest.mark.parametrize("username", [
    ("john"),
    (""),
    (1),
    ("^^^%&"),
    (None),
    ("agg^^^^")
])
def test_get_user_by_username_positive(username):
    response = pa.get_user_by_username(username)
    assert response.status_code in [400, 404], f"Некорректный статус ответа: {response.status_code}"


@pytest.mark.parametrize("username, password", [
    ("test_1", "test_pass_1"),
    ("test_2", "test_pass_2")
])
def test_user_login_positive(username, password):
    response = pa.get_user_login(username, password)
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"


@pytest.mark.parametrize("username, password", [
    ("test_1", "test_pass_2"),
    ("test_2", "test_pass_1"),
    ("", ""),
    (None, None),
    ("$$%$$$", "^^%^"),
    (1, 1)
])
def test_user_login_negative(username, password):
    response = pa.get_user_login(username, password)
    assert response.status_code in [400, 404], f"Некорректный статус ответа: {response.status_code}"


def test_user_logout():
    response = pa.get_user_logout()
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"


@pytest.mark.parametrize("username", [
    ("test_1"),
    ("test_2")
])
def test_delete_user(username):
    response = pa.delete_user(username)
    assert response.status_code == 200, f"Некорректный статус ответа: {response.status_code}"


@pytest.mark.parametrize("username", [
    ("orb"),
    (""),
    (1),
    ("^^^%&"),
    (None),
    ("agg^^^^")
])
def test_delete_user(username):
    response = pa.delete_user(username)
    assert response.status_code in [400, 404], f"Некорректный статус ответа: {response.status_code}"
