from datetime import datetime

from marshmallow import fields
from marshmallow import post_load
from marshmallow import Schema


class NatureRemoModel:
    """Base class for Nature Remo models."""

    def as_json_string(self) -> str:
        return self.schema().dumps(self, ensure_ascii=True, sort_keys=True)


class UserSchema(Schema):
    id = fields.Str()
    nickname = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class User(NatureRemoModel):
    def __init__(self, id: str, nickname: str):
        self.id = id
        self.nickname = nickname
        self.schema = UserSchema

    def __repr__(self):
        return f'User(id="{self.id}", nickname="{self.nickname}")'


class SensorValueSchema(Schema):
    val = fields.Float()
    created_at = fields.DateTime()


class DeviceSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    temperature_offset = fields.Int()
    humidity_offset = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    firmware_version = fields.Str()
    mac_address = fields.Str()
    serial_number = fields.Str()
    newest_events = fields.Dict(fields.Str(), fields.Nested(SensorValueSchema))

    @post_load
    def make_device(self, data, **kwargs):
        return Device(**data)


class Device(NatureRemoModel):
    def __init__(
        self,
        id: str,
        name: str,
        temperature_offset: int,
        humidity_offset: int,
        created_at: datetime,
        updated_at: datetime,
        firmware_version: str,
        mac_address: str,
        serial_number: str,
        newest_events: dict,
    ):
        self.id = id
        self.name = name
        self.temperature_offset = temperature_offset
        self.humidity_offset = humidity_offset
        self.created_at = created_at
        self.updated_at = updated_at
        self.firmware_version = firmware_version
        self.mac_address = mac_address
        self.serial_number = serial_number
        self.newest_events = newest_events
        self.schema = DeviceSchema

    def __repr__(self):
        return (
            f'Device(id="{self.id}", name="{self.name}", '
            + f"temprature_offset={self.temperature_offset}, "
            + f"humidity_offset={self.humidity_offset}, "
            + f"created_at={repr(self.created_at)}, "
            + f"updated_at={repr(self.updated_at)}, "
            + f'firmware_version="{self.firmware_version}", '
            + f'mac_address="{self.mac_address}", '
            + f'serial_number="{self.serial_number}", '
            + f"newest_events={self.newest_events})"
        )


# TODO
class ApplianceSchema(Schema):
    @post_load
    def make_appliance(self, data, **kwargs):
        return Appliance(**data)


# TODO
class Appliance(NatureRemoModel):
    def __init__(self):
        pass

    def __repr__(self):
        pass


# TODO
class SignalSchema(Schema):
    @post_load
    def make_signal(self, data, **kwargs):
        return Signal(**data)


# TODO
class Signal(NatureRemoModel):
    def __init__(self):
        pass

    def __repr__(self):
        pass
