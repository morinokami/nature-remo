from enum import auto
from enum import Enum
from typing import List

import requests
from marshmallow import EXCLUDE

from .__version__ import __url__
from .__version__ import __version__
from .errors import build_error_message
from .errors import NatureRemoError
from .models import Device
from .models import DeviceSchema
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
        return UserSchema().load(json, unknown=EXCLUDE)

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
        return UserSchema().load(json, unknown=EXCLUDE)

    def get_devices(self) -> List[Device]:
        """Fetch the list of Remo devices the user has access to.

        Returns:
            A List of Device objects.
        """
        endpoint = "/1/devices"
        resp = self.__request(endpoint, HTTPMethod.GET)
        json = self.__get_json(resp)
        return DeviceSchema(many=True, unknown=EXCLUDE).load(json)

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
        pass

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
        pass
