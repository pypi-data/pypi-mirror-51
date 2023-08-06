# aioecobee

## Python3 async library for interacting with the ecobee API

*Requirements:* aiofiles, aiohttp, asyncio

Install aioecobee with `python3 -m pip install aioecobee`.

## Usage

aioecobee's main class is EcobeeAPI; create an API object like this:

```python
from aiohttp import ClientSession
from aioecobee import EcobeeAPI

session = ClientSession()
api_key = xxxxxxxxxxxxxxxxxxxxx
config_file = "/path/to/ecobee.conf"

ecobee = EcobeeAPI(session, api_key=api_key, config_file=config_file)
```

Where:

- `session` is an instance of aiohttp.ClientSession(); 
- `api_key` is the API key obtained from ecobee.com (optional); and,
- `config_file` is the name of a config file for use with aioecobee (optional).

If config_file is not specified, api_key is required.

Obtain a PIN for authorizing on ecobee.com:

```python
await ecobee.request_pin()
```

After authorizing your app on ecobee.com, request tokens:

```python
await ecobee.request_tokens()
```

After obtaining tokens, populate (or update) ecobee.thermostats and ecobee.sensors:

```python
await ecobee.update()
```

Calls to the API will raise an ExpiredTokensError if tokens are expired and need refreshing:

```python
from aioecobee import ExpiredTokensError
try:
    await ecobee.update()
except ExpiredTokensError:
    await ecobee.refresh_tokens()
```

## example.py

An example script is provided to demonstrate the usage of aioecobee.

```bash
python example.py api_key
```

## Caveats

aioecobee does not implement timeouts; use asyncio_timeout in your client code to wrap calls to the API as needed.


## Contributing

Please open issues or pull requests.
