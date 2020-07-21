import json
from typing import Union


class NatureRemoModel:
    """Base class for Nature Remo models."""

    def as_json_string(self) -> str:
        return json.dumps(self.json_data, ensure_ascii=True, sort_keys=True)

    @classmethod
    def new(cls, data: Union[dict, list]):
        if type(data) is dict:
            return cls(**data)
        else:
            return cls(data)


class User(NatureRemoModel):
    """Class representing a User model."""

    def __init__(self, **kwargs):
        self.id = None
        self.nickname = None
        self.json_data = {
            "id": None,
            "nickname": None,
        }

        for (key, default) in self.json_data.items():
            setattr(self, key, kwargs.get(key, default))
            if key in kwargs:
                self.json_data[key] = kwargs[key]

    def __repr__(self):
        return f'User(id="{self.id}", nickname="{self.nickname}")'
