# ollehtv
[![Build Status](https://travis-ci.org/pmrowla/ollehtv.svg?branch=master)](https://travis-ci.org/pmrowla/ollehtv)
[![Coverage Status](https://coveralls.io/repos/github/pmrowla/ollehtv/badge.svg?branch=master)](https://coveralls.io/github/pmrowla/ollehtv?branch=master)

Python library for controlling an Olleh TV set-top-boxes.

## Installation

```
$ git clone https://github.com/pmrowla/ollehtv.git
$ cd ollehtv
$ pip install .
```

If you also wish to run the development tests you will need to do
```
$ pip install -r requirements-dev.txt
```

## Configuration

In order to control your STB you must also authenticate a remote using the Olleh playtv mobile app.
Once you have authenticated the app, you will need to [proxy](https://mitmproxy.org) an app API request to get the `DEVICE_ID` and `SVC_PW` values for your device.

![mitmproxy screenshot](http://i.imgur.com/1azSJKK.png)

## Example
```
>>> import ollehtv
>>> device_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
>>> svc_pw = "abcdef1234567890"
>>> otv = ollehtv.OllehTV(device_id, svc_pw)
>>> otv.turn_on()
>>> otv.unmute()
>>> otv.change_channel(5)
>>> otv.input_button(ollehtv.OllehTVButton.IJEON)
```
This example session turns on a STB, unmutes it, switches it to channel 5 and then switches it back to the previous channel.
