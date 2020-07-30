import urllib.parse
from datetime import datetime

import pytest
import responses

from .utils import load_json
from remo import Appliance
from remo import ApplianceModelAndParams
from remo import Device
from remo import IRSignal
from remo import NatureRemoAPI
from remo import NatureRemoError
from remo import NatureRemoLocalAPI
from remo import Signal
from remo import User
from remo.api import BASE_URL


@pytest.fixture
def api():
    return NatureRemoAPI("access_token")


class TestAPI:
    def test_rate_limit_before_request(self, api):
        assert api.rate_limit.checked_at is None
        assert api.rate_limit.limit is None
        assert api.rate_limit.remaining is None
        assert api.rate_limit.reset is None

    @responses.activate
    def test_rate_limit_after_request(self, api):
        date = "Tue, 28 Jul 2020 07:17:31 GMT"
        limit = 30
        remaining = 29
        reset = 1595920800
        responses.add(
            responses.GET,
            f"{BASE_URL}/1/users/me",
            headers={
                "Date": date,
                "X-Rate-Limit-Limit": str(limit),
                "X-Rate-Limit-Remaining": str(remaining),
                "X-Rate-Limit-Reset": str(reset),
            },
            json={"id": "user-id", "nickname": "lorem ipsum"},
            status=200,
        )

        api.get_user()

        assert api.rate_limit.checked_at == datetime(2020, 7, 28, 7, 17, 31)
        assert api.rate_limit.limit == limit
        assert api.rate_limit.remaining == remaining
        assert api.rate_limit.reset == datetime(2020, 7, 28, 7, 20)

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
        data = load_json("testdata/user.json")
        url = f"{BASE_URL}/1/users/me"
        responses.add(
            responses.GET, url, json=data, status=200,
        )

        user = api.get_user()

        assert type(user) is User
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_update_user(self, api):
        data = load_json("testdata/user.json")
        url = f"{BASE_URL}/1/users/me"
        responses.add(
            responses.POST, url, json=data, status=200,
        )

        user = api.update_user(data["nickname"])

        assert type(user) is User
        assert user.id == data["id"]
        assert user.nickname == data["nickname"]
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_get_devices(self, api):
        data = [load_json("testdata/device.json")]
        url = f"{BASE_URL}/1/devices"
        responses.add(
            responses.GET, url, json=data, status=200,
        )

        devices = api.get_devices()

        assert type(devices) is list
        assert len(devices) == 1
        assert all(type(d) is Device for d in devices)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_update_device(self, api):
        device = "device-id"
        name = "Remo"
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
        device = "device-id"
        name = "Remo"
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
        device = "device-id"
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
        device = "device-id"
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
        device = "device-id"
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
        device = "device-id"
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
        device = "device-id"
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
        device = "device-id"
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
    def test_detect_appliance(self, api):
        message = '{"format": "us", "freq": 38, "data": [0]}'
        data = [load_json("testdata/appliance_model_and_params.json")]
        url = f"{BASE_URL}/1/detectappliance"
        responses.add(
            responses.POST, url, json=data, status=200,
        )

        model_and_params = api.detect_appliance(message)

        assert type(model_and_params) is list
        assert len(model_and_params) == 1
        assert type(model_and_params[0]) is ApplianceModelAndParams

    @responses.activate
    def test_get_appliances(self, api):
        data = [load_json("testdata/appliance.json")]
        url = f"{BASE_URL}/1/appliances"
        responses.add(
            responses.GET, url, json=data, status=200,
        )

        appliances = api.get_appliances()

        assert type(appliances) is list
        assert len(appliances) == 1
        assert all(type(a) is Appliance for a in appliances)

    @responses.activate
    def test_create_appliance(self, api):
        data = load_json("testdata/appliance_minimal.json")
        url = f"{BASE_URL}/1/appliances"
        responses.add(
            responses.POST, url, json=data, status=201,
        )

        appliance = api.create_appliance(
            data["device"]["id"], data["nickname"], data["image"]
        )

        assert type(appliance) is Appliance
        assert appliance.id == data["id"]
        assert appliance.nickname == data["nickname"]
        assert appliance.image == data["image"]
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == (
            f"device={data['device']['id']}&nickname={data['nickname']}&"
            f"image={data['image']}"
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
        appliances = "id-xxx,id-yyy,id-zzz"
        url = f"{BASE_URL}/1/appliance_orders"
        responses.add(
            responses.POST, url, status=200,
        )

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
        appliances = "id-xxx,id-yyy,id-zzz"
        url = f"{BASE_URL}/1/appliance_orders"
        responses.add(
            responses.POST,
            url,
            json={"code": 123456, "message": "Bad Request"},
            status=400,
        )

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
        data = load_json("testdata/appliance_minimal.json")
        url = f"{BASE_URL}/1/appliances/{data['id']}"
        responses.add(responses.POST, url, json=data, status=200)

        appliance = api.update_appliance(
            data["id"], data["nickname"], data["image"]
        )

        assert type(appliance) is Appliance
        assert appliance.id == data["id"]
        assert appliance.nickname == data["nickname"]
        assert appliance.image == data["image"]
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"nickname={data['nickname']}&image={data['image']}"
        )

    @responses.activate
    def test_update_appliance_raises(self, api):
        appliance = "appliance-id"
        nickname = "appliance-nickname"
        image = "ico_appliance"
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
        appliance = "appliance-id"
        message = '{"freq": 38, "data": [2523, 2717, 786], "format": "us"}'
        data = load_json("testdata/signal.json")
        url = f"{BASE_URL}/1/appliances/{appliance}/signals"
        responses.add(
            responses.POST, url, json=data, status=201,
        )

        signal = api.create_signal(
            appliance, data["name"], message, data["image"]
        )

        assert type(signal) is Signal
        assert signal.name == data["name"]
        assert signal.image == data["image"]
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == (
            f"name={data['name']}&message={urllib.parse.quote_plus(message)}&"
            f"image={data['image']}"
        )

    @responses.activate
    def test_create_signal_raises(self, api):
        appliance = "appliance-id"
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
    def test_get_message(self, local_api):
        data = load_json("testdata/ir_signal.json")
        url = f"http://{local_api.addr}/messages"
        responses.add(
            responses.GET, url, json=data, status=200,
        )

        ir_signal = local_api.get_ir_signal()

        assert type(ir_signal) is IRSignal
        assert ir_signal.freq == data["freq"]
        assert ir_signal.data == data["data"]
        assert ir_signal.format == data["format"]
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_post_message(self, local_api):
        message = '{"format": "us", "freq": 38, "data": [0]}'
        url = f"http://{local_api.addr}/messages"
        responses.add(responses.POST, url, status=200)

        try:
            local_api.send_ir_signal(message)
        except NatureRemoError as e:
            pytest.fail(str(e))

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == message
