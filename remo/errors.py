import requests


class NatureRemoError(Exception):
    """Base class for Nature Remo errors."""

    pass


def build_error_message(resp: requests.models.Response) -> str:
    error = resp.json()
    return (
        f"HTTP Status Code: {resp.status_code}, "
        + f'Nature Remo Code: {error["code"]}, Message: {error["message"]}'
    )
