import urllib

import pytest
import responses

from remo import Appliance
from remo import Device
from remo import IRSignal
from remo import NatureRemoAPI
from remo import NatureRemoError
from remo import NatureRemoLocalAPI
from remo import Signal
from remo import User


BASE_URL = "https://api.nature.global"


@pytest.fixture
def api():
    return NatureRemoAPI("access_token")


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
        url = f"{BASE_URL}/1/users/me"
        responses.add(
            responses.GET,
            url,
            json={"id": user_id, "nickname": user_nickname},
            status=200,
        )

        user = api.get_user()

        assert type(user) is User
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_update_user(self, api):
        user_id = "user-id-123-abc"
        user_nickname = "lorem ipsum updated"
        url = f"{BASE_URL}/1/users/me"
        responses.add(
            responses.POST,
            url,
            json={"id": user_id, "nickname": user_nickname},
            status=200,
        )

        user = api.update_user(user_nickname)

        assert type(user) is User
        assert user.id == user_id
        assert user.nickname == user_nickname
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

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
        url = f"{BASE_URL}/1/devices"
        responses.add(
            responses.GET,
            url,
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
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_update_device(self, api):
        device = "my-device"
        name = "natureremo"
        url = f"{BASE_URL}/1/devices/{device}"
        responses.add(responses.POST, url, status=200)

        try:
            api.update_device(device, name)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == f"name={name}"

    @responses.activate
    def test_update_device_raises(self, api):
        device = "my-device"
        name = "natureremo"
        responses.add(
            responses.POST,
            f"{BASE_URL}/1/devices/{device}",
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.update_device(device, name)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_delete_device(self, api):
        device = "my-device"
        url = f"{BASE_URL}/1/devices/{device}/delete"
        responses.add(responses.POST, url, status=200)

        try:
            api.delete_device(device)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_delete_device_raises(self, api):
        device = "my-device"
        responses.add(
            responses.POST,
            f"{BASE_URL}/1/devices/{device}/delete",
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.delete_device(device)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_update_temperature_offset(self, api):
        device = "my-device"
        offset = 10
        url = f"{BASE_URL}/1/devices/{device}/temperature_offset"
        responses.add(
            responses.POST, url, status=200,
        )

        try:
            api.update_temperature_offset(device, offset)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == f"offset={offset}"

    @responses.activate
    def test_update_temperature_offset_raises(self, api):
        device = "my-device"
        offset = 10
        responses.add(
            responses.POST,
            f"{BASE_URL}/1/devices/{device}/temperature_offset",
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.update_temperature_offset(device, offset)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_update_humidity_offset(self, api):
        device = "my-device"
        offset = 10
        url = f"{BASE_URL}/1/devices/{device}/humidity_offset"
        responses.add(
            responses.POST, url, status=200,
        )

        try:
            api.update_humidity_offset(device, offset)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == f"offset={offset}"

    @responses.activate
    def test_update_humidity_offset_raises(self, api):
        device = "my-device"
        offset = 10
        responses.add(
            responses.POST,
            f"{BASE_URL}/1/devices/{device}/humidity_offset",
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.update_humidity_offset(device, offset)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_get_appliances(self, api):
        id = "appliance-id"
        device = {
            "id": "device_id",
            "name": "device_name",
            "temperature_offset": 0,
            "humidity_offset": 0,
            "created_at": "2020-01-01T01:23:45Z",
            "updated_at": "2020-01-01T01:23:45Z",
            "firmware_version": "Remo/1.0.23",
            "mac_address": "ab:cd:ef:01:23:45",
            "serial_number": "1W111111111111",
        }
        model = {
            "id": "appliance-modelid",
            "manufacturer": "XXX",
            "remote_name": "abc123",
            "name": "XXX AC 001",
            "image": "ico_appliance_model",
        }
        nickname = "appliance-nickname"
        image = "ico_appliance"
        type_ = "AC"
        settings = {
            "temp": "27",
            "mode": "cool",
            "vol": "auto",
            "dir": "swing",
            "button": "power-off",
        }
        aircon = {
            "range": {
                "modes": {
                    "mode1": {
                        "temp": ["1", "2", "3"],
                        "vol": ["1", "auto"],
                        "dir": ["1", "2"],
                    },
                    "mode2": {
                        "temp": ["1", "2"],
                        "vol": ["1", "2", "auto"],
                        "dir": ["auto", "swing"],
                    },
                },
                "fixedButtons": ["power-off"],
            },
            "tempUnit": "c",
        }
        signals = [
            {"id": "signal-id", "name": "signal-name", "image": "ico_signal"}
        ]
        tv = {
            "state": {"input": "t"},
            "buttons": [
                {
                    "name": "button-name",
                    "image": "ico_button",
                    "label": "button_label",
                }
            ],
        }
        responses.add(
            responses.GET,
            f"{BASE_URL}/1/appliances",
            json=[
                {
                    "id": id,
                    "device": device,
                    "model": model,
                    "nickname": nickname,
                    "image": image,
                    "type": type_,
                    "settings": settings,
                    "aircon": aircon,
                    "signals": signals,
                    "tv": tv,
                }
            ],
            status=200,
        )

        appliances = api.get_appliances()

        assert type(appliances) is list
        assert len(appliances) == 1
        assert all(type(a) is Appliance for a in appliances)

    @responses.activate
    def test_create_appliance(self, api):
        device_id = "device-id-123-abc"
        device_name = "Remo"
        temperature_offset = 0
        humidity_offset = 0
        dummy_datetime = "2020-01-01T01:23:45Z"
        firmware_version = "Remo/1.0.23"
        mac_address = "ab:cd:ef:01:23:45"
        serial_number = "1W111111111111"
        device = {
            "id": device_id,
            "name": device_name,
            "temperature_offset": temperature_offset,
            "humidity_offset": humidity_offset,
            "created_at": dummy_datetime,
            "updated_at": dummy_datetime,
            "firmware_version": firmware_version,
            "mac_address": mac_address,
            "serial_number": serial_number,
        }
        appliance_id = "appliance-id"
        nickname = "my-appliance"
        image = "ico_appliance"
        url = f"{BASE_URL}/1/appliances"
        responses.add(
            responses.POST,
            url,
            json={
                "id": appliance_id,
                "device": device,
                "nickname": nickname,
                "image": image,
                "model": None,
                "type": "IR",
                "settings": None,
                "aircon": None,
                "signals": [],
            },
            status=201,
        )

        appliance = api.create_appliance(device_id, nickname, image)

        assert type(appliance) is Appliance
        assert appliance.id == appliance_id
        assert appliance.nickname == nickname
        assert appliance.image == image
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"device={device_id}&nickname={nickname}&image={image}"
        )

    @responses.activate
    def test_create_appliance_raises(self, api):
        device_id = "device-id-123-abc"
        nickname = "my-appliance"
        image = "ico_appliance"
        url = f"{BASE_URL}/1/appliances"
        responses.add(
            responses.POST,
            url,
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.create_appliance(device_id, nickname, image)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_update_appliance_orders(self, api):
        url = f"{BASE_URL}/1/appliance_orders"
        responses.add(
            responses.POST, url, status=200,
        )

        appliances = "id-xxx,id-yyy,id-zzz"
        try:
            api.update_appliance_orders(appliances)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"appliances={urllib.parse.quote(appliances)}"
        )

    @responses.activate
    def test_update_appliance_orders_raises(self, api):
        url = f"{BASE_URL}/1/appliance_orders"
        responses.add(
            responses.POST,
            url,
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        appliances = "id-xxx,id-yyy,id-zzz"
        with pytest.raises(NatureRemoError) as excinfo:
            api.update_appliance_orders(appliances)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_delete_appliance(self, api):
        appliance = "appliance-id"
        url = f"{BASE_URL}/1/appliances/{appliance}/delete"
        responses.add(responses.POST, url, status=200)

        try:
            api.delete_appliance(appliance)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_delete_appliance_raises(self, api):
        appliance = "appliance-id"
        url = f"{BASE_URL}/1/appliances/{appliance}/delete"
        responses.add(
            responses.POST,
            url,
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.delete_appliance(appliance)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_update_appliance(self, api):
        appliance = "appliance-id"
        nickname = "appliance-nickname"
        image = "ico_nickname"
        url = f"{BASE_URL}/1/appliances/{appliance}"
        responses.add(responses.POST, url, status=200)

        try:
            api.update_appliance(appliance, nickname, image)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"nickname={nickname}&image={image}"
        )

    @responses.activate
    def test_update_appliance_raises(self, api):
        appliance = "appliance-id"
        nickname = "appliance-nickname"
        image = "ico_nickname"
        url = f"{BASE_URL}/1/appliances/{appliance}"
        responses.add(
            responses.POST,
            url,
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.update_appliance(appliance, nickname, image)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_update_aircon_settings(self, api):
        appliance = "appliance-id"
        operation_mode = "cool"
        temperature = "25"
        air_volume = "1"
        air_direction = "auto"
        button = "power-off"
        url = f"{BASE_URL}/1/appliances/{appliance}/aircon_settings"
        responses.add(responses.POST, url, status=200)

        try:
            api.update_aircon_settings(
                appliance,
                operation_mode,
                temperature,
                air_volume,
                air_direction,
                button,
            )
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"operation_mode={operation_mode}&temperature={temperature}&"
            + f"air_volume={air_volume}&air_direction={air_direction}"
            + f"&button={button}"
        )

    @responses.activate
    def test_update_aircon_settings_raises(self, api):
        appliance = "appliance-id"
        operation_mode = "cool"
        temperature = "25"
        air_volume = "1"
        air_direction = "auto"
        button = "power-off"
        url = f"{BASE_URL}/1/appliances/{appliance}/aircon_settings"
        responses.add(
            responses.POST,
            url,
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.update_aircon_settings(
                appliance,
                operation_mode,
                temperature,
                air_volume,
                air_direction,
                button,
            )
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_send_tv_infrared_signal(self, api):
        appliance = "appliance-id"
        button = "button1"
        url = f"{BASE_URL}/1/appliances/{appliance}/tv"
        responses.add(responses.POST, url, status=200)

        try:
            api.send_tv_infrared_signal(appliance, button)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == f"button={button}"

    @responses.activate
    def test_send_tv_infrared_signal_raises(self, api):
        appliance = "appliance-id"
        button = "button1"
        url = f"{BASE_URL}/1/appliances/{appliance}/tv"
        responses.add(
            responses.POST,
            url,
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.send_tv_infrared_signal(appliance, button)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_send_light_infrared_signal(self, api):
        appliance = "appliance-id"
        button = "button1"
        url = f"{BASE_URL}/1/appliances/{appliance}/light"
        responses.add(responses.POST, url, status=200)

        try:
            api.send_light_infrared_signal(appliance, button)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == f"button={button}"

    @responses.activate
    def test_send_light_infrared_signal_raises(self, api):
        appliance = "appliance-id"
        button = "button1"
        url = f"{BASE_URL}/1/appliances/{appliance}/light"
        responses.add(
            responses.POST,
            url,
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.send_light_infrared_signal(appliance, button)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_get_signals(self, api):
        signal1 = {"id": "id-1", "name": "signal1", "image": "ico_signal"}
        signal2 = {"id": "id-2", "name": "signal2", "image": "ico_signal"}
        appliance = "appliance-id"
        url = f"{BASE_URL}/1/appliances/{appliance}/signals"
        responses.add(responses.GET, url, json=[signal1, signal2], status=200)

        signals = api.get_signals(appliance)

        assert type(signals) is list
        assert len(signals) == 2
        assert all(type(s) is Signal for s in signals)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_create_signal(self, api):
        appliance = "appliance_id"
        name = "signal1"
        message = '{"freq": 38, "data": [2523, 2717, 786], "format": "us"}'
        image = "ico_signal"
        url = f"{BASE_URL}/1/appliances/{appliance}/signals"
        responses.add(
            responses.POST,
            url,
            json={"id": "signal-id", "name": name, "image": image},
            status=201,
        )

        signal = api.create_signal(appliance, name, message, image)

        assert type(signal) is Signal
        assert signal.name == name
        assert signal.image == image
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"name={name}&message={urllib.parse.quote_plus(message)}&"
            + f"image={image}"
        )

    @responses.activate
    def test_create_signal_raises(self, api):
        appliance = "appliance_id"
        name = "signal1"
        message = '{"freq": 38, "data": [2523, 2717, 786], "format": "us"}'
        image = "ico_signal"
        url = f"{BASE_URL}/1/appliances/{appliance}/signals"
        responses.add(
            responses.POST,
            url,
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.create_signal(appliance, name, message, image)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_update_signal_orders(self, api):
        appliance = "appliance-id"
        url = f"{BASE_URL}/1/appliances/{appliance}/signal_orders"
        responses.add(
            responses.POST, url, status=200,
        )

        signals = "id-xxx,id-yyy,id-zzz"
        try:
            api.update_signal_orders(appliance, signals)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"signals={urllib.parse.quote(signals)}"
        )

    @responses.activate
    def test_update_signal_orders_raises(self, api):
        appliance = "appliance-id"
        url = f"{BASE_URL}/1/appliances/{appliance}/signal_orders"
        responses.add(
            responses.POST,
            url,
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        signals = "id-xxx,id-yyy,id-zzz"
        with pytest.raises(NatureRemoError) as excinfo:
            api.update_signal_orders(appliance, signals)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_update_signal(self, api):
        signal = "signal-id"
        name = "signal1"
        image = "ico_signal"
        url = f"{BASE_URL}/1/signals/{signal}"
        responses.add(responses.POST, url, status=200)

        try:
            api.update_signal(signal, name, image)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == f"name={name}&image={image}"

    @responses.activate
    def test_update_signal_raises(self, api):
        signal = "signal-id"
        name = "signal1"
        image = "ico_signal"
        url = f"{BASE_URL}/1/signals/{signal}"
        responses.add(
            responses.POST,
            url,
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.update_signal(signal, name, image)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_delete_signal(self, api):
        signal = "signal-id"
        url = f"{BASE_URL}/1/signals/{signal}/delete"
        responses.add(responses.POST, url, status=200)

        try:
            api.delete_signal(signal)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_delete_signal_raises(self, api):
        signal = "signal-id"
        url = f"{BASE_URL}/1/signals/{signal}/delete"
        responses.add(
            responses.POST,
            url,
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.delete_signal(signal)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )

    @responses.activate
    def test_send_signal(self, api):
        signal = "signal-id"
        url = f"{BASE_URL}/1/signals/{signal}/send"
        responses.add(responses.POST, url, status=200)

        try:
            api.send_signal(signal)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_send_signal_raises(self, api):
        signal = "signal-id"
        url = f"{BASE_URL}/1/signals/{signal}/send"
        responses.add(
            responses.POST,
            url,
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

        with pytest.raises(NatureRemoError) as excinfo:
            api.send_signal(signal)
        assert (
            str(excinfo.value)
            == "HTTP Status Code: 400, "
            + "Nature Remo Code: 123456, Message: Bad Request"
        )


@pytest.fixture
def local_api():
    return NatureRemoLocalAPI("192.168.1.1")


class TestLocalAPI:
    @responses.activate
    def test_get(self, local_api):
        freq = 38
        data = [0]
        format = "us"
        url = f"http://{local_api.addr}/messages"
        responses.add(
            responses.GET,
            url,
            json={"freq": freq, "data": data, "format": format},
            status=200,
        )

        ir_signal = local_api.get()

        assert type(ir_signal) is IRSignal
        assert ir_signal.freq == freq
        assert ir_signal.data == data
        assert ir_signal.format == format
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_post(self, local_api):
        message = '{"format": "us", "freq": 38, "data": [0]}'
        url = f"http://{local_api.addr}/messages"
        responses.add(responses.POST, url, status=200)

        try:
            local_api.post(message)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == message
