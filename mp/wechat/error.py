# -*- coding: utf-8 -*-


class Error(object):
    """
    wechat error docs: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN
    """

    ERROR_MESSAGE = {
        -1:     'System is busy',
        40001:  'AppSecret no valid',
        40003:  'OpenID no valid',
        40004:  'Media type no valid',
        40005:  'File type no valid',
        40006:  'File size no valid',
        40007:  'Media id no valid',
        40008:  'Message tyoe no valid'
    }

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, no):
        if isinstance(no, str):
            no = int(no)

        return self.ERROR_MESSAGE.get(no, 'No suppert Error NO, No is %s' % no)
