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

# JSON Format

```javascript
{ "IF_DATE" : "yyyymmddhhmmss",
  "IT_CARRIERS" : [ { "LOCATION" : "<def>",
        "SENDER_ID" : "<abc>",
        "X" : "<xx.xxx>",
        "Y" : "<yy.yyy>",
        "Z" : "<zz.zzz>"
      } ]
}
```
There will be multiple IT_CARRIERS in the list.
