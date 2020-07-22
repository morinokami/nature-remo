from datetime import datetime
from datetime import timezone

from remo import DeviceSchema
from remo import UserSchema


def str_to_datetime(s: str) -> datetime:
    dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    return dt.replace(tzinfo=timezone.utc)


def test_user_model():
    user_id = "user-id-123-abc"
    user_nickname = "lorem ipsum"

    user = UserSchema().load({"id": user_id, "nickname": user_nickname})

    assert user.id == user_id
    assert user.nickname == user_nickname
    assert (
        user.as_json_string()
        == f'{{"id": "{user_id}", "nickname": "{user_nickname}"}}'
    )
    assert str(user) == f'User(id="{user_id}", nickname="{user_nickname}")'


def test_device_model():
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

    device = DeviceSchema().load(
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
    )

    assert device.id == device_id
    assert device.name == device_name
    assert device.temperature_offset == temperature_offset
    assert device.humidity_offset == humidity_offset
    assert device.created_at == str_to_datetime(dummy_datetime)
    assert device.updated_at == str_to_datetime(dummy_datetime)
    assert device.firmware_version == firmware_version
    assert device.mac_address == mac_address
    assert device.serial_number == serial_number
    assert device.newest_events["hu"]["val"] == hu_val
    assert device.newest_events["hu"]["created_at"] == str_to_datetime(
        dummy_datetime
    )
    assert device.newest_events["il"]["val"] == il_val
    assert device.newest_events["il"]["created_at"] == str_to_datetime(
        dummy_datetime
    )
    assert device.newest_events["mo"]["val"] == mo_val
    assert device.newest_events["mo"]["created_at"] == str_to_datetime(
        dummy_datetime
    )
    assert device.newest_events["te"]["val"] == te_val
    assert device.newest_events["te"]["created_at"] == str_to_datetime(
        dummy_datetime
    )

    assert device.as_json_string()
    assert str(device)
