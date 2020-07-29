import json
import urllib.parse

import pytest
import responses
from click.testing import CliRunner

from remo import NatureRemoError
from remo.api import BASE_URL
from remo.cli import create_appliance
from remo.cli import delete_appliance
from remo.cli import delete_device
from remo.cli import detect_appliance
from remo.cli import get_appliances
from remo.cli import get_devices
from remo.cli import get_ir_signal
from remo.cli import get_user
from remo.cli import send_ir_signal
from remo.cli import send_light_infrared_signal
from remo.cli import send_tv_infrared_signal
from remo.cli import update_aircon_settings
from remo.cli import update_appliance
from remo.cli import update_appliance_orders
from remo.cli import update_device
from remo.cli import update_humidity_offset
from remo.cli import update_temperature_offset
from remo.cli import update_user


def dumps(data):
    return json.dumps(data, ensure_ascii=True, sort_keys=True)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def set_token(monkeypatch):
    monkeypatch.setenv("REMO_ACCESS_TOKEN", "access_token")


class TestCLI:
    def test_no_access_token_raises(self, runner, monkeypatch):
        monkeypatch.delenv("REMO_ACCESS_TOKEN", raising=False)
        result = runner.invoke(get_user)

        assert result.exit_code != 0
        assert type(result.exception) is NatureRemoError
        assert str(result.exception) == "Access token must be supplied"

    @responses.activate
    def test_get_user(self, runner, set_token):
        url = f"{BASE_URL}/1/users/me"
        data = {"id": "user-id", "nickname": "lorem ipsum"}
        responses.add(responses.GET, url, json=data, status=200)

        result = runner.invoke(get_user)

        assert result.exit_code == 0
        assert result.output.strip() == dumps(data)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_update_user(self, runner, set_token):
        nickname = "lorem ipsum"
        url = f"{BASE_URL}/1/users/me"
        data = {"id": "user-id", "nickname": nickname}
        responses.add(
            responses.POST, url, json=data, status=200,
        )

        result = runner.invoke(update_user, [nickname])

        assert result.exit_code == 0
        assert result.output.strip() == dumps(data)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"nickname={urllib.parse.quote_plus(nickname)}"
        )

    @responses.activate
    def test_get_devices(self, runner, set_token):
        url = f"{BASE_URL}/1/devices"
        data = [
            {
                "id": "device-id",
                "name": "Remo",
                "temperature_offset": 0,
                "humidity_offset": 0,
                "created_at": "2020-01-01T01:23:45Z",
                "updated_at": "2020-01-01T01:23:45Z",
                "firmware_version": "Remo/1.0.23",
                "mac_address": "ab:cd:ef:01:23:45",
                "serial_number": "1W111111111111",
                "newest_events": {
                    "hu": {"val": 76, "created_at": "2020-01-01T01:23:45Z"},
                    "il": {"val": 0, "created_at": "2020-01-01T01:23:45Z"},
                    "mo": {"val": 1, "created_at": "2020-01-01T01:23:45Z"},
                    "te": {
                        "val": 25.149109,
                        "created_at": "2020-01-01T01:23:45Z",
                    },
                },
            }
        ]
        responses.add(responses.GET, url, json=data, status=200)

        result = runner.invoke(get_devices)

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_update_device(self, runner, set_token):
        device = "device-id"
        name = "remo"
        url = f"{BASE_URL}/1/devices/{device}"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(update_device, [device, name])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == f"name={name}"

    @responses.activate
    def test_delete_device(self, runner, set_token):
        device = "device-id"
        url = f"{BASE_URL}/1/devices/{device}/delete"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(delete_device, [device])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_update_temperature_offset(self, runner, set_token):
        device = "device-id"
        offset = "1"
        url = f"{BASE_URL}/1/devices/{device}/temperature_offset"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(update_temperature_offset, [device, offset])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == f"offset={offset}"

    @responses.activate
    def test_update_humidity_offset(self, runner, set_token):
        device = "device-id"
        offset = "1"
        url = f"{BASE_URL}/1/devices/{device}/humidity_offset"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(update_humidity_offset, [device, offset])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == f"offset={offset}"

    @responses.activate
    def test_detect_appliance(self, runner, set_token):
        message = '{"format": "us", "freq": 38, "data": [0]}'
        url = f"{BASE_URL}/1/detectappliance"
        data = [
            {
                "model": {
                    "id": "appliance-modelid",
                    "manufacturer": "XXX",
                    "remote_name": "abc123",
                    "name": "XXX AC 001",
                    "image": "ico_appliance_model",
                },
                "params": {
                    "temp": "27",
                    "mode": "cool",
                    "vol": "auto",
                    "dir": "swing",
                    "button": "power-off",
                },
            }
        ]
        responses.add(responses.POST, url, json=data, status=200)

        result = runner.invoke(detect_appliance, [message])

        assert result.exit_code == 0
        assert result.output.strip() == dumps(data)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"message={urllib.parse.quote_plus(message)}"
        )

    @responses.activate
    def test_get_appliances(self, runner, set_token):
        url = f"{BASE_URL}/1/appliances"
        data = [
            {
                "id": "appliance-id",
                "device": {
                    "id": "device_id",
                    "name": "device_name",
                    "temperature_offset": 0,
                    "humidity_offset": 0,
                    "created_at": "2020-01-01T01:23:45Z",
                    "updated_at": "2020-01-01T01:23:45Z",
                    "firmware_version": "Remo/1.0.23",
                    "mac_address": "ab:cd:ef:01:23:45",
                    "serial_number": "1W111111111111",
                },
                "model": {
                    "id": "appliance-modelid",
                    "manufacturer": "XXX",
                    "remote_name": "abc123",
                    "name": "XXX AC 001",
                    "image": "ico_appliance_model",
                },
                "nickname": "appliance-nickname",
                "image": "ico_appliance",
                "type": "AC",
                "settings": {
                    "temp": "27",
                    "mode": "cool",
                    "vol": "auto",
                    "dir": "swing",
                    "button": "power-off",
                },
                "aircon": {
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
                },
                "signals": [
                    {
                        "id": "signal-id",
                        "name": "signal-name",
                        "image": "ico_signal",
                    }
                ],
                "tv": {
                    "state": {"input": "t"},
                    "buttons": [
                        {
                            "name": "button-name",
                            "image": "ico_button",
                            "label": "button_label",
                        }
                    ],
                },
            }
        ]
        responses.add(responses.GET, url, json=data, status=200)

        result = runner.invoke(get_appliances)

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_create_appliance(self, runner, set_token):
        device = "device-id"
        nickname = "my-device"
        image = "ico_appliance"
        url = f"{BASE_URL}/1/appliances"
        data = {
            "id": "appliance-id",
            "device": {
                "id": "device-id-123-abc",
                "name": "Remo",
                "temperature_offset": 0,
                "humidity_offset": 0,
                "created_at": "2020-01-01T01:23:45Z",
                "updated_at": "2020-01-01T01:23:45Z",
                "firmware_version": "Remo/1.0.23",
                "mac_address": "ab:cd:ef:01:23:45",
                "serial_number": "1W111111111111",
            },
            "nickname": "my-appliance",
            "image": "ico_appliance",
            "model": None,
            "type": "IR",
            "settings": None,
            "aircon": None,
            "signals": [],
        }
        responses.add(responses.POST, url, json=data, status=201)

        result = runner.invoke(create_appliance, [device, nickname, image])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"device={device}&nickname={nickname}&image={image}"
        )

    @responses.activate
    def test_update_appliance_orders(self, runner, set_token):
        appliances = "id-xxx,id-yyy,id-zzz"
        url = f"{BASE_URL}/1/appliance_orders"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(update_appliance_orders, [appliances])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"appliances={urllib.parse.quote_plus(appliances)}"
        )

    @responses.activate
    def test_delete_appliance(self, runner, set_token):
        appliance = "appliance-id"
        url = f"{BASE_URL}/1/appliances/{appliance}/delete"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(delete_appliance, [appliance])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_update_appliance(self, runner, set_token):
        appliance = "appliance-id"
        nickname = "appliance-nickname"
        image = "ico_appliance"
        url = f"{BASE_URL}/1/appliances/{appliance}"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(update_appliance, [appliance, nickname, image])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_update_aircon_settings(self, runner, set_token):
        appliance = "appliance-id"
        air_direction = "auto"
        url = f"{BASE_URL}/1/appliances/{appliance}/aircon_settings"
        responses.add(
            responses.POST, url, status=200,
        )

        result = runner.invoke(
            update_aircon_settings,
            [appliance, "--air-direction", air_direction],
        )

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body == f"air_direction={air_direction}"
        )

    @responses.activate
    def test_send_tv_infrared_signal(self, runner, set_token):
        appliance = "appliance-id"
        button = "button"
        url = f"{BASE_URL}/1/appliances/{appliance}/tv"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(send_tv_infrared_signal, [appliance, button])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == f"button={button}"

    @responses.activate
    def test_send_light_infrared_signal(self, runner, set_token):
        appliance = "appliance-id"
        button = "button"
        url = f"{BASE_URL}/1/appliances/{appliance}/light"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(send_light_infrared_signal, [appliance, button])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == f"button={button}"

    @responses.activate
    def test_get_ir_signal(self, runner):
        ip_addr = "192.168.1.1"
        url = f"http://{ip_addr}/messages"
        data = {"freq": 38, "data": [0], "format": "us"}
        responses.add(
            responses.GET, url, json=data, status=200,
        )

        result = runner.invoke(get_ir_signal, [ip_addr])

        assert result.exit_code == 0
        assert result.output.strip() == dumps(data)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_send_ir_signal(self, runner):
        message = '{"format": "us", "freq": 38, "data": [0]}'
        ip_addr = "192.168.1.1"
        url = f"http://{ip_addr}/messages"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(send_ir_signal, [ip_addr, message])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == message
