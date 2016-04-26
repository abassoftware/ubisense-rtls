# ubisense-rtls
Mock server for ubisense rtls clients

This is a mock server that sends [ubisense rtls](http://ubisense.net/en/products/rtls-platform) JSON POST bodies to a specified URL.

Use Python 2.7

```bash
python ubisenseServer.py --url http://<server>:<port>/<endpoint-of-your-client>
```
This will send JSON Post body to the endpoint.

```bash
python ubisenseServer.py --url http://<server>:<port>/<endpoint-of-your-client> --location LOCATION1
```
This will send JSON Post body to the endpoint with an ubisense location LOCATION1
