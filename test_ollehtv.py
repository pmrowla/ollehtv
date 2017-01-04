# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import datetime
import pytest
import requests_mock

from factory import Factory

from ollehtv import (
    OllehTV,
    OllehTVButton,
    OllehTVError,
    OllehTVState,
)


class OllehTVFactory(Factory):

    class Meta:
        model = OllehTV

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
            with pytest.raises(OllehTVError):
                o.validate()

    def test_get_state_on(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                ('https://ollehtvplay.ktipmedia.co.kr/otp/v1'
                 '/rmt/getCurrentState'),
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                    'DATA': {'STB_STATE': '2'},
                },
                status_code=200,
            )
            o = OllehTVFactory()
            state = o.get_state()
            assert state['state'] == OllehTVState.ON

    def test_get_state_standby(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                ('https://ollehtvplay.ktipmedia.co.kr/otp/v1'
                 '/rmt/getCurrentState'),
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                    'DATA': {'STB_STATE': '1'},
                },
                status_code=200,
            )
            o = OllehTVFactory()
            state = o.get_state()
            assert state['state'] == OllehTVState.STANDBY

    def test_get_state_off(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                ('https://ollehtvplay.ktipmedia.co.kr/otp/v1'
                 '/rmt/getCurrentState'),
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                    'DATA': {'STB_STATE': '0'},
                },
                status_code=200,
            )
            o = OllehTVFactory()
            with pytest.raises(OllehTVError):
                o.get_state()

    def test_input_button(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                'https://ollehtvplay.ktipmedia.co.kr/otp/v1/rmt/inputButton',
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                },
                status_code=200,
            )
            o = OllehTVFactory()
            o.input_button(OllehTVButton.POWER)

    def test_mute(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                'https://ollehtvplay.ktipmedia.co.kr/otp/v1/rmt/inputButton',
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                },
                status_code=200,
            )
            m.register_uri(
                'POST',
                'https://ollehtvplay.ktipmedia.co.kr/otp/v1/rmt/getMuteState',
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                    'DATA': {
                        'STATE': '0',
                    },
                },
                status_code=200,
            )
            o = OllehTVFactory()
            assert not o.muted
            o.mute()
            m.register_uri(
                'POST',
                'https://ollehtvplay.ktipmedia.co.kr/otp/v1/rmt/getMuteState',
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                    'DATA': {
                        'STATE': '1',
                    },
                },
                status_code=200,
            )
            assert o.muted
            o.unmute()

    def test_power(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                'https://ollehtvplay.ktipmedia.co.kr/otp/v1/rmt/inputButton',
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                },
                status_code=200,
            )
            m.register_uri(
                'POST',
                ('https://ollehtvplay.ktipmedia.co.kr/otp/v1'
                 '/rmt/getCurrentState'),
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                    'DATA': {'STB_STATE': '1'},
                },
                status_code=200,
            )
            o = OllehTVFactory()
            o.turn_on()
            m.register_uri(
                'POST',
                ('https://ollehtvplay.ktipmedia.co.kr/otp/v1'
                 '/rmt/getCurrentState'),
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                    'DATA': {'STB_STATE': '2'},
                },
                status_code=200,
            )
            o.turn_off()

    def test_change_channel(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                'https://ollehtvplay.ktipmedia.co.kr/otp/v1/rmt/changeChannel',
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                },
                status_code=200,
            )
            o = OllehTVFactory()
            o.change_channel(123)

    def test_get_program_listing(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                'https://ollehtvplay.ktipmedia.co.kr/otp/v1/epg/list',
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                    'DATA': {},
                },
                status_code=200,
            )
            o = OllehTVFactory()
            o.get_program_listing()
            o.get_program_listing(search_date='20170101')
            o.get_program_listing(search_date=datetime.date(2017, 01, 01))

    def test_get_favorite_channels(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                'https://ollehtvplay.ktipmedia.co.kr/otp/v1/epg/getMyChannel',
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                    'DATA': {},
                },
                status_code=200,
            )
            o = OllehTVFactory()
            o.get_favorite_channels()

    def test_get_channel_detail(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                'https://ollehtvplay.ktipmedia.co.kr/otp/v1/epg/detail',
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                    'DATA': {},
                },
                status_code=200,
            )
            o = OllehTVFactory()
            o.get_channel_detail(1)

    def test_search(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST',
                'https://ollehtvplay.ktipmedia.co.kr/otp/v1/srch/epg',
                json={
                    'STATUS': {'CODE': '000', 'MESSAGE': 'OK'},
                    'DATA': {},
                },
                status_code=200,
            )
            o = OllehTVFactory()
            o.search('인기가요')
