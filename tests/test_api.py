import pytest
import responses

from remo import Device
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

    @responses.activate
    def test_get_devices(self, api):
        device_id = "device-id-123-abc"
        device_name = "Remo"
        temperature_offset = 0
        humidity_offset = 0
        dummy_datetime = "2020-01-01T01:23:45Z"
        firmware_version = "Remo/1.0.23"
        mac_address = "ab:cd:ef:01:23:45"
        serial_number = "1W111111111111"
        hu_val = 76
        il_val = 0
        mo_val = 1
        te_val = 25.149109
        responses.add(
            responses.GET,
            f"{BASE_URL}/1/devices",
            json=[
                {
                    "id": device_id,
                    "name": device_name,
                    "temperature_offset": temperature_offset,
                    "humidity_offset": humidity_offset,
                    "created_at": dummy_datetime,
                    "updated_at": dummy_datetime,
                    "firmware_version": firmware_version,
                    "mac_address": mac_address,
                    "serial_number": serial_number,
                    "newest_events": {
                        "hu": {"val": hu_val, "created_at": dummy_datetime},
                        "il": {"val": il_val, "created_at": dummy_datetime},
                        "mo": {"val": mo_val, "created_at": dummy_datetime},
                        "te": {"val": te_val, "created_at": dummy_datetime},
                    },
                }
            ],
            status=200,
        )

        devices = api.get_devices()

        assert type(devices) is list
        assert len(devices) == 1
        assert all(type(d) is Device for d in devices)

    @responses.activate
    def test_update_device(self, api):
        device = "my-device"
        name = "natureremo"
        responses.add(
            responses.POST, f"{BASE_URL}/1/devices/{device}", status=200
        )

        try:
            api.update_device(device, name)
        except NatureRemoError as e:
            pytest.fail(str(e))

    @responses.activate
    def test_update_device_raises(self, api):
        device = "my-device"
        name = "natureremo"
        responses.add(
            responses.POST, f"{BASE_URL}/1/devices/{device}", status=500
        )

        with pytest.raises(NatureRemoError):
            api.update_device(device, name)
