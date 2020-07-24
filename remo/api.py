from enum import auto
from enum import Enum
from typing import List

import requests

from .__version__ import __url__
from .__version__ import __version__
from .errors import build_error_message
from .errors import NatureRemoError
from .models import Appliance
from .models import ApplianceSchema
from .models import Device
from .models import DeviceSchema
from .models import Signal
from .models import SignalSchema
from .models import User
from .models import UserSchema

BASE_URL = "https://api.nature.global"


class HTTPMethod(Enum):
    GET = auto()
    POST = auto()


class NatureRemoAPI:
    """Client for the Nature Remo API."""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = BASE_URL

    def __request(
        self, endpoint: str, method: HTTPMethod, data: {} = None
    ) -> requests.models.Response:
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": f"nature-remo/{__version__} ({__url__})",
        }
        url = f"{self.base_url}{endpoint}"

        if method == HTTPMethod.GET:
            try:
                return requests.get(url, headers=headers)
            except requests.RequestException as e:
                raise NatureRemoError(str(e))
        elif method == HTTPMethod.POST:
            try:
                return requests.post(url, headers=headers, data=data)
            except requests.RequestException as e:
                raise NatureRemoError(str(e))

    def __get_json(self, resp: requests.models.Response):
        if resp.ok:
            return resp.json()
        raise NatureRemoError(build_error_message(resp))

    def get_user(self) -> User:
        """Fetch the authenticated user's information.

        Returns:
            A User object.
        """
        endpoint = "/1/users/me"
        resp = self.__request(endpoint, HTTPMethod.GET)
        json = self.__get_json(resp)
        return UserSchema().load(json)

    def update_user(self, nickname: str) -> User:
        """Update authenticated user's information.

        Args:
            nickname: User's nickname.

        Returns:
            A User object.
        """
        endpoint = "/1/users/me"
        resp = self.__request(
            endpoint, HTTPMethod.POST, {"nickname": nickname}
        )
        json = self.__get_json(resp)
        return UserSchema().load(json)

    def get_devices(self) -> List[Device]:
        """Fetch the list of Remo devices the user has access to.

        Returns:
            A List of Device objects.
        """
        endpoint = "/1/devices"
        resp = self.__request(endpoint, HTTPMethod.GET)
        json = self.__get_json(resp)
        return DeviceSchema(many=True).load(json)

    def update_device(self, device: str, name: str):
        """Update Remo.

        Args:
            device: Device ID.
            name: Device name.
        """
        endpoint = f"/1/devices/{device}"
        resp = self.__request(endpoint, HTTPMethod.POST, {"name": name})
        if not resp.ok:
            raise NatureRemoError(build_error_message(resp))

    def delete_device(self, device: str):
        """Delete Remo.

        Args:
            device: Device ID.
        """
        endpoint = f"/1/devices/{device}/delete"
        resp = self.__request(endpoint, HTTPMethod.POST)
        if not resp.ok:
            raise NatureRemoError(build_error_message(resp))

    def update_temperature_offset(self, device: str, offset: int):
        """Update temperature offset.

        Args:
            device: Device ID.
            offset: Temperature offset value added to the measured temperature.
        """
        endpoint = f"/1/devices/{device}/temperature_offset"
        resp = self.__request(endpoint, HTTPMethod.POST, {"offset": offset})
        if not resp.ok:
            raise NatureRemoError(build_error_message(resp))

    def update_humidity_offset(self, device: str, offset: int):
        """Update humidity offset.

        Args:
            device: Device ID.
            offset: Humidity offset value added to the measured humidity.
        """
        endpoint = f"/1/devices/{device}/humidity_offset"
        resp = self.__request(endpoint, HTTPMethod.POST, {"offset": offset})
        if not resp.ok:
            raise NatureRemoError(build_error_message(resp))

    def get_appliances(self) -> List[Appliance]:
        """Fetch the list of appliances.

        Returns:
            A list of Appliance objects.
        """
        endpoint = "/1/appliances"
        resp = self.__request(endpoint, HTTPMethod.GET)
        json = self.__get_json(resp)
        return ApplianceSchema(many=True).load(json)

    # TODO
    def create_appliance(
        self,
        nickname: str,
        device: str,
        image: str,
        model: str = None,
        model_type: str = None,
    ) -> Appliance:
        """Create a new appliance.

        Args:
            nickname: Appliance name.
            device: Device ID.
            image: Basename of the image file included in the app.
            model: ApplianceModel ID if the appliance we're trying to create
              is included in IRDB.
            model_type: Type of model.
        """
        endpoint = "​/1​/appliances"  # noqa: F841
        raise NotImplementedError

    def update_appliance_orders(self, appliances: str):
        """Reorder appliances.

        Args:
            appliances: List of all appliances' IDs comma separated.
        """
        endpoint = "/1/appliance_orders"
        resp = self.__request(
            endpoint, HTTPMethod.POST, {"appliances": appliances}
        )
        if not resp.ok:
            raise NatureRemoError(build_error_message(resp))

    # TODO
    def delete_appliance(self, appliance: str):
        """Delete appliance.

        Args:
            appliance: Appliance ID.
        """
        endpoint = f"/1/appliances/{appliance}/delete"  # noqa: F841
        raise NotImplementedError

    def update_appliance(
        self, appliance: str, nickname: str, image: str
    ) -> Appliance:
        """Update appliance.

        Args:
            appliance: Appliance ID.
            nickname: Appliance name.
            image: Basename of the image file included in the app.
        """
        endpoint = f"/1/appliances/{appliance}"
        resp = self.__request(
            endpoint, HTTPMethod.POST, {"nickname": nickname, "image": image}
        )
        if not resp.ok:
            raise NatureRemoError(build_error_message(resp))

    # TODO
    def update_aircon_settings(
        self,
        appliance: str,
        temperature: str,
        operation_mode: str,
        air_volume: str,
        air_direction: str,
        button: str,
    ):
        """Update air conditioner settings.

        Args:
            appliance: Appliance ID.
            temperature: Temperature.
            operation_mode: AC operation mode.
            air_volume: AC air volume.
            air_direction: AC air direction.
            button: Button.
        """
        endpoint = f"/1/appliances/{appliance}/aircon_settings"  # noqa: F841
        raise NotImplementedError

    def send_tv_infrared_signal(self, appliance: str, button: str):
        """Send tv infrared signal.

        Args:
            appliance: Appliance ID.
            button: Button name.
        """
        endpoint = f"/1/appliances/{appliance}/tv"
        resp = self.__request(endpoint, HTTPMethod.POST, {"button": button})
        if not resp.ok:
            raise NatureRemoError(build_error_message(resp))

    # TODO
    def send_light_infrared_signal(self, appliance: str, button: str):
        """Send light infrared signal.

        Args:
            appliance: Appliance ID.
            button: Button name.
        """
        endpoint = f"/1/appliances/{appliance}/light"  # noqa: F841
        raise NotImplementedError

    def get_signals(self, appliance: str) -> List[Signal]:
        """Fetch signals registered under this appliance.

        Args:
            appliance: Appliance ID.
        """
        endpoint = f"/1/appliances/{appliance}/signals"
        resp = self.__request(endpoint, HTTPMethod.GET)
        json = self.__get_json(resp)
        return SignalSchema(many=True).load(json)

    # TODO
    def create_signal(
        self, appliance: str, name: str, message: str, image: str
    ) -> Signal:
        """Create a signal under this appliance.

        Args:
            appliance: Appliance ID.
            name: Signal name.
            message: JSON serialized object describing infrared signals.
              Includes "data", "freq" and "format" keys.
            image: Basename of the image file included in the app.
        """
        endpoint = f"/1/appliances/{appliance}/signals"  # noqa: F841
        raise NotImplementedError

    # TODO
    def update_signal_orders(self, appliance: str, signals: str):
        """Reorder signals under this appliance.

        Args:
            appliance: Appliance ID.
            signals: List of all signals' IDs comma separated.
        """
        endpoint = f"/1/appliances/{appliance}/signal_orders"  # noqa: F841
        raise NotImplementedError

    # TODO
    def update_signal(self, signal: str, name: str, image: str):
        """Update infrared signal.

        Args:
            signal: Signal ID.
            name: Signal name.
            image: Basename of the image file included in the app.
        """
        endpoint = f"/1/signals/{signal}"  # noqa: F841
        raise NotImplementedError

    # TODO
    def delete_signal(self, signal: str):
        """Delete infrared signal.

        Args:
            signal: Signal ID.
        """
        endpoint = f"/1/signals/{signal}/delete"  # noqa: F841
        raise NotImplementedError

    # TODO
    def send_signal(self, signal: str):
        """Send infrared signal.

        Args:
            signal: Signal ID.
        """
        endpoint = f"​/1​/signals​/{signal}​/send"  # noqa: F841
        raise NotImplementedError
