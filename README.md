# Python Client for Nature Remo API

[![PyPI version](https://badge.fury.io/py/nature-remo.svg)](https://badge.fury.io/py/nature-remo)
![Test](https://github.com/morinokami/nature-remo/workflows/Test/badge.svg)

## Introduction

`nature-remo` is a Python client for the [Nature Remo API](https://developer.nature.global/).

## Installation

```sh
$ pip install nature-remo
```

## Usage

To create an instance of `remo.NatureRemoAPI` with your access token:

```py
>>> from remo import NatureRemoAPI
>>> api = NatureRemoAPI('access_token')
```

To fetch the authenticated user's information:

```py
>>> user = api.get_user()
>>> user.id
'user_id'
>>> user.nickname
'your_nickname'
```

To fetch the list of Remo devices and print the temperature of the first device:

```py
>>> devices = api.get_devices()
>>> devices[0].newest_events['te']['val']
26.528809
```

To fetch the list of appliances:

```py
>>> appliances = api.get_appliances()
>>> appliances[0].id
'appliance_id'
>>> appliances[0].type
'AC'
```

To update air conditioner settings:

```py
>>> aircon = appliances[0]
>>> api.update_aircon_settings(aircon.id, 'cool', '27', 'auto', 'swing', '')
```

To send a tv infrared signal:

```py
>>> appliances[1].type
'TV'
>>> tv = appliances[1]
>>> api.send_tv_infrared_signal(tv.id, 'power')
```

To check the current rate limit status:

```py
>>> api.get_user()
...
>>> api.rate_limit
RateLimit(checked_at=datetime.datetime(2020, 7, 28, 8, 11, 4), limit=30, remaining=29, reset=datetime.datetime(2020, 7, 28, 8, 15))
>>> api.rate_limit.checked_at, api.rate_limit.limit, api.rate_limit.remaining, api.rate_limit.reset
(datetime.datetime(2020, 7, 28, 8, 11, 4), 30, 29, datetime.datetime(2020, 7, 28, 8, 15))
```

To create an instance of `remo.NatureRemoLocalAPI`:

```py
>>> from remo import NatureRemoLocalAPI
>>> local_api = NatureRemoLocalAPI('ip_addr')
```

To fetch the newest received IR signal:

```py
>>> local_api.get_ir_signal()
IRSignal(freq=38, data=[0], format='us')
```

To emit an IR signal:

```py
>>> message = '{"format": "us", "freq": 38, "data": [0]}'
>>> local_api.send_ir_signal(message)
```

To print the underlying `urllib3` debug information:

```py
>>> api = NatureRemoAPI('access_token', debug=True)
>>> api.get_user()
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): api.nature.global:443
send: b'GET /1/users/me HTTP/1.1\r\nHost: api.nature.global\r\nUser-Agent: nature-remo/0.1.0 (https://github.com/morinokami/nature-remo)\r\nAccept-Encoding: gzip, deflate\r\nAccept: application/json\r\nConnection: keep-alive\r\nAuthorization: Bearer access_token\r\n\r\n'
reply: 'HTTP/1.1 200 OK\r\n'
header: Date: Mon, 27 Jul 2020 15:53:12 GMT
header: Content-Type: application/json; charset=utf-8
header: Content-Length: 72
header: Connection: keep-alive
header: Access-Control-Allow-Origin: *
header: Cache-Control: no-cache, no-store, must-revalidate, private, max-age=0
header: Expires: Thu, 01 Jan 1970 00:00:00 UTC
header: Pragma: no-cache
header: Strict-Transport-Security: max-age=86400
header: Vary: Accept-Encoding
header: X-Accel-Expires: 0
header: X-Content-Type-Options: nosniff
header: X-Frame-Options: SAMEORIGIN
header: X-Rate-Limit-Limit: 30
header: X-Rate-Limit-Remaining: 29
header: X-Rate-Limit-Reset: 1595865300
header: X-Xss-Protection: 1; mode=block
DEBUG:urllib3.connectionpool:https://api.nature.global:443 "GET /1/users/me HTTP/1.1" 200 72
User(id='user_id', nickname='your_nickname')
```

## Development Status

### [Cloud API](https://swagger.nature.global/) (Base URL: `api.nature.global/`)

Status | HTTP Method | Endpoint | API
--- | --- | --- | ---
⚡️ | GET | `/1/users/me` | `get_user`
⚡️ | POST | `/1/users/me` | `update_user`
⚡️ | GET | `/1/devices` | `get_devices`
️⚡️ | POST | `/1/detectappliance` | `detect_appliance`
⚡️ | GET | `/1/appliances` | `get_appliances`
⚡ | POST | `/1/appliances` | `create_appliance`
⚡️ | POST | `/1/appliance_orders` | `update_appliance_orders`
⚡ | POST | `/1/appliances/{appliance}/delete` | `delete_appliance`
⚡️ | POST | `/1/appliances/{appliance}` | `update_appliance`
⚡ | POST | `/1/appliances/{appliance}/aircon_settings` | `update_aircon_settings`
⚡️ | POST | `/1/appliances/{appliance}/tv` | `send_tv_infrared_signal`
️⚡ | POST | `/1/appliances/{appliance}/light` | `send_light_infrared_signal`
⚡️ | GET | `/1/appliances/{appliance}/signals` | `get_signals`
⚡ | POST | `/1/appliances/{appliance}/signals` | `create_signal`
⚡ | POST | `/1/appliances/{appliance}/signal_orders` | `update_signal_orders`
⚡ | POST | `/1/signals/{signal}` | `update_signal`
⚡ | POST | `/1/signals/{signal}/delete` | `delete_signal`
⚡ | POST | `/1/signals/{signal}/send` | `send_signal`
⚡️ | POST | `/1/devices/{device}` | `update_device`
⚡️ | POST | `/1/devices/{device}/delete` | `delete_device`
⚡️ | POST | `/1/devices/{device}/temperature_offset` | `update_temperature_offset`
⚡️ | POST | `/1/devices/{device}/humidity_offset` | `update_humidity_offset`

### [Local API](https://local.swagger.nature.global/) (Base URL: `remo.local/`)

Status | HTTP Method | Endpoint | API
--- | --- | --- | ---
⚡️ | GET | `/messages` | `get_ir_signal`
⚡️ | POST | `/messages` | `send_ir_signal`

## How to Develop

```sh
$ git clone git@github.com:morinokami/nature-remo.git
$ cd nature-remo
$ pipenv sync --dev
$ pipenv shell
$ pre-commit install
```

---

## はじめに

`nature-remo` は、[Nature Remo API](https://developer.nature.global/) の Python クライアントです。

## インストール

```sh
$ pip install nature-remo
```

## 使い方

アクセストークンを指定して `remo.NatureRemoAPI` のインスタンスを作成する:

```py
>>> from remo import NatureRemoAPI
>>> api = NatureRemoAPI('access_token')
```

認証されたユーザーの情報を取得する:

```py
>>> user = api.get_user()
>>> user.id
'user_id'
>>> user.nickname
'your_nickname'
```

Remo の機器リストを取得し、最初の機器の温度を表示する:

```py
>>> devices = api.get_devices()
>>> devices[0].newest_events['te']['val']
26.528809
```

家電製品のリストを取得する:

```py
>>> appliances = api.get_appliances()
>>> appliances[0].id
'appliance_id'
>>> appliances[0].type
'AC'
```

エアコンの設定を変更する:

```py
>>> aircon = appliances[0]
>>> api.update_aircon_settings(aircon.id, 'cool', '27', 'auto', 'swing', '')
```

テレビの赤外線を送信する:

```py
>>> appliances[1].type
'TV'
>>> tv = appliances[1]
>>> api.send_tv_infrared_signal(tv.id, "power")
```

現在の呼び出し制限 (Rate Limit) を確認する:

```py
>>> api.get_user()
...
>>> api.rate_limit
RateLimit(checked_at=datetime.datetime(2020, 7, 28, 8, 11, 4), limit=30, remaining=29, reset=datetime.datetime(2020, 7, 28, 8, 15))
>>> api.rate_limit.checked_at, api.rate_limit.limit, api.rate_limit.remaining, api.rate_limit.reset
(datetime.datetime(2020, 7, 28, 8, 11, 4), 30, 29, datetime.datetime(2020, 7, 28, 8, 15))
```

`remo.NatureRemoLocalAPI` のインスタンスを作成する:

```py
>>> from remo import NatureRemoLocalAPI
>>> local_api = NatureRemoLocalAPI('ip_addr')
```

受信した最新の赤外線信号を取得する:

```py
>>> local_api.get_ir_signal()
IRSignal(freq=38, data=[0], format='us')
```

赤外線を送出する:

```py
>>> message = '{"format": "us", "freq": 38, "data": [0]}'
>>> local_api.send_ir_signal(message)
```

`urllib3`のデバッグ情報を出力する:

```py
>>> api = NatureRemoAPI('access_token', debug=True)
>>> api.get_user()
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): api.nature.global:443
send: b'GET /1/users/me HTTP/1.1\r\nHost: api.nature.global\r\nUser-Agent: nature-remo/0.1.0 (https://github.com/morinokami/nature-remo)\r\nAccept-Encoding: gzip, deflate\r\nAccept: application/json\r\nConnection: keep-alive\r\nAuthorization: Bearer access_token\r\n\r\n'
reply: 'HTTP/1.1 200 OK\r\n'
header: Date: Mon, 27 Jul 2020 15:53:12 GMT
header: Content-Type: application/json; charset=utf-8
header: Content-Length: 72
header: Connection: keep-alive
header: Access-Control-Allow-Origin: *
header: Cache-Control: no-cache, no-store, must-revalidate, private, max-age=0
header: Expires: Thu, 01 Jan 1970 00:00:00 UTC
header: Pragma: no-cache
header: Strict-Transport-Security: max-age=86400
header: Vary: Accept-Encoding
header: X-Accel-Expires: 0
header: X-Content-Type-Options: nosniff
header: X-Frame-Options: SAMEORIGIN
header: X-Rate-Limit-Limit: 30
header: X-Rate-Limit-Remaining: 29
header: X-Rate-Limit-Reset: 1595865300
header: X-Xss-Protection: 1; mode=block
DEBUG:urllib3.connectionpool:https://api.nature.global:443 "GET /1/users/me HTTP/1.1" 200 72
User(id='user_id', nickname='your_nickname')
```
