# -*- coding: utf-8 -*-

import requests

from .sendcloud import SendCloud


class SendCloudEmail(SendCloud):

    API_STATUS_SUCCESS = 'success'

    SEND_EMAIL_URL = 'http://sendcloud.sohu.com/webapi/mail.send.json'
    SEND_TEMPLATE_EMAIL_URL = 'http://sendcloud.sohu.com/webapi/mail.send_template.json'

    EMAIL_FROM = '520@timekillyou.com'
    EMAIL_FROM_NAME = '520(Robot)'

    def __init__(self, *args, **kwargs):
        super(SendCloudEmail, self).__init__(*args, **kwargs)
        self._comment_params = {
            'api_user': self.user,
            'api_key': self.key,
            'resp_email_id': True
        }

    def send_email(self, mail_to, subject='默认标题', html='默认内容', template_invoke_name=None):
        assert mail_to
        url = SendCloudEmail.SEND_EMAIL_URL
        sub_var = {
            'to': mail_to,
            'subject': subject,
            'html': html,
            'from': SendCloudEmail.EMAIL_FROM,
            'fromname': SendCloudEmail.EMAIL_FROM_NAME
        }
        if template_invoke_name:
            sub_var.update(template_invoke_name=template_invoke_name)
            url = SendCloudEmail.SEND_TEMPLATE_EMAIL_URL

        return self._post(url, sub_var)

    def send_template_email(self,  mail_to, subject='默认标题', template_invoke_name=None):
        return self.send_email(mail_to, subject=subject, template_invoke_name=template_invoke_name)

    def _post(self, url, sub_var):
        # 注入
        data = dict(sub_var.items() + self._comment_params.items())
        response = requests.post(url, data=data)
        return self.extract_response_key(response, 'message') == SendCloudEmail.SEND_EMAIL_URL
