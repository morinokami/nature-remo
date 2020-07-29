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
@click.option("--debug", default=False, is_flag=True)
@check_token
def get_user(token: str, debug: bool):
    """Fetch the authenticated user's information."""
    api = NatureRemoAPI(token, debug)
    click.echo(api.get_user().as_json_string())


@user.command("update")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("nickname")
@check_token
def update_user(token: str, debug: bool, nickname: str):
    """Update authenticated user's information."""
    api = NatureRemoAPI(token, debug)
    click.echo(api.update_user(nickname).as_json_string())


@main.group()
def device():
    pass


@device.command("get")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@check_token
def get_devices(token: str, debug: bool):
    """Fetch the list of Remo devices the user has access to."""
    api = NatureRemoAPI(token, debug)
    output = f"[{', '.join(d.as_json_string() for d in api.get_devices())}]"
    click.echo(output)


@device.command("update")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@click.argument("name")
@check_token
def update_device(token: str, debug: bool, id: str, name: str):
    """Update Remo."""
    api = NatureRemoAPI(token, debug)
    api.update_device(id, name)


@device.command("delete")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@check_token
def delete_device(token: str, debug: bool, id: str):
    """Delete Remo."""
    api = NatureRemoAPI(token, debug)
    api.delete_device(id)


@device.command("update_temperature_offset")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@click.argument("offset", type=int)
@check_token
def update_temperature_offset(token: str, debug: bool, id: str, offset: int):
    """Update temperature offset."""
    api = NatureRemoAPI(token, debug)
    api.update_temperature_offset(id, offset)


@device.command("update_humidity_offset")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@click.argument("offset", type=int)
@check_token
def update_humidity_offset(token: str, debug: bool, id: str, offset: int):
    """Update humidity offset."""
    api = NatureRemoAPI(token, debug)
    api.update_humidity_offset(id, offset)


@main.group()
def appliance():
    pass


@appliance.command("detect")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("message")
@check_token
def detect_appliance(token: str, debug: bool, message: str):
    """Find the air conditioner best matching the provided infrared signal."""
    api = NatureRemoAPI(token, debug)
    joined = ", ".join(
        a.as_json_string() for a in api.detect_appliance(message)
    )
    output = f"[{joined}]"
    click.echo(output)


@appliance.command("get")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@check_token
def get_appliances(token: str, debug: bool):
    """Fetch the list of appliances."""
    api = NatureRemoAPI(token, debug)
    output = f"[{', '.join(a.as_json_string() for a in api.get_appliances())}]"
    click.echo(output)


@appliance.command("create")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.option("--model", default=None)
@click.option("--model-type", default=None)
@click.argument("device")
@click.argument("nickname")
@click.argument("image")
@check_token
def create_appliance(
    token: str,
    debug: bool,
    model: str,
    model_type: str,
    device: str,
    nickname: str,
    image: str,
):
    """Create a new appliance."""
    api = NatureRemoAPI(token, debug)
    click.echo(
        api.create_appliance(
            device, nickname, image, model, model_type
        ).as_json_string()
    )


@appliance.command("update_orders")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("appliances")
@check_token
def update_appliance_orders(token: str, debug: bool, appliances: str):
    """Reorder appliances."""
    api = NatureRemoAPI(token, debug)
    api.update_appliance_orders(appliances)


@appliance.command("delete")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@check_token
def delete_appliance(token: str, debug: bool, id: str):
    """Delete appliance."""
    api = NatureRemoAPI(token, debug)
    api.delete_appliance(id)


@appliance.command("update")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@click.argument("nickname")
@click.argument("image")
@check_token
def update_appliance(
    token: str, debug: bool, id: str, nickname: str, image: str
):
    """Update appliance."""
    api = NatureRemoAPI(token, debug)
    api.update_appliance(id, nickname, image)


@appliance.command("update_aircon_settings")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.option("--operation-mode", default=None)
@click.option("--temperature", default=None)
@click.option("--air-volume", default=None)
@click.option("--air-direction", default=None)
@click.option("--button", default=None)
@click.argument("id")
@check_token
def update_aircon_settings(
    token: str,
    debug: bool,
    operation_mode: str,
    temperature: str,
    air_volume: str,
    air_direction: str,
    button: str,
    id: str,
):
    """Update air conditioner settings."""
    api = NatureRemoAPI(token, debug)
    api.update_aircon_settings(
        id, operation_mode, temperature, air_volume, air_direction, button
    )


@appliance.command("send_tv_infrared_signal")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@click.argument("button")
def send_tv_infrared_signal(token: str, debug: str, id: str, button: str):
    """Send tv infrared signal."""
    api = NatureRemoAPI(token, debug)
    api.send_tv_infrared_signal(id, button)


@appliance.command("send_light_infrared_signal")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@click.argument("button")
def send_light_infrared_signal(token: str, debug: str, id: str, button: str):
    """Send light infrared signal.."""
    api = NatureRemoAPI(token, debug)
    api.send_light_infrared_signal(id, button)


@main.group()
def local():
    pass


@local.command("get")
@click.option("--debug", default=False, is_flag=True)
@click.argument("ip_addr")
def get_ir_signal(debug: bool, ip_addr: str):
    """Fetch the newest received IR signal."""
    local_api = NatureRemoLocalAPI(ip_addr, debug)
    click.echo(local_api.get_ir_signal().as_json_string())


@local.command("send")
@click.option("--debug", default=False, is_flag=True)
@click.argument("ip_addr")
@click.argument("message")
def send_ir_signal(debug: bool, ip_addr: str, message: str):
    """Emit IR signals provided by request body."""
    local_api = NatureRemoLocalAPI(ip_addr, debug)
    local_api.send_ir_signal(message)


if __name__ == "__main__":
    main()
