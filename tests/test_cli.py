import json
import urllib.parse

import pytest
import responses
from click.testing import CliRunner

from remo import NatureRemoError
from remo.api import BASE_URL
from remo.cli import delete_device
from remo.cli import get_devices
from remo.cli import get_ir_signal
from remo.cli import get_user
from remo.cli import send_ir_signal
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
