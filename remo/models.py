from datetime import datetime
from typing import List

from marshmallow import EXCLUDE
from marshmallow import fields
from marshmallow import post_load
from marshmallow import Schema


class NatureRemoModel:
    """Base class for Nature Remo models."""

    def as_json_string(self) -> str:
        return self.schema().dumps(  # type: ignore
            self, ensure_ascii=True, sort_keys=True
        )


class UserSchema(Schema):
    id = fields.Str()
    nickname = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class User(NatureRemoModel):
    def __init__(self, id: str, nickname: str):
        self.id = id
        self.nickname = nickname
        self.schema = UserSchema

    def __repr__(self):
        return f"User(id='{self.id}', nickname='{self.nickname}')"


class SensorValueSchema(Schema):
    val = fields.Float()
    created_at = fields.DateTime()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_sensor_value(self, data, **kwargs):
        return SensorValue(**data)


class SensorValue(NatureRemoModel):
    def __init__(self, val: float, created_at: datetime):
        self.val = val
        self.created_at = created_at
        self.schema = SensorValueSchema

    def __repr__(self):
        return (
            f"SensorValue(val={self.val}, created_at={repr(self.created_at)})"
        )


class DeviceCoreSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    temperature_offset = fields.Int()
    humidity_offset = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    firmware_version = fields.Str()
    mac_address = fields.Str()
    serial_number = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_device_core(self, data, **kwargs):
        return DeviceCore(**data)


class DeviceCore(NatureRemoModel):
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
        self.schema = DeviceCoreSchema

    def __repr__(self):
        return (
            f"Device(id='{self.id}', name='{self.name}', "
            f"temprature_offset={self.temperature_offset}, "
            f"humidity_offset={self.humidity_offset}, "
            f"created_at={repr(self.created_at)}, "
            f"updated_at={repr(self.updated_at)}, "
            f"firmware_version='{self.firmware_version}', "
            f"mac_address='{self.mac_address}', "
            f"serial_number='{self.serial_number}')"
        )


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

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_device(self, data, **kwargs):
        return Device(**data)


class Device(DeviceCore):
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
        super().__init__(
            id,
            name,
            temperature_offset,
            humidity_offset,
            created_at,
            updated_at,
            firmware_version,
            mac_address,
            serial_number,
        )
        self.newest_events = newest_events
        self.schema = DeviceSchema  # type: ignore

    def __repr__(self):
        return (
            f"Device(id='{self.id}', name='{self.name}', "
            f"temprature_offset={self.temperature_offset}, "
            f"humidity_offset={self.humidity_offset}, "
            f"created_at={repr(self.created_at)}, "
            f"updated_at={repr(self.updated_at)}, "
            f"firmware_version='{self.firmware_version}', "
            f"mac_address='{self.mac_address}', "
            f"serial_number='{self.serial_number}', "
            f"newest_events={self.newest_events})"
        )


class ApplianceModelSchema(Schema):
    id = fields.Str()
    manufacturer = fields.Str()
    remote_name = fields.Str()
    name = fields.Str()
    image = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_appliance_model(self, data, **kwargs):
        return ApplianceModel(**data)


class ApplianceModel(NatureRemoModel):
    def __init__(
        self,
        id: str,
        manufacturer: str,
        remote_name: str,
        name: str,
        image: str,
    ):
        self.id = id
        self.manufacturer = manufacturer
        self.remote_name = remote_name
        self.name = name
        self.image = image
        self.schema = ApplianceModelSchema

    def __repr__(self):
        return (
            f"ApplianceModel(id='{self.id}', "
            f"manufacturer='{self.manufacturer}', "
            f"remote_name='{self.remote_name}', "
            f"name='{self.name}', image='{self.image}')"
        )


class AirConParamsSchema(Schema):
    temp = fields.Str()
    mode = fields.Str()
    vol = fields.Str()
    dir = fields.Str()
    button = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_aircon_params(self, data, **kwargs):
        return AirConParams(**data)


class AirConParams(NatureRemoModel):
    def __init__(self, temp: str, mode: str, vol: str, dir: str, button: str):
        self.temp = temp
        self.mode = mode
        self.vol = vol
        self.dir = dir
        self.button = button
        self.schema = AirConParamsSchema

    def __repr__(self):
        return (
            f"AirConParams(temp='{self.temp}', mode='{self.mode}', "
            f"vol='{self.vol}', dir='{self.dir}', button='{self.button}')"
        )


class ApplianceModelAndParamsSchema(Schema):
    model = fields.Nested(ApplianceModelSchema)
    params = fields.Nested(AirConParamsSchema)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_appliance_model_and_params(self, data, **kwargs):
        return ApplianceModelAndParams(**data)


class ApplianceModelAndParams(NatureRemoModel):
    def __init__(self, model: ApplianceModel, params: AirConParams):
        self.model = model
        self.params = params
        self.schema = ApplianceModelAndParamsSchema

    def __repr__(self):
        return (
            f"ApplianceModelAndParams(model={self.model}, "
            f"params={self.params})"
        )


class AirConRangeModeSchema(Schema):
    temp = fields.List(fields.Str())
    vol = fields.List(fields.Str())
    dir = fields.List(fields.Str())

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_aircon_range_mode(self, data, **kwargs):
        return AirConRangeMode(**data)


class AirConRangeMode(NatureRemoModel):
    def __init__(self, temp: List[str], vol: List[str], dir: List[str]):
        self.temp = temp
        self.vol = vol
        self.dir = dir
        self.schema = AirConRangeModeSchema

    def __repr__(self):
        return (
            f"AirConRangeMode(temp={self.temp}, "
            f"vol={self.vol}, dir={self.dir})"
        )


class AirConRangeSchema(Schema):
    modes = fields.Dict(fields.Str(), fields.Nested(AirConRangeModeSchema))
    fixedButtons = fields.List(fields.Str())

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_aircon_range(self, data, **kwargs):
        return AirConRange(**data)


class AirConRange(NatureRemoModel):
    def __init__(self, modes: dict, fixedButtons: List[str]):
        self.modes = modes
        self.fixedButtons = fixedButtons
        self.schema = AirConRangeSchema

    def __repr__(self):
        return (
            f"AirConRange(modes={self.modes}, "
            f"fixedButtons={self.fixedButtons})"
        )


class AirConSchema(Schema):
    range = fields.Nested(AirConRangeSchema)
    tempUnit = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_aircon(self, data, **kwparams):
        return AirCon(**data)


class AirCon(NatureRemoModel):
    def __init__(self, range: dict, tempUnit: str):
        self.range = range
        self.tempUnit = tempUnit
        self.schema = AirConSchema

    def __repr__(self):
        return f'AirCon(range={self.range}, tempUnit="{self.tempUnit}")'


class SignalSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    image = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_signal(self, data, **kwargs):
        return Signal(**data)


class Signal(NatureRemoModel):
    def __init__(self, id: str, name: str, image: str):
        self.id = id
        self.name = name
        self.image = image
        self.schema = SignalSchema

    def __repr__(self):
        return (
            f"Signal(id='{self.id}', name='{self.name}', image='{self.image}')"
        )


class ButtonSchema(Schema):
    name = fields.Str()
    image = fields.Str()
    label = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_button(self, data, **kwargs):
        return Button(**data)


class Button(NatureRemoModel):
    def __init__(self, name: str, image: str, label: str):
        self.name = name
        self.image = image
        self.label = label
        self.schema = ButtonSchema

    def __repr__(self):
        return (
            f"Button(name='{self.name}', "
            f"image='{self.image}', "
            f"label='{self.label}')"
        )


class TVStateSchema(Schema):
    input = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_tv_state(self, data, **kwargs):
        return TVState(**data)


class TVState(NatureRemoModel):
    def __init__(self, input: str):
        self.input = input
        self.schema = TVStateSchema

    def __repr__(self):
        return f"TVState(input='{self.input}')"


class TVSchema(Schema):
    state = fields.Nested(TVStateSchema)
    buttons = fields.List(fields.Nested(ButtonSchema))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_tv(self, data, **kwargs):
        return TV(**data)


class TV(NatureRemoModel):
    def __init__(self, state: TVState, buttons: List[Button]):
        self.state = state
        self.buttons = buttons
        self.schema = TVSchema

    def __repr__(self):
        return f"TV(state={self.state}, buttons={self.buttons})"


class LightStateSchema(Schema):
    brightness = fields.Str()
    power = fields.Str()
    last_button = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_light_state(self, data, **kwargs):
        return LightState(**data)


class LightState(NatureRemoModel):
    def __init__(self, brightness: str, power: str, last_button: str):
        self.brightness = brightness
        self.power = power
        self.last_button = last_button
        self.schema = LightStateSchema

    def __repr__(self):
        return (
            f"LightState(brightness='{self.brightness}', "
            f"power='{self.power}', last_button='{self.last_button}')"
        )


class LightSchema(Schema):
    state = fields.Nested(LightStateSchema)
    buttons = fields.List(fields.Nested(ButtonSchema))

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_light(self, data, **kwargs):
        return Light(**data)


class Light(NatureRemoModel):
    def __init__(self, state: LightState, buttons: List[Button]):
        self.state = state
        self.buttons = buttons
        self.schema = LightSchema

    def __repr__(self):
        return f"Light(state={self.state}, buttons={self.buttons})"


# TODO
class EchonetLitePropertySchema(Schema):
    pass


class ApplianceSchema(Schema):
    id = fields.Str()
    device = fields.Nested(DeviceCoreSchema)
    model = fields.Nested(ApplianceModelSchema, allow_none=True)
    nickname = fields.Str()
    image = fields.Str()
    type = fields.Str()
    settings = fields.Nested(AirConParamsSchema, allow_none=True)
    aircon = fields.Nested(AirConSchema, allow_none=True)
    signals = fields.List(fields.Nested(SignalSchema))
    tv = fields.Nested(TVSchema, required=False)
    light = fields.Nested(LightSchema, required=False)
    # smart_meter

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_appliance(self, data, **kwargs):
        return Appliance(**data)


class Appliance(NatureRemoModel):
    def __init__(
        self,
        id: str,
        device: DeviceCore,
        model: ApplianceModel,
        nickname: str,
        image: str,
        type: str,
        settings: AirConParams,
        aircon: AirCon,
        signals: List[Signal],
        tv: TV = None,
        light: Light = None,
    ):
        self.id = id
        self.device = device
        self.model = model
        self.nickname = nickname
        self.image = image
        self.type = type
        self.settings = settings
        self.aircon = aircon
        self.signals = signals
        self.tv = tv
        self.light = light
        self.schema = ApplianceSchema

    def __repr__(self):
        return (
            f"Appliance(id='{self.id}', device={self.device}, "
            f"model={self.model}, nickname='{self.nickname}', "
            f"image='{self.image}', type='{self.type}', "
            f"settings={self.settings}, aircon={self.aircon}, "
            f"signals={self.signals}, tv={self.tv}, light={self.light})"
        )


class IRSignalSchema(Schema):
    freq = fields.Int()
    data = fields.List(fields.Int())
    format = fields.Str()

    @post_load
    def make_ir_signal(self, data, **kwargs):
        return IRSignal(**data)


class IRSignal(NatureRemoModel):
    def __init__(self, freq: int, data: List[int], format: str):
        self.freq = freq
        self.data = data
        self.format = format
        self.schema = IRSignalSchema

    def __repr__(self):
        return (
            f"IRSignal(freq={self.freq}, data={self.data}, "
            f"format='{self.format}')"
        )
