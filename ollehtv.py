#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Python module for interacting with Olleh TV set-top-boxes'''

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from future.utils import python_2_unicode_compatible

import enum
import requests


@enum.unique
class OllehTVButton(enum.IntEnum):

    JIUGI = 8
    HWAGIN = 10
    NAGAGI = 27
    HOME = 36
    ZERO = 48
    ONE = 49
    TWO = 50
    THREE = 51
    FOUR = 52
    FIVE = 53
    SIX = 54
    SEVEN = 55
    EIGHT = 56
    NINE = 57
    STAR = 112
    POUND = 113
    IJEON = 115
    RED = 403
    GREEN = 404
    YELLOW = 405
    BLUE = 406
    POWER = 409
    REWIND = 412
    STOP = 413
    PLAY_PAUSE = 415
    FAST_FORWARD = 417
    CHANNEL_UP = 427
    CHANNEL_DOWN = 428
    VOLUME_UP = 447
    VOLUME_DOWN = 448
    MUTE = 449


@enum.unique
class OllehTVState(enum.IntEnum):

    OFF = 0
    STANDBY = 1
    ON = 2


@python_2_unicode_compatible
class OllehTVError(Exception):
    '''Base OllehTV API Error class'''

    def __init__(self, code=-1, message='Unknown API error'):
        self.code = code
        self.message = message

    def __str__(self):
        return '{}: {}'.format(self.code, self.message)


@python_2_unicode_compatible
class OllehTV(object):
    '''Class for interacting with Olleh TV set-top-boxes.

    Constants:
        TVPLAY_API_URL: Base URL for the OTP API (including API version).
        TVPLAY_USER_AGENT: Default User-Agent for API requests (spoofs the
            IOS tvplay application).
        TVPLAY_API_HEADERS: Default HTTP headers to be included with all API
            requests.

    '''

    TVPLAY_API_URL = 'https://ollehtvplay.ktipmedia.co.kr/otp/v1'
    TVPLAY_USER_AGENT = ('%EC%98%AC%EB%A0%88%20tv%play/3.0.2 '
                         'CFNetwork/808.2.16 Darwin/16.3.0')
    TVPLAY_API_HEADERS = {
        'Accept-Language': 'ko-kr',
        'User-Agent': TVPLAY_USER_AGENT,
    }

    def __init__(self, device_id, svc_pw):
        '''Initialize OllehTV instance.

        Values for DEVICE_ID and SVC_PW must be obtained per set-top-box by
        proxying the ollehplay mobile application.

        Parameters:
            device_id (str): The UUID for the set-top-box in the form
                "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".
            svc_pw (str): The secret hex string for an authenticated tvplay
                remote. This string can be obtained by checking the SVC_PW
                parameter in a proxied tvplay app API request.

        '''

        self.device_id = device_id
        self.svc_pw = svc_pw

    def validate(self):
        '''Verify that this is a valid STB instance.'''
        self._post('etc/datetime')

    def _post(self, endpoint, payload={}):
        '''POST an API request.

        Parameters:
            endpoint (str): The API endpoint to query.
            payload (dict): A dictionary containing any parameters to include
                in the request. This dictionary will be json encoded at request
                time.

        Return:
            dict: A dictionary containing the request response data

        Raises:
            OllehTVError upon an API error.
            requests.exceptions.RequestException upon HTTP error.

        '''

        payload.update({
            'DEVICE_ID': self.device_id,
            'SVC_ID': 'OTP',
            'SVC_PW': self.svc_pw,
        })
        endpoint.lstrip('/')
        url = '{}/{}'.format(self.TVPLAY_API_URL, endpoint)
        r = requests.post(url, headers=self.TVPLAY_API_HEADERS, json=payload)
        r.raise_for_status()
        data = r.json()
        if 'STATUS' not in data:
            raise OllehTVError
        code = int(data['STATUS'].get('CODE', -1))
        if code != 0:
            message = data['STATUS'].get('MESSAGE', 'Unknown API error')
            raise OllehTVError(code, message)
        return data

    def get_state(self):
        '''Get the current STB state.

        Return:
            dict: A dictionary containing the current STB state.

        Raises:
            OllehTVError upon an API error.

        '''
        response = self._post('rmt/getCurrentState')
        if 'DATA' not in response:
            raise OllehTVError
        data = response['DATA']
        state = {
            'channel_name': data.get('CHNL_NM', ''),
            'channel_num': int(data.get('CHNL_NO', -1)),
            'program_id': data.get('PRGM_ID', ''),
            'program_name': data.get('PRGM_NM', ''),
            'start_time': data.get('STRT_TM', ''),
            'end_time': data.get('FIN_TM', ''),
            'state': int(data.get('STB_STATE', OllehTVState.OFF)),
        }
        if state['state'] == OllehTVState.OFF:
            raise OllehTVError(-1, 'The STB is unreachable.')
        return state

    def input_button(self, code):
        '''Send a remote button press to the STB.

        Parameters:
            code (int, str): The button key code to send.

        '''
        payload = {'KEY_CD': str(code)}
        self._post('rmt/inputButton', payload=payload)

    @property
    def muted(self):
        '''Return the current STB mute state.

        Return:
            bool: True if STB is muted, False if not muted.

        Raises:
            OllehTVError upon an API error.

        '''
        response = self._post('rmt/getMuteState')
        data = response['DATA']
        if 'STATE' not in data:
            raise OllehTVError
        if int(data['STATE']) == 0:
            return False
        else:
            return True

    def mute(self):
        '''Mute the STB.'''
        if not self.muted:
            self.input_button(OllehTVButton.MUTE)

    def unmute(self):
        '''Unmute the STB.'''
        if self.muted:
            self.input_button(OllehTVButton.MUTE)

    @property
    def powered_on(self):
        '''Return True if the STB is turned on'''
        s = self.get_state
        if s['state'] == OllehTVState.ON:
            return True
        else:
            return False

    def turn_on(self):
        '''Turn on the STB.'''
        s = self.get_state()
        if s['state'] == OllehTVState.STANDBY:
            self.input_button(OllehTVButton.POWER)

    def turn_off(self):
        '''Turn off the STB.'''
        s = self.get_state()
        if s['state'] == OllehTVState.ON:
            self.input_button(OllehTVButton.POWER)
