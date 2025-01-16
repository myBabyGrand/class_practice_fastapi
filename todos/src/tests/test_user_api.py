from http import HTTPStatus
from database.orm import User
from database.repository import UserRepository
from service.user import UserService



def test_user_sign_up(client, mocker):
    hash_password = mocker.patch.object(
        UserService,
        "hash_password",
        return_value="hashed_test_pw"
    )
    user_create = mocker.patch.object(
        User,
        "create",
        return_value=User(id=None, username="test_user", password="hashed_test_pw")
    )
    saved_user = mocker.patch.object(
        UserRepository,
        "save_user",
        return_value=User(id=99, username="test_user", password="hashed_test_pw")
    )

    body = {
        "username" : "test_user",
        "password" : "test_pw"
    }
    response = client.post("/users/sign-up", json=body)
    hash_password.assert_called_once_with(
        plain_password="test_pw"
    )
    user_create.assert_called_once_with(
        username = "test_user",
        hashed_password = "hashed_test_pw"
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id":99, "username":"test_user"}