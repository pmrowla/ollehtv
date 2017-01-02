# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import pytest
import requests_mock

from factory import Factory

import ollehtv


class OllehTVFactory(Factory):

    class Meta:
        model = ollehtv.OllehTV

    device_id = 'ABCDEF12-3456-7890-ABCD-EF1234567890'
    svc_pw = 'abcdef1234567890'


class TestOllehTV(object):

    def test_validate_success(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                'https://ollehtvplay.ktipmedia.co.kr/otp/v1/etc/datetime',
                json={'STATUS': {'CODE': '000', 'MESSAGE': 'OK'}},
                status_code=200,
            )
            o = OllehTVFactory()
            o.validate()

    def test_validate_failure(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                'https://ollehtvplay.ktipmedia.co.kr/otp/v1/etc/datetime',
                json={'STATUS': {'CODE': '102', 'MESSAGE': 'FAILURE'}},
                status_code=200,
            )
            o = OllehTVFactory()
            with pytest.raises(ollehtv.OllehTVError):
                o.validate()

    def test_get_state(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                ('https://ollehtvplay.ktipmedia.co.kr/otp/v1'
                 '/rmt/getCurrentState'),
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                    'DATA': {
                        'CHNL_NM': 'SBS',
                        'CHNL_NO': '5',
                        'FIN_TM': '16:00',
                        'PRGM_ID': 'A123456890',
                        'PRGM_NM': 'Foo',
                        'STB_STATE': '0',
                        'STRT_TM': '15:00',
                    },
                },
                status_code=200,
            )
            o = OllehTVFactory()
            state = o.get_state()
            assert state['channel_name'] == 'SBS'
            assert state['channel_num'] == 5
            assert state['state'] == 0
