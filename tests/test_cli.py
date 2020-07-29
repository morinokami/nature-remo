import json

import pytest
import responses
from click.testing import CliRunner

from remo import NatureRemoError
from remo.api import BASE_URL
from remo.cli import get_ir_signal
from remo.cli import get_user


def dumps(data):
    return json.dumps(data, ensure_ascii=True, sort_keys=True)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def set_token(monkeypatch):
    monkeypatch.setenv("REMO_ACCESS_TOKEN", "access_token")


class TestCLI:
    def test_no_access_token_raises(self, runner):
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

        assert result.output.strip() == dumps(data)

    @responses.activate
    def test_get_ir_signal(self, runner):
        ip_addr = "192.168.1.1"
        url = f"http://{ip_addr}/messages"
        data = {"freq": 38, "data": [0], "format": "us"}
        responses.add(
            responses.GET, url, json=data, status=200,
        )

        result = runner.invoke(get_ir_signal, [ip_addr])

        assert result.output.strip() == dumps(data)
