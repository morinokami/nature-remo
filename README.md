# Python Client for Nature Remo API

## Introduction

`nature-remo` is a Python client for the [Nature Remo API](https://developer.nature.global/).

## Setup

## Usage

## Development Status

### [Cloud API](https://swagger.nature.global/)

Status | HTTP Method | Endpoint
--- | --- | ---
🔥 | GET | `/1/users/me`
🔥 | POST | `/1/users/me`
🔥 | GET | `/1/devices`
🔥 | POST | `/1/detectappliance`
🔥 | GET | `/1/appliances`
🔥 | POST | `/1/appliances`
🔥 | POST | `/1/appliance_orders`
🔥 | POST | `/1/appliances/{appliance}/delete`
🔥 | POST | `/1/appliances/{appliance}`
🔥 | POST | `/1/appliances/{appliance}/aircon_settings`
🔥 | POST | `/1/appliances/{appliance}/tv`
🔥 | POST | `/1/appliances/{appliance}/light`
🔥 | GET | `/1/appliances/{appliance}/signals`
🔥 | POST | `/1/appliances/{appliance}/signals`
🔥 | POST | `/1/appliances/{appliance}/signal_orders`
🔥 | POST | `/1/signals/{signal}`
🔥 | POST | `/1/signals/{signal}/delete`
🔥 | POST | `/1/signals/{signal}/send`
🔥 | POST | `/1/devices/{device}`
🔥 | POST | `/1/devices/{device}/delete`
🔥 | POST | `/1/devices/{device}/temperature_offset`
🔥 | POST | `/1/devices/{device}/humidity_offset`

### [Local API](https://local.swagger.nature.global/)

Status | HTTP Method | Endpoint
--- | --- | ---
🔥 | GET | `/messages`
🔥 | POST | `/messages`

# How to Develop

```sh
$ pipenv install --dev
$ pipenv shell
$ pre-commit install
```
