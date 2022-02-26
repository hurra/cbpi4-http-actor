# Description
Generic HTTP Actor Plugin for Craftbeerpi4 https://github.com/craftbeerpi/craftbeerpi4/

When updating from 0.0.3 to 0.0.4 continuous mode and continuous interval must be set up again. This is due to renamed configuration parameters. 
# Features
* `HTTP GET` and `HTTP POST`
* set different request urls for `ON` and `OFF`
* option to set custom request timeout
* option to set custom `ON` and custom `OFF` request payload optionally
* option to set username and password for basic authentication
* continous mode to refresh remote url in custom time interval even if internal actor state hasn't changed
* option to disable certificate checking

# Known options for specific devices
* `Allnet ALL 3072`:
  * HTTP method: `GET`
  * Target url on: `http://<your-device>/xml/jsonswitch.php?id=1&set=1`
  * Target url off: `http://<your-device>/xml/jsonswitch.php?id=1&set=0`
  
* `Edimax SP-1101W`:
  * HTTP method: `POST`  
  * Target url on: `http://<your-device>:5000/smartplug.cgi`
  * Target url off: `http://<your-device>:5000/smartplug.cgi`
  * Request body on: `<?xml version="1.0" encoding="utf-8"?><SMARTPLUG id="edimax"><CMD id="setup"><Device.System.Power.State>ON</Device.System.Power.State></CMD></SMARTPLUG>`
  * Request body off: `<?xml version="1.0" encoding="utf-8"?><SMARTPLUG id="edimax"><CMD id="setup"><Device.System.Power.State>OFF</Device.System.Power.State></CMD></SMARTPLUG>`
  * Basic Authentication user: `<your-wifi-socket-username>`
  * Basic Authentication password: `<your-wifi-socket-password>`
