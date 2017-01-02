#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Python module for interacting with Olleh TV set-top-boxes'''

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import requests


class OllehTVError(Exception):
    '''Base OllehTV API Error class'''

    def __init__(self, code=-1, message='Unknown API error'):
        self.code = code
        self.message = message

    def __unicode__(self):
        return '{}: {}'.format(self.code, self.message)

    def __str__(self):
        return unicode(self).encode('utf-8')


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
            'state': int(data.get('STB_STATE', -1)),
        }
        return state
