import pytest
import responses

from remo import NatureRemoAPI
from remo import NatureRemoError
from remo import User


BASE_URL = "https://api.nature.global"


@pytest.fixture
def api():
    api = NatureRemoAPI("access_token")
    return api


class TestAPI:
    @responses.activate
    def test_unauthorized(self, api):
        responses.add(
            responses.GET,
            f"{BASE_URL}/1/users/me",
            json={"code": 401001, "message": "Unauthorized"},
            status=401,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.get_user()
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 401, "
            + "Nature Remo Code: 401001, Message: Unauthorized"
        )

    @responses.activate
    def test_get_user(self, api):
        user_id = "user-id-123-abc"
        user_nickname = "lorem ipsum"
        responses.add(
            responses.GET,
            f"{BASE_URL}/1/users/me",
            json={"id": user_id, "nickname": user_nickname},
            status=200,
        )

        user = api.get_user()
        assert type(user) is User
        assert user.id == user_id
        assert user.nickname == user_nickname
        assert (
            user.as_json_string()
            == f'{{"id": "{user_id}", "nickname": "{user_nickname}"}}'
        )
        assert str(user) == f'User(id="{user_id}", nickname="{user_nickname}")'

    @responses.activate
    def test_update_user(self, api):
        user_id = "user-id-123-abc"
        user_nickname = "lorem ipsum updated"
        responses.add(
            responses.POST,
            f"{BASE_URL}/1/users/me",
            json={"id": user_id, "nickname": user_nickname},
            status=200,
        )

        user = api.update_user(user_nickname)
        assert type(user) is User
        assert user.id == user_id
        assert user.nickname == user_nickname
        assert (
            user.as_json_string()
            == f'{{"id": "{user_id}", "nickname": "{user_nickname}"}}'
        )
        assert str(user) == f'User(id="{user_id}", nickname="{user_nickname}")'
