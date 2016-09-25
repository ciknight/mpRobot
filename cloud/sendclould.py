# -*- coding: utf-8 -*-


class SendCloud(object):

    def __init__(self, *args, **kwargs):
        super(SendCloud, self).__init__()
        self.user = kwargs.get('api_user')
        self.key = kwargs.get('api_key')
        assert self.key and self.user

    def extract_response_key(self, response, key='message', default=None):
        if (response is not None) and (response.status_code == 200):
            try:
                data = response.json()
                return data.get(key, default)
            except:
                pass
        return default
