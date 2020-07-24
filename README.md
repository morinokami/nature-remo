# Python Client for Nature Remo API

## Introduction

`nature-remo` is a Python client for the [Nature Remo API](https://developer.nature.global/).

## Setup

## Usage

## Development Status

### [Cloud API](https://swagger.nature.global/)

Status | HTTP Method | Endpoint | API
--- | --- | --- | ---
⚡️ | GET | `/1/users/me` | `get_user`
⚡️ | POST | `/1/users/me` | `update_user`
⚡️ | GET | `/1/devices` | `get_devices`
🔥 | POST | `/1/detectappliance` |
⚡️ | GET | `/1/appliances` | `get_appliances`
🔥 | POST | `/1/appliances` | `create_appliance`
⚡️ | POST | `/1/appliance_orders` | `update_appliance_orders`
🔥 | POST | `/1/appliances/{appliance}/delete` | `delete_appliance`
🔥 | POST | `/1/appliances/{appliance}` | `update_appliance`
🔥 | POST | `/1/appliances/{appliance}/aircon_settings` | `update_aircon_settings`
🔥 | POST | `/1/appliances/{appliance}/tv` | `send_tv_infrared_signal`
🔥 | POST | `/1/appliances/{appliance}/light` | `send_light_infrared_signal`
⚡️ | GET | `/1/appliances/{appliance}/signals` | `get_signals`
🔥 | POST | `/1/appliances/{appliance}/signals` | `create_signal`
🔥 | POST | `/1/appliances/{appliance}/signal_orders` | `update_signal_orders`
🔥 | POST | `/1/signals/{signal}` | `update_signal`
🔥 | POST | `/1/signals/{signal}/delete` | `delete_signal`
🔥 | POST | `/1/signals/{signal}/send` | `send_signal`
⚡️ | POST | `/1/devices/{device}` | `update_device`
⚡️ | POST | `/1/devices/{device}/delete` | `delete_device`
⚡️ | POST | `/1/devices/{device}/temperature_offset` | `update_temperature_offset`
⚡️ | POST | `/1/devices/{device}/humidity_offset` | `update_humidity_offset`

### [Local API](https://local.swagger.nature.global/)

Status | HTTP Method | Endpoint
--- | --- | ---
🔥 | GET | `/messages`
🔥 | POST | `/messages`

# How to Develop

```sh
$ git clone git@github.com:morinokami/nature-remo.git
$ cd nature-remo
$ pipenv sync --dev
$ pipenv shell
$ pre-commit install
```
