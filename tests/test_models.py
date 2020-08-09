import json
from datetime import datetime
from datetime import timezone

from .utils import load_json
from remo import AirConParamsSchema
from remo import AirConRangeModeSchema
from remo import AirConRangeSchema
from remo import AirConSchema
from remo import ApplianceModelAndParamsSchema
from remo import ApplianceModelSchema
from remo import ApplianceSchema
from remo import ButtonSchema
from remo import DeviceCoreSchema
from remo import DeviceSchema
from remo import IRSignalSchema
from remo import LightSchema
from remo import LightStateSchema
from remo import SensorValueSchema
from remo import SignalSchema
from remo import TVSchema
from remo import TVStateSchema
from remo import UserSchema


def str_to_datetime(s: str) -> datetime:
    dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    return dt.replace(tzinfo=timezone.utc)


def sorted_json(d: dict) -> str:
    return json.dumps(d, ensure_ascii=True, sort_keys=True)


def test_user():
    data = load_json("testdata/user.json")
    user = UserSchema().load(data)

    assert user.id == data["id"]
    assert user.nickname == data["nickname"]

    assert user.as_json_string() == sorted_json(data)
    assert str(user) == (
        f"User(id='{data['id']}', nickname='{data['nickname']}')"
    )


def test_sensor_value():
    data = load_json("testdata/sensor_value.json")
    sensor_value = SensorValueSchema().load(data)

    assert sensor_value.val == data["val"]
    assert sensor_value.created_at == str_to_datetime(data["created_at"])

    assert sensor_value.as_json_string()
    assert str(sensor_value)


def test_device_core():
    data = load_json("testdata/device_core.json")
    device_core = DeviceCoreSchema().load(data)

    assert device_core.id == data["id"]
    assert device_core.name == data["name"]
    assert device_core.temperature_offset == data["temperature_offset"]
    assert device_core.humidity_offset == data["humidity_offset"]
    assert device_core.created_at == str_to_datetime(data["created_at"])
    assert device_core.updated_at == str_to_datetime(data["updated_at"])
    assert device_core.firmware_version == data["firmware_version"]
    assert device_core.mac_address == data["mac_address"]
    assert device_core.serial_number == data["serial_number"]

    assert device_core.as_json_string()
    assert str(device_core)


def test_device():
    data = load_json("testdata/device.json")
    device = DeviceSchema().load(data)

    assert device.id == data["id"]
    assert device.name == data["name"]
    assert device.temperature_offset == data["temperature_offset"]
    assert device.humidity_offset == data["humidity_offset"]
    assert device.created_at == str_to_datetime(data["created_at"])
    assert device.updated_at == str_to_datetime(data["updated_at"])
    assert device.firmware_version == data["firmware_version"]
    assert device.mac_address == data["mac_address"]
    assert device.serial_number == data["serial_number"]
    assert device.newest_events["hu"].val == data["newest_events"]["hu"]["val"]
    assert device.newest_events["hu"].created_at == str_to_datetime(
        data["newest_events"]["hu"]["created_at"]
    )
    assert device.newest_events["il"].val == data["newest_events"]["il"]["val"]
    assert device.newest_events["il"].created_at == str_to_datetime(
        data["newest_events"]["il"]["created_at"]
    )
    assert device.newest_events["mo"].val == data["newest_events"]["mo"]["val"]
    assert device.newest_events["mo"].created_at == str_to_datetime(
        data["newest_events"]["mo"]["created_at"]
    )
    assert device.newest_events["te"].val == data["newest_events"]["te"]["val"]
    assert device.newest_events["te"].created_at == str_to_datetime(
        data["newest_events"]["te"]["created_at"]
    )

    assert device.as_json_string()
    assert str(device)


def test_appliance_model():
    data = load_json("testdata/appliance_model.json")
    appliance_model = ApplianceModelSchema().load(data)

    assert appliance_model.id == data["id"]
    assert appliance_model.manufacturer == data["manufacturer"]
    assert appliance_model.remote_name == data["remote_name"]
    assert appliance_model.name == data["name"]
    assert appliance_model.image == data["image"]

    assert appliance_model.as_json_string() == sorted_json(data)
    assert str(appliance_model) == (
        f"ApplianceModel(id='{data['id']}', "
        f"manufacturer='{data['manufacturer']}', "
        f"remote_name='{data['remote_name']}', "
        f"name='{data['name']}', image='{data['image']}')"
    )


def test_aircon_params():
    data = load_json("testdata/aircon_params.json")
    aircon_params = AirConParamsSchema().load(data)

    assert aircon_params.temp == data["temp"]
    assert aircon_params.mode == data["mode"]
    assert aircon_params.vol == data["vol"]
    assert aircon_params.dir == data["dir"]
    assert aircon_params.button == data["button"]

    assert aircon_params.as_json_string() == sorted_json(data)
    assert str(aircon_params) == (
        f"AirConParams(temp='{data['temp']}', mode='{data['mode']}', "
        f"vol='{data['vol']}', dir='{data['dir']}', "
        f"button='{data['button']}')"
    )


def test_appliance_model_and_params():
    data = load_json("testdata/appliance_model_and_params.json")
    model_and_params = ApplianceModelAndParamsSchema().load(data)

    assert model_and_params.model.id == data["model"]["id"]
    assert model_and_params.model.manufacturer == data["model"]["manufacturer"]
    assert model_and_params.model.remote_name == data["model"]["remote_name"]
    assert model_and_params.model.name == data["model"]["name"]
    assert model_and_params.model.image == data["model"]["image"]
    assert model_and_params.params.temp == data["params"]["temp"]
    assert model_and_params.params.mode == data["params"]["mode"]
    assert model_and_params.params.vol == data["params"]["vol"]
    assert model_and_params.params.dir == data["params"]["dir"]
    assert model_and_params.params.button == data["params"]["button"]

    assert model_and_params.as_json_string() == sorted_json(data)
    assert str(model_and_params)


def test_aircon_range_mode():
    data = load_json("testdata/aircon_range_mode.json")
    aircon_range_mode = AirConRangeModeSchema().load(data)

    assert aircon_range_mode.temp == data["temp"]
    assert aircon_range_mode.vol == data["vol"]
    assert aircon_range_mode.dir == data["dir"]

    assert aircon_range_mode.as_json_string() == sorted_json(data)
    assert str(aircon_range_mode) == (
        f"AirConRangeMode(temp={data['temp']}, vol={data['vol']}, "
        f"dir={data['dir']})"
    )


def test_aircon_range():
    data = load_json("testdata/aircon_range.json")
    aircon_range = AirConRangeSchema().load(data)

    assert "mode1" in aircon_range.modes
    assert aircon_range.modes["mode1"].temp == data["modes"]["mode1"]["temp"]
    assert aircon_range.modes["mode1"].vol == data["modes"]["mode1"]["vol"]
    assert aircon_range.modes["mode1"].dir == data["modes"]["mode1"]["dir"]
    assert "mode2" in aircon_range.modes
    assert aircon_range.modes["mode2"].temp == data["modes"]["mode2"]["temp"]
    assert aircon_range.modes["mode2"].vol == data["modes"]["mode2"]["vol"]
    assert aircon_range.modes["mode2"].dir == data["modes"]["mode2"]["dir"]
    assert aircon_range.fixedButtons == data["fixedButtons"]

    assert aircon_range.as_json_string() == sorted_json(data)
    assert str(aircon_range)


def test_aircon():
    data = load_json("testdata/aircon.json")
    aircon = AirConSchema().load(data)

    assert "mode1" in aircon.range.modes
    assert (
        aircon.range.modes["mode1"].temp
        == data["range"]["modes"]["mode1"]["temp"]
    )
    assert (
        aircon.range.modes["mode1"].vol
        == data["range"]["modes"]["mode1"]["vol"]
    )
    assert (
        aircon.range.modes["mode1"].dir
        == data["range"]["modes"]["mode1"]["dir"]
    )
    assert "mode2" in aircon.range.modes
    assert (
        aircon.range.modes["mode2"].temp
        == data["range"]["modes"]["mode2"]["temp"]
    )
    assert (
        aircon.range.modes["mode2"].vol
        == data["range"]["modes"]["mode2"]["vol"]
    )
    assert (
        aircon.range.modes["mode2"].dir
        == data["range"]["modes"]["mode2"]["dir"]
    )
    assert aircon.range.fixedButtons == data["range"]["fixedButtons"]
    assert aircon.tempUnit == data["tempUnit"]

    assert aircon.as_json_string() == sorted_json(data)
    assert str(aircon)


def test_signal():
    data = load_json("testdata/signal.json")
    signal = SignalSchema().load(data)

    assert signal.id == data["id"]
    assert signal.name == data["name"]
    assert signal.image == data["image"]

    assert signal.as_json_string() == sorted_json(data)
    assert str(signal) == (
        f"Signal(id='{data['id']}', name='{data['name']}', "
        f"image='{data['image']}')"
    )


def test_button():
    data = load_json("testdata/button.json")
    button = ButtonSchema().load(data)

    assert button.name == data["name"]
    assert button.image == data["image"]
    assert button.label == data["label"]

    assert button.as_json_string() == sorted_json(data)
    assert str(button) == (
        f"Button(name='{data['name']}', image='{data['image']}', "
        f"label='{data['label']}')"
    )


def test_tv_state():
    data = load_json("testdata/tv_state.json")
    tv_state = TVStateSchema().load(data)

    assert tv_state.input == data["input"]

    assert tv_state.as_json_string() == sorted_json(data)
    assert str(tv_state) == f"TVState(input='{data['input']}')"


def test_tv():
    data = load_json("testdata/tv.json")
    tv = TVSchema().load(data)

    assert tv.state.input == data["state"]["input"]
    assert len(tv.buttons) == 1
    assert tv.buttons[0].name == data["buttons"][0]["name"]
    assert tv.buttons[0].image == data["buttons"][0]["image"]
    assert tv.buttons[0].label == data["buttons"][0]["label"]

    assert tv.as_json_string() == sorted_json(data)
    assert str(tv) == (
        f"TV(state=TVState(input='{data['state']['input']}'), "
        f"buttons=[Button(name='{data['buttons'][0]['name']}', "
        f"image='{data['buttons'][0]['image']}', "
        f"label='{data['buttons'][0]['label']}')])"
    )


def test_light_state():
    data = load_json("testdata/light_state.json")
    light_state = LightStateSchema().load(data)

    assert light_state.brightness == data["brightness"]
    assert light_state.power == data["power"]
    assert light_state.last_button == data["last_button"]

    assert light_state.as_json_string() == sorted_json(data)
    assert str(light_state) == (
        f"LightState(brightness='{data['brightness']}', "
        f"power='{data['power']}',"
        f" last_button='{data['last_button']}')"
    )


def test_light():
    data = load_json("testdata/light.json")
    light_state = LightStateSchema().load(data["state"])
    button = ButtonSchema().load(data["buttons"][0])
    light = LightSchema().load(data)

    assert light.state.brightness == data["state"]["brightness"]
    assert light.state.power == data["state"]["power"]
    assert light.state.last_button == data["state"]["last_button"]
    assert len(light.buttons) == 1
    assert light.buttons[0].name == data["buttons"][0]["name"]
    assert light.buttons[0].image == data["buttons"][0]["image"]
    assert light.buttons[0].label == data["buttons"][0]["label"]

    assert light.as_json_string() == sorted_json(data)
    assert str(light) == (f"Light(state={light_state}, buttons=[{button}])")


def test_appliance():
    data = load_json("testdata/appliance.json")
    appliance = ApplianceSchema().load(data)

    assert appliance.id == data["id"]
    assert appliance.device.id == data["device"]["id"]
    assert appliance.device.name == data["device"]["name"]
    assert (
        appliance.device.temperature_offset
        == data["device"]["temperature_offset"]
    )
    assert (
        appliance.device.humidity_offset == data["device"]["humidity_offset"]
    )
    assert appliance.device.created_at == str_to_datetime(
        data["device"]["created_at"]
    )
    assert appliance.device.updated_at == str_to_datetime(
        data["device"]["updated_at"]
    )
    assert (
        appliance.device.firmware_version == data["device"]["firmware_version"]
    )
    assert appliance.device.mac_address == data["device"]["mac_address"]
    assert appliance.device.serial_number == data["device"]["serial_number"]
    assert appliance.model.id == data["model"]["id"]
    assert appliance.model.manufacturer == data["model"]["manufacturer"]
    assert appliance.model.remote_name == data["model"]["remote_name"]
    assert appliance.model.name == data["model"]["name"]
    assert appliance.model.image == data["model"]["image"]
    assert appliance.nickname == data["nickname"]
    assert appliance.image == data["image"]
    assert appliance.type == data["type"]
    assert appliance.settings.temp == data["settings"]["temp"]
    assert appliance.settings.mode == data["settings"]["mode"]
    assert appliance.settings.vol == data["settings"]["vol"]
    assert appliance.settings.dir == data["settings"]["dir"]
    assert appliance.settings.button == data["settings"]["button"]
    assert (
        appliance.aircon.range.modes["mode1"].temp
        == data["aircon"]["range"]["modes"]["mode1"]["temp"]
    )
    assert (
        appliance.aircon.range.modes["mode1"].vol
        == data["aircon"]["range"]["modes"]["mode1"]["vol"]
    )
    assert (
        appliance.aircon.range.modes["mode1"].dir
        == data["aircon"]["range"]["modes"]["mode1"]["dir"]
    )
    assert (
        appliance.aircon.range.modes["mode2"].temp
        == data["aircon"]["range"]["modes"]["mode2"]["temp"]
    )
    assert (
        appliance.aircon.range.modes["mode2"].vol
        == data["aircon"]["range"]["modes"]["mode2"]["vol"]
    )
    assert (
        appliance.aircon.range.modes["mode2"].dir
        == data["aircon"]["range"]["modes"]["mode2"]["dir"]
    )
    assert (
        appliance.aircon.range.fixedButtons
        == data["aircon"]["range"]["fixedButtons"]
    )
    assert appliance.aircon.tempUnit == data["aircon"]["tempUnit"]
    assert len(appliance.signals) == 1
    assert appliance.signals[0].id == data["signals"][0]["id"]
    assert appliance.signals[0].name == data["signals"][0]["name"]
    assert appliance.signals[0].image == data["signals"][0]["image"]
    assert appliance.tv.state.input == data["tv"]["state"]["input"]
    assert len(appliance.tv.buttons) == 1
    assert appliance.tv.buttons[0].name == data["tv"]["buttons"][0]["name"]
    assert appliance.tv.buttons[0].image == data["tv"]["buttons"][0]["image"]
    assert appliance.tv.buttons[0].label == data["tv"]["buttons"][0]["label"]

    assert appliance.as_json_string()
    assert str(appliance)


def test_ir_signal():
    data = load_json("testdata/ir_signal.json")
    signal = IRSignalSchema().load(data)

    assert signal.freq == data["freq"]
    assert signal.data == data["data"]
    assert signal.format == data["format"]

    assert signal.as_json_string() == sorted_json(data)
    assert str(signal) == (
        f"IRSignal(freq={data['freq']}, data={data['data']}, "
        f"format='{data['format']}')"
    )
