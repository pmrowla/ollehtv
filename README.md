# ollehtv
[![Build Status](https://travis-ci.org/pmrowla/ollehtv.svg?branch=master)](https://travis-ci.org/pmrowla/ollehtv)
[![Coverage Status](https://coveralls.io/repos/github/pmrowla/ollehtv/badge.svg?branch=master)](https://coveralls.io/github/pmrowla/ollehtv?branch=master)

Python library for controlling an Olleh TV set-top-boxes.

In order to control your STB you must also authenticate a remote using the Olleh playtv mobile app.
Once you have authenticated the app, you will need to [proxy](https://mitmproxy.org) an app API request to get the `DEVICE_ID` and `SVC_PW` values for your device.
