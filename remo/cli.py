import os
from functools import wraps
from typing import Callable

import click

from .api import NatureRemoAPI
from .api import NatureRemoLocalAPI
from .errors import NatureRemoError


def get_token_from_env() -> str:
    return os.environ.get("REMO_ACCESS_TOKEN", "")


def check_token(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(token: str, *args, **kwargs):
        token = token if token else get_token_from_env()
        if not token:
            raise NatureRemoError("Access token must be supplied")
        f(token, *args, **kwargs)

    return wrapper


@click.group()
def main():
    pass


@main.group()
def user():
    pass


@user.command("get")
@click.option("--token", default="")
@check_token
def get_user(token: str):
    """Fetch the authenticated user's information."""
    api = NatureRemoAPI(token)
    click.echo(api.get_user().as_json_string())


@user.command("update")
@click.option("--token", default="")
@click.argument("nickname")
@check_token
def update_user(token: str, nickname: str):
    """Update authenticated user's information."""
    api = NatureRemoAPI(token)
    click.echo(api.update_user(nickname).as_json_string())


@main.group()
def local():
    pass


@local.command("get")
@click.argument("ip_addr")
def get_ir_signal(ip_addr: str):
    """Fetch the newest received IR signal."""
    local_api = NatureRemoLocalAPI(ip_addr)
    click.echo(local_api.get_ir_signal().as_json_string())


@local.command("send")
@click.argument("ip_addr")
@click.argument("message")
def send_ir_signal(ip_addr: str, message: str):
    """Emit IR signals provided by request body."""
    local_api = NatureRemoLocalAPI(ip_addr)
    local_api.send_ir_signal(message)


if __name__ == "__main__":
    main()
