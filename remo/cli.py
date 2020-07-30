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


def handle_error(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except NatureRemoError as e:
            click.echo(f"Error: {e}")
            click.Abort()

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
@handle_error
@check_token
def get_user(token: str, debug: bool):
    """Fetch the authenticated user's information."""
    api = NatureRemoAPI(token, debug)
    click.echo(api.get_user().as_json_string())


@user.command("update")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("nickname")
@handle_error
@check_token
def update_user(token: str, debug: bool, nickname: str):
    """Update authenticated user's information.

    NICKNAME: User's nickname.
    """
    api = NatureRemoAPI(token, debug)
    click.echo(api.update_user(nickname).as_json_string())


@main.group()
def device():
    pass


@device.command("get")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@handle_error
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
@handle_error
@check_token
def update_device(token: str, debug: bool, id: str, name: str):
    """Update Remo.

    ID: Device ID.
    NAME: Device name.
    """
    api = NatureRemoAPI(token, debug)
    api.update_device(id, name)


@device.command("delete")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@handle_error
@check_token
def delete_device(token: str, debug: bool, id: str):
    """Delete Remo.

    ID: Device ID.
    """
    api = NatureRemoAPI(token, debug)
    api.delete_device(id)


@device.command("update_temperature_offset")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@click.argument("offset", type=int)
@handle_error
@check_token
def update_temperature_offset(token: str, debug: bool, id: str, offset: int):
    """Update temperature offset.

    ID: Device ID.
    OFFSET: Temperature offset value added to the measured temperature.
    """
    api = NatureRemoAPI(token, debug)
    api.update_temperature_offset(id, offset)


@device.command("update_humidity_offset")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@click.argument("offset", type=int)
@handle_error
@check_token
def update_humidity_offset(token: str, debug: bool, id: str, offset: int):
    """Update humidity offset.

    ID: Device ID.
    OFFSET: Humidity offset value added to the measured humidity.
    """
    api = NatureRemoAPI(token, debug)
    api.update_humidity_offset(id, offset)


@main.group()
def appliance():
    pass


@appliance.command("detect")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("message")
@handle_error
@check_token
def detect_appliance(token: str, debug: bool, message: str):
    """Find the air conditioner best matching the provided infrared signal.

    MESSAGE: JSON serialized object describing infrared signals. Includes
    "data", "freq" and "format" keys.
    """
    api = NatureRemoAPI(token, debug)
    joined = ", ".join(
        a.as_json_string() for a in api.detect_appliance(message)
    )
    output = f"[{joined}]"
    click.echo(output)


@appliance.command("get")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@handle_error
@check_token
def get_appliances(token: str, debug: bool):
    """Fetch the list of appliances."""
    api = NatureRemoAPI(token, debug)
    output = f"[{', '.join(a.as_json_string() for a in api.get_appliances())}]"
    click.echo(output)


@appliance.command("create")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.option(
    "--model",
    default=None,
    help=(
        "ApplianceModel ID if the appliance we're trying to create is "
        "included in IRDB."
    ),
)
@click.option("--model-type", default=None, help="Type of model.")
@click.argument("device")
@click.argument("nickname")
@click.argument("image")
@handle_error
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
    """Create a new appliance.

    DEVICE: Device ID.
    NICKNAME: Appliance name.
    IMAGE: Basename of the image file included in the app.
    """
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
@handle_error
@check_token
def update_appliance_orders(token: str, debug: bool, appliances: str):
    """Reorder appliances.

    APPLIANCES: List of all appliances' IDs comma separated.
    """
    api = NatureRemoAPI(token, debug)
    api.update_appliance_orders(appliances)


@appliance.command("delete")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@handle_error
@check_token
def delete_appliance(token: str, debug: bool, id: str):
    """Delete appliance.

    ID: Appliance ID.
    """
    api = NatureRemoAPI(token, debug)
    api.delete_appliance(id)


@appliance.command("update")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@click.argument("nickname")
@click.argument("image")
@handle_error
@check_token
def update_appliance(
    token: str, debug: bool, id: str, nickname: str, image: str
):
    """Update appliance.

    ID: Appliance ID.
    NICKNAME: Appliance name.
    IMAGE: Basename of the image file included in the app.
    """
    api = NatureRemoAPI(token, debug)
    click.echo(api.update_appliance(id, nickname, image).as_json_string())


@appliance.command("update_aircon_settings")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.option("--operation-mode", default=None, help="AC operation mode.")
@click.option("--temperature", default=None, help="Temperature.")
@click.option("--air-volume", default=None, help="AC air volume.")
@click.option("--air-direction", default=None, help="AC air direction.")
@click.option("--button", default=None, help="Button.")
@click.argument("id")
@handle_error
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
    """Update air conditioner settings.

    ID: Appliance ID.
    """
    api = NatureRemoAPI(token, debug)
    api.update_aircon_settings(
        id, operation_mode, temperature, air_volume, air_direction, button
    )


@appliance.command("send_tv_infrared_signal")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@click.argument("button")
@handle_error
@check_token
def send_tv_infrared_signal(token: str, debug: bool, id: str, button: str):
    """Send tv infrared signal.

    ID: Appliance ID.
    BUTTON: Button name.
    """
    api = NatureRemoAPI(token, debug)
    api.send_tv_infrared_signal(id, button)


@appliance.command("send_light_infrared_signal")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@click.argument("button")
@handle_error
@check_token
def send_light_infrared_signal(token: str, debug: bool, id: str, button: str):
    """Send light infrared signal.

    ID: Appliance ID.
    BUTTON: Button name.
    """
    api = NatureRemoAPI(token, debug)
    api.send_light_infrared_signal(id, button)


@main.group()
def signal():
    pass


@signal.command("get")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("appliance")
@handle_error
@check_token
def get_signals(token: str, debug: bool, appliance: str):
    """Fetch signals registered under this appliance.

    APPLIANCE: Appliance ID.
    """
    api = NatureRemoAPI(token, debug)
    joined = ", ".join(s.as_json_string() for s in api.get_signals(appliance))
    output = f"[{joined}]"
    click.echo(output)


@signal.command("create")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("appliance")
@click.argument("name")
@click.argument("message")
@click.argument("image")
@handle_error
@check_token
def create_signal(
    token: str,
    debug: bool,
    appliance: str,
    name: str,
    message: str,
    image: str,
):
    """Create a signal under this appliance.

    APPLIANCE: Appliance ID.
    NAME: Signal name.
    MESSAGE: JSON serialized object describing infrared signals. Includes
    "data", "freq" and "format" keys.
    IMAGE: Basename of the image file included in the app.
    """
    api = NatureRemoAPI(token, debug)
    click.echo(
        api.create_signal(appliance, name, message, image).as_json_string()
    )


@signal.command("update_orders")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("appliance")
@click.argument("signals")
@handle_error
@check_token
def update_signal_orders(
    token: str, debug: bool, appliance: str, signals: str
):
    """Reorder signals under this appliance.

    APPLIANCE: Appliance ID.
    SIGNALS: List of all signals' IDs comma separated.
    """
    api = NatureRemoAPI(token, debug)
    api.update_signal_orders(appliance, signals)


@signal.command("update")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@click.argument("name")
@click.argument("image")
@handle_error
@check_token
def update_signal(token: str, debug: bool, id: str, name: str, image: str):
    """Update infrared signal.

    ID: Signal ID.
    NAME: Signal name.
    IMAGE: Basename of the image file included in the app.
    """
    api = NatureRemoAPI(token, debug)
    api.update_signal(id, name, image)


@signal.command("delete")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@handle_error
@check_token
def delete_signal(token: str, debug: bool, id: str):
    """Delete infrared signal.

    ID: Signal ID.
    """
    api = NatureRemoAPI(token, debug)
    api.delete_signal(id)


@signal.command("send")
@click.option("--token", default="")
@click.option("--debug", default=False, is_flag=True)
@click.argument("id")
@handle_error
@check_token
def send_signal(token: str, debug: bool, id: str):
    """Send infrared signal.

    ID: Signal ID.
    """
    api = NatureRemoAPI(token, debug)
    api.send_signal(id)


@main.group()
def local():
    pass


@local.command("get")
@click.option("--debug", default=False, is_flag=True)
@click.argument("ip_addr")
@handle_error
def get_ir_signal(debug: bool, ip_addr: str):
    """Fetch the newest received IR signal.

    IP_ADDR: IP address of Remo.
    """
    local_api = NatureRemoLocalAPI(ip_addr, debug)
    click.echo(local_api.get_ir_signal().as_json_string())


@local.command("send")
@click.option("--debug", default=False, is_flag=True)
@click.argument("ip_addr")
@click.argument("message")
@handle_error
def send_ir_signal(debug: bool, ip_addr: str, message: str):
    """Emit IR signals provided by request body.

    IP_ADDR: IP address of Remo.
    MESSAGE: JSON serialized object describing infrared signals. Includes
    "data", "freq" and "format" keys.
    """
    local_api = NatureRemoLocalAPI(ip_addr, debug)
    local_api.send_ir_signal(message)


if __name__ == "__main__":
    main()
