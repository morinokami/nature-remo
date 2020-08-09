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
>>> devices[0].newest_events['te'].val
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

## CLI

`nature-remo` has the command line interface as well.
To invoke the command, type `remo`  on the command line:

```sh
$ remo
Usage: remo [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  appliance
  device
  local
  signal
  user
```

The `remo` command consists of five subcommands, which represent the object you interact with.
For example, the `device` subcommand can be used to interact with the Nature Remo devices associated with your account.
Enter `remo device` on the command line to see what actions the `device` subcommands supports:

```sh
$ remo device
Usage: remo device [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  delete                     Delete Remo.
  get                        Fetch the list of Remo devices the user has...
  update                     Update Remo.
  update_humidity_offset     Update humidity offset.
  update_temperature_offset  Update temperature offset.
```

We can see that the subcommand has five actions.
Thus, for example, if you want to know about the Remo devices associated with your account,
enter the following command:

```sh
$ remo device get --token <access_token>
[{"created_at": "2020-07-23T03:10:21+00:00", ...}]
```

The access token can be specified as an environment variable:

```sh
$ export REMO_ACCESS_TOKEN=<access_token>
$ remo device get
[{"created_at": "2020-07-23T03:10:21+00:00", ...}]
```

Use the `--debug` flag to inspect the details about the HTTP connection:

```sh
$ remo user update foo --debug
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): api.nature.global:443
send: b'POST /1/users/me HTTP/1.1\r\nHost: api.nature.global\r\nUser-Agent: nature-remo/0.3.0 (https://github.com/morinokami/nature-remo)\r\nAccept-Encoding: gzip, deflate\r\nAccept: application/json\r\nConnection: keep-alive\r\nAuthorization: Bearer access_token\r\nContent-Length: 12\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n'
send: b'nickname=foo'
reply: 'HTTP/1.1 200 OK\r\n'
header: Date: Fri, 31 Jul 2020 07:26:52 GMT
header: Content-Type: application/json; charset=utf-8
header: Content-Length: 62
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
header: X-Rate-Limit-Remaining: 21
header: X-Rate-Limit-Reset: 1596180600
header: X-Xss-Protection: 1; mode=block
DEBUG:urllib3.connectionpool:https://api.nature.global:443 "POST /1/users/me HTTP/1.1" 200 62
{"id": "user_id", "nickname": "foo"}
```

Internally, those `remo <subcommand> <action> (<args>)` commands are mapped to the Nature Remo API.
The full list of those mappings is as follows:

Command | Nature Remo API
--- | ---
`remo user get` | `GET /1/users/me`
`remo user update` | `POST /1/users/me`
`remo device get` | `GET /1/devices`
`remo device update` | `POST /1/devices/{device}`
`remo device delete` | `POST /1/devices/{device}/delete`
`remo device update_temperature_offset` | `POST /1/devices/{device}/temperature_offset`
`remo device update_humidity_offset` | `POST /1/devices/{device}/humidity_offset`
`remo appliance detect` | `POST /1/detectappliance`
`remo appliance create` | `POST /1/appliances`
`remo appliance get` | `GET /1/appliances`
`remo appliance update` | `POST /1/appliances/{appliance}`
`remo appliance delete` | `POST /1/appliances/{appliance}/delete`
`remo appliance update_orders` | `POST /1/appliance_orders`
`remo appliance update_aircon_settings` | `POST /1/appliances/{appliance}/aircon_settings`
`remo appliance send_tv_infrared_signal` | `POST /1/appliances/{appliance}/tv`
`remo appliance send_light_infrared_signal` | `POST /1/appliances/{appliance}/light`
`remo signal create` | `/1/appliances/{appliance}/signals`
`remo signal get` | `GET /1/appliances/{appliance}/signals`
`remo signal update` | `POST /1/signals/{signal}`
`remo signal delete` | `/1/signals/{signal}/delete`
`remo signal send` | `/1/signals/{signal}/send`
`remo signal update_orders` | `/1/appliances/{appliance}/signal_orders`


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
>>> devices[0].newest_events['te'].val
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

## CLI

`nature-remo` にはコマンドラインインターフェイスもあります。
コマンドを実行するには、コマンドラインで `remo` と入力してください:

```sh
$ remo
Usage: remo [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  appliance
  device
  local
  signal
  user
```

`remo` コマンドは五つのサブコマンドから成り、それぞれが操作の対象を表わしています。
たとえば、`device` サブコマンドは、あなたのアカウントに紐付いている Nature Remo の機器に対する操作を可能とします。
コマンドライン上で `remo device` と入力し、`device` がサポートしている操作を確認してみましょう:

```sh
$ remo device
Usage: remo device [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  delete                     Delete Remo.
  get                        Fetch the list of Remo devices the user has...
  update                     Update Remo.
  update_humidity_offset     Update humidity offset.
  update_temperature_offset  Update temperature offset.
```

このサブコマンドは五つの操作をサポートしていることがわかります。
これより、たとえばあなたのアカウントに紐付いている Remo の機器について知りたければ、次のコマンドを実行してください:

```sh
$ remo device get --token <access_token>
[{"created_at": "2020-07-23T03:10:21+00:00", ...}]
```

アクセストークンは環境変数により指定することもできます:

```sh
$ export REMO_ACCESS_TOKEN=<access_token>
$ remo device get
[{"created_at": "2020-07-23T03:10:21+00:00", ...}]
```

`--debug` フラグにより、HTTP 通信の詳細を確認することが可能です:

```sh
$ remo user update foo --debug
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): api.nature.global:443
send: b'POST /1/users/me HTTP/1.1\r\nHost: api.nature.global\r\nUser-Agent: nature-remo/0.3.0 (https://github.com/morinokami/nature-remo)\r\nAccept-Encoding: gzip, deflate\r\nAccept: application/json\r\nConnection: keep-alive\r\nAuthorization: Bearer access_token\r\nContent-Length: 12\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n'
send: b'nickname=foo'
reply: 'HTTP/1.1 200 OK\r\n'
header: Date: Fri, 31 Jul 2020 07:26:52 GMT
header: Content-Type: application/json; charset=utf-8
header: Content-Length: 62
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
header: X-Rate-Limit-Remaining: 21
header: X-Rate-Limit-Reset: 1596180600
header: X-Xss-Protection: 1; mode=block
DEBUG:urllib3.connectionpool:https://api.nature.global:443 "POST /1/users/me HTTP/1.1" 200 62
{"id": "user_id", "nickname": "foo"}
```

内部では、こうした `remo <subcommand> <action> (<args>)` コマンドは Nature Remo API へとマップされています。
マッピングのフルリストは以下の通りです:

Command | Nature Remo API
--- | ---
`remo user get` | `GET /1/users/me`
`remo user update` | `POST /1/users/me`
`remo device get` | `GET /1/devices`
`remo device update` | `POST /1/devices/{device}`
`remo device delete` | `POST /1/devices/{device}/delete`
`remo device update_temperature_offset` | `POST /1/devices/{device}/temperature_offset`
`remo device update_humidity_offset` | `POST /1/devices/{device}/humidity_offset`
`remo appliance detect` | `POST /1/detectappliance`
`remo appliance create` | `POST /1/appliances`
`remo appliance get` | `GET /1/appliances`
`remo appliance update` | `POST /1/appliances/{appliance}`
`remo appliance delete` | `POST /1/appliances/{appliance}/delete`
`remo appliance update_orders` | `POST /1/appliance_orders`
`remo appliance update_aircon_settings` | `POST /1/appliances/{appliance}/aircon_settings`
`remo appliance send_tv_infrared_signal` | `POST /1/appliances/{appliance}/tv`
`remo appliance send_light_infrared_signal` | `POST /1/appliances/{appliance}/light`
`remo signal create` | `/1/appliances/{appliance}/signals`
`remo signal get` | `GET /1/appliances/{appliance}/signals`
`remo signal update` | `POST /1/signals/{signal}`
`remo signal delete` | `/1/signals/{signal}/delete`
`remo signal send` | `/1/signals/{signal}/send`
`remo signal update_orders` | `/1/appliances/{appliance}/signal_orders`
