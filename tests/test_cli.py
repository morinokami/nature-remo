import json
import urllib.parse

import pytest
import responses
from click.testing import CliRunner

from .utils import load_json
from remo.api import BASE_URL
from remo.cli import create_appliance
from remo.cli import create_signal
from remo.cli import delete_appliance
from remo.cli import delete_device
from remo.cli import delete_signal
from remo.cli import detect_appliance
from remo.cli import get_appliances
from remo.cli import get_devices
from remo.cli import get_ir_signal
from remo.cli import get_signals
from remo.cli import get_user
from remo.cli import send_ir_signal
from remo.cli import send_light_infrared_signal
from remo.cli import send_signal
from remo.cli import send_tv_infrared_signal
from remo.cli import update_aircon_settings
from remo.cli import update_appliance
from remo.cli import update_appliance_orders
from remo.cli import update_device
from remo.cli import update_humidity_offset
from remo.cli import update_signal
from remo.cli import update_signal_orders
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

        assert result.output.strip() == "Error: Access token must be supplied"

    @responses.activate
    def test_get_user(self, runner, set_token):
        data = load_json("testdata/user.json")
        url = f"{BASE_URL}/1/users/me"
        responses.add(responses.GET, url, json=data, status=200)

        result = runner.invoke(get_user)

        assert result.exit_code == 0
        assert result.output.strip() == dumps(data)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_update_user(self, runner, set_token):
        data = load_json("testdata/user.json")
        url = f"{BASE_URL}/1/users/me"
        responses.add(
            responses.POST, url, json=data, status=200,
        )

        result = runner.invoke(update_user, [data["nickname"]])

        assert result.exit_code == 0
        assert result.output.strip() == dumps(data)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"nickname={urllib.parse.quote_plus(data['nickname'])}"
        )

    @responses.activate
    def test_get_devices(self, runner, set_token):
        data = [load_json("testdata/device.json")]
        url = f"{BASE_URL}/1/devices"
        responses.add(responses.GET, url, json=data, status=200)

        result = runner.invoke(get_devices)

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_update_device(self, runner, set_token):
        device = "device-id"
        name = "Remo"
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
        data = [load_json("testdata/appliance_model_and_params.json")]
        url = f"{BASE_URL}/1/detectappliance"
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
        data = [load_json("testdata/appliance.json")]
        url = f"{BASE_URL}/1/appliances"
        responses.add(responses.GET, url, json=data, status=200)

        result = runner.invoke(get_appliances)

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_create_appliance(self, runner, set_token):
        data = load_json("testdata/appliance.json")
        url = f"{BASE_URL}/1/appliances"
        responses.add(responses.POST, url, json=data, status=201)

        result = runner.invoke(
            create_appliance,
            [data["device"]["id"], data["nickname"], data["image"]],
        )

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == (
            f"device={data['device']['id']}&nickname={data['nickname']}&"
            f"image={data['image']}"
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
        data = load_json("testdata/appliance_minimal.json")
        url = f"{BASE_URL}/1/appliances/{data['id']}"
        responses.add(responses.POST, url, json=data, status=200)

        result = runner.invoke(
            update_appliance, [data["id"], data["nickname"], data["image"]]
        )

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
    def test_get_signals(self, runner, set_token):
        appliance = "appliance-id"
        data = [
            {"id": "id-1", "name": "signal1", "image": "ico_signal"},
            {"id": "id-2", "name": "signal2", "image": "ico_signal"},
        ]
        url = f"{BASE_URL}/1/appliances/{appliance}/signals"
        responses.add(responses.GET, url, json=data, status=200)

        result = runner.invoke(get_signals, [appliance])

        assert result.exit_code == 0
        assert result.output.strip() == dumps(data)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_create_signal(self, runner, set_token):
        appliance = "appliance_id"
        name = "signal1"
        message = '{"freq": 38, "data": [2523, 2717, 786], "format": "us"}'
        image = "ico_signal"
        data = load_json("testdata/signal.json")
        url = f"{BASE_URL}/1/appliances/{appliance}/signals"
        responses.add(
            responses.POST, url, json=data, status=201,
        )

        result = runner.invoke(
            create_signal, [appliance, name, message, image]
        )

        assert result.exit_code == 0
        assert result.output.strip() == dumps(data)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"name={name}&message={urllib.parse.quote_plus(message)}&"
            + f"image={image}"
        )

    @responses.activate
    def test_update_signal_orders(self, runner, set_token):
        appliance = "appliance-id"
        signals = "id-xxx,id-yyy,id-zzz"
        url = f"{BASE_URL}/1/appliances/{appliance}/signal_orders"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(update_signal_orders, [appliance, signals])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert (
            responses.calls[0].request.body
            == f"signals={urllib.parse.quote_plus(signals)}"
        )

    @responses.activate
    def test_update_signal(self, runner, set_token):
        signal = "signal-id"
        name = "signal"
        image = "ico_signal"
        url = f"{BASE_URL}/1/signals/{signal}"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(update_signal, [signal, name, image])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.body == f"name={name}&image={image}"

    @responses.activate
    def test_delete_signal(self, runner, set_token):
        signal = "signal-id"
        url = f"{BASE_URL}/1/signals/{signal}/delete"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(delete_signal, [signal])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

    @responses.activate
    def test_send_signal(self, runner, set_token):
        signal = "signal-id"
        url = f"{BASE_URL}/1/signals/{signal}/send"
        responses.add(responses.POST, url, status=200)

        result = runner.invoke(send_signal, [signal])

        assert result.exit_code == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url

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
