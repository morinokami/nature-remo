from enum import auto
from enum import Enum

import requests

from .__version__ import __url__
from .__version__ import __version__
from .errors import build_error_message
from .errors import NatureRemoError
from .models import User

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
        return User.new(json)

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
        return User.new(json)
