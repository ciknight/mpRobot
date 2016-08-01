# -*- coding: utf-8 -*-

import requests


class TuLing(object):

    TULING_API_URL = 'http://www.tuling123.com/openapi/api'

    SUB_TYPE_TEXT = 100000

    def __init__(self, *args, **kwargs):
        super(TuLing, self).__init__()
        self._api_key = kwargs.get('api_key')
        self._api_secret = kwargs.get('api_secret')
        self._api_url = kwargs.get('api_url', self.TULING_API_URL)
        assert self._api_key and self._api_secret

    def _post(self, data):
        response = requests.post(url=self._api_url, data=data)
        if response.status_code is not 200:
            return None
        return response.json()

    def replay_text(self, info):
        data = {
            'key': self._api_key,
            'info': info
        }
        return_dict = self._post(data)
        if return_dict['code'] != TuLing.SUB_TYPE_TEXT:
            return None

        message = return_dict['text']
        return message.encode('utf-8')
