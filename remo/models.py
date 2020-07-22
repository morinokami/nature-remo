from typing import Type

from marshmallow import fields
from marshmallow import post_load
from marshmallow import Schema


class NatureRemoModel:
    """Base class for Nature Remo models."""

    def as_json_string(self) -> str:
        return self.schema().dumps(self)


class UserSchema(Schema):
    id = fields.Str()
    nickname = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data, schema=UserSchema)


class User(NatureRemoModel):
    def __init__(self, id: str, nickname: str, schema: Type[UserSchema]):
        self.id = id
        self.nickname = nickname
        self.schema = schema

    def __repr__(self):
        return f'User(id="{self.id}", nickname="{self.nickname}")'
