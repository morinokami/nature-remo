import json
from datetime import datetime
from datetime import timezone

from remo import AirConParamsSchema
from remo import AirConRangeModeSchema
from remo import AirConRangeSchema
from remo import AirConSchema
from remo import ApplianceModelSchema
from remo import ApplianceSchema
from remo import ButtonSchema
from remo import DeviceCoreSchema
from remo import DeviceSchema
from remo import IRSignalSchema
from remo import LightSchema
from remo import LightStateSchema
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
    user_id = "user-id-123-abc"
    user_nickname = "lorem ipsum"
    data = {"id": user_id, "nickname": user_nickname}

    user = UserSchema().load(data)

    assert user.id == user_id
    assert user.nickname == user_nickname

    assert user.as_json_string() == sorted_json(data)
    assert str(user) == f'User(id="{user_id}", nickname="{user_nickname}")'


def test_device_core():
    device_id = "device-id-123-abc"
    device_name = "Remo"
    temperature_offset = 0
    humidity_offset = 0
    dummy_datetime = "2020-01-01T01:23:45Z"
    firmware_version = "Remo/1.0.23"
    mac_address = "ab:cd:ef:01:23:45"
    serial_number = "1W111111111111"
    data = {
        "id": device_id,
        "name": device_name,
        "temperature_offset": temperature_offset,
        "humidity_offset": humidity_offset,
        "created_at": dummy_datetime,
        "updated_at": dummy_datetime,
        "firmware_version": firmware_version,
        "mac_address": mac_address,
        "serial_number": serial_number,
    }

    device_core = DeviceCoreSchema().load(data)

    assert device_core.id == device_id
    assert device_core.name == device_name
    assert device_core.temperature_offset == temperature_offset
    assert device_core.humidity_offset == humidity_offset
    assert device_core.created_at == str_to_datetime(dummy_datetime)
    assert device_core.updated_at == str_to_datetime(dummy_datetime)
    assert device_core.firmware_version == firmware_version
    assert device_core.mac_address == mac_address
    assert device_core.serial_number == serial_number

    assert device_core.as_json_string()
    assert str(device_core)


def test_device():
    device_id = "device-id-123-abc"
    device_name = "Remo"
    temperature_offset = 0
    humidity_offset = 0
    dummy_datetime = "2020-01-01T01:23:45Z"
    firmware_version = "Remo/1.0.23"
    mac_address = "ab:cd:ef:01:23:45"
    serial_number = "1W111111111111"
    hu_val = 76
    il_val = 0
    mo_val = 1
    te_val = 25.149109
    data = {
        "id": device_id,
        "name": device_name,
        "temperature_offset": temperature_offset,
        "humidity_offset": humidity_offset,
        "created_at": dummy_datetime,
        "updated_at": dummy_datetime,
        "firmware_version": firmware_version,
        "mac_address": mac_address,
        "serial_number": serial_number,
        "newest_events": {
            "hu": {"val": hu_val, "created_at": dummy_datetime},
            "il": {"val": il_val, "created_at": dummy_datetime},
            "mo": {"val": mo_val, "created_at": dummy_datetime},
            "te": {"val": te_val, "created_at": dummy_datetime},
        },
    }

    device = DeviceSchema().load(data)

    assert device.id == device_id
    assert device.name == device_name
    assert device.temperature_offset == temperature_offset
    assert device.humidity_offset == humidity_offset
    assert device.created_at == str_to_datetime(dummy_datetime)
    assert device.updated_at == str_to_datetime(dummy_datetime)
    assert device.firmware_version == firmware_version
    assert device.mac_address == mac_address
    assert device.serial_number == serial_number
    assert device.newest_events["hu"]["val"] == hu_val
    assert device.newest_events["hu"]["created_at"] == str_to_datetime(
        dummy_datetime
    )
    assert device.newest_events["il"]["val"] == il_val
    assert device.newest_events["il"]["created_at"] == str_to_datetime(
        dummy_datetime
    )
    assert device.newest_events["mo"]["val"] == mo_val
    assert device.newest_events["mo"]["created_at"] == str_to_datetime(
        dummy_datetime
    )
    assert device.newest_events["te"]["val"] == te_val
    assert device.newest_events["te"]["created_at"] == str_to_datetime(
        dummy_datetime
    )

    assert device.as_json_string()
    assert str(device)


def test_appliance_model():
    id = "appliance-id"
    manufacturer = "XXX"
    remote_name = "abc123"
    name = "XXX AC 001"
    image = "ico_appliance"
    data = {
        "id": id,
        "manufacturer": manufacturer,
        "remote_name": remote_name,
        "name": name,
        "image": image,
    }

    appliance_model = ApplianceModelSchema().load(data)

    assert appliance_model.id == id
    assert appliance_model.manufacturer == manufacturer
    assert appliance_model.remote_name == remote_name
    assert appliance_model.name == name
    assert appliance_model.image == image

    assert appliance_model.as_json_string() == sorted_json(data)
    assert (
        str(appliance_model)
        == f'ApplianceModel(id="{id}", manufacturer="{manufacturer}", '
        + f'remote_name="{remote_name}", name="{name}", image="{image}")'
    )


def test_air_con_params():
    temp = "27"
    mode = "cool"
    vol = "auto"
    dir = "swing"
    button = "power-off"
    data = {
        "temp": temp,
        "mode": mode,
        "vol": vol,
        "dir": dir,
        "button": button,
    }

    air_con_params = AirConParamsSchema().load(data)

    assert air_con_params.temp == temp
    assert air_con_params.mode == mode
    assert air_con_params.vol == vol
    assert air_con_params.dir == dir
    assert air_con_params.button == button

    assert air_con_params.as_json_string() == sorted_json(data)
    assert (
        str(air_con_params)
        == f'AirConParams(temp="{temp}", mode="{mode}", vol="{vol}", '
        + f'dir="{dir}", button="{button}")'
    )


def test_air_con_range_mode():
    temp = ["25", "26", "27"]
    vol = ["1", "2", "3", "auto"]
    dir = ["1", "2", "auto", "swing"]
    data = {"temp": temp, "vol": vol, "dir": dir}

    air_con_range_mode = AirConRangeModeSchema().load(data)

    assert air_con_range_mode.temp == temp
    assert air_con_range_mode.vol == vol
    assert air_con_range_mode.dir == dir

    assert air_con_range_mode.as_json_string() == sorted_json(data)
    assert (
        str(air_con_range_mode)
        == f"AirConRangeMode(temp={json.dumps(temp)}, vol={json.dumps(vol)}, "
        + f"dir={json.dumps(dir)})"
    )


def test_air_con_range():
    modes = {
        "mode1": {
            "temp": ["1", "2", "3"],
            "vol": ["1", "auto"],
            "dir": ["1", "2"],
        },
        "mode2": {
            "temp": ["1", "2"],
            "vol": ["1", "2", "auto"],
            "dir": ["auto", "swing"],
        },
    }
    fixedButtons = ["power-off"]
    data = {"modes": modes, "fixedButtons": fixedButtons}

    air_con_range = AirConRangeSchema().load(data)

    assert "mode1" in air_con_range.modes
    assert air_con_range.modes["mode1"].temp == modes["mode1"]["temp"]
    assert air_con_range.modes["mode1"].vol == modes["mode1"]["vol"]
    assert air_con_range.modes["mode1"].dir == modes["mode1"]["dir"]
    assert "mode2" in air_con_range.modes
    assert air_con_range.modes["mode2"].temp == modes["mode2"]["temp"]
    assert air_con_range.modes["mode2"].vol == modes["mode2"]["vol"]
    assert air_con_range.modes["mode2"].dir == modes["mode2"]["dir"]
    assert air_con_range.fixedButtons == fixedButtons

    assert air_con_range.as_json_string() == sorted_json(data)
    assert str(air_con_range)


def test_air_con():
    modes = {
        "mode1": {
            "temp": ["1", "2", "3"],
            "vol": ["1", "auto"],
            "dir": ["1", "2"],
        },
        "mode2": {
            "temp": ["1", "2"],
            "vol": ["1", "2", "auto"],
            "dir": ["auto", "swing"],
        },
    }
    range = {
        "modes": modes,
        "fixedButtons": ["power-off"],
    }
    tempUnit = "c"
    data = {"range": range, "tempUnit": tempUnit}

    air_con = AirConSchema().load(data)

    assert "mode1" in air_con.range.modes
    assert air_con.range.modes["mode1"].temp == modes["mode1"]["temp"]
    assert air_con.range.modes["mode1"].vol == modes["mode1"]["vol"]
    assert air_con.range.modes["mode1"].dir == modes["mode1"]["dir"]
    assert "mode2" in air_con.range.modes
    assert air_con.range.modes["mode2"].temp == modes["mode2"]["temp"]
    assert air_con.range.modes["mode2"].vol == modes["mode2"]["vol"]
    assert air_con.range.modes["mode2"].dir == modes["mode2"]["dir"]
    assert air_con.range.fixedButtons == range["fixedButtons"]
    assert air_con.tempUnit == tempUnit

    assert air_con.as_json_string() == sorted_json(data)
    assert str(air_con)


def test_signal():
    id = "signal-id"
    name = "signal-name"
    image = "ico_signal"
    data = {"id": id, "name": name, "image": image}

    signal = SignalSchema().load(data)

    assert signal.id == id
    assert signal.name == name
    assert signal.image == image

    assert signal.as_json_string() == sorted_json(data)
    assert str(signal) == f'Signal(id="{id}", name="{name}", image="{image}")'


def test_button():
    name = "button-name"
    image = "ico_button"
    label = "button_label"
    data = {"name": name, "image": image, "label": label}

    button = ButtonSchema().load(data)

    assert button.name == name
    assert button.image == image
    assert button.label == label

    assert button.as_json_string() == sorted_json(data)
    assert (
        str(button)
        == f'Button(name="{name}", image="{image}", label="{label}")'
    )


def test_tv_state():
    input = "t"
    data = {"input": input}

    tv_state = TVStateSchema().load(data)

    assert tv_state.input == input

    assert tv_state.as_json_string() == sorted_json(data)
    assert str(tv_state) == f'TVState(input="{input}")'


def test_tv():
    state_input = "t"
    btn_name = "button-name"
    btn_image = "ico_button"
    btn_label = "button_label"
    data = {
        "state": {"input": state_input},
        "buttons": [
            {"name": btn_name, "image": btn_image, "label": btn_label}
        ],
    }

    tv = TVSchema().load(data)

    assert tv.state.input == state_input
    assert len(tv.buttons) == 1
    assert tv.buttons[0].name == btn_name
    assert tv.buttons[0].image == btn_image
    assert tv.buttons[0].label == btn_label

    assert tv.as_json_string() == sorted_json(data)
    assert str(tv) == (
        f'TV(state=TVState(input="{state_input}"), '
        + f'buttons=[Button(name="{btn_name}", image="{btn_image}", '
        + f'label="{btn_label}")])'
    )


def test_light_state():
    brightness = "bright"
    power = "on"
    last_button = "button"
    data = {
        "brightness": brightness,
        "power": power,
        "last_button": last_button,
    }

    light_state = LightStateSchema().load(data)

    assert light_state.brightness == brightness
    assert light_state.power == power
    assert light_state.last_button == last_button

    assert light_state.as_json_string() == sorted_json(data)
    assert (
        str(light_state)
        == f'LightState(brightness="{brightness}", power="{power}",'
        + f' last_button="{last_button}")'
    )


def test_light():
    state = {
        "brightness": "bright",
        "power": "on",
        "last_button": "button",
    }
    buttons = [
        {
            "name": "button-name",
            "image": "ico_button",
            "label": "button_label",
        }
    ]
    data = {"state": state, "buttons": buttons}

    light_state = LightStateSchema().load(state)
    button = ButtonSchema().load(buttons[0])
    light = LightSchema().load(data)

    assert light.state.brightness == state["brightness"]
    assert light.state.power == state["power"]
    assert light.state.last_button == state["last_button"]
    assert len(light.buttons) == 1
    assert light.buttons[0].name == buttons[0]["name"]
    assert light.buttons[0].image == buttons[0]["image"]
    assert light.buttons[0].label == buttons[0]["label"]

    assert light.as_json_string() == sorted_json(data)
    assert str(light) == f"Light(state={light_state}, buttons=[{button}])"


def test_appliance():
    id = "appliance-id"
    device = {
        "id": "device_id",
        "name": "device_name",
        "temperature_offset": 0,
        "humidity_offset": 0,
        "created_at": "2020-01-01T01:23:45Z",
        "updated_at": "2020-01-01T01:23:45Z",
        "firmware_version": "Remo/1.0.23",
        "mac_address": "ab:cd:ef:01:23:45",
        "serial_number": "1W111111111111",
    }
    model = {
        "id": "appliance-modelid",
        "manufacturer": "XXX",
        "remote_name": "abc123",
        "name": "XXX AC 001",
        "image": "ico_appliance_model",
    }
    nickname = "appliance-nickname"
    image = "ico_appliance"
    type = "AC"
    settings = {
        "temp": "27",
        "mode": "cool",
        "vol": "auto",
        "dir": "swing",
        "button": "power-off",
    }
    aircon = {
        "range": {
            "modes": {
                "mode1": {
                    "temp": ["1", "2", "3"],
                    "vol": ["1", "auto"],
                    "dir": ["1", "2"],
                },
                "mode2": {
                    "temp": ["1", "2"],
                    "vol": ["1", "2", "auto"],
                    "dir": ["auto", "swing"],
                },
            },
            "fixedButtons": ["power-off"],
        },
        "tempUnit": "c",
    }
    signals = [
        {"id": "signal-id", "name": "signal-name", "image": "ico_signal"}
    ]
    tv = {
        "state": {"input": "t"},
        "buttons": [
            {
                "name": "button-name",
                "image": "ico_button",
                "label": "button_label",
            }
        ],
    }
    data = {
        "id": id,
        "device": device,
        "model": model,
        "nickname": nickname,
        "image": image,
        "type": type,
        "settings": settings,
        "aircon": aircon,
        "signals": signals,
        "tv": tv,
    }

    appliance = ApplianceSchema().load(data)

    assert appliance.id == id
    assert appliance.device.id == device["id"]
    assert appliance.device.name == device["name"]
    assert appliance.device.temperature_offset == device["temperature_offset"]
    assert appliance.device.humidity_offset == device["humidity_offset"]
    assert appliance.device.created_at == str_to_datetime(device["created_at"])
    assert appliance.device.updated_at == str_to_datetime(device["updated_at"])
    assert appliance.device.firmware_version == device["firmware_version"]
    assert appliance.device.mac_address == device["mac_address"]
    assert appliance.device.serial_number == device["serial_number"]
    assert appliance.model.id == model["id"]
    assert appliance.model.manufacturer == model["manufacturer"]
    assert appliance.model.remote_name == model["remote_name"]
    assert appliance.model.name == model["name"]
    assert appliance.model.image == model["image"]
    assert appliance.nickname == nickname
    assert appliance.image == image
    assert appliance.type == type
    assert appliance.settings.temp == settings["temp"]
    assert appliance.settings.mode == settings["mode"]
    assert appliance.settings.vol == settings["vol"]
    assert appliance.settings.dir == settings["dir"]
    assert appliance.settings.button == settings["button"]
    assert (
        appliance.aircon.range.modes["mode1"].temp
        == aircon["range"]["modes"]["mode1"]["temp"]
    )
    assert (
        appliance.aircon.range.modes["mode1"].vol
        == aircon["range"]["modes"]["mode1"]["vol"]
    )
    assert (
        appliance.aircon.range.modes["mode1"].dir
        == aircon["range"]["modes"]["mode1"]["dir"]
    )
    assert (
        appliance.aircon.range.modes["mode2"].temp
        == aircon["range"]["modes"]["mode2"]["temp"]
    )
    assert (
        appliance.aircon.range.modes["mode2"].vol
        == aircon["range"]["modes"]["mode2"]["vol"]
    )
    assert (
        appliance.aircon.range.modes["mode2"].dir
        == aircon["range"]["modes"]["mode2"]["dir"]
    )
    assert (
        appliance.aircon.range.fixedButtons == aircon["range"]["fixedButtons"]
    )
    assert appliance.aircon.tempUnit == aircon["tempUnit"]
    assert len(appliance.signals) == 1
    assert appliance.signals[0].id == signals[0]["id"]
    assert appliance.signals[0].name == signals[0]["name"]
    assert appliance.signals[0].image == signals[0]["image"]
    assert appliance.tv.state.input == tv["state"]["input"]
    assert len(appliance.tv.buttons) == 1
    assert appliance.tv.buttons[0].name == tv["buttons"][0]["name"]
    assert appliance.tv.buttons[0].image == tv["buttons"][0]["image"]
    assert appliance.tv.buttons[0].label == tv["buttons"][0]["label"]

    assert appliance.as_json_string()
    assert str(appliance)


def test_ir_signal():
    freq = 38
    data = [0]
    format = "us"
    signal_data = {"freq": freq, "data": data, "format": format}

    signal = IRSignalSchema().load(signal_data)

    assert signal.freq == freq
    assert signal.data == data
    assert signal.format == format

    assert signal.as_json_string() == sorted_json(signal_data)
    assert (
        str(signal) == f'IRSignal(freq={freq}, data={data}, format="{format}")'
    )
