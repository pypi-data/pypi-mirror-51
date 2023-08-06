# Morpheus Python Module

## Installation

`pip install pymorpheus`

## Usage

MorpheusClient() will either retrieve a token (with username and password args), or use an existing token (with token arg)
Use `sslverify=False` to bypass certificate validation.

MorpheusClient.call() accepts the following vars:
- Required (positional):
  - method: one of string: get, post, put, delete
  - path: api call path after /api/
- Optional:
  - options: list of tuples eg. `[('max','50')]`
  - jsonpayload: JSON string of payload for POST/PUT methods

Reference at https://bertramdev.github.io/morpheus-apidoc

```from pymorpheus import MorpheusClient

morpheus = MorpheusClient("https://yoururl", username="youruser", password="yourpass")
results = morpheus.call("get", path="instances")
print(results)
# JSON Output of results
```