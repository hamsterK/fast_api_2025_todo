from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['email'] == 'testuser@mail.com'
    assert response.json()['first_name'] == 'Test'
    assert response.json()['last_name'] == 'User'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '111-11-11'


def test_change_password_success(test_user):
    response = client.put('/user/password', json={"old_password": "testpassword", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put('/user/password', json={"old_password": "wrrongpassword", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert response.json() == {'detail': 'Wrong initial password'}


def test_change_phone_success(test_user):
    response = client.put('/user/phone_number', json='222-22-22')
    assert response.status_code == status.HTTP_204_NO_CONTENT
